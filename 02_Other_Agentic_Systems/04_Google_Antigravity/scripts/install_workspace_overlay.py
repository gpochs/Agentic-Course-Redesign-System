#!/usr/bin/env python3
"""Preview or copy the Antigravity workspace overlay without overwrites."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path


ADAPTER_ROOT = Path(__file__).resolve().parent.parent
OVERLAY_ROOT = ADAPTER_ROOT / "workspace-overlay"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def overlay_files() -> list[Path]:
    return sorted(
        path
        for path in OVERLAY_ROOT.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix.casefold() not in {".pyc", ".pyo"}
    )


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def target_is_forbidden(path: Path) -> bool:
    resolved = path.expanduser().resolve(strict=False)
    home = Path.home().resolve(strict=False)
    anchor = Path(resolved.anchor).resolve(strict=False)
    adapter = ADAPTER_ROOT.resolve(strict=True)
    return (
        resolved == anchor
        or resolved == home
        or len(resolved.parts) < 4
        or is_relative_to(resolved, adapter)
        or is_relative_to(adapter, resolved)
    )


def build_report(target: Path) -> dict[str, object]:
    target = target.expanduser().resolve(strict=False)
    planned: list[dict[str, object]] = []
    conflicts: list[dict[str, object]] = []
    for source in overlay_files():
        relative = source.relative_to(OVERLAY_ROOT)
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
    existing_entries: list[str] = []
    if target.exists() and target.is_dir():
        existing_entries = sorted(path.name for path in target.iterdir())
    return {
        "mode": "preview",
        "adapter_root": str(ADAPTER_ROOT),
        "overlay_root": str(OVERLAY_ROOT),
        "target": str(target),
        "target_exists": target.exists(),
        "target_is_symlink": target.is_symlink(),
        "target_existing_top_level_entries": existing_entries,
        "planned_file_count": len(planned),
        "planned_files": planned,
        "conflict_count": len(conflicts),
        "conflicts": conflicts,
        "would_overwrite": bool(conflicts),
        "runtime_activation": False,
        "global_configuration_change": False,
    }


def install(target: Path, allow_nonempty: bool) -> dict[str, object]:
    report = build_report(target)
    resolved_target = Path(str(report["target"]))
    if not OVERLAY_ROOT.is_dir():
        raise FileNotFoundError("workspace-overlay is missing")
    if target_is_forbidden(resolved_target):
        raise ValueError(f"refusing broad, source, or nested target: {resolved_target}")
    if report["target_is_symlink"]:
        raise ValueError("refusing a symlink target")
    if resolved_target.exists() and not resolved_target.is_dir():
        raise NotADirectoryError(f"target is not a directory: {resolved_target}")
    if report["conflict_count"]:
        raise FileExistsError("refusing to overwrite existing overlay paths")
    if report["target_existing_top_level_entries"] and not allow_nonempty:
        raise FileExistsError(
            "target is not empty; review it and use --allow-nonempty only for the exact approved target"
        )

    resolved_target.mkdir(parents=True, exist_ok=True)
    installed: list[str] = []
    for source in overlay_files():
        relative = source.relative_to(OVERLAY_ROOT)
        destination = resolved_target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f"race-safe overwrite refusal: {destination}")
        shutil.copy2(source, destination)
        if sha256(source) != sha256(destination):
            raise OSError(f"copy verification failed: {destination}")
        installed.append(relative.as_posix())

    report.update(
        {
            "mode": "apply",
            "installed": True,
            "installed_at_utc": datetime.now(timezone.utc).isoformat(),
            "installed_files": installed,
            "verified_copy_count": len(installed),
            "runtime_activation": False,
            "global_configuration_change": False,
        }
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--allow-nonempty", action="store_true")
    args = parser.parse_args()
    try:
        report = (
            install(args.target, args.allow_nonempty)
            if args.apply
            else build_report(args.target)
        )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if not report.get("would_overwrite") else 2
    except Exception as exc:
        print(
            json.dumps(
                {
                    "mode": "apply" if args.apply else "preview",
                    "installed": False,
                    "target": os.fspath(args.target),
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "runtime_activation": False,
                    "global_configuration_change": False,
                },
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
