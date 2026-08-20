#!/usr/bin/env python3
"""Build twice, compare hashes, and validate the portable release archive."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "validation" / "build_portable_bundle.py"
VALIDATE = ROOT / "validation" / "validate_portable_bundle.py"


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
    archive = ROOT / str(second["archive"])
    hash_file = ROOT / str(second["hash_file"])
    validation = run_json([sys.executable, str(VALIDATE), str(archive)])
    expected_hash_line = f"{second['archive_sha256']}  {archive.name}"
    checks = [
        {
            "check": "deterministic ZIP SHA-256",
            "pass": first["archive_sha256"] == second["archive_sha256"],
        },
        {
            "check": "deterministic inventory SHA-256",
            "pass": first["inventory_sha256"] == second["inventory_sha256"],
        },
        {
            "check": "hash sidecar matches archive",
            "pass": hash_file.read_text(encoding="ascii").strip() == expected_hash_line,
        },
        {"check": "portable bundle validator", "pass": validation["pass"]},
    ]
    result = {
        "schema_version": 1,
        "pass": all(item["pass"] for item in checks),
        "archive": second["archive"],
        "archive_sha256": second["archive_sha256"],
        "archive_file_count": second["archive_file_count"],
        "inventory": second["inventory"],
        "inventory_sha256": second["inventory_sha256"],
        "checks": checks,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
