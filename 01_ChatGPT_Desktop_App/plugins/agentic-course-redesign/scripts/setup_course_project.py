#!/usr/bin/env python3
"""Preview or install the course-redesign project template without overwrites."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()


def load_eligibility_validator():
    sibling = SCRIPT_PATH.with_name("source_manifest.py")
    spec = importlib.util.spec_from_file_location("_acr_source_manifest", sibling)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load eligibility validator from {sibling}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_eligibility


validate_eligibility = load_eligibility_validator()


def locate_template_root() -> Path:
    candidates: list[Path] = []
    for ancestor in SCRIPT_PATH.parents:
        candidates.extend(
            [
                ancestor / "course-project-template",
                ancestor / "assets" / "project-template",
                ancestor,
            ]
        )
    for candidate in candidates:
        if (candidate / "AGENTS.md").is_file() and (
            candidate / "01_Control" / "state.json"
        ).is_file():
            return candidate
    raise FileNotFoundError(
        "course project template not found in shared-core, plugin-assets or workspace-overlay layout"
    )


TEMPLATE_ROOT = locate_template_root()
CORE_ROOT = TEMPLATE_ROOT.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def target_is_dangerously_broad(path: Path) -> bool:
    resolved = path.resolve(strict=False)
    home = Path.home().resolve(strict=False)
    anchor = Path(resolved.anchor).resolve(strict=False)
    return resolved == anchor or resolved == home or len(resolved.parts) < 4


def template_files() -> list[Path]:
    return sorted(p for p in TEMPLATE_ROOT.rglob("*") if p.is_file())


def build_report(
    target: Path, eligibility_record: Path | None = None
) -> dict[str, object]:
    target = target.expanduser().resolve(strict=False)
    eligibility = {"ok": False, "errors": ["Gate-0A eligibility record not supplied"]}
    if eligibility_record is not None:
        eligibility = validate_eligibility(eligibility_record.expanduser().resolve(strict=False))
    files = template_files()
    planned = []
    conflicts = []
    for source in files:
        relative = source.relative_to(TEMPLATE_ROOT)
        destination = target / relative
        record = {
            "relative_path": relative.as_posix(),
            "destination": str(destination),
            "bytes": source.stat().st_size,
            "sha256": sha256(source),
        }
        planned.append(record)
        if destination.exists() or destination.is_symlink():
            conflicts.append(record)
    existing_entries: list[str] | None = []
    target_contents_inspected = False
    if target.exists() and eligibility["ok"]:
        existing_entries = [str(p.relative_to(target)) for p in target.iterdir()]
        target_contents_inspected = True
    elif target.exists():
        # Do not enumerate arbitrary names in an existing folder before Gate 0A.
        existing_entries = None
    return {
        "mode": "preview",
        "core_root": str(CORE_ROOT),
        "template_root": str(TEMPLATE_ROOT),
        "target": str(target),
        "target_exists": target.exists(),
        "target_contents_inspected": target_contents_inspected,
        "target_existing_top_level_entries": sorted(existing_entries)
        if existing_entries is not None
        else None,
        "gate_0a_eligibility_valid": bool(eligibility["ok"]),
        "gate_0a_eligibility_errors": eligibility["errors"],
        "existing_target_requires_gate_0a_before_content_listing_or_apply": True,
        "planned_file_count": len(planned),
        "planned_files": planned,
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "would_overwrite": bool(conflicts),
    }


def install(
    target: Path,
    allow_nonempty: bool,
    eligibility_record: Path | None = None,
) -> dict[str, object]:
    report = build_report(target, eligibility_record)
    target = Path(str(report["target"]))
    if target_is_dangerously_broad(target):
        raise ValueError(f"Refusing dangerously broad target: {target}")
    if report["conflict_count"]:
        raise FileExistsError("Refusing to overwrite existing template paths")
    if report["target_exists"] and not report["gate_0a_eligibility_valid"]:
        raise PermissionError(
            "Refusing to inspect or add to an existing target before approved Gate 0A; "
            "use a new absent target or provide --eligibility-record"
        )
    if report["target_existing_top_level_entries"] and not allow_nonempty:
        raise FileExistsError(
            "Target is not empty. Rerun only after lecturer approval with --allow-nonempty."
        )
    target.mkdir(parents=True, exist_ok=True)
    installed = []
    for source in template_files():
        relative = source.relative_to(TEMPLATE_ROOT)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"Race-safe overwrite refusal: {destination}")
        shutil.copy2(source, destination)
        if sha256(source) != sha256(destination):
            raise OSError(f"Copy verification failed: {destination}")
        installed.append(relative.as_posix())
    report.update(
        {
            "mode": "apply",
            "installed": True,
            "installed_at_utc": datetime.now(timezone.utc).isoformat(),
            "installed_files": installed,
            "post_install_conflict_count": 0,
        }
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-nonempty", action="store_true")
    parser.add_argument(
        "--eligibility-record",
        type=Path,
        help="approved fingerprinted Gate-0A record required before inspecting or adding to an existing target",
    )
    args = parser.parse_args()
    try:
        report = (
            install(args.target, args.allow_nonempty, args.eligibility_record)
            if args.apply
            else build_report(args.target, args.eligibility_record)
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if not report.get("would_overwrite") else 2
    except Exception as exc:  # fail closed with a machine-readable result
        print(
            json.dumps(
                {
                    "mode": "apply" if args.apply else "preview",
                    "installed": False,
                    "target": os.fspath(args.target),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
