#!/usr/bin/env python3
"""Preview a fail-closed course-redesign state migration from schema 6 to 7.

This helper never writes a state file. It emits a candidate state and an audit
report to stdout so that a human can review a later, separately authorised
migration.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any


LINEAGE_FIELDS = [
    "run_id",
    "run_contract_id",
    "run_contract_version",
    "task_chat_reference",
    "shared_context_version",
    "source_manifest_fingerprint",
    "source_access_policy_version",
    "source_access_policy_fingerprint",
    "plan_version",
]

HITL3_STATUSES = [
    "not_started",
    "awaiting_lecturer_decision",
    "revision_requested",
    "conditional_acceptance_pending_verification",
    "accepted",
    "rejected",
]

SYSTEM_REVIEW_OFFER_STATUSES = [
    "not_offered",
    "offered_awaiting_response",
    "requested",
    "declined",
]

MANDATORY_SYSTEM_REVIEW_QUESTION = (
    "Would you like a separate, read-only system-improvement review covering "
    "the workflow skills and umbrella entry routing; plugin or platform "
    "adapter; AGENTS.md and agent configurations; project template, state "
    "schema and migration; validators, tests and QA; documentation; memory or "
    "other workflow-owned durable instruction stores; schedule contracts; "
    "permissions, tools, external egress and automatic behaviour; and "
    "compatibility, benefits, regressions, risks, residual risks and rollback, "
    "followed only by a versioned proposal? A yes authorises only that review "
    "and proposal; it does not authorise system-file changes, installation, "
    "publication or release, runtime activation, schedule registration or "
    "modification, an immediate run, or any added MCP server, connector, "
    "authentication, permission or external egress."
)

REQUIRED_SYSTEM_REVIEW_SCOPE = [
    "workflow_skills_and_umbrella_entry_routing",
    "plugin_or_platform_adapter",
    "AGENTS_md_and_agent_configurations",
    "project_template_state_schema_and_migration",
    "validators_tests_and_quality_assurance",
    "documentation",
    "memory_or_other_workflow_owned_durable_instruction_stores",
    "schedule_contracts",
    "permissions_tools_external_egress_and_automatic_behaviour",
    "compatibility_benefits_regressions_risks_residual_risks_and_rollback",
]

V6_COMBINED_TRANSITION_TRIGGER = (
    "fresh_hitl3_acceptance_and_system_review_request_after_verified_production_handoff"
)

V7_SPLIT_TRANSITIONS = [
    {
        "trigger": "fresh_hitl3_acceptance_after_verified_production_handoff",
        "authorises_through": "SYSTEM_REVIEW_OFFER",
        "purpose": "materials_acceptance_and_mandatory_system_review_question_only",
        "does_not_authorise_candidate_activation": True,
    },
    {
        "trigger": "fresh_system_improvement_review_request",
        "authorises_through": "SYSTEM_GATE",
        "purpose": "read_only_system_review_and_versioned_proposal_only",
        "does_not_authorise_system_file_changes": True,
        "does_not_authorise_candidate_activation": True,
    },
]


class MigrationError(ValueError):
    """Raised when a preview cannot be produced without inventing state."""


def umbrella_entry_routing() -> dict[str, Any]:
    return {
        "entry_name": "Agentic Course Redesign",
        "entry_skill": "course-redesign-orchestrator",
        "initial_gate": "GATE_0_AWAITING_BOUNDARY_CONFIRMATION",
        "missing_project_action": "invoke_course-redesign-setup_preview_only",
        "gate_0_required_before_course_source_reading": True,
        "gate_0_required_before_specialist_work": True,
    }


def schema_compatibility() -> dict[str, Any]:
    return {
        "current_schema_version": 7,
        "minimum_preview_migration_source_version": 6,
        "migration_helper": "scripts/migrate_state_v6_to_v7.py",
        "migration_mode": "preview_only",
        "automatic_apply_forbidden": True,
        "preserve_during_preview": [
            "status",
            "schedules",
            "active_run_id",
            "existing_run_ids_and_lineage",
            "source_manifest_and_access_policy",
            "permissions_and_tool_egress_boundaries",
            "activation_and_schedule_registration_status",
        ],
    }


def _lineage_record() -> dict[str, Any]:
    return {field: None for field in LINEAGE_FIELDS}


def hitl3_record() -> dict[str, Any]:
    decision = _lineage_record()
    decision.update(
        {
            "decision": None,
            "allowed_decisions": [
                "accept",
                "conditionally_accept_named_corrections",
                "request_revision",
                "reject",
            ],
            "named_corrections": [],
            "corrections_verification_reference": None,
            "final_acceptance_reference": None,
            "reply_reference": None,
            "validation_status": "not_run",
            "recorded_at": None,
        }
    )
    return {
        "status": "not_started",
        "allowed_statuses": copy.deepcopy(HITL3_STATUSES),
        "entry_requires": [
            "production_completion.status_is_complete",
            "production_completion.declaration.completed_reply.validation_status_is_passed",
            "production_completion.handoff_approval.completed_reply.validation_status_is_passed",
            "production_completion.handoff_verified_at_is_non_null",
        ],
        "required_matching_lineage_fields": copy.deepcopy(LINEAGE_FIELDS),
        "decision": decision,
    }


def system_improvement_review_offer_record() -> dict[str, Any]:
    offer = {"offer_id": None, **_lineage_record()}
    offer.update(
        {
            "hitl_3_final_acceptance_reference": None,
            "question_scope_presented": [],
            "question_text": None,
            "offer_reference": None,
            "offered_at": None,
            "validation_status": "not_run",
        }
    )
    response = _lineage_record()
    response.update(
        {
            "decision": None,
            "allowed_decisions": [
                "request_read_only_system_improvement_review_and_versioned_proposal",
                "decline_system_improvement_review",
            ],
            "reply_reference": None,
            "responded_at": None,
            "validation_status": "not_run",
        }
    )
    return {
        "status": "not_offered",
        "allowed_statuses": copy.deepcopy(SYSTEM_REVIEW_OFFER_STATUSES),
        "entry_requires": [
            "hitl_3.status_is_accepted",
            "hitl_3.decision.validation_status_is_passed",
            "hitl_3.decision.final_acceptance_reference_is_non_null",
            "current_lineage_matches",
        ],
        "mandatory_question": MANDATORY_SYSTEM_REVIEW_QUESTION,
        "required_question_scope": copy.deepcopy(REQUIRED_SYSTEM_REVIEW_SCOPE),
        "ask_exactly_once": True,
        "record_offer_before_asking": True,
        "idempotency_key_fields": [
            "run_id",
            "hitl_3_final_acceptance_reference",
        ],
        "offer": offer,
        "response": response,
        "resume_behavior": {
            "not_offered": "ask_once_only_after_prerequisites_pass_and_persist_offer_first",
            "offered_awaiting_response": "resume_wait_without_reasking",
            "requested": "continue_read_only_review_and_versioned_proposal_only_without_reasking",
            "declined": "end_without_system_action_and_do_not_reask",
            "lineage_mismatch": "fail_closed_and_request_reconfirmation",
        },
        "authority_on_request": {
            "authorises": [
                "read_only_review_of_current_system_and_successful_run_evidence",
                "prepare_one_versioned_system_improvement_proposal",
            ],
            "does_not_authorise": [
                "create_or_modify_system_files",
                "install_or_update_plugin",
                "publish_or_release",
                "activate_runtime",
                "register_or_modify_schedule",
                "trigger_immediate_run",
                "add_mcp_server_connector_authentication_permission_or_external_egress",
            ],
            "candidate_file_changes_require": "separate_system_gate_with_APPROVE SYSTEM FILES",
            "activation_requires": "later_separate_activation_decision",
            "schedule_requires": "active_matching_runtime_plus_no_write_simulation_and_separate_expiring_schedule_approval",
        },
    }


def resume_protocol() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "checkpoint_order": [
            "approvals.production_completion.declaration",
            "approvals.production_completion.handoff_approval",
            "approvals.production_completion.handoff_verified_at",
            "approvals.hitl_3",
            "approvals.system_improvement_review_offer",
        ],
        "receipt_reference_fields": [
            "approvals.production_completion.declaration.completed_reply.reply_reference",
            "approvals.production_completion.handoff_approval.completed_reply.reply_reference",
            "approvals.production_completion.handoff_verified_at",
            "approvals.hitl_3.decision.final_acceptance_reference",
            "approvals.system_improvement_review_offer.offer.offer_reference",
            "approvals.system_improvement_review_offer.response.reply_reference",
        ],
        "rules": {
            "persist_receipt_before_advancing_next_permitted_action": True,
            "same_receipt_reference_is_idempotent": True,
            "completed_checkpoint_must_not_repeat": True,
            "resume_from_first_incomplete_checkpoint": True,
            "current_lineage_required_before_resume": True,
            "lineage_mismatch_fails_closed": True,
        },
    }


def _run_records(data: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    template = data.get("run_template")
    runs = data.get("runs")
    if not isinstance(template, dict) or not isinstance(runs, list):
        raise MigrationError("schema-6 state must contain run_template object and runs list")
    records: list[tuple[str, dict[str, Any]]] = [("run_template", template)]
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            raise MigrationError(f"runs[{index}] must be an object")
        records.append((f"runs[{index}]", run))
    return records


def _replace_combined_transition(label: str, run: dict[str, Any]) -> None:
    authority = run.get("manual_stage_authority")
    if not isinstance(authority, dict) or not isinstance(authority.get("transition_rules"), list):
        raise MigrationError(f"{label}.manual_stage_authority.transition_rules is missing")
    rules = authority["transition_rules"]
    matches = [
        index
        for index, rule in enumerate(rules)
        if isinstance(rule, dict) and rule.get("trigger") == V6_COMBINED_TRANSITION_TRIGGER
    ]
    if len(matches) != 1:
        raise MigrationError(
            f"{label} must contain exactly one recognised schema-6 combined post-HITL3 transition"
        )
    index = matches[0]
    rules[index : index + 1] = copy.deepcopy(V7_SPLIT_TRANSITIONS)


def _check_v7_shape(data: dict[str, Any]) -> None:
    if data.get("schema_version") != 7:
        raise MigrationError("candidate is not schema 7")
    if data.get("umbrella_entry_routing") != umbrella_entry_routing():
        raise MigrationError("schema-7 umbrella_entry_routing is missing or divergent")
    compatibility = data.get("schema_compatibility")
    if compatibility != schema_compatibility():
        raise MigrationError("schema-7 preview-only compatibility record is missing")
    for label, run in _run_records(data):
        approvals = run.get("approvals")
        if not isinstance(approvals, dict):
            raise MigrationError(f"{label}.approvals is missing")
        if approvals.get("hitl_3") != hitl3_record():
            if approvals.get("hitl_3", {}).get("allowed_statuses") != HITL3_STATUSES:
                raise MigrationError(f"{label}.approvals.hitl_3 shape is missing or divergent")
        offer = approvals.get("system_improvement_review_offer")
        if not isinstance(offer, dict) or offer.get("allowed_statuses") != SYSTEM_REVIEW_OFFER_STATUSES:
            raise MigrationError(
                f"{label}.approvals.system_improvement_review_offer shape is missing or divergent"
            )
        if offer.get("mandatory_question") != MANDATORY_SYSTEM_REVIEW_QUESTION:
            raise MigrationError(f"{label} system-review mandatory question is divergent")
        if offer.get("required_question_scope") != REQUIRED_SYSTEM_REVIEW_SCOPE:
            raise MigrationError(f"{label} system-review mandatory scope is divergent")
        expected_authority = system_improvement_review_offer_record()["authority_on_request"]
        if offer.get("authority_on_request") != expected_authority:
            raise MigrationError(f"{label} system-review request authority is divergent")
        if offer.get("ask_exactly_once") is not True or offer.get(
            "record_offer_before_asking"
        ) is not True:
            raise MigrationError(f"{label} system-review exactly-once controls are divergent")
        if run.get("resume_protocol") != resume_protocol():
            raise MigrationError(f"{label}.resume_protocol is missing or divergent")
        triggers = {
            rule.get("trigger"): rule
            for rule in run.get("manual_stage_authority", {}).get("transition_rules", [])
            if isinstance(rule, dict)
        }
        for expected_transition in V7_SPLIT_TRANSITIONS:
            if triggers.get(expected_transition["trigger"]) != expected_transition:
                raise MigrationError(f"{label} schema-7 split transition is missing or divergent")
    update = data.get("activation", {}).get("system_update", {})
    if update.get("allowed_statuses") != [
        "not_started",
        "proposal_requested",
        "proposal_presented",
        "candidate_change_approved",
        "validated",
    ]:
        raise MigrationError("schema-7 system update statuses are missing or divergent")
    if set(update.get("prerequisites", [])) != {
        "matching_run_production_completion_complete",
        "matching_run_production_handoff_verified",
        "matching_run_hitl_3_accepted",
        "matching_run_system_improvement_review_offer_requested",
    }:
        raise MigrationError("schema-7 system update prerequisites are missing or divergent")
    requirements = set(update.get("completed_reply_requirements", []))
    if not {"run_id", "system_improvement_review_offer_reference"}.issubset(requirements):
        raise MigrationError("schema-7 system update lineage/offer requirements are missing")
    if not {
        "hitl_3_accepted",
        "system_improvement_review_offer_requested",
    }.issubset(set(data.get("activation", {}).get("required_before_active", []))):
        raise MigrationError("schema-7 activation prerequisites omit HITL3 or requested offer")


def _check_full_v7_state(data: dict[str, Any]) -> None:
    # The current validator targets schema 8. Keep this legacy staged helper
    # preview-only and validate its complete schema-7 control shape locally;
    # callers must then run migrate_state_v7_to_v8.py before any use.
    _check_v7_shape(data)
    try:
        json.dumps(data, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError) as exc:
        raise MigrationError(f"schema-7 candidate is not serializable: {exc}") from exc


def _preservation_checks(source: dict[str, Any], candidate: dict[str, Any]) -> dict[str, bool]:
    checks = {
        "status": candidate.get("status") == source.get("status"),
        "schedules": candidate.get("schedules") == source.get("schedules"),
        "active_run_id": candidate.get("active_run_id") == source.get("active_run_id"),
        "source_manifest": candidate.get("source_manifest") == source.get("source_manifest"),
        "source_access_policy": candidate.get("source_access_policy")
        == source.get("source_access_policy"),
        "schedule_registration_status": candidate.get("schedule_registration", {}).get("status")
        == source.get("schedule_registration", {}).get("status"),
        "activation_decision_status": candidate.get("activation", {})
        .get("separate_activation_decision", {})
        .get("status")
        == source.get("activation", {}).get("separate_activation_decision", {}).get("status"),
    }
    source_runs = _run_records(source)
    candidate_runs = _run_records(candidate)
    checks["run_count"] = len(source_runs) == len(candidate_runs)
    for (source_label, source_run), (candidate_label, candidate_run) in zip(
        source_runs, candidate_runs
    ):
        if source_label != candidate_label:
            checks[f"{source_label}.identity"] = False
            continue
        for field in ("run_id", "task_chat_reference", "active_run_id", "plan_version"):
            checks[f"{source_label}.{field}"] = candidate_run.get(field) == source_run.get(field)
        for field in (
            "contract_id",
            "version",
            "permitted_tools",
            "permitted_actions",
            "approved_source_classes",
            "approved_output_audiences",
            "source_access_policy_version",
            "source_access_policy_fingerprint",
        ):
            checks[f"{source_label}.contract.{field}"] = candidate_run.get("contract", {}).get(
                field
            ) == source_run.get("contract", {}).get(field)
        checks[f"{source_label}.shared_context.version"] = candidate_run.get(
            "shared_context", {}
        ).get("version") == source_run.get("shared_context", {}).get("version")
        checks[f"{source_label}.source_manifest_verification"] = candidate_run.get(
            "source_manifest_verification"
        ) == source_run.get("source_manifest_verification")
    return checks


def preview_migration(data: dict[str, Any], source: str = "<memory>") -> dict[str, Any]:
    """Return a preview report and candidate state without mutating *data*."""

    if not isinstance(data, dict):
        raise MigrationError("state root must be an object")
    source_schema = data.get("schema_version")
    if source_schema == 7:
        candidate = copy.deepcopy(data)
        _check_v7_shape(candidate)
        _check_full_v7_state(candidate)
        return {
            "ok": True,
            "mode": "preview_only",
            "would_write": False,
            "source": source,
            "source_schema_version": 7,
            "target_schema_version": 7,
            "changed_paths": [],
            "preservation_checks": {"already_schema_7_unchanged": True},
            "candidate_state": candidate,
        }
    if source_schema != 6:
        raise MigrationError("only schema 6 input or an already-valid schema 7 preview is supported")

    source_copy = copy.deepcopy(data)
    candidate = copy.deepcopy(data)
    for key in ("umbrella_entry_routing", "schema_compatibility"):
        if key in candidate:
            raise MigrationError(f"schema-6 state unexpectedly contains {key}; refusing to overwrite")

    candidate["schema_version"] = 7
    candidate["umbrella_entry_routing"] = umbrella_entry_routing()
    candidate["schema_compatibility"] = schema_compatibility()
    changed_paths = [
        "schema_version",
        "umbrella_entry_routing",
        "schema_compatibility",
    ]

    for label, run in _run_records(candidate):
        approvals = run.get("approvals")
        if not isinstance(approvals, dict):
            raise MigrationError(f"{label}.approvals is missing")
        for key in ("hitl_3", "system_improvement_review_offer"):
            if key in approvals:
                raise MigrationError(f"schema-6 {label}.approvals unexpectedly contains {key}")
        if "resume_protocol" in run:
            raise MigrationError(f"schema-6 {label} unexpectedly contains resume_protocol")
        approvals["hitl_3"] = hitl3_record()
        approvals["system_improvement_review_offer"] = system_improvement_review_offer_record()
        run["resume_protocol"] = resume_protocol()
        _replace_combined_transition(label, run)
        changed_paths.extend(
            [
                f"{label}.approvals.hitl_3",
                f"{label}.approvals.system_improvement_review_offer",
                f"{label}.resume_protocol",
                f"{label}.manual_stage_authority.transition_rules",
            ]
        )

    system_update = candidate.get("activation", {}).get("system_update")
    if not isinstance(system_update, dict):
        raise MigrationError("activation.system_update is missing")
    for key in ("allowed_statuses", "prerequisites"):
        if key in system_update:
            raise MigrationError(f"schema-6 activation.system_update unexpectedly contains {key}")
    system_update["allowed_statuses"] = [
        "not_started",
        "proposal_requested",
        "proposal_presented",
        "candidate_change_approved",
        "validated",
    ]
    system_update["prerequisites"] = [
        "matching_run_production_completion_complete",
        "matching_run_production_handoff_verified",
        "matching_run_hitl_3_accepted",
        "matching_run_system_improvement_review_offer_requested",
    ]
    requirements = system_update.get("completed_reply_requirements")
    approval = system_update.get("approval")
    if not isinstance(requirements, list) or not isinstance(approval, dict):
        raise MigrationError("activation.system_update approval schema is missing")
    if "run_id" not in requirements:
        insertion = requirements.index("validation_run_id") + 1
        requirements.insert(insertion, "run_id")
    if "system_improvement_review_offer_reference" not in requirements:
        insertion = requirements.index("proposal_version") + 1
        requirements.insert(insertion, "system_improvement_review_offer_reference")
    approval.setdefault("run_id", None)
    approval.setdefault("system_improvement_review_offer_reference", None)
    changed_paths.extend(
        [
            "activation.system_update.allowed_statuses",
            "activation.system_update.prerequisites",
            "activation.system_update.completed_reply_requirements",
            "activation.system_update.approval.run_id",
            "activation.system_update.approval.system_improvement_review_offer_reference",
        ]
    )

    required_before_active = candidate.get("activation", {}).get("required_before_active")
    if not isinstance(required_before_active, list):
        raise MigrationError("activation.required_before_active is missing")
    before = required_before_active.index("system_update_approved")
    for requirement in (
        "hitl_3_accepted",
        "system_improvement_review_offer_requested",
    ):
        if requirement not in required_before_active:
            required_before_active.insert(before, requirement)
            before += 1
    changed_paths.append("activation.required_before_active")

    checks = _preservation_checks(source_copy, candidate)
    failed = sorted(name for name, passed in checks.items() if not passed)
    if failed:
        raise MigrationError(f"preview changed protected existing values: {', '.join(failed)}")
    _check_v7_shape(candidate)
    _check_full_v7_state(candidate)
    return {
        "ok": True,
        "mode": "preview_only",
        "would_write": False,
        "source": source,
        "source_schema_version": 6,
        "target_schema_version": 7,
        "changed_paths": changed_paths,
        "preservation_checks": checks,
        "candidate_state": candidate,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="schema-6 or already-valid schema-7 state")
    args = parser.parse_args()
    try:
        raw = args.state.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        report = preview_migration(data, source=args.state.as_posix())
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
