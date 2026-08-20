#!/usr/bin/env python3
"""Validate essential fail-closed invariants in a course-redesign state file."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "status",
    "source_manifest",
    "source_access_policy",
    "activation",
    "schedule_registration",
    "run_template",
    "standing_schedule_contract_template",
    "runs",
    "schedules",
}

RESEARCH_TARGET_PATTERN = re.compile(
    r"^03_Research/[0-9]{4}-[0-9]{2}-[0-9]{2}_[A-Za-z0-9._-]+/[^/]+$"
)


def _safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value or "\\" in value or value.startswith("/"):
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def _validate_research_targets(gate: dict, errors: list[str]) -> None:
    if "approved_exact_targets" in gate:
        errors.append("Gate 2B must use approved_research_targets, not approved_exact_targets")
    targets = gate.get("approved_research_targets")
    if not isinstance(targets, list):
        errors.append("Gate 2B approved_research_targets must be a list")
        targets = []
    rules = gate.get("target_rules", {})
    expected_types = {"research_dossier", "research_handoff"}
    if rules.get("required_prefix") != "03_Research/":
        errors.append("Gate 2B research targets must use the 03_Research prefix")
    if rules.get("required_dated_run_folder_pattern") != RESEARCH_TARGET_PATTERN.pattern:
        errors.append("Gate 2B must enforce the exact dated 03_Research run-folder pattern")
    if set(rules.get("allowed_target_types", [])) != expected_types:
        errors.append("Gate 2B must allow exactly research_dossier and research_handoff targets")
    if set(rules.get("required_target_types_when_approved", [])) != expected_types:
        errors.append("an approved Gate 2B must require both research target types")
    if rules.get("course_material_production_authorised") is not False:
        errors.append("Gate 2B must not authorise course-material production")
    if set(rules.get("forbidden_prefixes", [])) != {
        "04_Working_Copies/",
        "05_Approved/",
    }:
        errors.append("Gate 2B must forbid working-copy and approved-release prefixes")
    seen_types: set[str] = set()
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            errors.append(f"Gate 2B research target {index} must be an object")
            continue
        target_type = target.get("target_type")
        relative_path = target.get("relative_path")
        if target_type not in expected_types:
            errors.append(f"Gate 2B research target {index} has invalid target_type")
        else:
            seen_types.add(target_type)
        if not _safe_relative_path(relative_path) or not RESEARCH_TARGET_PATTERN.fullmatch(relative_path):
            errors.append(
                f"Gate 2B research target {index} must be a dated file under 03_Research/YYYY-MM-DD_<run-id>/"
            )
    if gate.get("status") == "approved" and seen_types != expected_types:
        errors.append("an approved Gate 2B must name both research dossier and research handoff targets")


def _validate_material_targets(gate: dict, errors: list[str]) -> None:
    if "approved_exact_targets" in gate:
        errors.append("Gate 3 must use approved_material_targets, not approved_exact_targets")
    targets = gate.get("approved_material_targets")
    if not isinstance(targets, list):
        errors.append("Gate 3 approved_material_targets must be a list")
        targets = []
    rules = gate.get("target_rules", {})
    expected_map = {
        "working_copy": "04_Working_Copies/",
        "approved_release": "05_Approved/",
    }
    if rules.get("type_prefix_map") != expected_map:
        errors.append("Gate 3 material target types must map to 04_Working_Copies and 05_Approved")
    if rules.get("research_prefix_forbidden") != "03_Research/":
        errors.append("Gate 3 must forbid the 03_Research prefix for material targets")
    if rules.get("exact_targets_required_before_production") is not True:
        errors.append("Gate 3 must require exact material targets before production")
    if rules.get("gate_2b_research_target_approval_is_not_material_write_authority") is not True:
        errors.append("Gate 3 must not inherit material write authority from Gate 2B")
    for index, target in enumerate(targets):
        if not isinstance(target, dict):
            errors.append(f"Gate 3 material target {index} must be an object")
            continue
        target_type = target.get("target_type")
        relative_path = target.get("relative_path")
        required_prefix = expected_map.get(target_type)
        if required_prefix is None:
            errors.append(f"Gate 3 material target {index} has invalid target_type")
        if not _safe_relative_path(relative_path) or not (
            required_prefix and relative_path.startswith(required_prefix)
        ):
            errors.append(f"Gate 3 material target {index} violates its required prefix")
    if gate.get("status") == "approved" and not targets:
        errors.append("an approved Gate 3 must name at least one exact material target")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    if data.get("schema_version") != 6:
        errors.append("state schema_version must be 6")
    if data.get("status") not in {"candidate_not_active", "active", "suspended"}:
        errors.append("invalid top-level status")
    activation = data.get("activation", {})
    if activation.get("automatic_activation_forbidden") is not True:
        errors.append("automatic activation must be forbidden")
    separate = activation.get("separate_activation_decision", {})
    if not isinstance(separate, dict):
        errors.append("separate_activation_decision must be an object")
    contract = data.get("standing_schedule_contract_template", {})
    if contract.get("no_immediate_run") is not True:
        errors.append("standing schedule must forbid immediate runs")
    required_lines = contract.get("required_completed_approval_lines")
    expected = [
        "APPROVE SCHEDULES",
        "Schedule contract: <exact contract ID and version>",
        "Expires: <exact local date and time with IANA timezone>",
    ]
    if required_lines != expected:
        errors.append("standing schedule exact three-line approval is missing or changed")
    if contract.get("activation_requires_non_null_expires_at") is not True:
        errors.append("schedule activation must require an expiry")
    approval = data.get("schedule_registration", {}).get("approval", {})
    legacy_course_timezone_field = "parsed_expiry_europe" + "_zurich"
    if legacy_course_timezone_field in approval:
        errors.append("schedule template must not hardcode a course timezone")
    run_template = data.get("run_template", {})
    approvals = run_template.get("approvals", {})
    _validate_research_targets(approvals.get("gate_2b", {}), errors)
    _validate_material_targets(approvals.get("gate_3", {}), errors)
    envelope = run_template.get("specialist_return_envelope", {})
    fields = set(envelope.get("required_fields", []))
    for field in {
        "return_id",
        "run_id",
        "run_contract_id",
        "run_contract_version",
        "task_chat_reference",
        "shared_context_version",
        "source_manifest_fingerprint",
        "source_access_policy_version",
        "source_access_policy_fingerprint",
        "plan_version",
        "role_id",
        "stage_id",
    }:
        if field not in fields:
            errors.append(f"specialist return envelope missing {field}")
    retry = run_template.get("retry_policy", {})
    if retry.get("max_retries_per_specialist_per_stage") != 1:
        errors.append("retry ceiling must be exactly one per specialist per stage")
    if retry.get("replanning_never_resets_retry_counter") is not True:
        errors.append("replanning must not reset retry counters")
    coordination = run_template.get("coordination", {})
    stage_a = coordination.get("stage_a_role_statuses", [])
    expected_roles = {
        "course_mapper",
        "active_learning_researcher",
        "ai_integration_researcher",
        "student_experience_critic",
        "assessment_alignment_designer",
    }
    actual_roles = {
        item.get("role_id") for item in stage_a if isinstance(item, dict)
    }
    if actual_roles != expected_roles or len(stage_a) != 5:
        errors.append("Stage A must track exactly all five core roles")
    required_gate_2a = set(coordination.get("gate_2a_entry_requires", []))
    for requirement in {
        "all_five_stage_a_role_statuses_are_complete_accepted",
        "each_role_has_one_current_lineage_accepted_return_id",
        "preliminary_summary_exchange_complete",
        "live_alignment_ledger_started",
    }:
        if requirement not in required_gate_2a:
            errors.append(f"Gate 2A preconditions missing {requirement}")
    standing = data.get("standing_schedule_contract_template", {})
    runtime_versions = standing.get("runtime_versions", {})
    if runtime_versions.get("skill_name") != "course-redesign-orchestrator":
        errors.append("standing schedule must invoke course-redesign-orchestrator")
    naming_rule = standing.get("unique_output_naming_rule", "")
    if "03_Research/YYYY-MM-DD_<run-id>/" not in naming_rule or "02_Research" in naming_rule:
        errors.append("scheduled research output must use a unique dated 03_Research run folder")
    scheduled_after_gate_2b = set(
        standing.get("permitted_actions_after_fresh_gate_2b_target_approval", [])
    )
    for action in {
        "write_only_lecturer_approved_exact_research_dossier_and_research_handoff_targets_under_03_Research",
        "do_not_produce_course_materials_or_write_under_04_Working_Copies_or_05_Approved",
        "wait_at_gate_2b_and_end_schedule_authority",
    }:
        if action not in scheduled_after_gate_2b:
            errors.append(f"scheduled Gate 2B boundary missing {action}")
    if standing.get("write_authority") != (
        "research_dossier_and_research_handoff_under_03_Research_only_after_that_run_has_gate_2b_exact_research_target_approval"
    ):
        errors.append("scheduled write authority must be limited to Gate 2B research files")
    if data.get("status") == "candidate_not_active" and data.get("schedules") != []:
        errors.append("inactive template must register no schedules")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.state.read_text(encoding="utf-8"))
        errors = validate(data)
    except Exception as exc:
        errors = [f"{type(exc).__name__}: {exc}"]
    result = {
        "ok": not errors,
        "state": args.state.as_posix() if not args.state.is_absolute() else args.state.name,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
