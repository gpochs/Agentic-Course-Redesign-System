#!/usr/bin/env python3
"""Fail closed on public-source, workflow and adapter regressions."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CURRENT_VERSION = "0.2.2"
CURRENT_STATE_SCHEMA = 7
CURRENT_PROPOSAL = "ACR-SYS-20260820-004"
EXPECTED_TOP_LEVEL = {
    "01_ChatGPT_Desktop_App",
    "02_Other_Agentic_Systems",
    "03_Shared_Workflow_Core",
    "04_Documentation",
    "05_Validation",
}
EXPECTED_SKILLS = {
    "course-redesign-assessment",
    "course-redesign-materials",
    "course-redesign-orchestrator",
    "course-redesign-research",
    "course-redesign-setup",
    "course-redesign-system",
}
FORBIDDEN_PLUGIN_INTEGRATION_KEYS = (
    "apps",
    "mcpServers",
    "connectors",
    "hooks",
    "permissions",
    "authentication",
    "schedules",
)
MANDATORY_REVIEW_SCOPE_PHRASES = (
    "workflow skills and umbrella entry routing",
    "plugin or platform adapter",
    "AGENTS.md and agent configurations",
    "project template, state schema and migration",
    "validators, tests and QA",
    "documentation",
    "memory or other workflow-owned durable instruction stores",
    "schedule contracts",
    "permissions, tools, external egress and automatic behaviour",
    "compatibility, benefits, regressions, risks, residual risks and rollback",
)
MANDATORY_REVIEW_SCOPE_IDS = [
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
EXPECTED_REVIEW_AUTHORISES = [
    "read_only_review_of_current_system_and_successful_run_evidence",
    "prepare_one_versioned_system_improvement_proposal",
]
EXPECTED_REVIEW_DENIALS = [
    "create_or_modify_system_files",
    "install_or_update_plugin",
    "publish_or_release",
    "activate_runtime",
    "register_or_modify_schedule",
    "trigger_immediate_run",
    "add_mcp_server_connector_authentication_permission_or_external_egress",
]
ORCHESTRATION_ENTRY_PATHS = (
    "03_Shared_Workflow_Core/agent-skills/course-redesign-orchestrator/SKILL.md",
    "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/skills/course-redesign-orchestrator/SKILL.md",
    "01_ChatGPT_Desktop_App/openai-submission/source/agentic-course-redesign/skills/course-redesign-orchestrator/SKILL.md",
    "02_Other_Agentic_Systems/00_Portable_Core_Adapter/overlay/.claude/skills/course-redesign/references/workflow.md",
    "02_Other_Agentic_Systems/04_Google_Antigravity/workspace-overlay/.agents/skills/course-redesign-orchestrator/SKILL.md",
)
SYSTEM_LIFECYCLE_PATHS = (
    "03_Shared_Workflow_Core/agent-skills/course-redesign-system/SKILL.md",
    "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/skills/course-redesign-system/SKILL.md",
    "01_ChatGPT_Desktop_App/openai-submission/source/agentic-course-redesign/skills/course-redesign-system/SKILL.md",
    "02_Other_Agentic_Systems/00_Portable_Core_Adapter/overlay/.claude/skills/course-redesign/references/workflow.md",
    "02_Other_Agentic_Systems/04_Google_Antigravity/workspace-overlay/.agents/skills/course-redesign-system/SKILL.md",
)
STATE_MIRROR_PATHS = (
    "03_Shared_Workflow_Core/course-project-template/01_Control/state.json",
    "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/assets/project-template/01_Control/state.json",
    "01_ChatGPT_Desktop_App/openai-submission/source/agentic-course-redesign/assets/project-template/01_Control/state.json",
    "02_Other_Agentic_Systems/04_Google_Antigravity/workspace-overlay/01_Control/state.json",
)
SCRIPT_MIRROR_PATHS = {
    "validate_state.py": (
        "03_Shared_Workflow_Core/scripts/validate_state.py",
        "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/scripts/validate_state.py",
        "01_ChatGPT_Desktop_App/openai-submission/source/agentic-course-redesign/scripts/validate_state.py",
        "02_Other_Agentic_Systems/04_Google_Antigravity/workspace-overlay/.agents/skills/course-redesign-setup/scripts/validate_state.py",
    ),
    "migrate_state_v6_to_v7.py": (
        "03_Shared_Workflow_Core/scripts/migrate_state_v6_to_v7.py",
        "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/scripts/migrate_state_v6_to_v7.py",
        "01_ChatGPT_Desktop_App/openai-submission/source/agentic-course-redesign/scripts/migrate_state_v6_to_v7.py",
        "02_Other_Agentic_Systems/04_Google_Antigravity/workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v6_to_v7.py",
    ),
}
REQUIRED_ROOT_FILES = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
}
TEXT_SUFFIXES = {
    "",
    ".csv",
    ".html",
    ".json",
    ".jsonc",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
EXCLUDED_PARTS = {".git", "dist"}
DISALLOWED_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
}
DISALLOWED_SUFFIXES = {
    ".cer",
    ".crt",
    ".jks",
    ".key",
    ".keystore",
    ".p12",
    ".pem",
    ".pfx",
    ".pyc",
}
CONTENT_PATTERNS = {
    "windows_user_home": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'<>]+[\\/]"),
    "windows_onedrive_absolute": re.compile(r"(?i)[A-Z]:[\\/][^\r\n]*[\\/]OneDrive[\\/]"),
    "macos_user_home": re.compile("/" + "Users/" + r"[^/\s\"'<>]+/"),
    "linux_user_home": re.compile("/" + "home/" + r"[^/\s\"'<>]+/"),
    "email_address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_token": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def display_path(path: Path) -> str:
    try:
        return relative(path)
    except ValueError:
        return path.as_posix()


def source_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files, key=lambda item: relative(item).casefold())


def parse_skill_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing YAML delimiter") from exc
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    if not "\n".join(lines[end + 1 :]).strip():
        raise ValueError("empty skill instructions")
    return metadata


def normalized_prose(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?<=\w)-\s*\n\s*(?=\w)", "-", text)
    return re.sub(r"\s+", " ", text).casefold().replace("hitl-3", "hitl 3")


def validate_orchestration_entry(path: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not path.is_file():
        return [{"path": display_path(path), "kind": "missing_orchestration_entry"}]
    text = normalized_prose(path)
    positions: dict[str, int] = {}
    start = 0
    for marker in (
        "gate 0",
        "declare production complete",
        "approve production handoff",
        "hitl 3",
        "would you like a separate, read-only system-improvement review",
    ):
        position = text.find(marker, start)
        positions[marker] = position
        if position < 0:
            findings.append(
                {
                    "path": display_path(path),
                    "kind": "orchestration_stage_missing_or_out_of_order",
                    "detail": marker,
                }
            )
            break
        start = position + len(marker)

    declaration_position = positions.get("declare production complete", -1)
    handoff_position = positions.get("approve production handoff", -1)
    hitl_position = positions.get("hitl 3", -1)
    question_position = positions.get(
        "would you like a separate, read-only system-improvement review", -1
    )
    if declaration_position >= 0 and handoff_position >= 0 and question_position >= 0:
        declaration_context = text[max(0, declaration_position - 220) : handoff_position]
        handoff_context = text[handoff_position:question_position]
        verification_context = text[
            handoff_position : min(question_position, max(handoff_position, hitl_position) + 240)
        ]
        terminal_context = text[max(0, declaration_position - 300) : question_position]
        terminal_requirements = {
            "two completed current-lineage replies": (
                (
                    "two separate completed current-lineage replies"
                    in declaration_context
                    or (
                        terminal_context.count("current-lineage") >= 2
                        and declaration_context.count("completed") >= 2
                    )
                )
                and "second" in declaration_context
            ),
            "both approval tokens are standalone lines": terminal_context.count("standalone line")
            >= 2,
            "second reply repeats the exact target": (
                bool(re.search(r"exact.{0,160}target", terminal_context))
                and "repeat" in terminal_context
            ),
            "token-only or combined approval fails closed": (
                "token" in terminal_context
                and ("invalid" in terminal_context or "insufficient" in terminal_context)
            ),
            "handoff is independently reopened or verified": (
                "verify" in verification_context
                and (
                    "independently" in verification_context
                    or "reopen" in verification_context
                )
            ),
            "HITL3 remains closed until handoff verification": any(
                marker in verification_context
                for marker in (
                    "do not open hitl 3",
                    "do not enter hitl 3",
                    "hitl 3 remains forbidden",
                    "do not mark the course redesign complete until",
                )
            ),
            "unconditional current-lineage HITL3 acceptance precedes the offer": bool(
                re.search(
                    r"(?:unconditional current-lineage(?: hitl 3)? acceptance|"
                    r"current-lineage(?: hitl 3)? final acceptance)",
                    text[:question_position],
                )
            ),
        }
        for detail, passed in terminal_requirements.items():
            if not passed:
                findings.append(
                    {
                        "path": display_path(path),
                        "kind": "terminal_gate_contract_incomplete",
                        "detail": detail,
                    }
                )

    question_prefix = "would you like a separate, read-only system-improvement review"
    if text.count(question_prefix) != 1:
        findings.append(
            {
                "path": display_path(path),
                "kind": "system_review_question_count_mismatch",
                "detail": f"count={text.count(question_prefix)}",
            }
        )
    question_position = text.find(question_prefix)
    if question_position >= 0:
        question_context = text[max(0, question_position - 300) : question_position + 2600]
        for phrase in MANDATORY_REVIEW_SCOPE_PHRASES:
            if phrase.casefold() not in question_context:
                findings.append(
                    {
                        "path": display_path(path),
                        "kind": "system_review_question_scope_incomplete",
                        "detail": phrase,
                    }
                )
        for phrase in (
            "exactly once",
            "authorises only that review and proposal",
            "does not authorise system-file changes",
            "offered_awaiting_response",
            "requested",
            "declined",
        ):
            if phrase not in question_context:
                findings.append(
                    {
                        "path": display_path(path),
                        "kind": "system_review_offer_control_missing",
                        "detail": phrase,
                    }
                )
    return findings


def validate_system_lifecycle_entry(path: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    if not path.is_file():
        return [{"path": display_path(path), "kind": "missing_system_lifecycle_entry"}]
    text = normalized_prose(path)
    system_gate = text.find("approve system files")
    activation = text.find("activation", max(0, system_gate))
    schedule_gate = text.find("approve schedules", max(0, activation))
    for marker, position in (
        ("APPROVE SYSTEM FILES", system_gate),
        ("separate activation after System Gate", activation),
        ("APPROVE SCHEDULES after activation", schedule_gate),
    ):
        if position < 0:
            findings.append(
                {
                    "path": display_path(path),
                    "kind": "system_lifecycle_stage_missing_or_out_of_order",
                    "detail": marker,
                }
            )
    for marker in ("candidate_not_active", "no-write simulation"):
        if marker not in text:
            findings.append(
                {
                    "path": display_path(path),
                    "kind": "system_lifecycle_safety_control_missing",
                    "detail": marker,
                }
            )
    if not any(
        marker in text
        for marker in (
            "no immediate run",
            "does not authorise an immediate run",
            "must not trigger an immediate run",
            "do not trigger an immediate run",
            "never triggers an immediate run",
            "never triggers an immediate content run",
        )
    ):
        findings.append(
            {
                "path": display_path(path),
                "kind": "system_lifecycle_safety_control_missing",
                "detail": "no immediate run",
            }
        )
    return findings


def validate_candidate_control_record(
    path: Path, expected_phrases: tuple[str, ...]
) -> list[dict[str, str]]:
    if not path.is_file():
        return [{"path": display_path(path), "kind": "missing_candidate_control_record"}]
    text = normalized_prose(path)
    return [
        {
            "path": display_path(path),
            "kind": "candidate_control_record_mismatch",
            "detail": phrase,
        }
        for phrase in expected_phrases
        if phrase not in text
    ]


def validate_adapter_manifest(path: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [{"path": relative(path), "kind": "invalid_adapter_manifest", "detail": str(exc)}]
    for field in ("schema_version", "platform", "adapter_version", "status"):
        if field not in data:
            findings.append({"path": relative(path), "kind": f"missing_adapter_field:{field}"})
    if data.get("status") not in {"candidate_not_active", "template_not_installed", "validated_template"}:
        findings.append({"path": relative(path), "kind": "unsafe_adapter_status"})
    if data.get("adapter_version") != CURRENT_VERSION:
        findings.append({"path": relative(path), "kind": "adapter_release_version_mismatch"})
    # `source_files` may describe the external validated base and is not
    # expected to exist inside an adapter. Verify only frozen adapter outputs.
    records = data.get("files") or data.get("generated_files") or []
    if records and not isinstance(records, list):
        findings.append({"path": relative(path), "kind": "invalid_adapter_file_records"})
    for record in records if isinstance(records, list) else []:
        if not isinstance(record, dict):
            findings.append({"path": relative(path), "kind": "invalid_adapter_file_record"})
            continue
        rel_path = record.get("path") or record.get("relative_path")
        expected = record.get("sha256")
        if not rel_path or not expected:
            continue
        target = path.parent / str(rel_path)
        if not target.is_file():
            findings.append({"path": relative(path), "kind": "adapter_record_missing", "detail": str(rel_path)})
        elif sha256(target) != str(expected).upper():
            findings.append({"path": relative(path), "kind": "adapter_record_hash_mismatch", "detail": str(rel_path)})
    return findings


def load_private_denylist(path: Path | None) -> list[str]:
    if path is None:
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def scan(private_denylist: list[str] | None = None) -> dict[str, object]:
    findings: list[dict[str, str]] = []
    files = source_files()
    denylist = private_denylist or []

    for name in sorted(EXPECTED_TOP_LEVEL):
        if not (ROOT / name).is_dir():
            findings.append({"path": name, "kind": "missing_top_level_directory"})
    for name in sorted(REQUIRED_ROOT_FILES):
        if not (ROOT / name).is_file():
            findings.append({"path": name, "kind": "missing_required_root_file"})

    for path in files:
        rel = relative(path)
        parts = set(path.relative_to(ROOT).parts)
        if path.is_symlink():
            findings.append({"path": rel, "kind": "symlink_not_portable"})
        if parts & DISALLOWED_PARTS:
            findings.append({"path": rel, "kind": "cache_or_environment_artifact"})
        if path.name.startswith("~$"):
            findings.append({"path": rel, "kind": "office_lock_file"})
        if path.name.casefold().startswith(".env") or path.suffix.casefold() in DISALLOWED_SUFFIXES:
            findings.append({"path": rel, "kind": "secret_key_or_bytecode_file"})
        if path.suffix.casefold() == ".json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if path.name == "state.json":
                    if data.get("schema_version") != CURRENT_STATE_SCHEMA:
                        findings.append({"path": rel, "kind": "state_schema_version_mismatch"})
                    if data.get("plugin_version") != CURRENT_VERSION:
                        findings.append({"path": rel, "kind": "state_plugin_version_mismatch"})
                    if data.get("status") != "candidate_not_active":
                        findings.append({"path": rel, "kind": "state_not_inactive"})
                    if data.get("schedules") not in ([], None):
                        findings.append({"path": rel, "kind": "schedule_present"})
                    routing = data.get("umbrella_entry_routing", {})
                    if (
                        routing.get("entry_name") != "Agentic Course Redesign"
                        or routing.get("entry_skill") != "course-redesign-orchestrator"
                        or routing.get("initial_gate") != "GATE_0_AWAITING_BOUNDARY_CONFIRMATION"
                        or not routing.get("gate_0_required_before_course_source_reading")
                        or not routing.get("gate_0_required_before_specialist_work")
                    ):
                        findings.append({"path": rel, "kind": "state_umbrella_route_invalid"})
                    compatibility = data.get("schema_compatibility", {})
                    if (
                        compatibility.get("current_schema_version") != CURRENT_STATE_SCHEMA
                        or compatibility.get("migration_helper")
                        != "scripts/migrate_state_v6_to_v7.py"
                        or compatibility.get("migration_mode") != "preview_only"
                        or compatibility.get("automatic_apply_forbidden") is not True
                    ):
                        findings.append({"path": rel, "kind": "state_migration_contract_invalid"})
                    activation = data.get("activation", {})
                    if (
                        activation.get("automatic_activation_forbidden") is not True
                        or activation.get("separate_activation_decision", {}).get("status")
                        != "not_requested"
                    ):
                        findings.append({"path": rel, "kind": "state_activation_not_fail_closed"})
                    schedule = data.get("schedule_registration", {})
                    if (
                        schedule.get("status") != "not_approved"
                        or schedule.get("no_write_simulation_status") != "not_run"
                        or schedule.get("no_immediate_run_required") is not True
                        or schedule.get("approved_standing_contract_ids") != []
                        or schedule.get("approved_standing_contract_versions") != []
                    ):
                        findings.append({"path": rel, "kind": "state_schedule_not_fail_closed"})
                    run_template = data.get("run_template", {})
                    contract = run_template.get("contract", {})
                    if contract.get("permitted_tools") != [] or contract.get("permitted_actions") != []:
                        findings.append({"path": rel, "kind": "state_default_permission_expansion"})
                    approvals = run_template.get("approvals", {})
                    offer = approvals.get("system_improvement_review_offer", {})
                    if (
                        offer.get("required_question_scope") != MANDATORY_REVIEW_SCOPE_IDS
                        or offer.get("ask_exactly_once") is not True
                        or offer.get("record_offer_before_asking") is not True
                    ):
                        findings.append({"path": rel, "kind": "state_system_review_offer_invalid"})
                    question = str(offer.get("mandatory_question", ""))
                    for phrase in MANDATORY_REVIEW_SCOPE_PHRASES:
                        if phrase.casefold() not in question.casefold():
                            findings.append(
                                {
                                    "path": rel,
                                    "kind": "state_system_review_scope_incomplete",
                                    "detail": phrase,
                                }
                            )
                    authority = offer.get("authority_on_request", {})
                    if (
                        authority.get("authorises") != EXPECTED_REVIEW_AUTHORISES
                        or authority.get("does_not_authorise") != EXPECTED_REVIEW_DENIALS
                    ):
                        findings.append({"path": rel, "kind": "state_review_response_expands_authority"})
                    system_update = activation.get("system_update", {})
                    if (
                        "matching_run_system_improvement_review_offer_requested"
                        not in system_update.get("prerequisites", [])
                        or "run_id" not in system_update.get("completed_reply_requirements", [])
                        or "system_improvement_review_offer_reference"
                        not in system_update.get("completed_reply_requirements", [])
                    ):
                        findings.append({"path": rel, "kind": "state_system_gate_source_link_missing"})
            except Exception as exc:
                findings.append({"path": rel, "kind": "invalid_json", "detail": str(exc)})
        if path.suffix.casefold() == ".toml":
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                findings.append({"path": rel, "kind": "invalid_toml", "detail": str(exc)})
        if path.suffix.casefold() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            if "\ufffd" in text:
                findings.append({"path": rel, "kind": "replacement_character"})
            for marker in denylist:
                if marker.casefold() in text.casefold():
                    findings.append({"path": rel, "kind": "pilot_specific_content", "detail": marker})
            for kind, pattern in CONTENT_PATTERNS.items():
                if pattern.search(text):
                    findings.append({"path": rel, "kind": kind})
            if path.suffix.casefold() == ".svg" and "\r" in text:
                findings.append({"path": rel, "kind": "svg_not_lf_normalized"})

    skill_root = ROOT / "03_Shared_Workflow_Core" / "agent-skills"
    actual_skills = {path.parent.name for path in skill_root.glob("*/SKILL.md")}
    if actual_skills != EXPECTED_SKILLS:
        findings.append(
            {
                "path": relative(skill_root),
                "kind": "shared_skill_set_mismatch",
                "detail": f"expected={sorted(EXPECTED_SKILLS)} actual={sorted(actual_skills)}",
            }
        )
    for path in ROOT.rglob("SKILL.md"):
        if any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        try:
            metadata = parse_skill_frontmatter(path)
            name = metadata.get("name", "")
            description = metadata.get("description", "")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                findings.append({"path": relative(path), "kind": "invalid_skill_name"})
            if not description or len(description) > 1024:
                findings.append({"path": relative(path), "kind": "invalid_skill_description"})
        except Exception as exc:
            findings.append({"path": relative(path), "kind": "invalid_skill", "detail": str(exc)})

    skill_roots = (
        ROOT / "03_Shared_Workflow_Core" / "agent-skills",
        ROOT / "01_ChatGPT_Desktop_App" / "plugins" / "agentic-course-redesign" / "skills",
        ROOT
        / "01_ChatGPT_Desktop_App"
        / "openai-submission"
        / "source"
        / "agentic-course-redesign"
        / "skills",
        ROOT
        / "02_Other_Agentic_Systems"
        / "04_Google_Antigravity"
        / "workspace-overlay"
        / ".agents"
        / "skills",
    )
    for root in skill_roots:
        actual = {path.parent.name for path in root.glob("*/SKILL.md")}
        if actual != EXPECTED_SKILLS:
            findings.append(
                {
                    "path": relative(root),
                    "kind": "six_skill_bundle_mismatch",
                    "detail": f"expected={sorted(EXPECTED_SKILLS)} actual={sorted(actual)}",
                }
            )

    for rel_path in ORCHESTRATION_ENTRY_PATHS:
        findings.extend(validate_orchestration_entry(ROOT / rel_path))
    for rel_path in SYSTEM_LIFECYCLE_PATHS:
        findings.extend(validate_system_lifecycle_entry(ROOT / rel_path))

    state_paths = [ROOT / rel_path for rel_path in STATE_MIRROR_PATHS]
    if all(path.is_file() for path in state_paths):
        canonical_state = state_paths[0].read_bytes()
        for path in state_paths[1:]:
            if path.read_bytes() != canonical_state:
                findings.append({"path": relative(path), "kind": "canonical_state_mirror_drift"})
    else:
        for path in state_paths:
            if not path.is_file():
                findings.append({"path": relative(path), "kind": "missing_state_mirror"})

    for script_name, rel_paths in SCRIPT_MIRROR_PATHS.items():
        paths = [ROOT / rel_path for rel_path in rel_paths]
        if all(path.is_file() for path in paths):
            canonical_script = paths[0].read_bytes()
            for path in paths[1:]:
                if path.read_bytes() != canonical_script:
                    findings.append(
                        {
                            "path": relative(path),
                            "kind": "canonical_script_mirror_drift",
                            "detail": script_name,
                        }
                    )
        else:
            for path in paths:
                if not path.is_file():
                    findings.append(
                        {
                            "path": relative(path),
                            "kind": "missing_canonical_script_mirror",
                            "detail": script_name,
                        }
                    )

    adapter_manifests = sorted(ROOT.glob("02_Other_Agentic_Systems/**/adapter-manifest.json"))
    if len(adapter_manifests) < 4:
        findings.append(
            {
                "path": "02_Other_Agentic_Systems",
                "kind": "insufficient_adapter_manifests",
                "detail": f"found={len(adapter_manifests)}",
            }
        )
    for manifest in adapter_manifests:
        findings.extend(validate_adapter_manifest(manifest))

    root_marketplace = ROOT / ".agents" / "plugins" / "marketplace.json"
    if not root_marketplace.is_file():
        findings.append({"path": ".agents/plugins/marketplace.json", "kind": "missing_root_marketplace"})
    else:
        marketplace = json.loads(root_marketplace.read_text(encoding="utf-8"))
        plugins = marketplace.get("plugins", [])
        if len(plugins) != 1 or plugins[0].get("name") != "agentic-course-redesign":
            findings.append({"path": relative(root_marketplace), "kind": "unexpected_root_marketplace_plugins"})
        else:
            plugin_path = plugins[0].get("source", {}).get("path", "")
            target = ROOT / str(plugin_path).removeprefix("./")
            if not (target / ".codex-plugin" / "plugin.json").is_file():
                findings.append({"path": relative(root_marketplace), "kind": "root_marketplace_target_missing"})

    chatgpt_manifest = (
        ROOT
        / "01_ChatGPT_Desktop_App"
        / "plugins"
        / "agentic-course-redesign"
        / ".codex-plugin"
        / "plugin.json"
    )
    if not chatgpt_manifest.is_file():
        findings.append({"path": relative(chatgpt_manifest), "kind": "missing_chatgpt_plugin_manifest"})
    else:
        plugin_data = json.loads(chatgpt_manifest.read_text(encoding="utf-8"))
        if plugin_data.get("name") != "agentic-course-redesign" or plugin_data.get("version") != CURRENT_VERSION:
            findings.append({"path": relative(chatgpt_manifest), "kind": "chatgpt_plugin_identity_mismatch"})
        if plugin_data.get("interface", {}).get("displayName") != "Agentic Course Redesign":
            findings.append({"path": relative(chatgpt_manifest), "kind": "chatgpt_plugin_display_name_mismatch"})
        for forbidden_key in FORBIDDEN_PLUGIN_INTEGRATION_KEYS:
            if forbidden_key in plugin_data:
                findings.append(
                    {
                        "path": relative(chatgpt_manifest),
                        "kind": "unexpected_plugin_integration_or_permission",
                        "detail": forbidden_key,
                    }
                )

    public_plugin = (
        ROOT
        / "01_ChatGPT_Desktop_App"
        / "openai-submission"
        / "source"
        / "agentic-course-redesign"
    )
    custom_plugin = chatgpt_manifest.parent.parent
    for subtree in (".codex-plugin", "assets", "scripts", "skills"):
        custom_root = custom_plugin / subtree
        public_root = public_plugin / subtree
        custom_records = {
            path.relative_to(custom_root).as_posix(): path.read_bytes()
            for path in custom_root.rglob("*")
            if path.is_file()
        }
        public_records = {
            path.relative_to(public_root).as_posix(): path.read_bytes()
            for path in public_root.rglob("*")
            if path.is_file()
        }
        if custom_records != public_records:
            findings.append(
                {
                    "path": f"01_ChatGPT_Desktop_App/{subtree}",
                    "kind": "chatgpt_custom_public_runtime_drift",
                }
            )

    for forbidden_name in (".mcp.json", ".app.json", "hooks.json", "permissions.json", "oauth.json"):
        for plugin_root in (custom_plugin, public_plugin):
            for forbidden_path in plugin_root.rglob(forbidden_name):
                findings.append(
                    {
                        "path": relative(forbidden_path),
                        "kind": "unexpected_plugin_privileged_component",
                    }
                )

    umbrella_metadata = (
        chatgpt_manifest.parent.parent
        / "skills"
        / "course-redesign-orchestrator"
        / "agents"
        / "openai.yaml"
    )
    umbrella_skill = umbrella_metadata.parent.parent / "SKILL.md"
    if not umbrella_metadata.is_file() or not umbrella_skill.is_file():
        findings.append({"path": relative(umbrella_metadata), "kind": "missing_umbrella_entry"})
    else:
        metadata_text = umbrella_metadata.read_text(encoding="utf-8")
        skill_text = umbrella_skill.read_text(encoding="utf-8")
        if 'display_name: "Agentic Course Redesign"' not in metadata_text:
            findings.append({"path": relative(umbrella_metadata), "kind": "umbrella_display_name_mismatch"})
        if "$course-redesign-orchestrator" not in metadata_text:
            findings.append({"path": relative(umbrella_metadata), "kind": "umbrella_default_prompt_mismatch"})
        if "## Umbrella entry routing" not in skill_text or "$course-redesign-setup" not in skill_text:
            findings.append({"path": relative(umbrella_skill), "kind": "umbrella_routing_missing"})

    antigravity_overlay = ROOT / "02_Other_Agentic_Systems" / "04_Google_Antigravity" / "workspace-overlay"
    for forbidden in (
        antigravity_overlay / ".agents" / "hooks.json",
        antigravity_overlay / ".agents" / "mcp_config.json",
        antigravity_overlay / ".agents" / "plugins",
    ):
        if forbidden.exists():
            findings.append({"path": relative(forbidden), "kind": "privileged_antigravity_component_auto_discovered"})

    ignore_path = ROOT / ".gitignore"
    if ignore_path.is_file():
        ignore_text = ignore_path.read_text(encoding="utf-8")
        for forbidden in (".agents/", ".codex/", ".claude/", ".opencode/", ".github/"):
            if re.search(rf"(?m)^\s*{re.escape(forbidden)}\s*$", ignore_text):
                findings.append({"path": ".gitignore", "kind": "control_directory_ignored", "detail": forbidden})

    version_path = ROOT / "03_Shared_Workflow_Core" / "VERSION"
    if not version_path.is_file() or version_path.read_text(encoding="utf-8").strip() != CURRENT_VERSION:
        findings.append({"path": relative(version_path), "kind": "canonical_version_mismatch"})

    adapter_contract_path = ROOT / "03_Shared_Workflow_Core" / "adapter-contract.json"
    if not adapter_contract_path.is_file():
        findings.append({"path": relative(adapter_contract_path), "kind": "missing_adapter_contract"})
    else:
        try:
            adapter_contract = json.loads(adapter_contract_path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append(
                {
                    "path": relative(adapter_contract_path),
                    "kind": "invalid_adapter_contract",
                    "detail": str(exc),
                }
            )
        else:
            security = adapter_contract.get("security_defaults", {})
            if (
                adapter_contract.get("core_version") != CURRENT_VERSION
                or adapter_contract.get("state_schema_version") != CURRENT_STATE_SCHEMA
                or adapter_contract.get("status") != "candidate_not_active"
                or adapter_contract.get("schedules") != []
                or any(
                    security.get(key) is not False
                    for key in (
                        "runtime_active",
                        "hooks_active",
                        "mcp_servers_active",
                        "schedule_registered",
                    )
                )
            ):
                findings.append(
                    {"path": relative(adapter_contract_path), "kind": "unsafe_adapter_contract"}
                )

    proposal_path = ROOT / "01_ChatGPT_Desktop_App" / "SYSTEM_PROPOSAL_v0.2.2.md"
    rollback_path = ROOT / "01_ChatGPT_Desktop_App" / "ROLLBACK_v0.2.2.md"
    validation_report_path = ROOT / "05_Validation" / "VALIDATION_REPORT_v0.2.2.md"
    control_expectations = {
        proposal_path: (
            f"proposal id: `{CURRENT_PROPOSAL.casefold()}`",
            f"proposal version: `{CURRENT_VERSION}`",
            "system-file candidate approved; repository publication separately authorised",
            "runtime not installed, activated, or scheduled by that publication",
            "base: published `v0.2.1`",
            "`03_shared_workflow_core/**`",
            "`01_chatgpt_desktop_app/**`",
            "`02_other_agentic_systems/**`",
            "`04_documentation/**`",
            "`05_validation/**`",
            "exactly six bundled skills",
            "preview-only `scripts/migrate_state_v6_to_v7.py`",
            "no mcp/app/hook/auth/permission/schedule payload",
            "`schedules=[]`",
        ),
        rollback_path: (
            f"release: `{CURRENT_PROPOSAL.casefold()}` version `{CURRENT_VERSION}`",
            "repository source and matching evidence are published",
            "release publication does not install the plugin",
            "`03_shared_workflow_core/**`",
            "`01_chatgpt_desktop_app/**`",
            "`02_other_agentic_systems/**`",
            "`04_documentation/**`",
            "`05_validation/**`",
            "do not delete or rewrite course projects",
            "do not delete, move, or rewrite the published v0.2.2 tag",
            "keep the published v0.2.1 tag and release assets unchanged",
            "rollback never authorises publication, activation, migration application, or schedule registration",
        ),
        validation_report_path: (
            f"proposal: `{CURRENT_PROPOSAL.casefold()}`",
            f"release version: `{CURRENT_VERSION}`",
            "pass — validated repository release source",
            "no course-material path was changed",
            "repository unit suite | pass: 47/47",
            "exactly six skills remain available",
            "no mcp server, app, connector, hook, authentication, permission, schedule",
            "repository publication does not install, activate, or schedule v0.2.2",
            "31 may/31 december cadence has not been registered",
        ),
    }
    for path, expected_phrases in control_expectations.items():
        findings.extend(validate_candidate_control_record(path, expected_phrases))
    if proposal_path.is_file():
        proposal_text = normalized_prose(proposal_path)
        for phrase in MANDATORY_REVIEW_SCOPE_PHRASES:
            if phrase.casefold() not in proposal_text:
                findings.append(
                    {
                        "path": relative(proposal_path),
                        "kind": "candidate_proposal_review_scope_incomplete",
                        "detail": phrase,
                    }
                )

    attributes_path = ROOT / ".gitattributes"
    if attributes_path.is_file():
        attributes = attributes_path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^\*\.svg text eol=lf$", attributes):
            findings.append({"path": ".gitattributes", "kind": "missing_svg_lf_rule"})
        if not re.search(r"(?m)^03_Shared_Workflow_Core/VERSION text eol=lf$", attributes):
            findings.append({"path": ".gitattributes", "kind": "missing_version_lf_rule"})

    return {
        "schema_version": 1,
        "pass": not findings,
        "repository": "Agentic-Course-Redesign-System",
        "source_file_count": len(files),
        "shared_skill_count": len(actual_skills),
        "adapter_manifest_count": len(adapter_manifests),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--private-denylist",
        type=Path,
        help="Optional local-only newline-delimited course markers; never commit this file.",
    )
    args = parser.parse_args()
    result = scan(load_private_denylist(args.private_denylist))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
