#!/usr/bin/env python3
"""Preview a fail-closed course-redesign state migration from schema 7 to 8.

This helper has no apply or write path. It preserves existing run and schedule
records in the preview, installs schema-8 templates for future runs/contracts,
and reports the mandatory eligibility and schedule reconfirmation work that a
later separately authorised migration must resolve. Immutable terminal schema-7
run history is indexed by a canonical SHA-256 receipt and remains on a bounded
legacy validation profile; non-terminal or malformed schema-7 history fails
closed rather than being rewritten.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import runpy
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()

LEGACY_SCHEMA_7_RUN_STATUSES = [
    "not_started",
    "active",
    "waiting_at_gate",
    "completed",
    "handed_off",
    "failed_safe",
    "cancelled",
    "expired",
]
LEGACY_SCHEMA_7_TERMINAL_STATUSES = [
    "completed",
    "handed_off",
    "failed_safe",
    "cancelled",
    "expired",
]
LEGACY_SCHEMA_7_REQUIRED_APPROVALS = {
    "gate_0",
    "gate_1",
    "gate_2a",
    "gate_2b",
    "gate_3",
    "artefact_gate",
    "production_completion",
    "hitl_3",
    "system_improvement_review_offer",
}
LEGACY_VALIDATION_PROFILE = "schema_7_terminal_history_v0_2_2"
LEGACY_SCHEMA_7_SCHEDULE_ALLOWED_STATUSES = [
    "not_approved",
    "active",
    "paused",
    "expired",
    "cancelled",
]
LEGACY_SCHEMA_7_PRESERVABLE_SCHEDULE_STATUSES = [
    "paused",
    "expired",
    "cancelled",
]
LEGACY_SCHEDULE_VALIDATION_PROFILE = "schema_7_inactive_schedule_history_v0_2_2"
LEGACY_HASH_METHOD = (
    "sha256_utf8_canonical_json_sorted_keys_no_insignificant_whitespace"
)
MIGRATION_REQUIRED_BEFORE_USE = [
    "approve_and_fingerprint_material_processing_eligibility_without_source_disclosure",
    "preserve_and_validate_terminal_schema_7_history_by_indexed_canonical_sha256_receipt",
    "preserve_and_validate_inactive_schema_7_schedule_history_by_indexed_canonical_sha256_receipt",
    "resolve_every_nonterminal_schema_7_run_before_migration_without_rewriting_history",
    "reconfirm_every_schedule_against_current_eligibility_fingerprint_before_future_trigger",
    "run_schema_8_validator_after_separately_authorised_application",
]


class MigrationError(ValueError):
    """Raised when a safe preview cannot be produced."""


def _canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def _legacy_terminal_run_errors(run: Any, index: int) -> list[str]:
    """Return bounded schema-7 history errors without upgrading the run."""

    label = f"runs[{index}]"
    if not isinstance(run, dict):
        return [f"{label} must be an object"]
    errors: list[str] = []
    if run.get("template_only") is not False:
        errors.append(f"{label} historical run must set template_only false")
    if not isinstance(run.get("run_id"), str) or not run.get("run_id"):
        errors.append(f"{label} historical run is missing run_id")
    if run.get("allowed_run_statuses") != LEGACY_SCHEMA_7_RUN_STATUSES:
        errors.append(f"{label} schema-7 allowed run statuses are missing or reordered")
    status = run.get("status")
    if status not in LEGACY_SCHEMA_7_TERMINAL_STATUSES:
        errors.append(f"{label} is not terminal schema-7 history")
    allowed_modes = run.get("allowed_modes")
    if allowed_modes != ["manual", "scheduled"] or run.get("mode") not in allowed_modes:
        errors.append(f"{label} has an invalid schema-7 run mode")
    if not run.get("started_at"):
        errors.append(f"{label} terminal schema-7 history is missing started_at")

    termination = run.get("termination")
    if not isinstance(termination, dict):
        errors.append(f"{label}.termination must be an object")
    else:
        if termination.get("allowed_statuses") != LEGACY_SCHEMA_7_TERMINAL_STATUSES:
            errors.append(f"{label} schema-7 termination statuses are missing or reordered")
        if termination.get("status") != status:
            errors.append(f"{label} termination status does not match run status")
        for field in ("reason", "recorded_at"):
            if not termination.get(field):
                errors.append(f"{label} terminal schema-7 history is missing termination.{field}")

    approvals = run.get("approvals")
    if not isinstance(approvals, dict) or not LEGACY_SCHEMA_7_REQUIRED_APPROVALS.issubset(
        approvals
    ):
        errors.append(f"{label} schema-7 approval structure is incomplete")
    for field in (
        "contract",
        "source_manifest_verification",
        "shared_context",
        "manual_stage_authority",
        "resume_protocol",
    ):
        if not isinstance(run.get(field), dict):
            errors.append(f"{label}.{field} must be an object")
    transitions = run.get("manual_stage_authority", {}).get("transition_rules")
    if not isinstance(transitions, list):
        errors.append(f"{label} schema-7 transition rules must be a list")
    resume = run.get("resume_protocol", {})
    if isinstance(resume, dict):
        if resume.get("schema_version") != 1:
            errors.append(f"{label} schema-7 resume protocol version must be 1")
        if not isinstance(resume.get("checkpoint_order"), list) or not isinstance(
            resume.get("receipt_reference_fields"), list
        ) or not isinstance(resume.get("rules"), dict):
            errors.append(f"{label} schema-7 resume protocol is incomplete")
    return errors


def _legacy_history_receipts(runs: Any, active_run_id: Any) -> list[dict[str, Any]]:
    if not isinstance(runs, list):
        raise MigrationError("schema-7 runs must be a list")
    receipts: list[dict[str, Any]] = []
    seen_run_ids: set[str] = set()
    for index, run in enumerate(runs):
        errors = _legacy_terminal_run_errors(run, index)
        if errors:
            raise MigrationError("unsafe schema-7 run history: " + "; ".join(errors))
        run_id = run["run_id"]
        if run_id in seen_run_ids:
            raise MigrationError(f"unsafe schema-7 run history: duplicate run_id {run_id}")
        seen_run_ids.add(run_id)
        if active_run_id == run_id:
            raise MigrationError(
                f"unsafe schema-7 run history: terminal run {run_id} remains active_run_id"
            )
        receipts.append(
            {
                "run_index": index,
                "run_id": run_id,
                "terminal_status": run["status"],
                "source_schema_version": 7,
                "validation_profile": LEGACY_VALIDATION_PROFILE,
                "canonical_json_sha256": _canonical_json_sha256(run),
            }
        )
    if active_run_id is not None:
        raise MigrationError(
            "unsafe schema-7 run history: active_run_id is set but no non-terminal run can be migrated without rewriting history"
        )
    return receipts


def _legacy_schedule_errors(schedule: Any, index: int) -> list[str]:
    """Validate a bounded, inactive v0.2.2 schedule without upgrading it."""

    label = f"schedules[{index}]"
    if not isinstance(schedule, dict):
        return [f"{label} must be an object"]
    errors: list[str] = []
    for field in (
        "schedule_id",
        "material_processing_eligibility_fingerprint",
        "material_processing_eligibility_match_rule",
        "status_transition_receipt",
        "status_history",
    ):
        if field in schedule:
            errors.append(f"{label} contains schema-8-only field {field}")
    if schedule.get("allowed_statuses") != LEGACY_SCHEMA_7_SCHEDULE_ALLOWED_STATUSES:
        errors.append(f"{label} schema-7 allowed schedule statuses are missing or reordered")
    if schedule.get("status") not in LEGACY_SCHEMA_7_PRESERVABLE_SCHEDULE_STATUSES:
        errors.append(f"{label} is not inactive preservable schema-7 schedule history")
    for field in ("contract_id", "contract_version"):
        if not schedule.get(field):
            errors.append(f"{label} is missing {field}")
    if schedule.get("task_type") != "standalone_fresh_task_per_run":
        errors.append(f"{label} has an invalid schema-7 task_type")
    if schedule.get("no_immediate_run") is not True:
        errors.append(f"{label} must preserve no_immediate_run true")
    if schedule.get("protected_roots") != ["00_Source_Materials", "00_Context"]:
        errors.append(f"{label} protected roots are missing or reordered")

    project = schedule.get("project")
    course = schedule.get("course")
    if not isinstance(project, dict) or not all(
        project.get(field) for field in ("project_id", "project_root")
    ):
        errors.append(f"{label}.project is incomplete")
    if not isinstance(course, dict) or not all(
        course.get(field) for field in ("course_id", "course_title")
    ):
        errors.append(f"{label}.course is incomplete")

    runtime = schedule.get("runtime_versions")
    if not isinstance(runtime, dict):
        errors.append(f"{label}.runtime_versions must be an object")
    else:
        for field in (
            "prompt_version",
            "skill_version",
            "validated_system_proposal_id",
            "validated_system_proposal_version",
            "activation_decision_reference",
        ):
            if not runtime.get(field):
                errors.append(f"{label}.runtime_versions is missing {field}")
        if runtime.get("skill_name") != "course-redesign-orchestrator":
            errors.append(f"{label} has an invalid schema-7 skill_name")
        if runtime.get("required_runtime_status") != "active":
            errors.append(f"{label} has an invalid schema-7 required runtime status")

    baseline = schedule.get("baseline_approvals")
    if not isinstance(baseline, dict):
        errors.append(f"{label}.baseline_approvals must be an object")
    else:
        if "gate_0a_approval_id" in baseline:
            errors.append(f"{label} contains schema-8-only Gate-0A baseline lineage")
        for field in (
            "gate_0_approval_id",
            "gate_1_approval_id",
            "source_manifest_path",
            "source_manifest_fingerprint",
            "source_access_policy_version",
            "source_access_policy_fingerprint",
            "verified_still_valid_at",
        ):
            if not baseline.get(field):
                errors.append(f"{label}.baseline_approvals is missing {field}")
        if baseline.get("verification_result") != "passed":
            errors.append(f"{label} schema-7 baseline verification must be passed")

    for field in (
        "main_goal",
        "data_egress_boundary",
        "source_access_policy_version",
        "source_access_policy_fingerprint",
        "assessment_security_boundary",
        "timezone",
        "approved_contract_snapshot_reference",
        "approved_at",
        "activation_time",
        "expires_at",
        "last_reconfirmed_at",
    ):
        if not schedule.get(field):
            errors.append(f"{label} is missing {field}")
    for field in (
        "success_criteria",
        "stop_conditions",
        "constraints",
        "permitted_tools",
        "permitted_actions",
        "permitted_source_classes",
        "permitted_output_audiences",
        "recurrence",
    ):
        if not isinstance(schedule.get(field), list) or not schedule.get(field):
            errors.append(f"{label}.{field} must be a nonempty list")

    terminal_rules = schedule.get("terminal_rules")
    if not isinstance(terminal_rules, dict) or terminal_rules.get("allowed") != [
        "completed",
        "handed_off",
        "failed_safe",
        "cancelled",
        "expired",
    ]:
        errors.append(f"{label} schema-7 terminal rules are incomplete")
    for field in ("pause", "renew", "rollback"):
        if not isinstance(schedule.get(field), dict):
            errors.append(f"{label}.{field} must be an object")

    approval = schedule.get("lecturer_approval")
    if not isinstance(approval, dict):
        errors.append(f"{label}.lecturer_approval must be an object")
    else:
        if approval.get("status") != "approved" or approval.get(
            "reply_must_contain_exactly_and_only_three_lines"
        ) is not True:
            errors.append(f"{label} lacks the exact-only schema-7 lecturer approval")
        expected_line_2 = (
            f"Schedule contract: {schedule.get('contract_id')} "
            f"{schedule.get('contract_version')}"
        )
        expected_line_3 = f"Expires: {schedule.get('expires_at')}"
        if approval.get("line_1") != "APPROVE SCHEDULES":
            errors.append(f"{label} lecturer approval line 1 is invalid")
        if approval.get("line_2") != expected_line_2:
            errors.append(f"{label} lecturer approval line 2 does not match the contract")
        if approval.get("line_3") != expected_line_3:
            errors.append(f"{label} lecturer approval line 3 does not match the expiry")
        for field in ("completed_reply_reference", "recorded_at"):
            if not approval.get(field):
                errors.append(f"{label}.lecturer_approval is missing {field}")
        if approval.get("validation_status") != "passed":
            errors.append(f"{label} lecturer approval validation must be passed")
    return errors


def _legacy_schedule_history_receipts(
    schedules: Any, schedule_registration: Any
) -> list[dict[str, Any]]:
    if not isinstance(schedules, list):
        raise MigrationError("schema-7 schedules must be a list")
    if not isinstance(schedule_registration, dict):
        raise MigrationError("schema-7 schedule-registration record is missing")
    if schedules and schedule_registration.get("status") != "not_approved":
        raise MigrationError(
            "unsafe schema-7 schedule history: currently registered schedules must be disabled before preview migration"
        )
    receipts: list[dict[str, Any]] = []
    seen_pairs: set[tuple[Any, Any]] = set()
    for index, schedule in enumerate(schedules):
        errors = _legacy_schedule_errors(schedule, index)
        if errors:
            raise MigrationError("unsafe schema-7 schedule history: " + "; ".join(errors))
        pair = (schedule["contract_id"], schedule["contract_version"])
        if pair in seen_pairs:
            raise MigrationError(
                "unsafe schema-7 schedule history: duplicate contract ID/version pair"
            )
        seen_pairs.add(pair)
        receipts.append(
            {
                "schedule_index": index,
                "contract_id": schedule["contract_id"],
                "contract_version": schedule["contract_version"],
                "status": schedule["status"],
                "source_schema_version": 7,
                "validation_profile": LEGACY_SCHEDULE_VALIDATION_PROFILE,
                "canonical_json_sha256": _canonical_json_sha256(schedule),
            }
        )
    return receipts


def _canonical_v8() -> dict[str, Any]:
    candidates: list[Path] = []
    for ancestor in SCRIPT_PATH.parents:
        candidates.extend(
            [
                ancestor / "course-project-template" / "01_Control" / "state.json",
                ancestor / "assets" / "project-template" / "01_Control" / "state.json",
                ancestor / "01_Control" / "state.json",
            ]
        )
    template = next((path for path in candidates if path.is_file()), None)
    if template is None:
        raise MigrationError(
            "canonical schema-8 state template not found in shared-core, plugin-assets or workspace-overlay layout"
        )
    value = json.loads(template.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != 8:
        raise MigrationError("canonical schema-8 template is missing or invalid")
    return value


def _insert_once(items: list[Any], value: Any, before: str | None = None) -> None:
    if value in items:
        return
    if before is not None and before in items:
        items.insert(items.index(before), value)
    else:
        items.append(value)


def _upgrade_activation(candidate: dict[str, Any], canonical: dict[str, Any]) -> None:
    activation = candidate.get("activation")
    if not isinstance(activation, dict):
        raise MigrationError("schema-7 activation record is missing")
    required = activation.get("required_before_active")
    if not isinstance(required, list):
        raise MigrationError("schema-7 activation prerequisites are missing")
    _insert_once(required, "gate_0a_recorded", before="gate_0_recorded")
    _insert_once(
        required,
        "matching_course_run_terminal_complete_dormant",
        before="system_update_approved",
    )
    system_update = activation.get("system_update")
    if not isinstance(system_update, dict):
        raise MigrationError("schema-7 system-update record is missing")
    prerequisites = system_update.get("prerequisites")
    requirements = system_update.get("completed_reply_requirements")
    approval = system_update.get("approval")
    if not isinstance(prerequisites, list) or not isinstance(requirements, list) or not isinstance(
        approval, dict
    ):
        raise MigrationError("schema-7 system-update lineage schema is missing")
    _insert_once(prerequisites, "matching_run_terminal_complete_dormant_and_not_active")
    _insert_once(
        requirements,
        "material_processing_eligibility_fingerprint",
        before="source_manifest_fingerprint",
    )
    approval.setdefault("material_processing_eligibility_fingerprint", None)
    # Structural controls are canonical; progressed receipt values remain in place.
    for field in (
        "allowed_statuses",
        "automatic_activation_forbidden",
    ):
        activation[field] = copy.deepcopy(canonical["activation"][field])
    system_update["allowed_statuses"] = copy.deepcopy(
        canonical["activation"]["system_update"]["allowed_statuses"]
    )


def _upgrade_schedule_registration(
    candidate: dict[str, Any], canonical: dict[str, Any]
) -> None:
    registration = candidate.get("schedule_registration")
    if not isinstance(registration, dict):
        raise MigrationError("schema-7 schedule-registration record is missing")
    registration["required_material_processing_eligibility"] = copy.deepcopy(
        canonical["schedule_registration"]["required_material_processing_eligibility"]
    )


def _preservation_checks(source: dict[str, Any], candidate: dict[str, Any]) -> dict[str, bool]:
    checks: dict[str, bool] = {
        "top_level_status": candidate.get("status") == source.get("status"),
        "course": candidate.get("course") == source.get("course")
        or all(
            candidate.get("course", {}).get(key) == value
            for key, value in source.get("course", {}).items()
        ),
        "source_manifest": candidate.get("source_manifest") == source.get("source_manifest"),
        "active_run_id": candidate.get("active_run_id") == source.get("active_run_id"),
        "existing_runs": candidate.get("runs") == source.get("runs"),
        "existing_schedules": candidate.get("schedules") == source.get("schedules"),
        "activation_status": candidate.get("activation", {}).get("status")
        == source.get("activation", {}).get("status"),
        "system_update_status": candidate.get("activation", {})
        .get("system_update", {})
        .get("status")
        == source.get("activation", {}).get("system_update", {}).get("status"),
        "schedule_registration_status": candidate.get("schedule_registration", {}).get(
            "status"
        )
        == source.get("schedule_registration", {}).get("status"),
    }
    source_policy = source.get("source_access_policy", {})
    candidate_policy = candidate.get("source_access_policy", {})
    checks["source_access_policy_existing_fields"] = isinstance(source_policy, dict) and all(
        candidate_policy.get(key) == value for key, value in source_policy.items()
    )
    return checks


def preview_migration(data: dict[str, Any], source: str = "<memory>") -> dict[str, Any]:
    """Return a migration preview without mutating *data* or writing a file."""

    if not isinstance(data, dict):
        raise MigrationError("state root must be an object")
    source_schema = data.get("schema_version")
    if source_schema == 8:
        candidate = copy.deepcopy(data)
        validator = runpy.run_path(str(Path(__file__).with_name("validate_state.py")))[
            "validate"
        ]
        errors = validator(copy.deepcopy(candidate))
        if errors:
            raise MigrationError("schema-8 state is invalid: " + "; ".join(errors[:8]))
        hold = candidate.get("schema_8_migration_hold", {})
        reconfirmation_required = isinstance(hold, dict) and hold.get("status") == (
            "blocked_pending_reconfirmation"
        )
        return {
            "ok": True,
            "mode": "preview_only",
            "would_write": False,
            "source": source,
            "source_schema_version": 8,
            "target_schema_version": 8,
            "changed_paths": [],
            "reconfirmation_required": reconfirmation_required,
            "required_before_use": (
                copy.deepcopy(MIGRATION_REQUIRED_BEFORE_USE)
                if reconfirmation_required
                else []
            ),
            "preservation_checks": {"already_schema_8_unchanged": True},
            "candidate_activation_ready": False,
            "candidate_state": candidate,
        }
    if source_schema != 7:
        raise MigrationError("only schema 7 input or an already-valid schema 8 preview is supported")
    if data.get("status") != "candidate_not_active":
        raise MigrationError(
            "schema-7 runtime must be explicitly inactive before preview migration; active or suspended state is never rewritten implicitly"
        )

    source_copy = copy.deepcopy(data)
    candidate = copy.deepcopy(data)
    canonical = _canonical_v8()
    legacy_receipts = _legacy_history_receipts(
        candidate.get("runs"), candidate.get("active_run_id")
    )
    legacy_schedule_receipts = _legacy_schedule_history_receipts(
        candidate.get("schedules"), candidate.get("schedule_registration")
    )
    candidate["schema_version"] = 8
    candidate["plugin_version"] = canonical["plugin_version"]
    for field in (
        "umbrella_entry_routing",
        "schema_compatibility",
        "adaptive_course_scope",
        "material_processing_eligibility",
    ):
        candidate[field] = copy.deepcopy(canonical[field])
    course = candidate.get("course")
    if not isinstance(course, dict):
        raise MigrationError("schema-7 course record is missing")
    for field in (
        "educational_context_type",
        "discipline_or_subject",
        "qualification_or_framework",
        "adaptation_inputs_confirmed",
    ):
        course.setdefault(field, canonical["course"][field])
    policy = candidate.get("source_access_policy")
    if not isinstance(policy, dict):
        raise MigrationError("schema-7 source-access-policy record is missing")
    policy.setdefault("material_processing_eligibility_fingerprint", None)
    candidate["setup"] = copy.deepcopy(canonical["setup"])
    _upgrade_activation(candidate, canonical)
    _upgrade_schedule_registration(candidate, canonical)
    # Templates are not run history. Replace them with the schema-8 canonical
    # forms so every future trigger is fresh and eligibility-bound.
    candidate["run_template"] = copy.deepcopy(canonical["run_template"])
    candidate["standing_schedule_contract_template"] = copy.deepcopy(
        canonical["standing_schedule_contract_template"]
    )
    candidate["open_questions"] = copy.deepcopy(canonical["open_questions"])
    candidate["legacy_preserved_run_history"] = {
        "source_schema_version": 7,
        "validation_profile": LEGACY_VALIDATION_PROFILE,
        "hash_method": LEGACY_HASH_METHOD,
        "immutable_history_no_upgrade_or_rewrite": True,
        "receipts": legacy_receipts,
    }
    candidate["legacy_preserved_schedule_history"] = {
        "source_schema_version": 7,
        "validation_profile": LEGACY_SCHEDULE_VALIDATION_PROFILE,
        "hash_method": LEGACY_HASH_METHOD,
        "immutable_history_no_upgrade_or_rewrite": True,
        "receipts": legacy_schedule_receipts,
    }
    candidate["schema_8_migration_hold"] = {
        "status": "blocked_pending_reconfirmation",
        "source_schema_version": 7,
        "material_processing_eligibility_reconfirmation_required": True,
        "nonterminal_run_reconfirmation_required": False,
        "schedule_reconfirmation_required": bool(candidate.get("schedules"))
        or candidate.get("schedule_registration", {}).get("status") == "approved",
        "automatic_apply_forbidden": True,
        "clear_only_after_separate_reconfirmation_and_validation": True,
    }

    checks = _preservation_checks(source_copy, candidate)
    failed = sorted(key for key, passed in checks.items() if not passed)
    if failed:
        raise MigrationError("preview changed protected history: " + ", ".join(failed))
    changed_paths = [
        "schema_version",
        "plugin_version",
        "umbrella_entry_routing",
        "schema_compatibility",
        "adaptive_course_scope",
        "material_processing_eligibility",
        "course.schema_8_adaptation_fields",
        "source_access_policy.material_processing_eligibility_fingerprint",
        "setup",
        "activation.schema_8_prerequisites_and_lineage",
        "schedule_registration.required_material_processing_eligibility",
        "run_template",
        "standing_schedule_contract_template",
        "open_questions",
        "legacy_preserved_run_history",
        "legacy_preserved_schedule_history",
        "schema_8_migration_hold",
    ]
    return {
        "ok": True,
        "mode": "preview_only",
        "would_write": False,
        "source": source,
        "source_schema_version": 7,
        "target_schema_version": 8,
        "changed_paths": changed_paths,
        "reconfirmation_required": True,
        "required_before_use": copy.deepcopy(MIGRATION_REQUIRED_BEFORE_USE),
        "preservation_checks": checks,
        "candidate_activation_ready": False,
        "candidate_state": candidate,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="schema-7 or already-valid schema-8 state")
    args = parser.parse_args()
    try:
        raw = args.state.read_bytes()
        value = json.loads(raw.decode("utf-8"))
        report = preview_migration(value, source=args.state.as_posix())
        report["source_sha256"] = hashlib.sha256(raw).hexdigest().upper()
    except Exception as exc:
        report = {
            "ok": False,
            "mode": "preview_only",
            "would_write": False,
            "source": args.state.as_posix(),
            "error": f"{type(exc).__name__}: {exc}",
        }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
