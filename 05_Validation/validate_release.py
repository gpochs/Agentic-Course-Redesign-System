#!/usr/bin/env python3
"""Validate archive paths, inventory, hashes, public scrub and sidecar."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent.parent
DIST = (ROOT / "dist").resolve()
TEXT_SUFFIXES = {"", ".csv", ".html", ".json", ".jsonc", ".md", ".py", ".svg", ".toml", ".txt", ".yaml", ".yml"}
BAD_PARTS = {".git", "__pycache__", ".pytest_cache", ".venv", "dist"}
CONTENT_PATTERNS = {
    "windows_user_home": re.compile(rb"(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'<>]+[\\/]"),
    "private_key_block": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github_token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_token": re.compile(rb"\bsk-[A-Za-z0-9_-]{20,}\b"),
}
ARCHIVE_NAME = re.compile(
    r"^Agentic-Course-Redesign-System_v(?P<version>\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\.zip$"
)
REPORT_NAME = re.compile(
    r"^system-release-validation-v(?P<version>\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\.json$"
)
SHA256_HEX = re.compile(r"^[0-9A-Fa-f]{64}$")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def validate_report_output_path(
    report_path: Path,
    archive_path: Path,
    archive_version: str | None,
) -> list[dict[str, str]]:
    """Return findings that make exclusive report creation unsafe."""
    findings: list[dict[str, str]] = []
    resolved_report = report_path.resolve()
    resolved_archive = archive_path.resolve()
    resolved_sidecar = archive_path.with_suffix(".sha256.txt").resolve()
    resolved_inventory = (archive_path.parent / "package-inventory.json").resolve()

    report_match = REPORT_NAME.fullmatch(report_path.name)
    if report_match is None:
        findings.append({"path": str(report_path), "kind": "invalid_versioned_report_name"})
    elif report_match.group("version") != archive_version:
        findings.append(
            {
                "path": str(report_path),
                "kind": "report_archive_version_mismatch",
                "detail": f"report={report_match.group('version')!r} archive={archive_version!r}",
            }
        )

    protected_outputs = {
        resolved_archive: "archive",
        resolved_sidecar: "hash_sidecar",
        resolved_inventory: "external_inventory",
    }
    if resolved_report in protected_outputs:
        findings.append(
            {
                "path": str(report_path),
                "kind": "report_output_collision",
                "detail": protected_outputs[resolved_report],
            }
        )
    if resolved_report.is_relative_to(ROOT) and not resolved_report.is_relative_to(DIST):
        findings.append(
            {
                "path": str(report_path),
                "kind": "report_output_inside_source_tree",
            }
        )
    if resolved_report.exists():
        findings.append({"path": str(report_path), "kind": "report_output_already_exists"})

    existing_parent = resolved_report.parent
    while not existing_parent.exists() and existing_parent != existing_parent.parent:
        existing_parent = existing_parent.parent
    if existing_parent.exists() and not existing_parent.is_dir():
        findings.append(
            {
                "path": str(report_path.parent),
                "kind": "report_output_parent_not_directory",
            }
        )
    return findings


def safe_inventory_relative_path(value: object) -> str | None:
    if (
        not isinstance(value, str)
        or not value
        or "\\" in value
        or ":" in value
        or any(ord(character) < 32 for character in value)
    ):
        return None
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or ".." in path.parts
        or path.as_posix() != value
        or value == "package-inventory.json"
    ):
        return None
    return value


def validate_inventory(
    archive: zipfile.ZipFile,
    inventory_name: str,
    names: list[str],
) -> tuple[str | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    try:
        inventory = json.loads(archive.read(inventory_name).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError) as exc:
        return None, [
            {
                "path": inventory_name,
                "kind": "invalid_embedded_inventory_json",
                "detail": f"{type(exc).__name__}: {exc}",
            }
        ]
    if not isinstance(inventory, dict):
        return None, [{"path": inventory_name, "kind": "invalid_embedded_inventory_object"}]

    raw_version = inventory.get("version")
    inventory_version = raw_version if isinstance(raw_version, str) and raw_version else None
    archive_match = ARCHIVE_NAME.fullmatch(Path(archive.filename).name) if archive.filename else None
    archive_version = archive_match.group("version") if archive_match else None
    if type(inventory.get("schema_version")) is not int or inventory.get("schema_version") != 1:
        findings.append({"path": inventory_name, "kind": "inventory_schema_version_mismatch"})
    if inventory_version != archive_version:
        findings.append(
            {
                "path": inventory_name,
                "kind": "inventory_archive_version_mismatch",
                "detail": f"inventory={inventory_version!r} archive={archive_version!r}",
            }
        )
    if inventory.get("bundle_root_name") != "Agentic-Course-Redesign-System":
        findings.append({"path": inventory_name, "kind": "inventory_root_name_mismatch"})

    records = inventory.get("files")
    if not isinstance(records, list):
        findings.append({"path": inventory_name, "kind": "invalid_inventory_file_records"})
        records = []
    declared_count = inventory.get("file_count")
    if type(declared_count) is not int or declared_count != len(records):
        findings.append(
            {
                "path": inventory_name,
                "kind": "inventory_file_count_mismatch",
                "detail": f"declared={declared_count!r} records={len(records)}",
            }
        )

    expected_names: set[str] = set()
    seen_paths: set[str] = set()
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            findings.append(
                {
                    "path": inventory_name,
                    "kind": "invalid_inventory_file_record",
                    "detail": f"index={index}",
                }
            )
            continue
        rel_path = safe_inventory_relative_path(record.get("relative_path"))
        if rel_path is None:
            findings.append(
                {
                    "path": inventory_name,
                    "kind": "unsafe_inventory_relative_path",
                    "detail": f"index={index} value={record.get('relative_path')!r}",
                }
            )
            continue
        folded = rel_path.casefold()
        if folded in seen_paths:
            findings.append(
                {
                    "path": inventory_name,
                    "kind": "duplicate_inventory_relative_path",
                    "detail": rel_path,
                }
            )
        seen_paths.add(folded)
        member = f"Agentic-Course-Redesign-System/{rel_path}"
        expected_names.add(member)

        expected_bytes = record.get("bytes")
        expected_hash = record.get("sha256")
        valid_bytes = type(expected_bytes) is int and expected_bytes >= 0
        valid_hash = isinstance(expected_hash, str) and SHA256_HEX.fullmatch(expected_hash) is not None
        if not valid_bytes:
            findings.append(
                {
                    "path": inventory_name,
                    "kind": "invalid_inventory_byte_count",
                    "detail": f"index={index} value={expected_bytes!r}",
                }
            )
        if not valid_hash:
            findings.append(
                {
                    "path": inventory_name,
                    "kind": "invalid_inventory_sha256",
                    "detail": f"index={index}",
                }
            )
        if member in names and valid_bytes and valid_hash:
            data = archive.read(member)
            if len(data) != expected_bytes or sha256_bytes(data) != expected_hash.upper():
                findings.append({"path": member, "kind": "inventory_hash_or_size_mismatch"})

    actual_names = set(names) - {inventory_name}
    if expected_names != actual_names:
        findings.append({"path": inventory_name, "kind": "inventory_membership_mismatch"})
    return inventory_version, findings


def validate(
    archive_path: Path,
    private_denylist: list[str] | None = None,
    expected_version: str | None = None,
    report_path: Path | None = None,
) -> dict[str, object]:
    findings: list[dict[str, str]] = []
    denylist = private_denylist or []
    archive_match = ARCHIVE_NAME.fullmatch(archive_path.name)
    archive_version = archive_match.group("version") if archive_match else None
    if archive_match is None:
        findings.append({"path": archive_path.name, "kind": "invalid_versioned_archive_name"})
    if expected_version is not None and archive_version != expected_version:
        findings.append(
            {
                "path": archive_path.name,
                "kind": "expected_release_version_mismatch",
                "detail": f"expected={expected_version!r} archive={archive_version!r}",
            }
        )
    report_findings = (
        validate_report_output_path(report_path, archive_path, archive_version)
        if report_path is not None
        else []
    )
    findings.extend(report_findings)
    inventory_version: str | None = None
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
            inventory_version, inventory_findings = validate_inventory(
                archive, inventory_name, names
            )
            findings.extend(inventory_findings)
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
        "report_output_safe": report_path is None or not report_findings,
        "release_version": archive_version,
        "inventory_version": inventory_version,
        "archive": archive_path.name,
        "archive_sha256": archive_hash,
        "archive_bytes": archive_path.stat().st_size,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--expected-version")
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
    archive_path = args.archive.resolve()
    report_path = args.report.resolve() if args.report else None
    result = validate(
        archive_path,
        denylist,
        expected_version=args.expected_version,
        report_path=report_path,
    )
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if report_path is not None and result["report_output_safe"]:
        try:
            report_path.parent.mkdir(parents=True, exist_ok=True)
            with report_path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(rendered + "\n")
        except OSError as exc:
            result["findings"].append(
                {
                    "path": str(report_path),
                    "kind": "report_output_write_failed",
                    "detail": f"{type(exc).__name__}: {exc}",
                }
            )
            result["pass"] = False
            result["report_output_safe"] = False
            rendered = json.dumps(result, ensure_ascii=False, indent=2)
    print(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
