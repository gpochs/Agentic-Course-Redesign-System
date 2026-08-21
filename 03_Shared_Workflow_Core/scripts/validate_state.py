#!/usr/bin/env python3
"""Validate essential fail-closed invariants in a course-redesign state file."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "status",
    "umbrella_entry_routing",
    "schema_compatibility",
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
PRODUCTION_HANDOFF_PATTERN = re.compile(
    r"^04_Working_Copies/[A-Za-z0-9._-]+/Production_Handoff\.md$"
)

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

EXPECTED_UMBRELLA_ROUTING = {
    "entry_name": "Agentic Course Redesign",
    "entry_skill": "course-redesign-orchestrator",
    "initial_gate": "GATE_0_AWAITING_BOUNDARY_CONFIRMATION",
    "missing_project_action": "invoke_course-redesign-setup_preview_only",
    "gate_0_required_before_course_source_reading": True,
    "gate_0_required_before_specialist_work": True,
}

EXPECTED_RESUME_PROTOCOL = {
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


def _expected_lineage(run: dict) -> dict[str, object]:
    contract = run.get("contract", {})
    context = run.get("shared_context", {})
    verification = run.get("source_manifest_verification", {})
    return {
        "run_id": run.get("run_id"),
        "run_contract_id": contract.get("contract_id"),
        "run_contract_version": contract.get("version"),
        "task_chat_reference": run.get("task_chat_reference"),
        "shared_context_version": context.get("version"),
        "source_manifest_fingerprint": verification.get("source_manifest_fingerprint"),
        "source_access_policy_version": verification.get("source_access_policy_version"),
        "source_access_policy_fingerprint": verification.get(
            "source_access_policy_fingerprint"
        ),
        "plan_version": run.get("plan_version"),
    }


def _lineage_value_missing(field: str, value: object) -> bool:
    if value is None or value == "":
        return True
    return field in {
        "run_contract_version",
        "shared_context_version",
        "source_access_policy_version",
        "plan_version",
    } and value == 0


def _validate_lineage_record(
    record: object,
    expected: dict[str, object],
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(record, dict):
        errors.append(f"{label} must be an object with current lineage")
        return
    for field in LINEAGE_FIELDS:
        expected_value = expected.get(field)
        if _lineage_value_missing(field, expected_value):
            errors.append(f"{label} cannot validate because current run lineage is missing {field}")
        elif record.get(field) != expected_value:
            errors.append(f"{label} has stale or mismatched {field}")


def _record_has_progress(record: object, fields: set[str]) -> bool:
    return isinstance(record, dict) and any(record.get(field) not in {None, "", "not_run"} for field in fields)


def _validate_resume_protocol(run: dict, label: str, errors: list[str]) -> None:
    if run.get("resume_protocol") != EXPECTED_RESUME_PROTOCOL:
        errors.append(f"{label} resume_protocol must preserve exactly-once fail-closed recovery")


def _validate_production_hitl3_offer(
    run: dict,
    label: str,
    errors: list[str],
) -> str | None:
    transitions = run.get("manual_stage_authority", {}).get("transition_rules", [])
    if not isinstance(transitions, list):
        errors.append(f"{label} manual stage transition rules must be a list")
        transitions = []
    by_trigger = {
        item.get("trigger"): item for item in transitions if isinstance(item, dict)
    }
    if (
        "fresh_hitl3_acceptance_and_system_review_request_after_verified_production_handoff"
        in by_trigger
    ):
        errors.append(f"{label} must not conflate HITL3 acceptance with system-review request")
    expected_hitl3_transition = {
        "trigger": "fresh_hitl3_acceptance_after_verified_production_handoff",
        "authorises_through": "SYSTEM_REVIEW_OFFER",
        "purpose": "materials_acceptance_and_mandatory_system_review_question_only",
        "does_not_authorise_candidate_activation": True,
    }
    expected_offer_transition = {
        "trigger": "fresh_system_improvement_review_request",
        "authorises_through": "SYSTEM_GATE",
        "purpose": "read_only_system_review_and_versioned_proposal_only",
        "does_not_authorise_system_file_changes": True,
        "does_not_authorise_candidate_activation": True,
    }
    if by_trigger.get(expected_hitl3_transition["trigger"]) != expected_hitl3_transition:
        errors.append(f"{label} HITL3 transition must stop at the mandatory review offer")
    if by_trigger.get(expected_offer_transition["trigger"]) != expected_offer_transition:
        errors.append(f"{label} review request transition must remain proposal-only")

    approvals = run.get("approvals", {})
    if not isinstance(approvals, dict):
        errors.append(f"{label}.approvals must be an object")
        return None
    expected = _expected_lineage(run)
    template_only = run.get("template_only") is True

    production = approvals.get("production_completion", {})
    production_statuses = [
        "not_started",
        "awaiting_declaration",
        "declared_awaiting_handoff_approval",
        "handoff_approved_awaiting_verification",
        "complete",
    ]
    if not isinstance(production, dict):
        errors.append(f"{label}.approvals.production_completion must be an object")
        return None
    if production.get("allowed_statuses") != production_statuses:
        errors.append(f"{label} production completion statuses are missing or reordered")
    production_status = production.get("status")
    if production_status not in production_statuses:
        errors.append(f"{label} has invalid production completion status")
        production_index = 0
    else:
        production_index = production_statuses.index(production_status)
    if production.get("required_matching_lineage_fields") != LINEAGE_FIELDS:
        errors.append(f"{label} production completion must require exact current lineage")

    declaration = production.get("declaration", {})
    declaration_reply = declaration.get("completed_reply", {}) if isinstance(declaration, dict) else {}
    if declaration.get("required_standalone_line") != "DECLARE PRODUCTION COMPLETE":
        errors.append(f"{label} production declaration token is missing or changed")
    if production_index >= 2:
        if template_only:
            errors.append(f"{label} template cannot be advanced past production declaration")
        _validate_lineage_record(declaration_reply, expected, f"{label} production declaration", errors)
        if declaration_reply.get("standalone_line") != "DECLARE PRODUCTION COMPLETE":
            errors.append(f"{label} production declaration must contain the standalone line")
        if declaration_reply.get("validation_status") != "passed":
            errors.append(f"{label} production declaration must be validated before handoff")
        for field in ("reply_reference", "recorded_at"):
            if not declaration_reply.get(field):
                errors.append(f"{label} production declaration is missing {field}")
    elif _record_has_progress(
        declaration_reply,
        {"standalone_line", "reply_reference", "recorded_at", "validation_status"},
    ):
        errors.append(f"{label} production declaration receipt exists before its status advances")

    handoff = production.get("handoff_approval", {})
    handoff_reply = handoff.get("completed_reply", {}) if isinstance(handoff, dict) else {}
    if handoff.get("required_standalone_line") != "APPROVE PRODUCTION HANDOFF":
        errors.append(f"{label} production handoff approval token is missing or changed")
    handoff_target = handoff.get("exact_handoff_target")
    if production_index >= 3:
        if template_only:
            errors.append(f"{label} template cannot be advanced past handoff approval")
        if not _safe_relative_path(handoff_target) or not PRODUCTION_HANDOFF_PATTERN.fullmatch(
            handoff_target or ""
        ):
            errors.append(f"{label} Production Handoff target must be the exact approved working-copy path")
        _validate_lineage_record(handoff_reply, expected, f"{label} handoff approval", errors)
        if handoff_reply.get("standalone_line") != "APPROVE PRODUCTION HANDOFF":
            errors.append(f"{label} handoff approval must contain the standalone line")
        if handoff_reply.get("repeated_exact_handoff_target") != handoff_target:
            errors.append(f"{label} handoff approval must repeat the exact handoff target")
        expected_handoff_target = (
            f"04_Working_Copies/{expected.get('run_id')}/Production_Handoff.md"
        )
        if handoff_target != expected_handoff_target:
            errors.append(f"{label} Production Handoff target must belong to the current run")
        if handoff_reply.get("validation_status") != "passed":
            errors.append(f"{label} handoff approval must be validated before verification")
        for field in ("reply_reference", "recorded_at"):
            if not handoff_reply.get(field):
                errors.append(f"{label} handoff approval is missing {field}")
        declaration_reference = declaration_reply.get("reply_reference")
        handoff_reference = handoff_reply.get("reply_reference")
        if declaration_reference and declaration_reference == handoff_reference:
            errors.append(
                f"{label} production declaration and handoff approval must use distinct reply references"
            )
    elif _record_has_progress(
        handoff_reply,
        {
            "standalone_line",
            "repeated_exact_handoff_target",
            "reply_reference",
            "recorded_at",
            "validation_status",
        },
    ):
        errors.append(f"{label} handoff approval receipt exists before declaration/approval sequencing")

    handoff_verified_at = production.get("handoff_verified_at")
    if production_status == "complete" and not handoff_verified_at:
        errors.append(f"{label} production cannot be complete before handoff verification")
    if production_status != "complete" and handoff_verified_at:
        errors.append(f"{label} handoff verification receipt cannot precede production completion")

    hitl3 = approvals.get("hitl_3", {})
    if not isinstance(hitl3, dict):
        errors.append(f"{label}.approvals.hitl_3 must be an object")
        return None
    if hitl3.get("allowed_statuses") != HITL3_STATUSES:
        errors.append(f"{label} HITL3 statuses are missing or reordered")
    expected_hitl3_entry = [
        "production_completion.status_is_complete",
        "production_completion.declaration.completed_reply.validation_status_is_passed",
        "production_completion.handoff_approval.completed_reply.validation_status_is_passed",
        "production_completion.handoff_verified_at_is_non_null",
    ]
    if hitl3.get("entry_requires") != expected_hitl3_entry:
        errors.append(f"{label} HITL3 must require declared, approved and verified production handoff")
    if hitl3.get("required_matching_lineage_fields") != LINEAGE_FIELDS:
        errors.append(f"{label} HITL3 must require exact current lineage")
    hitl3_status = hitl3.get("status")
    if hitl3_status not in HITL3_STATUSES:
        errors.append(f"{label} has invalid HITL3 status")
        hitl3_status = "not_started"
    if hitl3_status != "not_started" and production_status != "complete":
        errors.append(f"{label} HITL3 cannot open before production handoff verification")
    decision = hitl3.get("decision", {})
    if not isinstance(decision, dict):
        errors.append(f"{label} HITL3 decision must be an object")
        decision = {}
    if decision.get("allowed_decisions") != [
        "accept",
        "conditionally_accept_named_corrections",
        "request_revision",
        "reject",
    ]:
        errors.append(f"{label} HITL3 allowed decisions are missing or reordered")
    if hitl3_status in {
        "revision_requested",
        "conditional_acceptance_pending_verification",
        "accepted",
        "rejected",
    }:
        if template_only:
            errors.append(f"{label} template cannot contain a completed HITL3 decision")
        _validate_lineage_record(decision, expected, f"{label} HITL3 decision", errors)
        if decision.get("validation_status") != "passed":
            errors.append(f"{label} HITL3 decision must be validated")
        for field in ("reply_reference", "recorded_at"):
            if not decision.get(field):
                errors.append(f"{label} HITL3 decision is missing {field}")
    elif _record_has_progress(
        decision,
        {
            "decision",
            "reply_reference",
            "final_acceptance_reference",
            "recorded_at",
            "validation_status",
        },
    ):
        errors.append(f"{label} HITL3 decision receipt exists before its status advances")
    decision_value = decision.get("decision")
    if hitl3_status == "revision_requested" and decision_value != "request_revision":
        errors.append(f"{label} HITL3 revision status must carry request_revision")
    if hitl3_status == "rejected" and decision_value != "reject":
        errors.append(f"{label} HITL3 rejected status must carry reject")
    if hitl3_status == "conditional_acceptance_pending_verification":
        if decision_value != "conditionally_accept_named_corrections":
            errors.append(f"{label} conditional HITL3 status must name conditional acceptance")
        if not decision.get("named_corrections"):
            errors.append(f"{label} conditional HITL3 acceptance must name corrections")
        if decision.get("corrections_verification_reference") or decision.get(
            "final_acceptance_reference"
        ):
            errors.append(f"{label} conditional HITL3 status cannot claim verified final acceptance")
    if hitl3_status == "accepted":
        if decision_value not in {"accept", "conditionally_accept_named_corrections"}:
            errors.append(f"{label} accepted HITL3 must carry an acceptance decision")
        if not decision.get("final_acceptance_reference"):
            errors.append(f"{label} accepted HITL3 is missing final_acceptance_reference")
        if decision_value == "conditionally_accept_named_corrections":
            if not decision.get("named_corrections"):
                errors.append(f"{label} conditional HITL3 acceptance must name corrections")
            if not decision.get("corrections_verification_reference"):
                errors.append(f"{label} conditional HITL3 acceptance requires verified corrections")

    offer_gate = approvals.get("system_improvement_review_offer", {})
    if not isinstance(offer_gate, dict):
        errors.append(f"{label}.approvals.system_improvement_review_offer must be an object")
        return None
    if offer_gate.get("allowed_statuses") != SYSTEM_REVIEW_OFFER_STATUSES:
        errors.append(f"{label} system-review offer statuses are missing or reordered")
    if offer_gate.get("mandatory_question") != MANDATORY_SYSTEM_REVIEW_QUESTION:
        errors.append(f"{label} system-review offer must contain the complete mandatory question")
    if offer_gate.get("required_question_scope") != REQUIRED_SYSTEM_REVIEW_SCOPE:
        errors.append(f"{label} system-review question scope is incomplete or reordered")
    if offer_gate.get("ask_exactly_once") is not True:
        errors.append(f"{label} system-review question must be asked exactly once")
    if offer_gate.get("record_offer_before_asking") is not True:
        errors.append(f"{label} system-review offer must be persisted before asking")
    if offer_gate.get("idempotency_key_fields") != [
        "run_id",
        "hitl_3_final_acceptance_reference",
    ]:
        errors.append(f"{label} system-review offer idempotency fields are invalid")
    expected_offer_entry = [
        "hitl_3.status_is_accepted",
        "hitl_3.decision.validation_status_is_passed",
        "hitl_3.decision.final_acceptance_reference_is_non_null",
        "current_lineage_matches",
    ]
    if offer_gate.get("entry_requires") != expected_offer_entry:
        errors.append(f"{label} system-review offer must require accepted current-lineage HITL3")
    authority = offer_gate.get("authority_on_request", {})
    if set(authority.get("authorises", [])) != {
        "read_only_review_of_current_system_and_successful_run_evidence",
        "prepare_one_versioned_system_improvement_proposal",
    }:
        errors.append(f"{label} system-review request must authorise only review and proposal")
    if set(authority.get("does_not_authorise", [])) != {
        "create_or_modify_system_files",
        "install_or_update_plugin",
        "publish_or_release",
        "activate_runtime",
        "register_or_modify_schedule",
        "trigger_immediate_run",
        "add_mcp_server_connector_authentication_permission_or_external_egress",
    }:
        errors.append(f"{label} system-review request forbidden-authority list is incomplete")
    if authority.get("candidate_file_changes_require") != (
        "separate_system_gate_with_APPROVE SYSTEM FILES"
    ):
        errors.append(f"{label} candidate changes must require a separate System Gate")
    if authority.get("activation_requires") != "later_separate_activation_decision":
        errors.append(f"{label} review request must not activate the runtime")
    if authority.get("schedule_requires") != (
        "active_matching_runtime_plus_no_write_simulation_and_separate_expiring_schedule_approval"
    ):
        errors.append(f"{label} review request must not register or alter schedules")
    expected_resume_behavior = {
        "not_offered": "ask_once_only_after_prerequisites_pass_and_persist_offer_first",
        "offered_awaiting_response": "resume_wait_without_reasking",
        "requested": "continue_read_only_review_and_versioned_proposal_only_without_reasking",
        "declined": "end_without_system_action_and_do_not_reask",
        "lineage_mismatch": "fail_closed_and_request_reconfirmation",
    }
    if offer_gate.get("resume_behavior") != expected_resume_behavior:
        errors.append(f"{label} system-review resume behavior is missing or divergent")

    offer_status = offer_gate.get("status")
    if offer_status not in SYSTEM_REVIEW_OFFER_STATUSES:
        errors.append(f"{label} has invalid system-review offer status")
        offer_status = "not_offered"
    offer = offer_gate.get("offer", {})
    response = offer_gate.get("response", {})
    if not isinstance(offer, dict):
        errors.append(f"{label} system-review offer receipt must be an object")
        offer = {}
    if not isinstance(response, dict):
        errors.append(f"{label} system-review response receipt must be an object")
        response = {}
    if response.get("allowed_decisions") != [
        "request_read_only_system_improvement_review_and_versioned_proposal",
        "decline_system_improvement_review",
    ]:
        errors.append(f"{label} system-review response decisions are missing or reordered")
    if offer_status != "not_offered":
        if hitl3_status != "accepted":
            errors.append(f"{label} system-review offer cannot precede accepted HITL3")
        if template_only:
            errors.append(f"{label} template cannot contain a presented system-review offer")
        _validate_lineage_record(offer, expected, f"{label} system-review offer", errors)
        if offer.get("validation_status") != "passed":
            errors.append(f"{label} system-review offer must be validated before asking")
        for field in ("offer_id", "offer_reference", "offered_at"):
            if not offer.get(field):
                errors.append(f"{label} system-review offer is missing {field}")
        if offer.get("hitl_3_final_acceptance_reference") != decision.get(
            "final_acceptance_reference"
        ):
            errors.append(f"{label} system-review offer is not bound to final HITL3 acceptance")
        if offer.get("question_text") != MANDATORY_SYSTEM_REVIEW_QUESTION:
            errors.append(f"{label} recorded system-review question is incomplete")
        if offer.get("question_scope_presented") != REQUIRED_SYSTEM_REVIEW_SCOPE:
            errors.append(f"{label} recorded system-review scope is incomplete or reordered")
        expected_offer_id = (
            f"system-review-offer:{expected.get('run_id')}:"
            f"{decision.get('final_acceptance_reference')}"
        )
        if offer.get("offer_id") != expected_offer_id:
            errors.append(f"{label} system-review offer idempotency key does not match its inputs")
    elif _record_has_progress(
        offer,
        {"offer_id", "offer_reference", "offered_at", "validation_status"},
    ):
        errors.append(f"{label} system-review offer receipt exists while status is not_offered")

    if offer_status in {"requested", "declined"}:
        _validate_lineage_record(response, expected, f"{label} system-review response", errors)
        if response.get("validation_status") != "passed":
            errors.append(f"{label} system-review response must be validated")
        for field in ("reply_reference", "responded_at"):
            if not response.get(field):
                errors.append(f"{label} system-review response is missing {field}")
        expected_decision = (
            "request_read_only_system_improvement_review_and_versioned_proposal"
            if offer_status == "requested"
            else "decline_system_improvement_review"
        )
        if response.get("decision") != expected_decision:
            errors.append(f"{label} system-review response does not match its status")
        if response.get("reply_reference") and response.get("reply_reference") == decision.get(
            "reply_reference"
        ):
            errors.append(
                f"{label} HITL3 decision and system-review response must use distinct reply references"
            )
    elif offer_status == "offered_awaiting_response" and _record_has_progress(
        response,
        {"decision", "reply_reference", "responded_at", "validation_status"},
    ):
        errors.append(f"{label} system-review response cannot be recorded before status advances")
    elif offer_status == "not_offered" and _record_has_progress(
        response,
        {"decision", "reply_reference", "responded_at", "validation_status"},
    ):
        errors.append(f"{label} system-review response cannot precede its offer")

    _validate_resume_protocol(run, label, errors)
    return offer.get("offer_id") if offer_status != "not_offered" else None


def _validated_exact_targets(value: object, label: str, errors: list[str]) -> list[str]:
    if not isinstance(value, list) or not value:
        errors.append(f"{label} must name at least one exact target")
        return []
    targets: list[str] = []
    for index, target in enumerate(value):
        if not _safe_relative_path(target):
            errors.append(f"{label}[{index}] must be a safe exact repository-relative path")
        else:
            targets.append(target)
    if len(targets) != len(set(targets)):
        errors.append(f"{label} must not contain duplicate targets")
    return targets


def _validate_system_update_progression(
    activation: dict,
    system_update: dict,
    expected_statuses: list[str],
    runs_by_id: dict[object, dict],
    errors: list[str],
) -> None:
    system_status = system_update.get("status")
    if system_status not in expected_statuses:
        errors.append("invalid system update status")
        return

    approval = system_update.get("approval", {})
    if not isinstance(approval, dict):
        errors.append("activation.system_update.approval must be an object")
        approval = {}

    if system_status == "not_started":
        if any(
            system_update.get(field) not in {None, ""}
            for field in ("proposal_id", "proposal_version", "proposal_reference")
        ) or system_update.get("proposed_exact_targets") not in (None, []):
            errors.append("system update proposal data cannot precede proposal_requested status")
        if _record_has_progress(
            approval,
            {
                *LINEAGE_FIELDS,
                "validation_run_id",
                "standalone_line",
                "proposal_id",
                "proposal_version",
                "system_improvement_review_offer_reference",
                "completed_reply_reference",
                "validation_status",
                "recorded_at",
            },
        ) or approval.get("approved_exact_targets") not in (None, []):
            errors.append("system update approval receipt cannot precede proposal_requested status")
        return

    source_run_id = approval.get("run_id")
    source_run = runs_by_id.get(source_run_id)
    source_offer: dict = {}
    if source_run is None:
        errors.append("system update must identify one existing successful source run")
    else:
        _validate_lineage_record(
            approval,
            _expected_lineage(source_run),
            "activation.system_update.approval",
            errors,
        )
        source_offer = source_run.get("approvals", {}).get(
            "system_improvement_review_offer", {}
        )
        if source_offer.get("status") != "requested":
            errors.append("system update cannot begin before the source run requests review")
        source_offer_reference = source_offer.get("offer", {}).get("offer_reference")
        if approval.get("system_improvement_review_offer_reference") != source_offer_reference:
            errors.append("system update is not bound to the requested review offer")

    status_index = expected_statuses.index(system_status)
    if status_index >= expected_statuses.index("proposal_presented"):
        for field in ("proposal_id", "proposal_version", "proposal_reference"):
            if not system_update.get(field):
                errors.append(f"presented system update is missing {field}")
        _validated_exact_targets(
            system_update.get("proposed_exact_targets"),
            "activation.system_update.proposed_exact_targets",
            errors,
        )

    if status_index < expected_statuses.index("candidate_change_approved"):
        for field in (
            "validation_run_id",
            "standalone_line",
            "proposal_id",
            "proposal_version",
            "completed_reply_reference",
            "recorded_at",
        ):
            if approval.get(field):
                errors.append(f"System Gate field {field} cannot precede candidate_change_approved")
        if approval.get("approved_exact_targets") not in (None, []):
            errors.append("System Gate approved targets cannot precede candidate_change_approved")
        if approval.get("validation_status") != "not_run":
            errors.append("System Gate validation receipt cannot precede candidate_change_approved")

    if status_index >= expected_statuses.index("candidate_change_approved"):
        if approval.get("standalone_line") != "APPROVE SYSTEM FILES":
            errors.append("system update approval must contain standalone APPROVE SYSTEM FILES")
        if approval.get("proposal_id") != system_update.get("proposal_id"):
            errors.append("system update approval proposal_id must match the visible proposal")
        if approval.get("proposal_version") != system_update.get("proposal_version"):
            errors.append("system update approval proposal_version must match the visible proposal")
        proposed_targets = _validated_exact_targets(
            system_update.get("proposed_exact_targets"),
            "activation.system_update.proposed_exact_targets",
            errors,
        )
        approved_targets = _validated_exact_targets(
            approval.get("approved_exact_targets"),
            "activation.system_update.approval.approved_exact_targets",
            errors,
        )
        if approved_targets != proposed_targets:
            errors.append("system update approval targets must exactly match the visible proposal")
        for field in (
            "validation_run_id",
            "completed_reply_reference",
            "recorded_at",
        ):
            if not approval.get(field):
                errors.append(f"system update approval is missing {field}")
        if approval.get("validation_status") != "passed":
            errors.append("system update approval completed reply must be validated")
        if not activation.get("validation_run_id"):
            errors.append("approved system update requires activation.validation_run_id")
        elif activation.get("validation_run_id") != approval.get("validation_run_id"):
            errors.append("approved system update must match its approval validation_run_id")
        review_response_reference = source_offer.get("response", {}).get("reply_reference")
        if approval.get("completed_reply_reference") and approval.get(
            "completed_reply_reference"
        ) == review_response_reference:
            errors.append(
                "system review response and System Gate approval must use distinct reply references"
            )

    if system_status == "validated" and approval.get("validation_status") != "passed":
        errors.append("validated system update requires a passed System Gate approval")


def _validate_activation_progression(
    data: dict,
    activation: dict,
    system_update: dict,
    errors: list[str],
) -> None:
    expected_top_statuses = ["candidate_not_active", "active", "suspended"]
    if activation.get("allowed_statuses") != expected_top_statuses:
        errors.append("activation statuses are missing or reordered")

    separate = activation.get("separate_activation_decision", {})
    if not isinstance(separate, dict):
        errors.append("separate_activation_decision must be an object")
        return
    expected_decision_statuses = ["not_requested", "pending", "approved", "rejected"]
    if separate.get("allowed_statuses") != expected_decision_statuses:
        errors.append("separate activation decision statuses are missing or reordered")
    expected_matching_fields = {
        "proposal_id",
        "proposal_version",
        "validation_evidence_reference",
        "residual_risks_reference",
        "rollback_reference",
    }
    if set(separate.get("required_matching_system_update_fields", [])) != expected_matching_fields:
        errors.append("separate activation matching fields are missing or divergent")
    expected_decisions = [
        "activate_exact_validated_version",
        "keep_inactive",
        "revise_and_revalidate",
    ]
    if separate.get("allowed_decisions") != expected_decisions:
        errors.append("separate activation allowed decisions are missing or reordered")
    if separate.get("matching_rule") != (
        "approval_is_valid_only_when_proposal_id_and_version_match_activation.system_update_and_validation_status_is_passed"
    ):
        errors.append("separate activation matching rule is missing or changed")

    decision_status = separate.get("status")
    if decision_status not in expected_decision_statuses:
        errors.append("invalid separate activation decision status")
        decision_status = "not_requested"
    if decision_status == "not_requested":
        for field in (
            "validated_system_proposal_id",
            "validated_system_proposal_version",
            "validation_evidence_reference",
            "residual_risks_reference",
            "rollback_reference",
            "decision",
            "lecturer_reply_reference",
            "prerequisites_verified_at",
            "recorded_at",
        ):
            if separate.get(field):
                errors.append(f"activation decision field {field} cannot precede a request")
        if separate.get("validation_status") != "not_run":
            errors.append("activation validation receipt cannot precede a request")
    if decision_status == "pending":
        if system_update.get("status") != "validated":
            errors.append("pending activation requires a validated system update")
        if separate.get("decision") is not None:
            errors.append("pending activation cannot contain a lecturer decision")
    if decision_status == "approved":
        if system_update.get("status") != "validated":
            errors.append("activation decision cannot be approved before system update validation")
        if separate.get("validated_system_proposal_id") != system_update.get("proposal_id"):
            errors.append("activation decision proposal_id must match the validated system update")
        if separate.get("validated_system_proposal_version") != system_update.get(
            "proposal_version"
        ):
            errors.append("activation decision proposal_version must match the validated system update")
        for field in (
            "validation_evidence_reference",
            "residual_risks_reference",
            "rollback_reference",
            "lecturer_reply_reference",
            "prerequisites_verified_at",
            "recorded_at",
        ):
            if not separate.get(field):
                errors.append(f"approved activation decision is missing {field}")
        if separate.get("validation_status") != "passed":
            errors.append("approved activation decision requires passing validation evidence")
        if separate.get("decision") != "activate_exact_validated_version":
            errors.append("approved activation must name activate_exact_validated_version")
        system_reply_reference = system_update.get("approval", {}).get(
            "completed_reply_reference"
        )
        if separate.get("lecturer_reply_reference") and separate.get(
            "lecturer_reply_reference"
        ) == system_reply_reference:
            errors.append("System Gate and activation must use distinct lecturer replies")
    if decision_status == "rejected":
        if separate.get("decision") not in {"keep_inactive", "revise_and_revalidate"}:
            errors.append("rejected activation must explicitly keep inactive or require revalidation")
        if data.get("status") != "candidate_not_active":
            errors.append("rejected activation decision must keep the runtime inactive")

    top_status = data.get("status")
    if top_status in {"active", "suspended"}:
        if decision_status != "approved" or separate.get("decision") != (
            "activate_exact_validated_version"
        ):
            errors.append("active or suspended runtime requires a separate approved activation decision")
        if not activation.get("activated_at"):
            errors.append("active or suspended runtime is missing activated_at")
    elif top_status == "candidate_not_active":
        if activation.get("activated_at"):
            errors.append("inactive candidate cannot carry an activation timestamp")
        if decision_status == "approved":
            errors.append("approved activation decision must not leave the runtime candidate_not_active")


def _valid_iana_timezone(value: object) -> bool:
    if not isinstance(value, str) or not re.fullmatch(
        r"(?:UTC|[A-Za-z_]+(?:/[A-Za-z0-9_+.-]+)+)", value
    ):
        return False
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError):
        return False
    return True


def _parse_zoned_datetime(
    value: object,
    expected_timezone: object,
    label: str,
    errors: list[str],
) -> datetime | None:
    if not isinstance(value, str) or not isinstance(expected_timezone, str):
        errors.append(f"{label} must be an offset timestamp followed by [IANA/Timezone]")
        return None
    match = re.fullmatch(
        r"(?P<stamp>[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(?::[0-9]{2})?(?:\.[0-9]+)?[+-][0-9]{2}:[0-9]{2})\[(?P<zone>(?:UTC|[A-Za-z_]+(?:/[A-Za-z0-9_+.-]+)+))\]",
        value,
    )
    if not match:
        errors.append(f"{label} must use canonical offset[IANA/Timezone] format")
        return None
    if match.group("zone") != expected_timezone:
        errors.append(f"{label} IANA timezone does not match the contract timezone")
        return None
    try:
        parsed = datetime.fromisoformat(match.group("stamp"))
    except ValueError:
        errors.append(f"{label} contains an invalid date or time")
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        errors.append(f"{label} must contain an explicit UTC offset")
        return None
    try:
        zone = ZoneInfo(expected_timezone)
    except (ZoneInfoNotFoundError, ValueError):
        errors.append(f"{label} names an unavailable IANA timezone")
        return None
    converted = parsed.astimezone(zone)
    if converted.utcoffset() != parsed.utcoffset() or converted.replace(
        tzinfo=None
    ) != parsed.replace(tzinfo=None):
        errors.append(f"{label} UTC offset does not match the IANA timezone at that date")
        return None
    return parsed


def _expected_contract_snapshot_reference(contract: dict) -> str:
    mutable_or_post_approval_fields = {
        "schedule_id",
        "status",
        "approved_contract_snapshot_reference",
        "approved_at",
        "lecturer_approval",
        "last_reconfirmed_at",
        "reconfirmation_history",
        "pause",
        "renew",
        "rollback",
    }
    payload = {
        key: value
        for key, value in contract.items()
        if key not in mutable_or_post_approval_fields
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _validate_three_line_schedule_approval(
    approval: object,
    contract: dict,
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(approval, dict):
        errors.append(f"{label} must be an object")
        return
    if approval.get("line_1") != "APPROVE SCHEDULES":
        errors.append(f"{label} line_1 must be exactly APPROVE SCHEDULES")
    line_2 = approval.get("line_2")
    match = re.fullmatch(
        r"Schedule contract: ([A-Za-z0-9._-]+) ([A-Za-z0-9._-]+)",
        line_2 or "",
    )
    if not match:
        errors.append(f"{label} line_2 must contain only the exact contract ID and version")
    else:
        if match.group(1) != str(contract.get("contract_id")):
            errors.append(f"{label} line_2 contract ID does not match")
        if match.group(2) != str(contract.get("contract_version")):
            errors.append(f"{label} line_2 contract version does not match")
    expiry = contract.get("expires_at")
    if approval.get("line_3") != (f"Expires: {expiry}" if expiry else None):
        errors.append(f"{label} line_3 must repeat the exact contract expiry")
    if approval.get("parsed_contract_id") != contract.get("contract_id"):
        errors.append(f"{label} parsed contract ID does not match")
    if approval.get("parsed_contract_version") != contract.get("contract_version"):
        errors.append(f"{label} parsed contract version does not match")
    if approval.get("parsed_expiry_local_with_iana_timezone") != expiry:
        errors.append(f"{label} parsed expiry does not match")
    for field in ("completed_reply_reference", "recorded_at"):
        if not approval.get(field):
            errors.append(f"{label} is missing {field}")
    if approval.get("validation_status") != "passed":
        errors.append(f"{label} must have passing validation_status")


def _validate_complete_active_contract(
    data: dict,
    contract: dict,
    template: dict,
    label: str,
    errors: list[str],
) -> None:
    exact_safety_fields = (
        "allowed_statuses",
        "task_type",
        "canonical_mission",
        "source_access_policy_match_rule",
        "protected_roots",
        "permitted_actions_before_gate_2a",
        "permitted_actions_after_fresh_gate_2a_approval",
        "permitted_actions_after_fresh_gate_2b_target_approval",
        "write_authority",
        "no_write_before_exact_target_approval",
        "unique_output_naming_rule",
        "first_required_wait",
        "maximum_stage",
        "retry_rules",
        "escalation_rules",
        "terminal_rules",
        "no_immediate_run",
        "activation_requires_non_null_expires_at",
        "expiry_behavior",
        "stale_baseline_context_or_manifest_behavior",
        "reconfirmation_triggers",
        "activation_requires",
    )
    for field in exact_safety_fields:
        if contract.get(field) != template.get(field):
            errors.append(f"{label} safety field {field} diverges from the canonical contract")
    if contract.get("timezone_requires_lecturer_confirmation") is not True:
        errors.append(f"{label} must require lecturer confirmation of the IANA timezone")

    project = contract.get("project", {})
    course = contract.get("course", {})
    for container, fields, container_label in (
        (project, ("project_id", "project_root"), "project"),
        (course, ("course_id", "course_title"), "course"),
    ):
        if not isinstance(container, dict):
            errors.append(f"{label}.{container_label} must be an object")
            continue
        for field in fields:
            if not container.get(field):
                errors.append(f"{label}.{container_label} is missing {field}")

    baseline = contract.get("baseline_approvals", {})
    if not isinstance(baseline, dict):
        errors.append(f"{label}.baseline_approvals must be an object")
        baseline = {}
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
    if baseline.get("verification_result") not in {True, "passed"}:
        errors.append(f"{label} baseline verification must be passed")

    for field in ("main_goal", "data_egress_boundary", "assessment_security_boundary"):
        if not contract.get(field):
            errors.append(f"{label} is missing {field}")
    for field in (
        "success_criteria",
        "stop_conditions",
        "constraints",
        "permitted_tools",
        "permitted_actions",
        "permitted_source_classes",
        "permitted_output_audiences",
    ):
        value = contract.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{label} must contain a nonempty {field} list")

    policy = data.get("source_access_policy", {})
    if not isinstance(policy, dict):
        errors.append(f"{label} cannot bind to a missing top-level source access policy")
        policy = {}
    if policy.get("status") == "pending_lecturer_confirmation" or not policy.get(
        "lecturer_approval_reference"
    ):
        errors.append(f"{label} requires a current lecturer-confirmed source access policy")
    if contract.get("source_access_policy_version") != baseline.get(
        "source_access_policy_version"
    ) or contract.get("source_access_policy_fingerprint") != baseline.get(
        "source_access_policy_fingerprint"
    ):
        errors.append(f"{label} source policy must match its verified baseline")
    if contract.get("source_access_policy_version") != policy.get("version") or contract.get(
        "source_access_policy_fingerprint"
    ) != policy.get("fingerprint"):
        errors.append(f"{label} source policy must match current top-level policy")
    if data.get("source_manifest") in (None, ""):
        errors.append(f"{label} requires a current source manifest")

    recurrence = contract.get("recurrence")
    if isinstance(recurrence, list):
        recurrence_keys: list[str] = []
        for index, item in enumerate(recurrence):
            if isinstance(item, str):
                if not item.strip() or "\n" in item or "\r" in item:
                    errors.append(f"{label}.recurrence[{index}] must be one nonempty line")
            elif isinstance(item, dict):
                if not item:
                    errors.append(f"{label}.recurrence[{index}] must not be empty")
            else:
                errors.append(f"{label}.recurrence[{index}] must be a string or object")
            recurrence_keys.append(json.dumps(item, sort_keys=True, separators=(",", ":")))
        if len(recurrence_keys) != len(set(recurrence_keys)):
            errors.append(f"{label}.recurrence must not contain duplicate triggers")

    timezone_name = contract.get("timezone")
    activation_time = _parse_zoned_datetime(
        contract.get("activation_time"), timezone_name, f"{label}.activation_time", errors
    )
    expiry = _parse_zoned_datetime(
        contract.get("expires_at"), timezone_name, f"{label}.expires_at", errors
    )
    if activation_time and expiry:
        if expiry <= activation_time:
            errors.append(f"{label} expiry must be later than activation_time")
        if expiry.astimezone(timezone.utc) <= datetime.now(timezone.utc):
            errors.append(f"{label} active schedule is expired")

    expected_snapshot = _expected_contract_snapshot_reference(contract)
    if contract.get("approved_contract_snapshot_reference") != expected_snapshot:
        errors.append(
            f"{label} approved contract snapshot reference must match its canonical SHA-256"
        )

    runtime = contract.get("runtime_versions", {})
    if runtime.get("skill_name") != "course-redesign-orchestrator":
        errors.append(f"{label} must invoke course-redesign-orchestrator")
    pause = contract.get("pause", {})
    if pause.get("requires_lecturer_direction") is not True or pause.get("action") != (
        "disable_future_triggers_preserve_contract_and_run_history"
    ):
        errors.append(f"{label} pause controls are missing or changed")
    renew = contract.get("renew", {})
    if not all(
        renew.get(field) is True
        for field in (
            "requires_new_contract_version",
            "requires_new_expiry",
            "requires_no_write_simulation",
            "requires_all_three_completed_approval_lines",
        )
    ):
        errors.append(f"{label} renewal controls are missing or changed")
    rollback = contract.get("rollback", {})
    if rollback.get("requires_lecturer_direction") is not True or rollback.get("action") != (
        "disable_schedule_restore_last_approved_contract_snapshot_and_preserve_run_history"
    ):
        errors.append(f"{label} rollback controls are missing or changed")


def _validate_schedule_progression(
    data: dict,
    activation: dict,
    system_update: dict,
    errors: list[str],
) -> None:
    registration = data.get("schedule_registration", {})
    if not isinstance(registration, dict):
        errors.append("schedule_registration must be an object")
        return
    registration_statuses = {"not_approved", "approved"}
    registration_status = registration.get("status")
    if registration_status not in registration_statuses:
        errors.append("invalid schedule registration status")
    if registration.get("required_completed_approval_lines") != [
        "APPROVE SCHEDULES",
        "Schedule contract: <exact contract ID and version>",
        "Expires: <exact local date and time with IANA timezone>",
    ]:
        errors.append("schedule registration exact three-line approval is missing or changed")
    if registration.get("approval_reply_must_contain_exactly_and_only_the_three_lines") is not True:
        errors.append("schedule registration must require exactly and only three approval lines")
    if registration.get("no_immediate_run_required") is not True:
        errors.append("schedule registration must forbid an immediate run")
    required_runtime = registration.get("required_active_runtime", {})
    if required_runtime.get("status_path") != "$.status" or required_runtime.get(
        "status_must_equal"
    ) != "active":
        errors.append("schedule registration must require top-level active runtime status")
    if required_runtime.get("match_rule") != (
        "top_level_status_must_be_active_and_schedule_contract_runtime_id_and_version_must_match_the_separately_activated_validated_runtime"
    ):
        errors.append("schedule registration active-runtime match rule is missing or changed")
    if registration.get("no_write_simulation_status") not in {"not_run", "passed", "failed"}:
        errors.append("invalid no-write simulation status")

    schedules = data.get("schedules")
    if not isinstance(schedules, list):
        errors.append("schedules must be a list")
        return
    if data.get("status") == "candidate_not_active" and schedules:
        errors.append("inactive template must register no schedules")

    approved_ids = registration.get("approved_standing_contract_ids", [])
    approved_versions = registration.get("approved_standing_contract_versions", [])
    if not isinstance(approved_ids, list) or not isinstance(approved_versions, list):
        errors.append("approved standing-contract IDs and versions must be lists")
        approved_ids, approved_versions = [], []
    if len(approved_ids) != len(approved_versions):
        errors.append("approved standing-contract IDs and versions must form equal-length pairs")
    approved_pairs = list(zip(approved_ids, approved_versions))
    if len(approved_pairs) != len(set(approved_pairs)):
        errors.append("approved standing-contract ID/version pairs must be unique")
    registration_approval = registration.get("approval", {})
    if not isinstance(registration_approval, dict):
        errors.append("schedule_registration.approval must be an object")
        registration_approval = {}
    simulation_status = registration.get("no_write_simulation_status")
    contract_template = data.get("standing_schedule_contract_template", {})
    if not isinstance(contract_template, dict):
        errors.append("standing_schedule_contract_template must be an object")
        contract_template = {}
    if registration_status == "not_approved":
        if approved_ids or approved_versions:
            errors.append("unapproved schedule registration cannot list approved contracts")
        if _record_has_progress(
            registration_approval,
            {
                "line_1",
                "line_2",
                "line_3",
                "parsed_contract_id",
                "parsed_contract_version",
                "parsed_expiry_local_with_iana_timezone",
                "completed_reply_reference",
                "validation_status",
                "recorded_at",
            },
        ):
            errors.append("schedule approval receipt cannot exist while registration is not_approved")
        simulation_result = registration.get("no_write_simulation_result")
        simulation_recorded_at = registration.get("no_write_simulation_recorded_at")
        if simulation_status == "not_run" and (simulation_result or simulation_recorded_at):
            errors.append("not-run schedule simulation cannot contain a result or timestamp")
        if simulation_status in {"passed", "failed"} and not (
            simulation_result and simulation_recorded_at
        ):
            errors.append("completed schedule simulation requires a result and timestamp")
        if simulation_status == "passed":
            _validate_complete_active_contract(
                data,
                contract_template,
                contract_template,
                "standing_schedule_contract_template simulated proposal",
                errors,
            )

    active_schedules: list[tuple[int, dict]] = []
    seen_contract_pairs: set[tuple[object, object]] = set()
    for index, schedule in enumerate(schedules):
        label = f"schedules[{index}]"
        if not isinstance(schedule, dict):
            errors.append(f"{label} must be a versioned standing-contract object")
            continue
        if not schedule.get("schedule_id"):
            errors.append(f"{label} is missing schedule_id")
        pair = (schedule.get("contract_id"), schedule.get("contract_version"))
        if pair in seen_contract_pairs:
            errors.append(f"{label} duplicates an existing contract ID/version pair")
        seen_contract_pairs.add(pair)
        schedule_status = schedule.get("status")
        if schedule_status not in {"active", "paused", "expired", "cancelled"}:
            errors.append(f"{label} has invalid registered schedule status")
        if schedule_status == "active":
            active_schedules.append((index, schedule))

    if active_schedules and registration_status != "approved":
        errors.append("active schedules require approved schedule registration")
    if registration_status == "approved" and not active_schedules:
        errors.append("approved schedule registration must identify at least one active schedule")
    if not active_schedules:
        return

    if data.get("status") != "active":
        errors.append("active schedules require a separately activated top-level runtime")
    separate = activation.get("separate_activation_decision", {})
    if separate.get("status") != "approved" or separate.get("decision") != (
        "activate_exact_validated_version"
    ):
        errors.append("active schedules require the separate exact-version activation decision")
    if registration.get("no_write_simulation_status") != "passed":
        errors.append("schedule registration requires a successful no-write simulation")
    for field in ("no_write_simulation_result", "no_write_simulation_recorded_at"):
        if not registration.get(field):
            errors.append(f"schedule registration is missing {field}")

    activation_reply = separate.get("lecturer_reply_reference")
    for index, contract in active_schedules:
        label = f"schedules[{index}]"
        _validate_complete_active_contract(data, contract, contract_template, label, errors)
        contract_id = contract.get("contract_id")
        contract_version = contract.get("contract_version")
        if not contract_id or contract_version in {None, ""}:
            errors.append(f"{label} must name a contract ID and version")
        if (contract_id, contract_version) not in approved_pairs:
            errors.append(f"{label} is not listed in the approved standing-contract IDs and versions")
        if contract.get("no_immediate_run") is not True:
            errors.append(f"{label} must forbid an immediate run")
        timezone = contract.get("timezone")
        if not _valid_iana_timezone(timezone):
            errors.append(f"{label} must contain a lecturer-confirmed IANA timezone")
        expiry = contract.get("expires_at")
        if not expiry or (timezone and timezone not in str(expiry)):
            errors.append(f"{label} must contain an expiry with its confirmed IANA timezone")
        if not isinstance(contract.get("recurrence"), list) or not contract.get("recurrence"):
            errors.append(f"{label} must contain a nonempty recurrence")
        for field in ("activation_time", "approved_at", "approved_contract_snapshot_reference"):
            if not contract.get(field):
                errors.append(f"{label} is missing {field}")
        runtime = contract.get("runtime_versions", {})
        if runtime.get("validated_system_proposal_id") != separate.get(
            "validated_system_proposal_id"
        ) or runtime.get("validated_system_proposal_version") != separate.get(
            "validated_system_proposal_version"
        ):
            errors.append(f"{label} runtime proposal does not match the activated version")
        if runtime.get("activation_decision_reference") != activation_reply:
            errors.append(f"{label} runtime is not bound to the activation decision")
        if runtime.get("required_runtime_status") != "active":
            errors.append(f"{label} must require active runtime status")
        for field in ("prompt_version", "skill_version"):
            if not runtime.get(field):
                errors.append(f"{label} runtime is missing {field}")
        if runtime.get("skill_version") != data.get("plugin_version"):
            errors.append(f"{label} skill_version must match the active plugin version")
        lecturer_approval = contract.get("lecturer_approval", {})
        if lecturer_approval.get("status") != "approved" or lecturer_approval.get(
            "reply_must_contain_exactly_and_only_three_lines"
        ) is not True:
            errors.append(f"{label} lacks the exact-only lecturer schedule approval")
        _validate_three_line_schedule_approval(lecturer_approval, contract, f"{label} approval", errors)

    approved_contract = next(
        (
            contract
            for _, contract in active_schedules
            if contract.get("contract_id") == registration_approval.get("parsed_contract_id")
            and contract.get("contract_version")
            == registration_approval.get("parsed_contract_version")
        ),
        None,
    )
    if approved_contract is None:
        errors.append("schedule registration approval does not match an active standing contract")
    else:
        _validate_three_line_schedule_approval(
            registration_approval,
            approved_contract,
            "schedule_registration.approval",
            errors,
        )
        if registration_approval.get("completed_reply_reference") == activation_reply:
            errors.append("activation and schedule registration must use distinct lecturer replies")
        required_runtime_id = required_runtime.get("validated_system_proposal_id")
        required_runtime_version = required_runtime.get("validated_system_proposal_version")
        if required_runtime_id != separate.get("validated_system_proposal_id") or (
            required_runtime_version != separate.get("validated_system_proposal_version")
        ):
            errors.append("schedule registration runtime does not match the activated proposal")
        if required_runtime.get("activation_decision_reference") != activation_reply:
            errors.append("schedule registration is not bound to the activation decision")


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    if data.get("schema_version") != 7:
        errors.append("state schema_version must be 7")
    if data.get("status") not in {"candidate_not_active", "active", "suspended"}:
        errors.append("invalid top-level status")
    if data.get("umbrella_entry_routing") != EXPECTED_UMBRELLA_ROUTING:
        errors.append("umbrella entry must route through setup preview and Gate 0")
    compatibility = data.get("schema_compatibility", {})
    if compatibility.get("current_schema_version") != 7:
        errors.append("schema compatibility must identify current schema 7")
    if compatibility.get("minimum_preview_migration_source_version") != 6:
        errors.append("schema compatibility must support preview migration from schema 6")
    if compatibility.get("migration_helper") != "scripts/migrate_state_v6_to_v7.py":
        errors.append("schema compatibility migration helper path is missing or changed")
    if compatibility.get("migration_mode") != "preview_only":
        errors.append("schema migration must remain preview-only")
    if compatibility.get("automatic_apply_forbidden") is not True:
        errors.append("schema migration must forbid automatic apply")
    activation = data.get("activation", {})
    if activation.get("automatic_activation_forbidden") is not True:
        errors.append("automatic activation must be forbidden")
    separate = activation.get("separate_activation_decision", {})
    if not isinstance(separate, dict):
        errors.append("separate_activation_decision must be an object")
    required_before_active = set(activation.get("required_before_active", []))
    for requirement in {
        "production_completion_declared",
        "production_handoff_target_approved",
        "production_handoff_verified",
        "hitl_3_accepted",
        "system_improvement_review_offer_requested",
        "system_update_approved",
        "separate_activation_decision_recorded",
    }:
        if requirement not in required_before_active:
            errors.append(f"activation prerequisites missing {requirement}")
    system_update = activation.get("system_update", {})
    expected_system_statuses = [
        "not_started",
        "proposal_requested",
        "proposal_presented",
        "candidate_change_approved",
        "validated",
    ]
    if system_update.get("allowed_statuses") != expected_system_statuses:
        errors.append("system update statuses are missing or reordered")
    expected_system_prerequisites = {
        "matching_run_production_completion_complete",
        "matching_run_production_handoff_verified",
        "matching_run_hitl_3_accepted",
        "matching_run_system_improvement_review_offer_requested",
    }
    if set(system_update.get("prerequisites", [])) != expected_system_prerequisites:
        errors.append("system update must require production, HITL3 and requested offer")
    completed_requirements = set(system_update.get("completed_reply_requirements", []))
    expected_completed_requirements = set(LINEAGE_FIELDS) | {
        "validation_run_id",
        "proposal_id",
        "proposal_version",
        "system_improvement_review_offer_reference",
        "all_exact_targets_match_visible_proposal",
        "APPROVE SYSTEM FILES_as_a_standalone_line",
    }
    if completed_requirements != expected_completed_requirements:
        errors.append("system update completed reply requirements are incomplete or expanded")
    if system_update.get("required_standalone_line") != "APPROVE SYSTEM FILES":
        errors.append("system update must require standalone APPROVE SYSTEM FILES")
    if system_update.get("maximum_authorised_stage") != "SYSTEM_GATE":
        errors.append("system update authority must stop at SYSTEM_GATE")
    if system_update.get("does_not_authorise_candidate_activation") is not True:
        errors.append("System Gate must not authorise candidate activation")
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
    offer_ids: set[str] = set()
    template_offer_id = _validate_production_hitl3_offer(
        run_template, "run_template", errors
    )
    if template_offer_id:
        offer_ids.add(template_offer_id)
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
    runs = data.get("runs", [])
    if not isinstance(runs, list):
        errors.append("runs must be a list")
        runs = []
    run_ids: set[object] = set()
    runs_by_id: dict[object, dict] = {}
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            errors.append(f"runs[{index}] must be an object")
            continue
        label = f"runs[{index}]"
        run_id = run.get("run_id")
        if not run_id:
            errors.append(f"{label} is missing run_id")
        elif run_id in run_ids:
            errors.append(f"duplicate run_id {run_id}")
        else:
            run_ids.add(run_id)
            runs_by_id[run_id] = run
        run_approvals = run.get("approvals", {})
        _validate_research_targets(run_approvals.get("gate_2b", {}), errors)
        _validate_material_targets(run_approvals.get("gate_3", {}), errors)
        offer_id = _validate_production_hitl3_offer(run, label, errors)
        if offer_id:
            if offer_id in offer_ids:
                errors.append(f"duplicate system-review offer idempotency key {offer_id}")
            offer_ids.add(offer_id)

    _validate_system_update_progression(
        activation,
        system_update,
        expected_system_statuses,
        runs_by_id,
        errors,
    )
    _validate_activation_progression(data, activation, system_update, errors)
    _validate_schedule_progression(data, activation, system_update, errors)
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
