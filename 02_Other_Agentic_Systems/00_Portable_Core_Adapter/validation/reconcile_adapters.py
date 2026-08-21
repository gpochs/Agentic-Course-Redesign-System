#!/usr/bin/env python3
"""Preview or apply deterministic v0.2.3 shared-core adapter reconciliation."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
REPOSITORY_ROOT = SCRIPT_PATH.parents[3]
ADAPTERS_ROOT = REPOSITORY_ROOT / "02_Other_Agentic_Systems"
CORE_ROOT = REPOSITORY_ROOT / "03_Shared_Workflow_Core"
VERSION = "0.2.3"
PROPOSAL_ID = "ACR-SYS-20260821-005"

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
    "01_GitHub_Copilot",
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


def refresh_thin_manifest(folder: str, hashes: dict[str, str], apply: bool) -> bool:
    root = ADAPTERS_ROOT / folder
    manifest_path = root / "adapter-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["adapter_version"] = VERSION
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
        {"version": VERSION, "status": "candidate_not_active", "generated_on": "2026-08-21"}
    )
    manifest["provenance"] = {
        "workflow_package_id": "agentic-course-redesign",
        "workflow_proposal_id": PROPOSAL_ID,
        "validated_base_version": VERSION,
        "adapter_release_version": VERSION,
        "workflow_semantics": (
            "reconciled to shared course-independent schema-8 candidate v0.2.3; "
            "candidate remains inactive and adds no permission, external egress, "
            "runtime activation, or schedule registration"
        ),
    }
    manifest["source"] = {
        "package_id": "agentic-course-redesign",
        "proposal_id": PROPOSAL_ID,
        "version": VERSION,
        "validation_date": "2026-08-21",
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
        help="Copy only the declared shared-core mirrors and refresh all adapter manifests.",
    )
    args = parser.parse_args()

    mirror_changes = reconcile_mirrors(args.apply)
    sources = source_entries()
    hashes = {entry["path"]: entry["sha256"] for entry in sources}
    manifest_changes = {
        folder: refresh_thin_manifest(folder, hashes, args.apply)
        for folder in THIN_ADAPTERS
    }
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
