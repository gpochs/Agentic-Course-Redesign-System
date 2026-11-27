#!/usr/bin/env python3
"""Build a deterministic public source ZIP, inventory and SHA-256 sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import re
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
ARCHIVE_ROOT = "Agentic-Course-Redesign-System"
VERSION_PATH = ROOT / "03_Shared_Workflow_Core" / "VERSION"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
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


def current_version() -> str:
    version = VERSION_PATH.read_text(encoding="utf-8").strip()
    if not SEMVER.fullmatch(version):
        raise ValueError(f"invalid current version in {VERSION_PATH}: {version!r}")
    return version


def source_files() -> list[Path]:
    # Package only reviewed paths. A course file beside the checkout is never a release input.
    if (ROOT / ".git").exists():
        records = subprocess.run(
            ["git", "ls-files", "--cached", "-z"], cwd=ROOT, check=True, capture_output=True
        ).stdout.split(b"\0")
        names = [os.fsdecode(record) for record in records if record]
    else:
        inventory = json.loads((ROOT / "package-inventory.json").read_text(encoding="utf-8"))
        names = [record["relative_path"] for record in inventory["files"]]

    paths: list[Path] = []
    for name in names:
        relative = Path(name)
        if relative.is_absolute() or relative.drive or ".." in relative.parts or "\\" in name:
            raise ValueError(f"unsafe source path: {name!r}")
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        path = ROOT / relative
        if path.name in EXCLUDED_NAMES or path.name.startswith("~$"):
            continue
        if path.name.casefold().startswith(".env") or path.suffix.casefold() in EXCLUDED_SUFFIXES:
            continue
        current = ROOT
        for part in relative.parts:
            current = current / part
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError(f"linked source path: {name!r}")
        if not stat.S_ISREG(info.st_mode):
            raise ValueError(f"expected a regular source file: {name!r}")
        paths.append(path)
    return sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix().casefold())


def inventory_bytes(records: list[dict], version: str) -> bytes:
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
    expected_version = current_version()
    if version != expected_version:
        raise ValueError(
            f"release version {version!r} does not match canonical core version {expected_version!r}"
        )
    paths = source_files()
    DIST.mkdir(parents=True, exist_ok=True)
    archive_path = DIST / f"Agentic-Course-Redesign-System_v{version}.zip"
    inventory_path = DIST / "package-inventory.json"
    sidecar = DIST / f"Agentic-Course-Redesign-System_v{version}.sha256.txt"
    with tempfile.TemporaryDirectory(dir=DIST) as temp:
        staging = Path(temp)
        candidate = staging / archive_path.name
        records = []
        with zipfile.ZipFile(candidate, "w") as archive:
            for path in paths:
                name = path.relative_to(ROOT).as_posix()
                data = path.read_bytes()
                records.append({"relative_path": name, "bytes": len(data), "sha256": sha256_bytes(data)})
                add_bytes(archive, data, f"{ARCHIVE_ROOT}/{name}")
            inventory = inventory_bytes(records, version)
            add_bytes(archive, inventory, f"{ARCHIVE_ROOT}/package-inventory.json")
        with zipfile.ZipFile(candidate) as archive:
            bad_member = archive.testzip()
            member_count = len(archive.namelist())
        if bad_member is not None:
            raise ValueError(f"archive integrity check failed for {bad_member}")
        archive_hash = sha256(candidate)
        (staging / inventory_path.name).write_bytes(inventory)
        (staging / sidecar.name).write_text(f"{archive_hash}  {archive_path.name}\n", encoding="ascii")
        for output in (archive_path, inventory_path, sidecar):
            (staging / output.name).replace(output)
    return {
        "schema_version": 1,
        "pass": bad_member is None,
        "release_version": version,
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
    parser.add_argument("--version", default=current_version())
    args = parser.parse_args()
    try:
        result = build(args.version)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
