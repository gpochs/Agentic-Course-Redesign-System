#!/usr/bin/env python3
"""Build the skills-only ZIP twice, compare hashes, and validate its contents."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "openai-submission" / "build_skills_only_zip.py"
VALIDATE = ROOT / "validation" / "validate_public_submission.py"


def run_json(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr or completed.stdout)
    return json.loads(completed.stdout)


def main() -> int:
    first = run_json([sys.executable, str(BUILD)])
    second = run_json([sys.executable, str(BUILD)])
    archive = ROOT / "dist" / str(second["archive"])
    hash_file = ROOT / "dist" / str(second["hash_file"])
    validation = run_json(
        [sys.executable, str(VALIDATE), "--archive", str(archive)]
    )
    expected_hash_line = f"{second['archive_sha256']}  {archive.name}"
    checks = [
        {
            "check": "deterministic skills-only ZIP SHA-256",
            "pass": first["archive_sha256"] == second["archive_sha256"],
        },
        {
            "check": "single top-level plugin root",
            "pass": bool(second["single_top_level_root"]),
        },
        {
            "check": "hash sidecar matches archive",
            "pass": hash_file.read_text(encoding="ascii").strip() == expected_hash_line,
        },
        {
            "check": "public source and review validation",
            "pass": bool(validation["pass"]),
        },
        {
            "check": "owner blockers remain explicit",
            "pass": validation["submission_ready"] is False
            and bool(validation["owner_submission_blockers"]),
        },
    ]
    result = {
        "schema_version": 1,
        "pass": all(item["pass"] for item in checks),
        "archive": f"dist/{archive.name}",
        "archive_sha256": second["archive_sha256"],
        "archive_file_count": second["archive_file_count"],
        "hash_file": f"dist/{hash_file.name}",
        "submission_ready": validation["submission_ready"],
        "owner_submission_blockers": validation["owner_submission_blockers"],
        "checks": checks,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
