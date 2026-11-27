#!/usr/bin/env python3
"""Preview or apply deterministic v0.3.3 non-Copilot adapter reconciliation."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tomllib
import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPOSITORY_ROOT = SCRIPT_PATH.parents[3]
ADAPTERS_ROOT = REPOSITORY_ROOT / "02_Other_Agentic_Systems"
CORE_ROOT = REPOSITORY_ROOT / "03_Shared_Workflow_Core"
VERSION = "0.3.3"
PROPOSAL_ID = "ACR-SYS-20261127-004"

SOURCE_RELATIVES = (
    "VERSION",
    "adapter-contract.json",
    "course-project-template/AGENTS.md",
    "course-project-template/01_Control/GATES.md",
    "course-project-template/01_Control/material-processing-eligibility.template.json",
    "course-project-template/01_Control/state.json",
    "agent-skills/course-redesign-assessment/SKILL.md",
    "agent-skills/course-redesign-materials/SKILL.md",
    "agent-skills/course-redesign-orchestrator/SKILL.md",
    "agent-skills/course-redesign-research/SKILL.md",
    "agent-skills/course-redesign-setup/SKILL.md",
    "agent-skills/course-redesign-system/SKILL.md",
    "scripts/create_material_processing_eligibility.py",
)

ANTIGRAVITY_MIRRORS = {
    "course-project-template/AGENTS.md": "workspace-overlay/AGENTS.md",
    "course-project-template/00_NOT_ACTIVE_UNTIL_VALIDATED.txt": (
        "workspace-overlay/00_NOT_ACTIVE_UNTIL_VALIDATED.txt"
    ),
    "course-project-template/00_Source_Materials/README.txt": (
        "workspace-overlay/00_Source_Materials/README.txt"
    ),
    "course-project-template/01_Control/GATES.md": (
        "workspace-overlay/01_Control/GATES.md"
    ),
    "course-project-template/01_Control/README.md": (
        "workspace-overlay/01_Control/README.md"
    ),
    "course-project-template/01_Control/material-processing-eligibility.template.json": (
        "workspace-overlay/01_Control/material-processing-eligibility.template.json"
    ),
    "course-project-template/01_Control/run-contract.template.json": (
        "workspace-overlay/01_Control/run-contract.template.json"
    ),
    "course-project-template/01_Control/source-access-policy.template.json": (
        "workspace-overlay/01_Control/source-access-policy.template.json"
    ),
    "course-project-template/01_Control/state.json": (
        "workspace-overlay/01_Control/state.json"
    ),
    "agent-skills/course-redesign-assessment/SKILL.md": (
        "workspace-overlay/.agents/skills/course-redesign-assessment/SKILL.md"
    ),
    "agent-skills/course-redesign-materials/SKILL.md": (
        "workspace-overlay/.agents/skills/course-redesign-materials/SKILL.md"
    ),
    "agent-skills/course-redesign-research/SKILL.md": (
        "workspace-overlay/.agents/skills/course-redesign-research/SKILL.md"
    ),
    "scripts/fingerprint_file.py": (
        "workspace-overlay/.agents/skills/course-redesign-setup/scripts/fingerprint_file.py"
    ),
    "scripts/create_material_processing_eligibility.py": (
        "workspace-overlay/.agents/skills/course-redesign-setup/scripts/"
        "create_material_processing_eligibility.py"
    ),
    "scripts/source_manifest.py": (
        "workspace-overlay/.agents/skills/course-redesign-setup/scripts/source_manifest.py"
    ),
    "scripts/validate_state.py": (
        "workspace-overlay/.agents/skills/course-redesign-setup/scripts/validate_state.py"
    ),
    "scripts/migrate_state_v6_to_v7.py": (
        "workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v6_to_v7.py"
    ),
    "scripts/migrate_state_v7_to_v8.py": (
        "workspace-overlay/.agents/skills/course-redesign-setup/scripts/migrate_state_v7_to_v8.py"
    ),
}

THIN_ADAPTERS = (
    "00_Portable_Core_Adapter",
    "02_Claude_Code",
    "03_OpenCode",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_inside(path: Path, root: Path) -> None:
    resolved = path.resolve()
    root_resolved = root.resolve()
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise ValueError(f"path leaves controlled adapter root: {path}")


def inventory(root: Path, manifest_path: Path) -> list[dict[str, object]]:
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
        and path != manifest_path
        and "__pycache__" not in path.parts
        and path.suffix.casefold() not in {".pyc", ".pyo"}
    ]


def source_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for relative in SOURCE_RELATIVES:
        path = CORE_ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(f"missing canonical source: {relative}")
        entries.append(
            {"path": relative, "sha256": sha256(path), "bytes": path.stat().st_size}
        )
    return entries


def source_hashes() -> dict[str, str]:
    return {entry["path"]: entry["sha256"] for entry in source_entries()}


def reconcile_mirrors(apply: bool) -> list[str]:
    antigravity = ADAPTERS_ROOT / "04_Google_Antigravity"
    changed: list[str] = []
    for source_relative, target_relative in ANTIGRAVITY_MIRRORS.items():
        source = CORE_ROOT / source_relative
        target = antigravity / target_relative
        if not source.is_file():
            raise FileNotFoundError(f"missing canonical mirror source: {source_relative}")
        assert_inside(target, antigravity)
        if not target.is_file() or source.read_bytes() != target.read_bytes():
            changed.append(target_relative)
            if apply:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
    return changed


def reconcile_roles_and_copilot(apply: bool) -> list[str]:
    copilot = ADAPTERS_ROOT / "01_GitHub_Copilot"
    plugin = copilot / "plugin/agentic-course-redesign"
    spec = importlib.util.spec_from_file_location("copilot_contract", copilot / "validation/validate_native_plugin.py")
    contract = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contract)
    build_spec = importlib.util.spec_from_file_location("host_builder", ADAPTERS_ROOT / "build_host_package.py")
    builder = importlib.util.module_from_spec(build_spec)
    build_spec.loader.exec_module(builder)
    changed = []
    def emit(path, data):
        if isinstance(data, str):
            data = (data.rstrip() + "\n").encode()
        if not path.is_file() or path.read_bytes() != data:
            changed.append(path.relative_to(ADAPTERS_ROOT).as_posix())
            if apply:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    overrides = "\n\n".join((contract.COPILOT_CHOICE_CAPACITY_OVERRIDE, contract.COPILOT_RUNTIME_COMPATIBILITY_OVERRIDE))
    def host_role_guide(edition, skill_root, source_bytes):
        native = edition / "native-intake.md"
        if not native.is_file():
            return source_bytes
        emit(skill_root / builder.NATIVE_GUIDE, builder.read_reviewed(native))
        return builder.link_native_intake(source_bytes)

    emit(plugin / "assets/PARTICIPANT_QUICK_START.md", (CORE_ROOT / "PARTICIPANT_QUICK_START.md").read_bytes())
    # Older manual overlays have host-specific stage instructions. Expose the
    # same staged intake there as in the standalone native packages.
    skills = CORE_ROOT / "agent-skills"
    brief = (skills / "course-redesign-orchestrator/SKILL.md").read_text(encoding="utf-8")
    context = brief[brief.index("Build the brief progressively."):brief.index("Pass the confirmed context")].strip()
    teaching_steps = brief[brief.index("## How to talk with the teacher"):brief.index("## Invariants")].strip()
    confirmations = brief[brief.index("### Plain-language confirmations"):brief.index("## Lecturer Decision Dialogue Contract")].strip()
    opener = brief[brief.index("### Step 1 "):brief.index("The latest stated way of working")].strip()
    portable = ADAPTERS_ROOT / "00_Portable_Core_Adapter/overlay/.claude/skills/course-redesign"
    antigravity = ADAPTERS_ROOT / "04_Google_Antigravity/workspace-overlay/.agents/skills"
    for path in (portable / "references/workflow.md", antigravity / "course-redesign-orchestrator/SKILL.md"):
        text = path.read_text(encoding="utf-8")
        marker = "<!-- teaching conversation -->"
        end = "<!-- end teaching conversation -->"
        detail = "\n\n".join((marker, teaching_steps, opener, confirmations, end))
        if marker in text:
            before, existing = text.split(marker, 1)
            text = before + detail + existing.split(end, 1)[1]
        else:
            title = text.index("\n", text.index("\n# ") + 1) if "\n# " in text else text.index("\n")
            text = text[:title] + "\n\n" + detail + text[title:]
        gate = text.index("Gate 1: course brief and run contract")
        insert = text.index("\n#", gate)
        prefix = text[:insert].split("\nBuild the brief progressively.")[0].rstrip()
        emit(path, prefix + "\n\n" + context + "\n" + text[insert:])
    for folder, dest in (("agent-skills", "skills"), ("scripts", "scripts"), ("course-project-template", "assets/project-template")):
        for source in builder.selected_files(CORE_ROOT / folder):
            rel = source.relative_to(CORE_ROOT / folder)
            target = plugin / dest / rel
            extra = None
            if source.name == "SKILL.md" or rel.as_posix() == "AGENTS.md":
                extra = overrides
            elif rel.as_posix() == "01_Control/GATES.md":
                extra = contract.COPILOT_CHOICE_CAPACITY_OVERRIDE
            data = builder.read_reviewed(source)
            if extra is not None:
                data = data.decode("utf-8").replace("\r\n", "\n").rstrip() + "\n\n" + extra
            if folder == "agent-skills" and rel == builder.ROLE_GUIDE:
                data = host_role_guide(copilot, plugin / "skills", data)
            emit(target, data)
            if folder == "agent-skills" and source.name != "SKILL.md":
                overlay_data = source.read_bytes()
                if rel == builder.ROLE_GUIDE:
                    overlay_data = host_role_guide(ADAPTERS_ROOT / "04_Google_Antigravity", antigravity, overlay_data)
                emit(antigravity / rel, overlay_data)
            elif folder == "agent-skills" and source.name == "SKILL.md":
                # Manual Antigravity skills retain their native instructions while
                # the picker uses the same teacher-facing names as the other hosts.
                overlay_skill = antigravity / rel
                live = overlay_skill.read_text(encoding="utf-8")
                old_desc = next(line for line in live.splitlines() if line.startswith("description: "))
                new_desc = next(line for line in source.read_text(encoding="utf-8").splitlines() if line.startswith("description: "))
                if old_desc != new_desc:
                    emit(overlay_skill, live.replace(old_desc, new_desc, 1))
    roles = REPOSITORY_ROOT / "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/assets/project-template/.codex/agents"
    for source in roles.glob("*.toml"):
        role = tomllib.loads(source.read_text(encoding="utf-8"))
        body = role["developer_instructions"].strip()
        for path in (ADAPTERS_ROOT / "02_Claude_Code/overlay/.claude/agents" / (source.stem + ".md"),
                     ADAPTERS_ROOT / "03_OpenCode/overlay/.opencode/agents" / (source.stem + ".md"),
                     ADAPTERS_ROOT / "04_Google_Antigravity/workspace-overlay/.agents/agents" / (source.stem + ".md"),
                     copilot / "overlay/.github/agents" / (source.stem + ".agent.md")):
            prefix = path.read_text(encoding="utf-8").split("\n## Specialist method\n")[0].rstrip()
            marker = "A role instruction does not provide an isolated sandbox."
            method = body.partition(marker)[2].strip()
            if not method:
                raise ValueError(f"Missing specialist method for {source.name}")
            emit(path, prefix + "\n\n## Specialist method\n\n" + method)
        target = plugin / "agents" / (source.stem + ".agent.md")
        header = target.read_text(encoding="utf-8").split("\n---\n", 1)[0]
        if source.stem in contract.COPILOT_AGENT_BODY_REPLACEMENTS:
            old, new = contract.COPILOT_AGENT_BODY_REPLACEMENTS[source.stem]
            body = body.replace(old, new)
        emit(target, header + "\n---\n\n" + body + "\n\n\n" + contract.COPILOT_AGENT_DIALOGUE_SUFFIX)
    return changed


def refresh_thin_manifest(folder: str, hashes: dict[str, str], apply: bool) -> bool:
    root = ADAPTERS_ROOT / folder
    manifest_path = root / "adapter-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_version"] = VERSION
    manifest["status"] = "candidate_not_active"
    manifest["compose_after"] = [] if folder == "00_Portable_Core_Adapter" else [
        f"portable-core@{VERSION}"
    ]
    manifest["source_provenance"] = {
        "system_id": PROPOSAL_ID,
        "version": VERSION,
        "source_status": "approved inactive candidate; not activated",
        "origin_label": "03_Shared_Workflow_Core",
        "hash_algorithm": "sha256",
        "hashes": hashes,
    }
    if folder == "01_GitHub_Copilot":
        manifest["native_plugin"].update(proposal_id=PROPOSAL_ID, package_version=VERSION,
            base_semantic_version=VERSION, rollback_package_version="0.3.2")
    manifest["files"] = inventory(root, manifest_path)
    overlay = root / "overlay"
    manifest["overlay_files"] = sorted(
        path.relative_to(overlay).as_posix()
        for path in overlay.rglob("*")
        if path.is_file()
    )
    candidate = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    changed = candidate != manifest_path.read_text(encoding="utf-8")
    if apply and changed:
        manifest_path.write_text(candidate, encoding="utf-8", newline="\n")
    return changed


def refresh_antigravity_manifest(
    sources: list[dict[str, object]], apply: bool
) -> bool:
    root = ADAPTERS_ROOT / "04_Google_Antigravity"
    manifest_path = root / "adapter-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_version"] = VERSION
    manifest["status"] = "candidate_not_active"
    manifest["adapter"].update(
        {"version": VERSION, "status": "candidate_not_active", "generated_on": "2026-11-27"}
    )
    manifest["provenance"] = {
        "workflow_package_id": "agentic-course-redesign",
        "workflow_proposal_id": PROPOSAL_ID,
        "validated_base_version": VERSION,
        "adapter_release_version": VERSION,
        "workflow_semantics": (
            "reconciled to shared course-independent schema-8 candidate v0.3.3; "
            "adds adaptive one-decision lecturer interaction and deterministic "
            "preview-first Gate-0A eligibility generation; "
            "candidate remains inactive and adds no permission, external egress, "
            "runtime activation, or schedule registration"
        ),
    }
    manifest["source"] = {
        "package_id": "agentic-course-redesign",
        "proposal_id": PROPOSAL_ID,
        "version": VERSION,
        "validation_date": "2026-11-27",
        "status": "approved inactive candidate; not activated",
        "source_root_recorded": False,
        "source_root_note": (
            "Canonical source is repository-relative 03_Shared_Workflow_Core; "
            "no local absolute path is recorded."
        ),
        "hash_algorithm": "SHA-256",
    }
    manifest["source_file_count"] = len(sources)
    manifest["source_files"] = sources
    generated = inventory(root, manifest_path)
    manifest["generated_file_count"] = len(generated)
    manifest["generated_files"] = generated
    manifest["integrity_exclusions"] = ["adapter-manifest.json"]
    candidate = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    changed = candidate != manifest_path.read_text(encoding="utf-8")
    if apply and changed:
        manifest_path.write_text(candidate, encoding="utf-8", newline="\n")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help=(
            "Copy only declared Antigravity shared-core mirrors and refresh the "
            "portable, Claude Code, OpenCode, and Antigravity manifests."
        ),
    )
    args = parser.parse_args()

    mirror_changes = reconcile_mirrors(args.apply) + reconcile_roles_and_copilot(args.apply)
    sources = source_entries()
    hashes = {entry["path"]: entry["sha256"] for entry in sources}
    manifest_changes = {
        folder: refresh_thin_manifest(folder, hashes, args.apply)
        for folder in THIN_ADAPTERS
    }
    manifest_changes["01_GitHub_Copilot"] = refresh_thin_manifest("01_GitHub_Copilot", hashes, args.apply)
    manifest_changes["04_Google_Antigravity"] = refresh_antigravity_manifest(
        sources, args.apply
    )
    print(
        json.dumps(
            {
                "mode": "apply" if args.apply else "preview",
                "would_write": bool(args.apply),
                "mirror_changes": mirror_changes,
                "manifest_changes": manifest_changes,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
