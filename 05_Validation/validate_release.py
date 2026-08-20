#!/usr/bin/env python3
"""Validate archive paths, inventory, hashes, public scrub and sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath


TEXT_SUFFIXES = {"", ".csv", ".html", ".json", ".jsonc", ".md", ".py", ".svg", ".toml", ".txt", ".yaml", ".yml"}
BAD_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "dist"}
CONTENT_PATTERNS = {
    "windows_user_home": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'<>]+[\\/]"),
    "private_key_block": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_token": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def validate(archive_path: Path, private_denylist: list[str] | None = None) -> dict[str, object]:
    findings: list[dict[str, str]] = []
    denylist = private_denylist or []
    with zipfile.ZipFile(archive_path) as archive:
        bad = archive.testzip()
        if bad:
            findings.append({"path": bad, "kind": "crc_failure"})
        infos = archive.infolist()
        names = [item.filename for item in infos]
        if len(names) != len(set(names)) or len(names) != len({name.casefold() for name in names}):
            findings.append({"path": str(archive_path), "kind": "duplicate_archive_member"})
        roots: set[str] = set()
        for info in infos:
            name = info.filename
            path = PurePosixPath(name)
            if not path.parts:
                findings.append({"path": name, "kind": "empty_member_name"})
                continue
            roots.add(path.parts[0])
            if name.startswith(("/", "\\")) or "\\" in name or ":" in name or ".." in path.parts:
                findings.append({"path": name, "kind": "unsafe_archive_path"})
            if set(path.parts) & BAD_PARTS or path.suffix.casefold() == ".pyc":
                findings.append({"path": name, "kind": "excluded_artifact_in_archive"})
            unix_mode = (info.external_attr >> 16) & 0o170000
            if unix_mode == 0o120000:
                findings.append({"path": name, "kind": "symlink_member"})
            data = archive.read(info)
            if path.suffix.casefold() in TEXT_SUFFIXES:
                decoded = data.decode("utf-8", errors="replace").casefold()
                for marker in denylist:
                    if marker.casefold() in decoded:
                        findings.append({"path": name, "kind": "pilot_specific_content", "detail": marker})
                for kind, pattern in CONTENT_PATTERNS.items():
                    if pattern.search(data):
                        findings.append({"path": name, "kind": kind})
        if roots != {"Agentic-Course-Redesign-System"}:
            findings.append({"path": str(archive_path), "kind": "unexpected_archive_roots", "detail": str(sorted(roots))})
        inventory_name = "Agentic-Course-Redesign-System/package-inventory.json"
        if inventory_name not in names:
            findings.append({"path": inventory_name, "kind": "missing_embedded_inventory"})
        else:
            inventory = json.loads(archive.read(inventory_name).decode("utf-8"))
            records = inventory.get("files", [])
            expected_names = {f"Agentic-Course-Redesign-System/{item['relative_path']}" for item in records}
            actual_names = set(names) - {inventory_name}
            if expected_names != actual_names:
                findings.append({"path": inventory_name, "kind": "inventory_membership_mismatch"})
            for record in records:
                member = f"Agentic-Course-Redesign-System/{record['relative_path']}"
                if member not in names:
                    continue
                data = archive.read(member)
                if len(data) != record.get("bytes") or sha256_bytes(data) != str(record.get("sha256", "")).upper():
                    findings.append({"path": member, "kind": "inventory_hash_or_size_mismatch"})
    sidecar = archive_path.with_suffix(".sha256.txt")
    archive_hash = sha256_bytes(archive_path.read_bytes())
    if not sidecar.is_file():
        findings.append({"path": str(sidecar), "kind": "missing_hash_sidecar"})
    else:
        expected_line = f"{archive_hash}  {archive_path.name}"
        if sidecar.read_text(encoding="ascii").strip() != expected_line:
            findings.append({"path": str(sidecar), "kind": "hash_sidecar_mismatch"})
    return {
        "schema_version": 1,
        "pass": not findings,
        "archive": archive_path.name,
        "archive_sha256": archive_hash,
        "archive_bytes": archive_path.stat().st_size,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--private-denylist",
        type=Path,
        help="Optional local-only newline-delimited course markers; never commit this file.",
    )
    args = parser.parse_args()
    denylist = []
    if args.private_denylist:
        denylist = [
            line.strip()
            for line in args.private_denylist.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
    result = validate(args.archive.resolve(), denylist)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
