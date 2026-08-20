#!/usr/bin/env python3
"""Print a deterministic SHA-256 fingerprint for a file or JSON policy.

The default ``raw`` mode hashes the file bytes. ``policy`` mode implements the
source-access-policy contract used by this plugin: UTF-8 canonical JSON, sorted
keys, no insignificant whitespace, excluding the top-level fingerprint and
lecturer-approval metadata. The canonical payload can be emitted for audit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


POLICY_EXCLUDED_FIELDS = frozenset({"fingerprint", "lecturer_decision", "approved_at"})


def canonical_policy_payload(path: Path) -> bytes:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("policy JSON must be an object")
    value = {key: item for key, item in value.items() if key not in POLICY_EXCLUDED_FIELDS}
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def fingerprint(path: Path, mode: str) -> tuple[str, bytes]:
    payload = canonical_policy_payload(path) if mode == "policy" else path.read_bytes()
    return hashlib.sha256(payload).hexdigest().upper(), payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--mode", choices=("raw", "policy"), default="raw")
    parser.add_argument(
        "--show-canonical-payload",
        action="store_true",
        help="include the decoded canonical payload in policy-mode output",
    )
    args = parser.parse_args()
    if not args.path.is_file():
        print(json.dumps({"ok": False, "error": "file missing", "path": str(args.path)}))
        return 1
    try:
        digest, payload = fingerprint(args.path, args.mode)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(json.dumps({"ok": False, "error": str(exc), "path": str(args.path)}))
        return 1
    result = {
        "ok": True,
        "path": str(args.path),
        "mode": args.mode,
        "sha256": digest,
        "excluded_top_level_fields": sorted(POLICY_EXCLUDED_FIELDS)
        if args.mode == "policy"
        else [],
    }
    if args.show_canonical_payload and args.mode == "policy":
        result["canonical_payload"] = payload.decode("utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
