#!/usr/bin/env python3
"""Build a deterministic, single-root OpenAI skills-only plugin archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "openai-submission" / "source" / "agentic-course-redesign"
DEFAULT_OUTPUT = ROOT / "dist"
sys.path.insert(0, str(ROOT / "validation"))
from release_inputs import verified_public_payload

ARCHIVE_ROOT = "agentic-course-redesign"
FIXED_TIMESTAMP = (2026, 8, 20, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def add_file(archive: zipfile.ZipFile, relative: str, content: bytes) -> None:
    info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o100644 & 0xFFFF) << 16
    archive.writestr(info, content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    payload = verified_public_payload(SOURCE)
    manifest = json.loads(payload[".codex-plugin/plugin.json"])
    version = manifest["version"]
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    archive_path = output_dir / f"agentic-course-redesign-openai-skills-only-v{version}.zip"

    with zipfile.ZipFile(archive_path, "w") as archive:
        for name in sorted(payload, key=str.casefold):
            add_file(archive, name, payload[name])

    with zipfile.ZipFile(archive_path) as archive:
        bad_member = archive.testzip()
        names = archive.namelist()

    digest = sha256(archive_path)
    hash_path = output_dir / f"agentic-course-redesign-openai-skills-only-v{version}.sha256.txt"
    hash_path.write_text(f"{digest}  {archive_path.name}\n", encoding="ascii")
    result = {
        "schema_version": 1,
        "ok": bad_member is None,
        "version": version,
        "archive": archive_path.name,
        "archive_sha256": digest,
        "archive_file_count": len(names),
        "single_top_level_root": len({name.split("/", 1)[0] for name in names}) == 1,
        "hash_file": hash_path.name,
        "bad_member": bad_member,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] and result["single_top_level_root"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
