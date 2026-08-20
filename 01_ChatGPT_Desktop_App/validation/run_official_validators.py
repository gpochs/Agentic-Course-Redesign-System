#!/usr/bin/env python3
"""Run installed Codex plugin/skill validators without bundling them."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOTS = {
    "custom marketplace plugin": ROOT / "plugins" / "agentic-course-redesign",
    "OpenAI skills-only source": (
        ROOT / "openai-submission" / "source" / "agentic-course-redesign"
    ),
}


def system_skill_root() -> Path | None:
    candidates = []
    if os.environ.get("CODEX_HOME"):
        candidates.append(Path(os.environ["CODEX_HOME"]) / "skills" / ".system")
    candidates.append(Path.home() / ".codex" / "skills" / ".system")
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def sanitise(message: str) -> str:
    home = str(Path.home())
    return message.replace(home, "<HOME>").replace(home.replace("\\", "/"), "<HOME>")


def run_validator(label: str, command: list[str]) -> dict[str, object]:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    record: dict[str, object] = {
        "validator": label,
        "status": "passed" if completed.returncode == 0 else "failed",
        "return_code": completed.returncode,
    }
    if completed.returncode != 0:
        combined = (completed.stderr or completed.stdout).strip()
        record["diagnostic"] = sanitise(combined[-1000:])
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-missing", action="store_true")
    args = parser.parse_args()
    skill_root = system_skill_root()
    if skill_root is None:
        result = {
            "schema_version": 1,
            "pass": bool(args.allow_missing),
            "status": "skipped_missing_installed_codex_validator_bundle"
            if args.allow_missing
            else "failed_missing_installed_codex_validator_bundle",
            "validators": [],
        }
        print(json.dumps(result, indent=2))
        return 0 if result["pass"] else 1

    plugin_validator = skill_root / "plugin-creator" / "scripts" / "validate_plugin.py"
    skill_validator = skill_root / "skill-creator" / "scripts" / "quick_validate.py"
    missing = [
        name
        for name, path in {
            "plugin validator": plugin_validator,
            "skill validator": skill_validator,
        }.items()
        if not path.is_file()
    ]
    if missing:
        result = {
            "schema_version": 1,
            "pass": bool(args.allow_missing),
            "status": "skipped_missing_validator_scripts"
            if args.allow_missing
            else "failed_missing_validator_scripts",
            "missing": missing,
            "validators": [],
        }
        print(json.dumps(result, indent=2))
        return 0 if result["pass"] else 1

    records = []
    for package_label, plugin in PLUGIN_ROOTS.items():
        records.append(
            run_validator(
                f"official plugin validator: {package_label}",
                [sys.executable, str(plugin_validator), str(plugin)],
            )
        )
        for skill in sorted((plugin / "skills").iterdir()):
            if skill.is_dir():
                records.append(
                    run_validator(
                        f"official quick validator: {package_label}: {skill.name}",
                        [sys.executable, str(skill_validator), str(skill)],
                    )
                )
    result = {
        "schema_version": 1,
        "pass": all(item["status"] == "passed" for item in records),
        "status": "passed" if all(item["status"] == "passed" for item in records) else "failed",
        "validators": records,
    }
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
