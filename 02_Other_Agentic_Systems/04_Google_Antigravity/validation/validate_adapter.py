#!/usr/bin/env python3
"""Validate the static Google Antigravity course-redesign adapter."""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any


ADAPTER_ROOT = Path(__file__).resolve().parent.parent
OVERLAY_ROOT = ADAPTER_ROOT / "workspace-overlay"
EXPECTED_SKILLS = {
    "course-redesign-assessment",
    "course-redesign-materials",
    "course-redesign-orchestrator",
    "course-redesign-research",
    "course-redesign-setup",
    "course-redesign-system",
}
EXPECTED_WORKFLOWS = {
    "course-redesign-continue.md",
    "course-redesign-start.md",
    "course-redesign-system-review.md",
    "course-redesign-validate.md",
}
EXPECTED_AGENTS = {
    "active-learning-researcher.md": "active_learning_researcher",
    "ai-integration-researcher.md": "ai_integration_researcher",
    "artefact-accessibility-visual-qa.md": "artefact_accessibility_visual_qa",
    "assessment-alignment-designer.md": "assessment_alignment_designer",
    "course-mapper.md": "course_mapper",
    "evidence-feasibility-red-team.md": "evidence_feasibility_red_team",
    "learning-designer.md": "learning_designer",
    "learning-material-designer.md": "learning_material_designer",
    "source-verification-citation-auditor.md": "source_verification_citation_auditor",
    "student-experience-critic.md": "student_experience_critic",
}
READ_ONLY_AGENT_TOOLS = ["view_file", "grep_search"]
AGENT_SKILL_PATHS = ["skills/course-redesign-orchestrator"]
REQUIRED_PATHS = {
    "README.md",
    "OFFICIAL_LIMITATIONS.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "scripts/install_workspace_overlay.py",
    "workspace-overlay/AGENTS.md",
    "workspace-overlay/00_NOT_ACTIVE_UNTIL_VALIDATED.txt",
    "workspace-overlay/PROJECT_SETUP.md",
    "workspace-overlay/01_Control/GATES.md",
    "workspace-overlay/01_Control/material-processing-eligibility.template.json",
    "workspace-overlay/01_Control/run-contract.template.json",
    "workspace-overlay/01_Control/source-access-policy.template.json",
    "workspace-overlay/01_Control/state.json",
    "workspace-overlay/.agents/skills/course-redesign-setup/scripts/fingerprint_file.py",
    "workspace-overlay/.agents/skills/course-redesign-setup/scripts/create_material_processing_eligibility.py",
    "workspace-overlay/.agents/skills/course-redesign-setup/scripts/source_manifest.py",
    "workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v6_to_v7.py",
    "workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v7_to_v8.py",
    "workspace-overlay/.agents/skills/course-redesign-setup/scripts/validate_state.py",
    "workspace-overlay/.agents/rules/00-trust-and-scope.md",
    "workspace-overlay/.agents/rules/10-gates-and-lineage.md",
    "workspace-overlay/.agents/rules/20-assessment-and-release-security.md",
    "optional-privileged-examples/hooks.json.example",
    "optional-privileged-examples/mcp_config.json.example",
    "adapter-manifest.json",
}
SOURCE_HASH_PATTERN = re.compile(r"^[0-9a-f]{64}$")
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
SECRET_PATTERNS = {
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),
    "aws-access-key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github-token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "openai-style-key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "google-api-key": re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
    "assigned-secret": re.compile(
        r"(?i)(?:api[_-]?key|client[_-]?secret|access[_-]?token|password|authorization)"
        r"\s*[=:]\s*[\"']?(?!(?:REPLACE|YOUR_|EXAMPLE|<|null|false|true))"
        r"[A-Za-z0-9+/=_-]{12,}"
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _parse_yaml_scalar(value: str) -> Any:
    cleaned = value.strip().strip('"').strip("'")
    if cleaned == "[]":
        return []
    if cleaned.casefold() == "true":
        return True
    if cleaned.casefold() == "false":
        return False
    return cleaned


def parse_agent_frontmatter(path: Path) -> dict[str, Any]:
    """Parse the restricted, dependency-free YAML subset used by agent files."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc

    values: dict[str, Any] = {}
    active_list: str | None = None
    for raw_line in lines[1:end]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[0].isspace():
            item = raw_line.strip()
            if active_list is None or not item.startswith("- "):
                raise ValueError(f"invalid nested frontmatter line: {raw_line}")
            values[active_list].append(_parse_yaml_scalar(item[2:]))
            continue
        if ":" not in raw_line:
            raise ValueError(f"invalid frontmatter line: {raw_line}")
        key, raw_value = raw_line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if not raw_value:
            values[key] = []
            active_list = key
        else:
            values[key] = _parse_yaml_scalar(raw_value)
            active_list = None
    return values


def validate_agent_definition(path: Path, expected_role: str) -> list[str]:
    errors: list[str] = []
    try:
        frontmatter = parse_agent_frontmatter(path)
    except (OSError, UnicodeError, ValueError) as exc:
        return [f"invalid custom-agent frontmatter {path.name}: {exc}"]

    expected_keys = {
        "name",
        "description",
        "tools",
        "mainAgent",
        "subagent",
        "model",
        "commandExecutionPolicy",
        "inheritMcp",
        "skills",
        "mcpServers",
        "plugins",
    }
    if set(frontmatter) != expected_keys:
        errors.append(
            f"custom-agent frontmatter keys changed for {path.name}: "
            f"expected {sorted(expected_keys)}, got {sorted(frontmatter)}"
        )
    if frontmatter.get("name") != path.stem:
        errors.append(f"custom-agent name/file mismatch: {path.name}")
    if len(str(frontmatter.get("description", ""))) < 40:
        errors.append(f"custom-agent description is not discriminating: {path.name}")
    if frontmatter.get("tools") != READ_ONLY_AGENT_TOOLS:
        errors.append(
            f"custom-agent tools must be exactly {READ_ONLY_AGENT_TOOLS}: {path.name}"
        )
    if frontmatter.get("mainAgent") is not False:
        errors.append(f"custom agent must not be selectable as main agent: {path.name}")
    if frontmatter.get("subagent") is not True:
        errors.append(f"custom agent must be subagent-enabled: {path.name}")
    if frontmatter.get("model") != "inherit":
        errors.append(f"custom agent must inherit the selected model: {path.name}")
    if frontmatter.get("commandExecutionPolicy") != "off":
        errors.append(f"custom-agent command execution must be off: {path.name}")
    if frontmatter.get("inheritMcp") is not False:
        errors.append(f"custom-agent MCP inheritance must be disabled: {path.name}")
    if frontmatter.get("skills") != AGENT_SKILL_PATHS:
        errors.append(f"custom agent must load only the orchestrator skill: {path.name}")
    if frontmatter.get("mcpServers") != []:
        errors.append(f"custom agent must declare no MCP servers: {path.name}")
    if frontmatter.get("plugins") != []:
        errors.append(f"custom agent must declare no plugins: {path.name}")

    body = path.read_text(encoding="utf-8")
    required_fragments = {
        f"Act only as role `{expected_role}`": "canonical role",
        "root `AGENTS.md`": "root control contract",
        ".agents/rules/": "project-local rules",
        "specialist-role-contracts.md": "shared role contract",
        "current state capsule": "current lineage capsule",
        "assigned subgoals": "bounded assignment",
        "`view_file` and `grep_search`": "read-only tools",
        "never write": "write prohibition",
        "MCP egress": "MCP and egress prohibition",
        "publish": "publication prohibition",
        "persist state": "state-persistence prohibition",
        "ESCALATE_TO_ORCHESTRATOR:": "fail-closed escalation",
    }
    for fragment, label in required_fragments.items():
        if fragment not in body:
            errors.append(f"custom agent lacks {label}: {path.name}")
    return errors


def adapter_files(root: Path = ADAPTER_ROOT) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix.casefold() not in {".pyc", ".pyo"}
    )


def validate_state_fields(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state.get("schema_version") != 8:
        errors.append("state schema_version must be 8")
    if state.get("status") != "candidate_not_active":
        errors.append("adapter state must remain candidate_not_active")
    if state.get("schedules") != []:
        errors.append("inactive adapter must contain no registered schedules")
    activation = state.get("activation", {})
    if activation.get("automatic_activation_forbidden") is not True:
        errors.append("automatic activation must be forbidden")
    if not {
        "gate_0a_recorded",
        "matching_course_run_terminal_complete_dormant",
    }.issubset(set(activation.get("required_before_active", []))):
        errors.append("activation prerequisites must bind Gate 0A and dormant closeout")
    routing = state.get("umbrella_entry_routing", {})
    if routing != {
        "entry_name": "Agentic Course Redesign",
        "entry_skill": "course-redesign-orchestrator",
        "initial_gate": "GATE_0A_AWAITING_MATERIAL_ENVIRONMENT_ELIGIBILITY",
        "missing_project_action": "invoke_course-redesign-setup_preview_only",
        "gate_0a_required_before_any_course_source_path_filename_list_read_copy_hash_or_intake": True,
        "gate_0_required_before_course_source_reading": True,
        "gate_0_required_before_specialist_work": True,
    }:
        errors.append("schema 8 umbrella entry must hard-stop at pre-source Gate 0A")
    compatibility = state.get("schema_compatibility", {})
    if (
        compatibility.get("current_schema_version") != 8
        or compatibility.get("minimum_preview_migration_source_version") != 7
        or compatibility.get("migration_helper") != "scripts/migrate_state_v7_to_v8.py"
        or compatibility.get("migration_mode") != "preview_only"
        or compatibility.get("automatic_apply_forbidden") is not True
    ):
        errors.append("schema 8 compatibility contract or preview-only migration changed")
    eligibility = state.get("material_processing_eligibility", {})
    if eligibility.get("gate") != "GATE_0A_MATERIAL_ENVIRONMENT_ELIGIBILITY":
        errors.append("material-processing eligibility gate is missing")
    if eligibility.get("material_scope", {}).get(
        "public_availability_alone_is_insufficient"
    ) is not True:
        errors.append("public availability alone must remain insufficient")
    if set(eligibility.get("source_detail_prohibition_before_approval", [])) != {
        "no_source_paths",
        "no_source_filenames",
        "no_source_lists",
        "no_source_content",
        "no_source_hashes",
    }:
        errors.append("Gate 0A source-detail prohibition changed")
    adaptive = state.get("adaptive_course_scope", {})
    if (
        adaptive.get(
            "adapt_to_supplied_material_context_level_learners_objectives_assessment_language_and_constraints"
        )
        is not True
        or adaptive.get("subject_level_qualification_and_institutional_policy_assumptions_forbidden")
        is not True
    ):
        errors.append("course-independent adaptive scope changed")
    run_template = state.get("run_template", {})
    approvals = run_template.get("approvals", {})
    gate_2b = approvals.get("gate_2b", {})
    gate_2b_rules = gate_2b.get("target_rules", {})
    if gate_2b_rules.get("course_material_production_authorised") is not False:
        errors.append("Gate 2B must not authorise course-material production")
    if set(gate_2b_rules.get("forbidden_prefixes", [])) != {
        "04_Working_Copies/",
        "05_Approved/",
    }:
        errors.append("Gate 2B must forbid material-output prefixes")
    gate_3 = approvals.get("gate_3", {})
    type_map = gate_3.get("target_rules", {}).get("type_prefix_map")
    if type_map != {
        "working_copy": "04_Working_Copies/",
        "approved_release": "05_Approved/",
    }:
        errors.append("Gate 3 material target mapping changed")
    retry = run_template.get("retry_policy", {})
    if retry.get("max_retries_per_specialist_per_stage") != 1:
        errors.append("specialist retry ceiling must remain one")
    contract = run_template.get("contract", {})
    if "material_processing_eligibility_fingerprint" not in contract:
        errors.append("run contract must bind the Gate-0A eligibility fingerprint")
    gate_0a = approvals.get("gate_0a", {})
    if (
        gate_0a.get("basis")
        != "category_only_material_and_exact_processing_environment_declaration"
        or "material_processing_eligibility_fingerprint" not in gate_0a
    ):
        errors.append("run Gate 0A approval contract changed")
    return_envelope = run_template.get("specialist_return_envelope", {})
    if "material_processing_eligibility_fingerprint" not in return_envelope.get(
        "lineage_must_match_current_state", []
    ):
        errors.append("specialist return lineage must bind Gate-0A eligibility")
    hitl_3 = approvals.get("hitl_3", {})
    if hitl_3.get("allowed_statuses") != [
        "not_started",
        "awaiting_lecturer_decision",
        "revision_requested",
        "conditional_acceptance_pending_verification",
        "accepted",
        "rejected",
    ]:
        errors.append("HITL 3 status contract is incomplete or reordered")
    if set(hitl_3.get("entry_requires", [])) != {
        "production_completion.status_is_complete",
        "production_completion.declaration.completed_reply.validation_status_is_passed",
        "production_completion.handoff_approval.completed_reply.validation_status_is_passed",
        "production_completion.handoff_verified_at_is_non_null",
    }:
        errors.append("HITL 3 must require declaration, handoff approval, and verification")
    offer = approvals.get("system_improvement_review_offer", {})
    if offer.get("allowed_statuses") != [
        "not_offered",
        "offered_awaiting_response",
        "requested",
        "declined",
    ]:
        errors.append("system-review offer status contract is incomplete or reordered")
    if offer.get("ask_exactly_once") is not True or offer.get("record_offer_before_asking") is not True:
        errors.append("system-review offer must be durable and idempotent before asking")
    if offer.get("idempotency_key_fields") != [
        "run_id",
        "hitl_3_final_acceptance_reference",
    ]:
        errors.append("system-review offer idempotency key changed")
    if offer.get("mandatory_question") != MANDATORY_SYSTEM_REVIEW_QUESTION:
        errors.append("mandatory system-review question changed or is incomplete")
    if offer.get("required_question_scope") != REQUIRED_SYSTEM_REVIEW_SCOPE:
        errors.append("mandatory system-review question scope changed")
    authority = offer.get("authority_on_request", {})
    if authority.get("authorises") != [
        "read_only_review_of_current_system_and_successful_run_evidence",
        "prepare_one_versioned_system_improvement_proposal",
    ]:
        errors.append("system-review request authority must remain proposal-only")
    if set(authority.get("does_not_authorise", [])) != {
        "create_or_modify_system_files",
        "install_or_update_plugin",
        "publish_or_release",
        "activate_runtime",
        "register_or_modify_schedule",
        "trigger_immediate_run",
        "add_mcp_server_connector_authentication_permission_or_external_egress",
    }:
        errors.append("system-review request forbidden authority set changed")
    if authority.get("course_run_must_close_before_separate_system_work") is not True:
        errors.append("system work must remain separate from the closed course run")
    termination = run_template.get("termination", {})
    if (
        "complete_dormant" not in termination.get("allowed_statuses", [])
        or termination.get("never_resume_after_terminal") is not True
        or termination.get("closeout_requires_explicit_system_improvement_response")
        is not True
        or termination.get("silence_remains_waiting") is not True
    ):
        errors.append("terminal complete_dormant closeout contract changed")
    guidance = approvals.get("trigger_guidance_offer", {})
    if (
        guidance.get("offer_exactly_once") is not True
        or guidance.get("informational_only") is not True
        or guidance.get("optional_schedule_guidance", {}).get("no_immediate_run")
        is not True
    ):
        errors.append("informational trigger-guidance contract changed")
    resume = run_template.get("resume_protocol", {})
    if resume.get("checkpoint_order") != [
        "approvals.production_completion.declaration",
        "approvals.production_completion.handoff_approval",
        "approvals.production_completion.handoff_verified_at",
        "approvals.hitl_3",
        "approvals.system_improvement_review_offer",
        "termination.status",
        "approvals.trigger_guidance_offer",
    ]:
        errors.append("schema 8 resume checkpoint order changed")
    resume_rules = resume.get("rules", {})
    if not all(
        resume_rules.get(key) is True
        for key in (
            "persist_receipt_before_advancing_next_permitted_action",
            "same_receipt_reference_is_idempotent",
            "completed_checkpoint_must_not_repeat",
            "resume_from_first_incomplete_checkpoint",
            "current_lineage_required_before_resume",
            "lineage_mismatch_fails_closed",
            "silence_is_not_a_system_improvement_decision",
            "complete_dormant_is_terminal_and_never_resumable",
        )
    ):
        errors.append("schema 8 resume protocol must remain durable and fail closed")
    system_update = activation.get("system_update", {})
    for required in (
        "run_id",
        "material_processing_eligibility_fingerprint",
        "system_improvement_review_offer_reference",
    ):
        if required not in system_update.get("completed_reply_requirements", []):
            errors.append(f"System Gate approval must require {required}")
    schedule = state.get("standing_schedule_contract_template", {})
    if schedule.get("no_immediate_run") is not True:
        errors.append("standing schedule must forbid an immediate run")
    if (
        "material_processing_eligibility_fingerprint" not in schedule
        or "gate_0a_approval_id" not in schedule.get("baseline_approvals", {})
    ):
        errors.append("standing schedule must bind current Gate-0A eligibility")
    return errors


WORKFLOW_CONTROL_PATHS = {
    "orchestrator": (
        OVERLAY_ROOT
        / ".agents"
        / "skills"
        / "course-redesign-orchestrator"
        / "SKILL.md"
    ),
    "system": (
        OVERLAY_ROOT / ".agents" / "skills" / "course-redesign-system" / "SKILL.md"
    ),
    "setup": (
        OVERLAY_ROOT / ".agents" / "skills" / "course-redesign-setup" / "SKILL.md"
    ),
    "continue": (
        OVERLAY_ROOT / ".agents" / "workflows" / "course-redesign-continue.md"
    ),
    "system_review": (
        OVERLAY_ROOT / ".agents" / "workflows" / "course-redesign-system-review.md"
    ),
    "gates": OVERLAY_ROOT / "01_Control" / "GATES.md",
}


def validate_workflow_completeness(
    documents: dict[str, str] | None = None,
) -> list[str]:
    errors: list[str] = []
    if documents is None:
        documents = {}
        for name, path in WORKFLOW_CONTROL_PATHS.items():
            try:
                documents[name] = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"cannot read {name} workflow control: {exc}")
        if errors:
            return errors

    normalized = {
        name: " ".join(text.split())
        for name, text in documents.items()
    }
    required_by_document = {
        "orchestrator": (
            "## Umbrella entry, Gate 0A and Gate 0",
            "course-redesign-setup",
            "Public availability alone is insufficient",
            "without source/path leakage",
            "### Gate 1: course brief and run contract",
            "### Stage A: concurrent preliminary scan",
            "### HITL 1 / Gate 2A",
            "### Stage B/C: deep research and reconciliation",
            "### HITL 2 / Gate 2B",
            "### Gate 3: blueprint and exact targets",
            "enter the named artefact gate for each approved file",
            "### Production completion and verified handoff",
            "DECLARE PRODUCTION COMPLETE",
            "APPROVE PRODUCTION HANDOFF",
            "Do not enter HITL 3 until that verification passes",
            "Persist a system-improvement offer record",
            MANDATORY_SYSTEM_REVIEW_QUESTION,
            "idempotency key",
            "offered_awaiting_response",
            "requested",
            "declined",
            "complete_dormant",
            "clear top-level `active_run_id`",
            "informational trigger-guidance offer",
            "trigger creates a fresh run and lineage",
            "## Lecturer interaction",
            "exactly one unresolved decision",
            "live host can show the complete",
            "mutually exclusive option set and a custom-answer path",
            "capacity is unknown",
            "complete set exceeds its capacity",
            "listing every valid numbered option plus `Other - type your answer`",
            "Never prune, hide or combine valid choices",
            "Every valid option remains visible",
            "keep every valid option visible",
            "split, merge, reorder, or rename",
            "safest truthful, evidence-aligned, reversible",
            "never preselect",
            "Preserve every custom answer verbatim",
            "Blank, skipped, partial, or ambiguous answers do not advance",
            "Before each gate, recap",
            "Specialists are evidence lenses",
            "an outcome change requires rechecking implications for assessment evidence",
            "a student-experience or accessibility concern",
        ),
        "system": (
            "## Required successful-run evidence",
            "closed terminal `complete_dormant`",
            "explicit response is `requested`",
            "workflow skills and umbrella routing",
            "plugin or platform adapter",
            "`AGENTS.md`, rules, workflows, agent configurations",
            "project template, state schema and migration",
            "validators, tests and QA",
            "documentation",
            "memory or other workflow-owned durable instruction stores",
            "schedule contracts",
            "permissions, tools, external egress and automatic behaviour",
            "compatibility, benefits, regressions, risks, residual risks and rollback",
            "does not authorise system-file changes, installation, publication, release, activation, schedule registration or modification, an immediate run",
            "new MCP server, connector, authentication, permission or external egress",
            "APPROVE SYSTEM FILES",
            "as a standalone line",
            "The token alone is invalid",
            "current Gate-0A eligibility fingerprint",
            "Each later recurrence creates a fresh run and lineage",
        ),
        "setup": (
            "create_material_processing_eligibility.py",
            "Run its preview first",
            "must refuse every overwrite",
            "generic host fallback",
            "one unresolved decision at a time",
            "exact no-overwrite approval",
            "Never invent a value",
            "add an MCP dependency",
            "Preserve custom answers verbatim",
        ),
        "continue": (
            "production declaration and handoff replies",
            "reopen it, and verify it before HITL 3",
            "persist the mandatory complete read-only system-review offer before asking it exactly once",
            "offered_awaiting_response",
            "requested",
            "declined",
            "complete_dormant",
            "Persist one informational manual/optional-automation trigger-guidance offer",
            "Only a fresh trigger creates another run",
        ),
        "system_review": (
            "closed terminal `complete_dormant` run",
            "explicit response is `requested`",
            "workflow skills and umbrella routing",
            "plugin or platform adapter",
            "state schema and migration",
            "validators, tests and QA",
            "workflow-owned durable instructions",
            "schedule contracts",
            "The request authorises only read-only review and one versioned proposal",
        ),
        "gates": (
            "## Gate 0A",
            "## Gate 0",
            "Public availability alone is insufficient",
            "DECLARE PRODUCTION COMPLETE",
            "APPROVE PRODUCTION HANDOFF",
            "independent verification of the saved Production Handoff",
            "## HITL 3",
            "Silence is `offered_awaiting_response`",
            "terminal `complete_dormant`",
            "informational trigger-guidance offer",
            "## System Gate",
            "## Separate runtime activation",
            "## Standing schedule",
        ),
    }
    for name, required_markers in required_by_document.items():
        text = normalized.get(name, "")
        for marker in required_markers:
            if marker not in text:
                errors.append(f"{name} omits workflow-completeness control: {marker}")

    orchestrator_order = (
        "## Umbrella entry, Gate 0A and Gate 0",
        "### Gate 1: course brief and run contract",
        "### Stage A: concurrent preliminary scan",
        "### HITL 1 / Gate 2A",
        "### Stage B/C: deep research and reconciliation",
        "### HITL 2 / Gate 2B",
        "### Gate 3: blueprint and exact targets",
        "### Production and independent QA",
        "### Production completion and verified handoff",
        "### HITL 3",
        "## After success",
    )
    orchestrator = normalized.get("orchestrator", "")
    positions = [orchestrator.find(marker) for marker in orchestrator_order]
    if -1 not in positions and positions != sorted(positions):
        errors.append("orchestrator workflow completeness controls are reordered")
    return errors


def find_secret_like_material(root: Path = ADAPTER_ROOT) -> list[str]:
    findings: list[str] = []
    text_suffixes = {
        ".md",
        ".txt",
        ".json",
        ".example",
        ".py",
        ".yaml",
        ".yml",
        ".toml",
        ".ps1",
    }
    for path in adapter_files(root):
        if path.suffix.casefold() not in text_suffixes:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        relative = path.relative_to(root).as_posix()
        if re.search(r"(?i)C:\\Users\\[A-Za-z0-9._-]+", text):
            findings.append(f"user-home-path:{relative}")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{name}:{relative}")
    return findings


def load_private_denylist(path: Path | None) -> list[str]:
    if path is None:
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def validate(
    source_root: Path | None = None,
    private_denylist: list[str] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, Any] = {}

    for relative in sorted(REQUIRED_PATHS):
        if not (ADAPTER_ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")
    checks["required_paths"] = len(REQUIRED_PATHS)

    if not OVERLAY_ROOT.is_dir():
        errors.append("workspace-overlay is missing")
        return {"ok": False, "errors": errors, "warnings": warnings, "checks": checks}

    forbidden_paths = [
        OVERLAY_ROOT / ".agents" / "hooks.json",
        OVERLAY_ROOT / ".agents" / "mcp_config.json",
        OVERLAY_ROOT / ".agents" / "plugins",
        OVERLAY_ROOT / "_agents" / "plugins",
        OVERLAY_ROOT / ".codex",
    ]
    for path in forbidden_paths:
        if path.exists() or path.is_symlink():
            errors.append(f"forbidden active or product-specific path: {path.relative_to(OVERLAY_ROOT).as_posix()}")
    for path in OVERLAY_ROOT.rglob("plugin.json"):
        errors.append(f"active plugin manifest forbidden: {path.relative_to(OVERLAY_ROOT).as_posix()}")

    skills_root = OVERLAY_ROOT / ".agents" / "skills"
    actual_skills = {path.name for path in skills_root.iterdir() if path.is_dir()}
    if actual_skills != EXPECTED_SKILLS:
        errors.append(
            f"skill set mismatch: expected {sorted(EXPECTED_SKILLS)}, got {sorted(actual_skills)}"
        )
    for name in sorted(EXPECTED_SKILLS):
        skill_path = skills_root / name / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"missing skill entrypoint: {name}/SKILL.md")
            continue
        try:
            frontmatter = parse_frontmatter(skill_path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"invalid skill frontmatter {name}: {exc}")
            continue
        if frontmatter.get("name") != name:
            errors.append(f"skill name/folder mismatch: {name}")
        if not frontmatter.get("description"):
            errors.append(f"skill description missing: {name}")
    checks["skills"] = len(actual_skills)

    workflows_root = OVERLAY_ROOT / ".agents" / "workflows"
    workflows = {path.name for path in workflows_root.glob("*.md")}
    if workflows != EXPECTED_WORKFLOWS:
        errors.append(
            f"workflow set mismatch: expected {sorted(EXPECTED_WORKFLOWS)}, got {sorted(workflows)}"
        )
    for path in sorted(workflows_root.glob("*.md")):
        try:
            frontmatter = parse_frontmatter(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(f"invalid workflow frontmatter {path.name}: {exc}")
            continue
        if not frontmatter.get("description"):
            errors.append(f"workflow description missing: {path.name}")
        if len(path.read_text(encoding="utf-8")) > 12_000:
            errors.append(f"workflow exceeds documented 12,000-character limit: {path.name}")
    checks["workflows"] = len(workflows)
    workflow_errors = validate_workflow_completeness()
    errors.extend(workflow_errors)
    checks["workflow_completeness_controls"] = 0 if workflow_errors else 6

    rules_root = OVERLAY_ROOT / ".agents" / "rules"
    rules = sorted(rules_root.glob("*.md"))
    if len(rules) < 3:
        errors.append("at least three scoped rule files are required")
    for path in rules:
        if len(path.read_text(encoding="utf-8")) > 12_000:
            errors.append(f"rule exceeds documented 12,000-character limit: {path.name}")
    checks["rules"] = len(rules)

    agents_root = OVERLAY_ROOT / ".agents" / "agents"
    if not agents_root.is_dir():
        errors.append("project-local custom-agent directory is missing")
        actual_agents: set[str] = set()
    else:
        actual_agents = {path.name for path in agents_root.glob("*.md")}
    if actual_agents != set(EXPECTED_AGENTS):
        errors.append(
            f"custom-agent roster mismatch: expected {sorted(EXPECTED_AGENTS)}, "
            f"got {sorted(actual_agents)}"
        )
    for filename, role in sorted(EXPECTED_AGENTS.items()):
        agent_path = agents_root / filename
        if not agent_path.is_file():
            continue
        errors.extend(validate_agent_definition(agent_path, role))
    checks["agents"] = len(actual_agents)

    role_reference = (
        skills_root
        / "course-redesign-orchestrator"
        / "references"
        / "specialist-role-contracts.md"
    )
    if not role_reference.is_file():
        errors.append("shared specialist-role reference is missing")

    state_path = OVERLAY_ROOT / "01_Control" / "state.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
        errors.extend(validate_state_fields(state))
        validator_path = (
            skills_root
            / "course-redesign-setup"
            / "scripts"
            / "validate_state.py"
        )
        spec = importlib.util.spec_from_file_location(
            "antigravity_course_redesign_state_validator", validator_path
        )
        if spec is None or spec.loader is None:
            errors.append("cannot load project-local schema-8 state validator")
        else:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            errors.extend(
                f"schema-8 validator: {item}" for item in module.validate(state)
            )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid state JSON: {exc}")
    except Exception as exc:  # pragma: no cover - fail closed on validator load
        errors.append(f"cannot execute project-local state validator: {exc}")

    for path in adapter_files():
        if path.suffix.casefold() == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (OSError, UnicodeError, SyntaxError) as exc:
                errors.append(f"invalid Python syntax {path.relative_to(ADAPTER_ROOT).as_posix()}: {exc}")
        if path.suffix.casefold() == ".json" or path.name.endswith(".json.example"):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                errors.append(f"invalid JSON {path.relative_to(ADAPTER_ROOT).as_posix()}: {exc}")

    hook_example = json.loads(
        (ADAPTER_ROOT / "optional-privileged-examples" / "hooks.json.example").read_text(
            encoding="utf-8"
        )
    )
    if not hook_example or any(
        not isinstance(value, dict) or value.get("enabled") is not False
        for value in hook_example.values()
    ):
        errors.append("every optional hook example must be explicitly disabled")
    mcp_example = json.loads(
        (ADAPTER_ROOT / "optional-privileged-examples" / "mcp_config.json.example").read_text(
            encoding="utf-8"
        )
    )
    servers = mcp_example.get("mcpServers", {})
    if not servers or any(
        value.get("disabled") is not True or value.get("disabledTools") != ["*"]
        for value in servers.values()
        if isinstance(value, dict)
    ):
        errors.append("every optional MCP example must be disabled with all tools withheld")

    secret_findings = find_secret_like_material()
    errors.extend(f"secret-like material detected: {finding}" for finding in secret_findings)
    checks["secret_findings"] = len(secret_findings)

    pilot_markers = private_denylist or []
    for path in adapter_files():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for marker in pilot_markers:
            if marker.casefold() in text.casefold():
                errors.append(
                    f"course-specific pilot marker in {path.relative_to(ADAPTER_ROOT).as_posix()}"
                )

    manifest_path = ADAPTER_ROOT / "adapter-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"invalid adapter manifest: {exc}")
        manifest = {}
    if manifest:
        if manifest.get("platform") != "google-antigravity":
            errors.append("adapter manifest platform must be google-antigravity")
        if manifest.get("adapter_version") != "0.2.4":
            errors.append("adapter manifest top-level adapter_version must be 0.2.4")
        if manifest.get("status") != "candidate_not_active":
            errors.append("adapter manifest top-level status must remain candidate_not_active")
        adapter = manifest.get("adapter", {})
        if adapter.get("platform") != "google-antigravity":
            errors.append("nested adapter platform must be google-antigravity")
        if adapter.get("version") != "0.2.4":
            errors.append("nested adapter version must be 0.2.4")
        if adapter.get("status") != "candidate_not_active":
            errors.append("nested adapter status must remain candidate_not_active")
        provenance = manifest.get("provenance", {})
        if provenance.get("workflow_proposal_id") != "ACR-SYS-20260822-007":
            errors.append("workflow provenance must identify ACR-SYS-20260822-007")
        if provenance.get("validated_base_version") != "0.2.4":
            errors.append("workflow provenance must identify shared base version 0.2.4")
        if provenance.get("adapter_release_version") != "0.2.4":
            errors.append("workflow provenance must identify adapter release version 0.2.4")
        if manifest.get("source", {}).get("version") != "0.2.4":
            errors.append("source version must identify shared candidate 0.2.4")
        source_files = manifest.get("source_files", [])
        if not source_files:
            errors.append("adapter manifest has no source-file hashes")
        for item in source_files:
            source_path = item.get("path", "")
            expected_hash = item.get("sha256", "")
            if not source_path or not SOURCE_HASH_PATTERN.fullmatch(expected_hash):
                errors.append(f"invalid source manifest entry: {item}")
                continue
            if source_root is not None:
                actual_path = source_root / Path(source_path)
                if not actual_path.is_file():
                    errors.append(f"source file missing during live verification: {source_path}")
                elif sha256(actual_path) != expected_hash:
                    errors.append(f"source hash mismatch: {source_path}")
        if source_root is None:
            warnings.append("shared-core source root not supplied; recorded source hashes were not live-reverified")
        generated = manifest.get("generated_files", [])
        manifested_paths: set[str] = set()
        for item in generated:
            relative = item.get("path", "")
            expected_hash = item.get("sha256", "")
            if not relative or not SOURCE_HASH_PATTERN.fullmatch(expected_hash):
                errors.append(f"invalid generated-file manifest entry: {item}")
                continue
            manifested_paths.add(relative)
            path = ADAPTER_ROOT / Path(relative)
            if not path.is_file():
                errors.append(f"manifested adapter file missing: {relative}")
            elif sha256(path) != expected_hash:
                errors.append(f"adapter hash mismatch: {relative}")
        actual_paths = {
            path.relative_to(ADAPTER_ROOT).as_posix()
            for path in adapter_files()
            if path.name != "adapter-manifest.json"
        }
        if manifested_paths != actual_paths:
            missing = sorted(actual_paths - manifested_paths)
            extra = sorted(manifested_paths - actual_paths)
            if missing:
                errors.append(f"unmanifested adapter files: {missing}")
            if extra:
                errors.append(f"manifest entries without files: {extra}")
        checks["source_hashes"] = len(source_files)
        checks["generated_hashes"] = len(generated)

    checks["adapter_files"] = len(adapter_files())
    return {"ok": not errors, "errors": errors, "warnings": warnings, "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Optional 03_Shared_Workflow_Core root for live source-hash verification.",
    )
    parser.add_argument(
        "--private-denylist",
        type=Path,
        help=(
            "Optional local-only newline-delimited course markers for a private "
            "pre-publication scrub; never add this file to the adapter."
        ),
    )
    args = parser.parse_args()
    source_root = args.source_root.resolve(strict=True) if args.source_root else None
    denylist = load_private_denylist(args.private_denylist)
    result = validate(source_root, denylist)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
