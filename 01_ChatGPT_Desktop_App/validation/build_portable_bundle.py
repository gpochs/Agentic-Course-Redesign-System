#!/usr/bin/env python3
"""Build a deterministic portable workshop ZIP and source-file inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
INVENTORY = DIST / "package-inventory.json"
EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
    "env",
    "venv",
}
EXCLUDED_NAMES = {
    "package-inventory.json",
}
EXCLUDED_REPORT_PREFIXES = ("forward-test-report", "local-", "portable-bundle-validation")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def source_files() -> list[Path]:
    paths = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if (
            path.name in EXCLUDED_NAMES
            or path.name.startswith("~$")
            or (
                relative.parts[0] == "validation"
                and path.suffix.casefold() == ".json"
                and path.name.startswith(EXCLUDED_REPORT_PREFIXES)
            )
            or path.suffix.casefold() in {".log", ".pyc", ".tmp", ".temp"}
        ):
            continue
        paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix().casefold())


def write_inventory(paths: list[Path]) -> None:
    records = [
        {
            "relative_path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in paths
    ]
    payload = {
        "schema_version": 1,
        "bundle_root_name": "Agentic_Course_Redesign",
        "inventory_scope": "all public bundle source files excluding dist, generated local reports, caches, environments, bytecode, temporary files, and this inventory file",
        "file_count": len(records),
        "files": records,
    }
    INVENTORY.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def add_file(archive: zipfile.ZipFile, source: Path, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, date_time=(2026, 8, 20, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o100644 & 0xFFFF) << 16
    archive.writestr(info, source.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.2.1")
    args = parser.parse_args()
    paths = source_files()
    DIST.mkdir(parents=True, exist_ok=True)
    write_inventory(paths)
    archive_path = DIST / f"Agentic_Course_Redesign_v{args.version}.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix().casefold()):
            relative = path.relative_to(ROOT).as_posix()
            add_file(archive, path, f"Agentic_Course_Redesign/{relative}")
        add_file(
            archive,
            INVENTORY,
            "Agentic_Course_Redesign/validation/package-inventory.json",
        )
    with zipfile.ZipFile(archive_path) as archive:
        bad = archive.testzip()
        names = archive.namelist()
    result = {
        "ok": bad is None,
        "archive": archive_path.relative_to(ROOT).as_posix(),
        "archive_sha256": sha256(archive_path),
        "archive_bytes": archive_path.stat().st_size,
        "archive_file_count": len(names),
        "inventory": INVENTORY.relative_to(ROOT).as_posix(),
        "inventory_sha256": sha256(INVENTORY),
        "bad_member": bad,
    }
    hash_path = DIST / f"Agentic_Course_Redesign_v{args.version}.sha256.txt"
    hash_path.write_text(f"{result['archive_sha256']}  {archive_path.name}\n", encoding="ascii")
    result["hash_file"] = hash_path.relative_to(ROOT).as_posix()
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
