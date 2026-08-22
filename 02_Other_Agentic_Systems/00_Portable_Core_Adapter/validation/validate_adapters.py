#!/usr/bin/env python3
"""Static validation for portable, Claude Code, and OpenCode adapter templates."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
ADAPTERS = {
    "00_Portable_Core_Adapter": None,
    "02_Claude_Code": ".claude/agents",
    "03_OpenCode": ".opencode/agents",
}
PLATFORMS = {
    "00_Portable_Core_Adapter": "portable",
    "02_Claude_Code": "claude-code",
    "03_OpenCode": "opencode-v2",
}
ROLES = {
    "active-learning-researcher",
    "ai-integration-researcher",
    "artefact-accessibility-visual-qa",
    "assessment-alignment-designer",
    "course-mapper",
    "evidence-feasibility-red-team",
    "learning-designer",
    "learning-material-designer",
    "source-verification-citation-auditor",
    "student-experience-critic",
}
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SOURCE_PATHS = {
    "VERSION": "VERSION",
    "adapter-contract.json": "adapter-contract.json",
    "course-project-template/AGENTS.md": "course-project-template/AGENTS.md",
    "course-project-template/01_Control/GATES.md": (
        "course-project-template/01_Control/GATES.md"
    ),
    "course-project-template/01_Control/material-processing-eligibility.template.json": (
        "course-project-template/01_Control/material-processing-eligibility.template.json"
    ),
    "course-project-template/01_Control/state.json": (
        "course-project-template/01_Control/state.json"
    ),
    "scripts/create_material_processing_eligibility.py": (
        "scripts/create_material_processing_eligibility.py"
    ),
    **{
        f"agent-skills/{name}/SKILL.md": f"agent-skills/{name}/SKILL.md"
        for name in (
            "course-redesign-assessment",
            "course-redesign-materials",
            "course-redesign-orchestrator",
            "course-redesign-research",
            "course-redesign-setup",
            "course-redesign-system",
        )
    },
}
EXPECTED_GATE_ORDER = [
    "gate_0a",
    "gate_0",
    "gate_1",
    "hitl_1_gate_2a",
    "hitl_2_gate_2b",
    "gate_3",
    "named_artefact_gates",
    "production_declaration",
    "production_handoff_approval_and_verification",
    "hitl_3",
    "mandatory_system_improvement_review_offer_and_explicit_response",
    "terminal_complete_dormant_closeout_and_trigger_guidance",
    "optional_system_gate",
    "optional_separate_activation",
    "optional_separate_expiring_schedule",
]


def frontmatter(text: str) -> tuple[set[str], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as exc:
        raise ValueError("missing closing frontmatter delimiter") from exc
    keys = set()
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):", line)
        if match:
            keys.add(match.group(1))
    return keys, "\n".join(lines[end + 1 :])


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(source: Path | None = None) -> list[str]:
    errors: list[str] = []
    contract_path = ROOT.parent / "03_Shared_Workflow_Core" / "adapter-contract.json"
    try:
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(errors, f"shared adapter contract is invalid: {exc}")
    else:
        if contract.get("gate_order") != EXPECTED_GATE_ORDER:
            fail(errors, "shared adapter contract gate order is incomplete or reordered")
        if contract.get("core_version") != "0.2.4":
            fail(errors, "shared adapter contract core_version must be 0.2.4")
        if contract.get("state_schema_version") != 8:
            fail(errors, "shared adapter contract state_schema_version must be 8")
        routing = contract.get("umbrella_entry_routing", {})
        if (
            routing.get("initial_gate")
            != "GATE_0A_AWAITING_MATERIAL_ENVIRONMENT_ELIGIBILITY"
            or routing.get(
                "gate_0a_required_before_any_course_source_path_filename_list_read_copy_hash_or_intake"
            )
            is not True
        ):
            fail(errors, "shared adapter contract must hard-stop at pre-source Gate 0A")
        eligibility = contract.get("pre_source_processing_eligibility", {})
        if (
            eligibility.get("fingerprinted") is not True
            or eligibility.get("public_availability_alone_is_insufficient") is not True
            or eligibility.get("mixed_or_uncertain")
            != "fail_closed_until_segregated_or_clarified"
        ):
            fail(errors, "shared adapter contract weakens processing eligibility")
        closeout = contract.get("course_run_closeout", {})
        if (
            closeout.get("silence_means_waiting") is not True
            or closeout.get("terminal_status") != "complete_dormant"
            or closeout.get("never_resume_terminal_run") is not True
            or closeout.get("manual_or_scheduled_trigger_creates_fresh_run_and_lineage")
            is not True
        ):
            fail(errors, "shared adapter contract weakens terminal dormant closeout")

    for folder, agent_dir in ADAPTERS.items():
        base = ROOT / folder
        for required in ("README.md", "CAPABILITIES.md", "adapter-manifest.json", "overlay"):
            if not (base / required).exists():
                fail(errors, f"{folder}: missing {required}")
        manifest_path = base / "adapter-manifest.json"
        if not manifest_path.is_file():
            continue
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            fail(errors, f"{folder}: invalid manifest: {exc}")
            continue
        if manifest.get("adapter_version") != "0.2.4":
            fail(errors, f"{folder}: adapter_version must be 0.2.4")
        if manifest.get("platform") != PLATFORMS[folder]:
            fail(errors, f"{folder}: incorrect or missing normalized platform")
        if manifest.get("status") != "candidate_not_active":
            fail(errors, f"{folder}: status must be candidate_not_active")
        if manifest.get("overlay_root") != "overlay":
            fail(errors, f"{folder}: overlay_root must be overlay")
        expected_compose = [] if folder == "00_Portable_Core_Adapter" else ["portable-core@0.2.4"]
        if manifest.get("compose_after") != expected_compose:
            fail(errors, f"{folder}: compose_after is not aligned to portable core 0.2.4")
        provenance = manifest.get("source_provenance", {})
        if provenance.get("system_id") != "ACR-SYS-20260822-007":
            fail(errors, f"{folder}: source proposal ID must be ACR-SYS-20260822-007")
        if provenance.get("version") != "0.2.4":
            fail(errors, f"{folder}: shared semantic source version must be 0.2.4")
        hashes = provenance.get("hashes", {})
        if not hashes or any(
            not isinstance(value, str) or not SHA256.fullmatch(value)
            for value in hashes.values()
        ):
            fail(errors, f"{folder}: missing or invalid source SHA-256 values")
        if source is not None:
            for label, expected in hashes.items():
                relative = SOURCE_PATHS.get(label)
                if relative is None:
                    fail(errors, f"{folder}: no verification mapping for source {label}")
                    continue
                source_file = source / relative
                if not source_file.is_file():
                    fail(errors, f"{folder}: missing canonical source {relative}")
                elif file_sha256(source_file) != expected:
                    fail(errors, f"{folder}: source hash mismatch for {label}")
        inventory_meta = manifest.get("file_inventory", {})
        if inventory_meta != {
            "base": "adapter_root",
            "hash_algorithm": "sha256",
            "manifest_self_excluded": True,
            "excluded_paths": ["adapter-manifest.json"],
        }:
            fail(errors, f"{folder}: file_inventory must document exact manifest self-exclusion")
        actual_adapter_files = {
            path.relative_to(base).as_posix(): path
            for path in base.rglob("*")
            if path.is_file()
            and path != manifest_path
            and "__pycache__" not in path.parts
            and path.suffix.casefold() not in {".pyc", ".pyo"}
        }
        file_entries = manifest.get("files")
        declared_adapter_files: dict[str, dict[str, object]] = {}
        if not isinstance(file_entries, list):
            fail(errors, f"{folder}: files must be an array")
            file_entries = []
        for entry in file_entries:
            if not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256"}:
                fail(errors, f"{folder}: malformed files entry")
                continue
            relative = entry.get("path")
            if not isinstance(relative, str):
                fail(errors, f"{folder}: files entry path must be a string")
                continue
            normalized = PurePosixPath(relative)
            if (
                not relative
                or "\\" in relative
                or normalized.is_absolute()
                or ".." in normalized.parts
                or normalized.as_posix() != relative
            ):
                fail(errors, f"{folder}: non-normalized files path {relative!r}")
                continue
            if relative == "adapter-manifest.json":
                fail(errors, f"{folder}: manifest must be self-excluded from files")
            if relative in declared_adapter_files:
                fail(errors, f"{folder}: duplicate files entry for {relative}")
                continue
            declared_adapter_files[relative] = entry
        if set(declared_adapter_files) != set(actual_adapter_files):
            fail(errors, f"{folder}: files array differs from all non-manifest adapter files")
        for relative in set(declared_adapter_files) & set(actual_adapter_files):
            entry = declared_adapter_files[relative]
            actual_file = actual_adapter_files[relative]
            if entry.get("bytes") != actual_file.stat().st_size:
                fail(errors, f"{folder}: byte count mismatch for {relative}")
            expected_hash = entry.get("sha256")
            if not isinstance(expected_hash, str) or not SHA256.fullmatch(expected_hash):
                fail(errors, f"{folder}: invalid file SHA-256 for {relative}")
            elif file_sha256(actual_file) != expected_hash:
                fail(errors, f"{folder}: file hash mismatch for {relative}")
        overlay = base / "overlay"
        actual = sorted(
            path.relative_to(overlay).as_posix()
            for path in overlay.rglob("*")
            if path.is_file()
        )
        declared = sorted(manifest.get("overlay_files", []))
        if actual != declared:
            fail(errors, f"{folder}: overlay inventory differs from manifest")
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".md", ".json", ".py"}:
                if path.resolve() == Path(__file__).resolve():
                    continue
                text = path.read_text(encoding="utf-8")
                if re.search(r"[A-Za-z]:\\", text):
                    fail(errors, f"{folder}: absolute Windows path in {path.relative_to(base)}")
        if agent_dir:
            native = overlay / agent_dir
            suffix = ".agent.md" if folder == "01_GitHub_Copilot" else ".md"
            found = {
                path.name[: -len(suffix)]
                for path in native.glob(f"*{suffix}")
                if path.is_file()
            }
            if found != ROLES:
                fail(errors, f"{folder}: native role set differs from canonical ten roles")
            for path in native.glob(f"*{suffix}"):
                text = path.read_text(encoding="utf-8")
                try:
                    keys, body = frontmatter(text)
                except ValueError as exc:
                    fail(errors, f"{folder}: {path.name}: {exc}")
                    continue
                if "description" not in keys:
                    fail(errors, f"{folder}: {path.name}: missing description")
                if "role-contracts.md" not in body or "control-contract.md" not in body:
                    fail(errors, f"{folder}: {path.name}: not a thin core wrapper")
                if "ESCALATE_TO_ORCHESTRATOR:" not in body:
                    fail(errors, f"{folder}: {path.name}: missing fail-closed escalation")
                expected_role = path.name[: -len(suffix)].replace("-", "_")
                if f"`{expected_role}`" not in body:
                    fail(errors, f"{folder}: {path.name}: role ID does not match file ID")
                if folder == "02_Claude_Code":
                    if "tools: Read, Glob, Grep" not in text:
                        fail(errors, f"{folder}: {path.name}: unsafe or missing tool allowlist")
                elif folder == "03_OpenCode":
                    for token in ("mode: subagent", "action: \"*\"", "effect: deny"):
                        if token not in text:
                            fail(errors, f"{folder}: {path.name}: missing {token}")
                    actions = set(re.findall(r"^\s*- action: \"?([^\"\n]+)\"?\s*$", text, re.MULTILINE))
                    if actions != {"*", "read", "glob", "grep", "skill"}:
                        fail(errors, f"{folder}: {path.name}: unexpected permission action set")
    skill_path = ROOT / "00_Portable_Core_Adapter/overlay/.claude/skills/course-redesign/SKILL.md"
    if skill_path.is_file():
        try:
            skill_text = skill_path.read_text(encoding="utf-8")
            keys, body = frontmatter(skill_text)
            if keys != {"name", "description"}:
                fail(errors, "portable skill frontmatter must contain only name and description")
            name_match = re.search(r"^name:\s*(\S+)\s*$", skill_text, re.MULTILINE)
            description_match = re.search(r"^description:\s*(.+)\s*$", skill_text, re.MULTILINE)
            if not name_match or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name_match.group(1)):
                fail(errors, "portable skill name is not lowercase kebab-case")
            elif name_match.group(1) != skill_path.parent.name or len(name_match.group(1)) > 64:
                fail(errors, "portable skill name must match its directory and be at most 64 characters")
            if not description_match or not 1 <= len(description_match.group(1)) <= 1024:
                fail(errors, "portable skill description must contain 1-1024 characters")
            elif any(character in description_match.group(1) for character in "<>"):
                fail(errors, "portable skill description may not contain angle brackets")
            if not body.strip():
                fail(errors, "portable skill body is empty")
        except ValueError as exc:
            fail(errors, f"portable skill: {exc}")
    workflow_path = (
        ROOT
        / "00_Portable_Core_Adapter/overlay/.claude/skills/course-redesign/references/workflow.md"
    )
    if workflow_path.is_file():
        workflow_text = workflow_path.read_text(encoding="utf-8")
        workflow_text_normalized = " ".join(workflow_text.split())
        for required in (
            "## Gate 0A: pre-source processing eligibility",
            "public availability, classroom use, or a link alone is insufficient",
            "Institution-internal or restricted material is route-only",
            "Mixed or uncertain material is blocked",
            "canonical SHA-256 fingerprint",
            "## Gate 0: source access and integrity",
            "DECLARE PRODUCTION COMPLETE",
            "APPROVE PRODUCTION HANDOFF",
            "reopen it and verify",
            "Do not enter HITL 3 until this saved handoff verification passes",
            "## HITL 3: final lecturer acceptance",
            "all editable deliverables and representative previews",
            "known limitations and rights boundaries",
            "final quality-assurance evidence",
            "accept the package, conditionally accept it with named revisions",
            "Would you like a separate, read-only system-improvement review",
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
            "followed only by a versioned proposal",
            "A yes authorises only that review and proposal",
            "does not authorise system-file changes, installation, publication or release, runtime activation, schedule registration or modification, an immediate run",
            "added MCP server, connector, authentication, permission or external egress",
            "persist the offer record",
            "complete question exactly once",
            "offered_awaiting_response",
            "wait silently",
            "terminal `complete_dormant`",
            "clears `active_run_id`",
            "informational trigger guidance",
            "The offer creates or registers no task, automation, schedule, hook, connector, permission, or immediate run",
            "Never continue the dormant run",
            "idempotency key",
            "APPROVE SYSTEM FILES",
            "status=candidate_not_active",
            "one lecturer reply containing exactly and only these three completed lines",
            "APPROVE SCHEDULES",
            "Schedule contract: <exact contract ID and version>",
            "Expires: <exact local date and time with IANA timezone>",
            "Registration never triggers an immediate run",
            "A later scheduled trigger creates a fresh run",
            "## Lecturer interaction contract",
            "exactly one unresolved decision",
            "live host tool can show the complete",
            "mutually exclusive option set plus a custom-answer path",
            "capacity is unknown",
            "complete set exceeds its capacity",
            "listing every valid numbered option plus `Other - type your answer`",
            "Never prune, hide or combine valid choices",
            "Every valid option remains visible",
            "every valid option visible",
            "split, merge, reorder, or rename clusters",
            "safest truthful, evidence-aligned, reversible",
            "never preselected",
            "Preserve custom answers verbatim",
            "Blank, skipped, partial, or ambiguous answers do not",
            "Before every gate, recap",
            "Specialist roles are evidence lenses",
            "an outcome change requires rechecking assessment evidence",
            "a student-experience or accessibility concern",
            "scripts/create_material_processing_eligibility.py",
            "generic host fallback",
            "Never overwrite an eligibility record",
            "Never continue the dormant run",
        ):
            if required not in workflow_text_normalized:
                fail(errors, f"portable workflow omits workflow-completeness control: {required}")
        ordered_markers = (
            "## Gate 0A: pre-source processing eligibility",
            "## Gate 0: source access and integrity",
            "## Gate 1: course brief and run contract",
            "## Stage A and Gate 2A",
            "## Stage B and Gate 2B",
            "## Blueprint and Gate 3",
            "## Gated production and QA",
            "DECLARE PRODUCTION COMPLETE",
            "APPROVE PRODUCTION HANDOFF",
            "Do not enter HITL 3 until this saved handoff verification passes",
            "## HITL 3: final lecturer acceptance",
            "Would you like a separate, read-only system-improvement review",
            "## Separate reusable-system lifecycle",
        )
        positions = [workflow_text_normalized.find(marker) for marker in ordered_markers]
        if -1 not in positions and positions != sorted(positions):
            fail(errors, "portable workflow completeness controls are reordered")
    opencode_overlay = ROOT / "03_OpenCode/overlay"
    if opencode_overlay.exists():
        executable = [
            path for path in opencode_overlay.rglob("*")
            if path.is_file() and path.suffix.lower() in {".js", ".mjs", ".cjs", ".ts"}
        ]
        if executable:
            fail(errors, "OpenCode overlay contains an executable plugin or script")
    return errors


if __name__ == "__main__":
    source_arg = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else None
    if len(sys.argv) > 2:
        print("usage: validate_adapters.py [canonical-source-root]")
        sys.exit(2)
    problems = validate(source_arg)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}")
        sys.exit(1)
    source_note = "; all declared source hashes match" if source_arg else ""
    non_manifest_count = sum(
        1
        for folder in ADAPTERS
        for path in (ROOT / folder).rglob("*")
        if path.is_file()
        and path.name != "adapter-manifest.json"
        and "__pycache__" not in path.parts
        and path.suffix.casefold() not in {".pyc", ".pyo"}
    )
    overlay_count = sum(
        1
        for folder in ADAPTERS
        for path in (ROOT / folder / "overlay").rglob("*")
        if path.is_file()
    )
    print(
        f"PASS: 3 release-0.2.4 adapters, {non_manifest_count} frozen non-manifest "
        f"files, {overlay_count} overlay files, and 20 native role wrappers are "
        "project-local, fail-closed, and "
        f"hash-consistent{source_note}"
    )
