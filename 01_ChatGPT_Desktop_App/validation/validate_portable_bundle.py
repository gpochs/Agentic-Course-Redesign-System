#!/usr/bin/env python3
"""Validate the portable workshop ZIP against its embedded source inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import zipfile
from pathlib import Path, PurePosixPath

from public_scrub import EXPECTED_AGENTS, EXPECTED_SKILLS, inspect_text


PREFIX = "Agentic_Course_Redesign/"
INVENTORY_NAME = PREFIX + "validation/package-inventory.json"
ALLOWED_SUFFIXES = {"", ".md", ".json", ".svg", ".toml", ".py", ".yaml", ".yml", ".txt", ".csv"}
ROOT = Path(__file__).resolve().parent.parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def display_path(path: Path) -> str:
    resolved = path.resolve(strict=False)
    try:
        return resolved.relative_to(ROOT).as_posix()
    except ValueError:
        return resolved.name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    failures: list[str] = []
    checks: list[dict[str, object]] = []

    if not args.archive.is_file():
        failures.append("archive missing")
        result = {"pass": False, "archive": display_path(args.archive), "failures": failures}
    else:
        with zipfile.ZipFile(args.archive) as archive:
            bad = archive.testzip()
            names = archive.namelist()
            if bad:
                failures.append(f"corrupt member: {bad}")
            unsafe = []
            disallowed = []
            for name in names:
                path = PurePosixPath(name)
                normalized = posixpath.normpath(name)
                if (
                    not name.startswith(PREFIX)
                    or name.startswith("/")
                    or ".." in path.parts
                    or normalized != name.rstrip("/")
                ):
                    unsafe.append(name)
                if Path(name).suffix.casefold() not in ALLOWED_SUFFIXES:
                    disallowed.append(name)
            if unsafe:
                failures.append(f"unsafe archive paths: {unsafe}")
            if disallowed:
                failures.append(f"disallowed file types: {disallowed}")
            required = {
                PREFIX + ".agents/plugins/marketplace.json",
                PREFIX + "plugins/agentic-course-redesign/.codex-plugin/plugin.json",
                PREFIX + "plugins/agentic-course-redesign/assets/PARTICIPANT_QUICK_START.md",
                PREFIX + "plugins/agentic-course-redesign/assets/project-template/AGENTS.md",
                PREFIX + "validation/plugin-test-cases.json",
                INVENTORY_NAME,
            }
            missing_required = sorted(required - set(names))
            if missing_required:
                failures.append(f"missing required members: {missing_required}")
            skill_members = [name for name in names if name.endswith("/SKILL.md")]
            skill_names = {
                PurePosixPath(name).parent.name for name in skill_members
            }
            if skill_names != EXPECTED_SKILLS:
                failures.append(
                    f"skill set mismatch: expected={sorted(EXPECTED_SKILLS)} actual={sorted(skill_names)}"
                )
            agent_prefix = PREFIX + "plugins/agentic-course-redesign/assets/project-template/.codex/agents/"
            agent_names = {
                PurePosixPath(name).name
                for name in names
                if name.startswith(agent_prefix) and name.endswith(".toml")
            }
            if agent_names != EXPECTED_AGENTS:
                failures.append(
                    f"agent set mismatch: expected={sorted(EXPECTED_AGENTS)} actual={sorted(agent_names)}"
                )

            inventory = json.loads(archive.read(INVENTORY_NAME).decode("utf-8"))
            inventory_records = {item["relative_path"]: item for item in inventory["files"]}
            actual_source_names = {
                name[len(PREFIX) :]
                for name in names
                if name != INVENTORY_NAME and not name.endswith("/")
            }
            if set(inventory_records) != actual_source_names:
                failures.append(
                    "inventory membership mismatch: "
                    f"missing={sorted(set(inventory_records) - actual_source_names)}, "
                    f"extra={sorted(actual_source_names - set(inventory_records))}"
                )
            hash_mismatches = []
            for relative, record in inventory_records.items():
                data = archive.read(PREFIX + relative)
                if len(data) != record["bytes"] or digest(data) != record["sha256"]:
                    hash_mismatches.append(relative)
            if hash_mismatches:
                failures.append(f"inventory hash mismatch: {hash_mismatches}")

            sensitive_hits = []
            for name in names:
                if Path(name).suffix.casefold() not in {"", ".md", ".json", ".svg", ".toml", ".py", ".yaml", ".yml", ".txt", ".csv"}:
                    continue
                text = archive.read(name).decode("utf-8", errors="replace")
                sensitive_hits.extend(inspect_text(name[len(PREFIX) :], text))
            if sensitive_hits:
                failures.append(f"public-source leakage: {sensitive_hits}")

            checks = [
                {"check": "ZIP CRC", "pass": bad is None},
                {"check": "safe relative paths", "pass": not unsafe},
                {"check": "allowlisted file types", "pass": not disallowed},
                {"check": "required plugin members", "pass": not missing_required},
                {"check": "exact six skills", "pass": skill_names == EXPECTED_SKILLS},
                {"check": "exact ten agents", "pass": agent_names == EXPECTED_AGENTS},
                {"check": "inventory membership", "pass": set(inventory_records) == actual_source_names},
                {"check": "inventory bytes and SHA-256", "pass": not hash_mismatches},
                {"check": "no public-source leakage", "pass": not sensitive_hits},
            ]
        result = {
            "schema_version": 1,
            "archive": display_path(args.archive),
            "archive_sha256": digest(args.archive.read_bytes()),
            "archive_file_count": len(names),
            "pass": not failures,
            "checks": checks,
            "failures": failures,
        }

    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
