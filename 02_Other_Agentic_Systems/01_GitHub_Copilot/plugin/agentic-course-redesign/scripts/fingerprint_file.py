#!/usr/bin/env python3
"""Print a gated deterministic SHA-256 for a source or trusted control record.

``eligibility`` is the only pre-Gate-0A mode and is restricted to a structured
``01_Control/material-processing-eligibility.json`` record. ``policy`` and
``course-source`` require a separately approved current eligibility record,
validated before the target path is inspected or read. There is no ambiguous
ungated raw-file mode.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


POLICY_EXCLUDED_FIELDS = frozenset({"fingerprint", "lecturer_decision", "approved_at"})
ELIGIBILITY_EXCLUDED_FIELDS = frozenset(
    {"fingerprint", "lecturer_declaration_reference", "recorded_at"}
)
CONTROL_FILENAMES = {
    "eligibility": "material-processing-eligibility.json",
    "policy": "source-access-policy.json",
}


def _load_eligibility_validator():
    sibling = Path(__file__).with_name("source_manifest.py")
    spec = importlib.util.spec_from_file_location("course_redesign_source_manifest", sibling)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load eligibility validator from {sibling}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_eligibility


validate_eligibility = _load_eligibility_validator()


def _assert_control_target(path: Path, mode: str) -> None:
    expected_name = CONTROL_FILENAMES[mode]
    if path.name != expected_name or path.parent.name != "01_Control":
        raise ValueError(
            f"{mode} mode is restricted to 01_Control/{expected_name}"
        )


def _canonical_json_payload(
    path: Path, excluded_fields: frozenset[str], mode: str
) -> bytes:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("control JSON must be an object")
    if value.get("schema_version") != 1:
        raise ValueError(f"{mode} control schema_version must be 1")
    if mode == "eligibility":
        if value.get("gate") != "GATE_0A_MATERIAL_ENVIRONMENT_ELIGIBILITY" or not all(
            key in value for key in ("environment", "material_scope", "decision")
        ):
            raise ValueError("eligibility control structure is incomplete")
    elif mode == "policy" and not all(
        key in value
        for key in (
            "policy_id",
            "policy_version",
            "material_processing_eligibility_fingerprint",
            "per_source_entries",
            "role_tool_egress_permissions",
            "permitted_output_audiences",
            "assessment_security_boundary",
        )
    ):
        raise ValueError("source-access-policy control structure is incomplete")
    value = {key: item for key, item in value.items() if key not in excluded_fields}
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def fingerprint(
    path: Path, mode: str, eligibility_record: Path | None = None
) -> tuple[str, bytes]:
    if mode not in {"eligibility", "policy", "course-source"}:
        raise ValueError("mode must be eligibility, policy or course-source")
    if mode == "eligibility":
        _assert_control_target(path, mode)
        payload = _canonical_json_payload(path, ELIGIBILITY_EXCLUDED_FIELDS, mode)
    else:
        if eligibility_record is None:
            raise PermissionError(
                "approved Gate-0A eligibility record is required before target inspection"
            )
        eligibility = validate_eligibility(eligibility_record)
        if not eligibility["ok"]:
            raise PermissionError(
                "Gate-0A does not permit target inspection: "
                + "; ".join(eligibility["errors"])
            )
        if mode == "policy":
            _assert_control_target(path, mode)
            payload = _canonical_json_payload(path, POLICY_EXCLUDED_FIELDS, mode)
        else:
            payload = path.read_bytes()
    return hashlib.sha256(payload).hexdigest().upper(), payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument(
        "--mode", choices=("eligibility", "policy", "course-source"), required=True
    )
    parser.add_argument(
        "--eligibility-record",
        type=Path,
        help="approved fingerprinted Gate-0A record; required for policy/course-source",
    )
    parser.add_argument(
        "--show-canonical-payload",
        action="store_true",
        help="include the decoded canonical payload in policy/eligibility-mode output",
    )
    args = parser.parse_args()
    try:
        digest, payload = fingerprint(
            args.path, args.mode, eligibility_record=args.eligibility_record
        )
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError, PermissionError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}))
        return 1
    result = {
        "ok": True,
        "path": str(args.path),
        "mode": args.mode,
        "sha256": digest,
        "excluded_top_level_fields": sorted(
            POLICY_EXCLUDED_FIELDS
            if args.mode == "policy"
            else ELIGIBILITY_EXCLUDED_FIELDS
            if args.mode == "eligibility"
            else []
        ),
    }
    if args.show_canonical_payload and args.mode in {"policy", "eligibility"}:
        result["canonical_payload"] = payload.decode("utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
