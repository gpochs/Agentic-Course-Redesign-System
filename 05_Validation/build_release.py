#!/usr/bin/env python3
"""Build a deterministic public source ZIP, inventory and SHA-256 sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
ARCHIVE_ROOT = "Agentic-Course-Redesign-System"
EXCLUDED_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "dist",
    "venv",
}
EXCLUDED_NAMES = {"package-inventory.json"}
EXCLUDED_SUFFIXES = {".log", ".pyc", ".tmp", ".temp"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def source_files() -> list[Path]:
    paths: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        if path.name in EXCLUDED_NAMES or path.name.startswith("~$"):
            continue
        if path.name.casefold().startswith(".env") or path.suffix.casefold() in EXCLUDED_SUFFIXES:
            continue
        paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix().casefold())


def inventory_bytes(paths: list[Path], version: str) -> bytes:
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
        "bundle_root_name": ARCHIVE_ROOT,
        "version": version,
        "file_count": len(records),
        "files": records,
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def add_bytes(archive: zipfile.ZipFile, data: bytes, arcname: str) -> None:
    info = zipfile.ZipInfo(arcname, date_time=(2026, 8, 20, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o100644 & 0xFFFF) << 16
    archive.writestr(info, data)


def build(version: str) -> dict[str, object]:
    paths = source_files()
    inventory = inventory_bytes(paths, version)
    DIST.mkdir(parents=True, exist_ok=True)
    archive_path = DIST / f"Agentic-Course-Redesign-System_v{version}.zip"
    inventory_path = DIST / "package-inventory.json"
    inventory_path.write_bytes(inventory)
    with zipfile.ZipFile(archive_path, "w") as archive:
        for path in paths:
            rel = path.relative_to(ROOT).as_posix()
            add_bytes(archive, path.read_bytes(), f"{ARCHIVE_ROOT}/{rel}")
        add_bytes(archive, inventory, f"{ARCHIVE_ROOT}/package-inventory.json")
    with zipfile.ZipFile(archive_path) as archive:
        bad_member = archive.testzip()
        member_count = len(archive.namelist())
    archive_hash = sha256(archive_path)
    sidecar = DIST / f"Agentic-Course-Redesign-System_v{version}.sha256.txt"
    sidecar.write_text(f"{archive_hash}  {archive_path.name}\n", encoding="ascii")
    return {
        "schema_version": 1,
        "pass": bad_member is None,
        "archive": archive_path.relative_to(ROOT).as_posix(),
        "archive_bytes": archive_path.stat().st_size,
        "archive_sha256": archive_hash,
        "archive_member_count": member_count,
        "inventory": inventory_path.relative_to(ROOT).as_posix(),
        "inventory_sha256": sha256(inventory_path),
        "sidecar": sidecar.relative_to(ROOT).as_posix(),
        "bad_member": bad_member,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="0.2.1")
    args = parser.parse_args()
    result = build(args.version)
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
