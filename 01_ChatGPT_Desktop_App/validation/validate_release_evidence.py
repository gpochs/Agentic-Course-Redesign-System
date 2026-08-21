#!/usr/bin/env python3
"""Fail closed when a release report does not describe the exact archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def validate(report: dict, archive: Path, expected_version: str) -> list[str]:
    errors: list[str] = []
    if report.get("pass") is not True:
        errors.append("release report must record pass=true")
    if report.get("archive") != archive.name:
        errors.append("release report archive name does not match the selected archive")
    version_marker = f"v{expected_version}"
    for label, name in (("selected archive", archive.name), ("release report archive", report.get("archive"))):
        if not isinstance(name, str) or not re.search(
            rf"(?:^|[-_]){re.escape(version_marker)}(?:[-_.]|$)", name
        ):
            errors.append(f"{label} does not identify expected version {expected_version}")
    actual_bytes = archive.stat().st_size
    if report.get("archive_bytes") != actual_bytes:
        errors.append("release report byte count does not match the selected archive")
    actual_hash = sha256(archive)
    if str(report.get("archive_sha256", "")).upper() != actual_hash:
        errors.append("release report SHA-256 does not match the selected archive")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--expected-version", required=True)
    args = parser.parse_args()

    errors: list[str] = []
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        errors.extend(validate(report, args.archive, args.expected_version))
    except Exception as exc:
        errors.append(f"{type(exc).__name__}: {exc}")
    result = {
        "schema_version": 1,
        "pass": not errors,
        "report": args.report.name,
        "archive": args.archive.name,
        "expected_version": args.expected_version,
        "errors": errors,
    }
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
