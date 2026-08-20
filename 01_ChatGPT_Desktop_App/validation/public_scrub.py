#!/usr/bin/env python3
"""Fail closed on public-source leakage and package-shape regressions."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "agentic-course-redesign"
PUBLIC_PLUGIN = ROOT / "openai-submission" / "source" / "agentic-course-redesign"

EXPECTED_SKILLS = {
    "course-redesign-assessment",
    "course-redesign-materials",
    "course-redesign-orchestrator",
    "course-redesign-research",
    "course-redesign-setup",
    "course-redesign-system",
}
EXPECTED_AGENTS = {
    "active-learning-researcher.toml",
    "ai-integration-researcher.toml",
    "artefact-accessibility-visual-qa.toml",
    "assessment-alignment-designer.toml",
    "course-mapper.toml",
    "evidence-feasibility-red-team.toml",
    "learning-designer.toml",
    "learning-material-designer.toml",
    "source-verification-citation-auditor.toml",
    "student-experience-critic.toml",
}
TEXT_SUFFIXES = {"", ".csv", ".json", ".md", ".py", ".svg", ".toml", ".txt", ".yaml", ".yml"}
DISALLOWED_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "env",
    "dist",
}
IGNORED_GENERATED_PARTS = {"dist"}
DISALLOWED_SUFFIXES = {".cer", ".crt", ".jks", ".key", ".keystore", ".p12", ".pem", ".pfx", ".pyc"}
GENERATED_REPORT_PREFIXES = (
    "forward-test-report",
    "local-",
    "portable-bundle-validation",
)

CONTENT_PATTERNS = {
    "windows_user_home": re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+[^\\/\s\"'<>]+[\\/]"),
    "windows_onedrive_absolute": re.compile(r"(?i)[A-Z]:[\\/][^\r\n]*[\\/]OneDrive[\\/]"),
    "macos_user_home": re.compile("/" + "Users/" + r"[^/\s\"'<>]+/"),
    "linux_user_home": re.compile("/" + "home/" + r"[^/\s\"'<>]+/"),
    "email_address": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
    "private_key_block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "aws_access_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "openai_style_token": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "slack_token": re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
}


def inspect_text(relative_path: str, text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for kind, pattern in CONTENT_PATTERNS.items():
        if pattern.search(text):
            findings.append({"path": relative_path, "kind": kind})
    unsupported_product_pattern = re.compile(
        r"(?i)\b(?:" + "clau" + "de|" + "co" + "work)\b"
    )
    if unsupported_product_pattern.search(text):
        findings.append({"path": relative_path, "kind": "unsupported_product_route"})
    return findings


def scan(root: Path = ROOT) -> dict[str, object]:
    findings: list[dict[str, str]] = []
    inspected_file_count = 0
    files = sorted(path for path in root.rglob("*") if path.is_file())
    for path in files:
        relative = path.relative_to(root).as_posix()
        parts = set(path.relative_to(root).parts)
        if ".git" in parts:
            continue
        if parts & IGNORED_GENERATED_PARTS:
            continue
        inspected_file_count += 1
        if parts & DISALLOWED_PARTS:
            findings.append({"path": relative, "kind": "cache_temp_or_dist_artifact"})
            continue
        if relative == "validation/package-inventory.json" or (
            relative.startswith("validation/")
            and path.suffix.casefold() == ".json"
            and path.name.startswith(GENERATED_REPORT_PREFIXES)
        ):
            findings.append({"path": relative, "kind": "generated_local_report_in_source"})
            continue
        if path.name.startswith("~$"):
            findings.append({"path": relative, "kind": "office_lock_file"})
        if path.suffix.casefold() in DISALLOWED_SUFFIXES or path.name.casefold().startswith(".env"):
            findings.append({"path": relative, "kind": "secret_key_or_bytecode_file"})
        if path.suffix.casefold() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            findings.extend(inspect_text(relative, text))

    actual_skills = {
        path.parent.name for path in (PLUGIN / "skills").glob("*/SKILL.md")
    }
    if actual_skills != EXPECTED_SKILLS:
        findings.append(
            {
                "path": "plugins/agentic-course-redesign/skills",
                "kind": "skill_set_mismatch",
                "detail": f"expected={sorted(EXPECTED_SKILLS)} actual={sorted(actual_skills)}",
            }
        )
    actual_public_skills = {
        path.parent.name for path in (PUBLIC_PLUGIN / "skills").glob("*/SKILL.md")
    }
    if actual_public_skills != EXPECTED_SKILLS:
        findings.append(
            {
                "path": "openai-submission/source/agentic-course-redesign/skills",
                "kind": "public_skill_set_mismatch",
                "detail": f"expected={sorted(EXPECTED_SKILLS)} actual={sorted(actual_public_skills)}",
            }
        )
    agent_root = PLUGIN / "assets" / "project-template" / ".codex" / "agents"
    actual_agents = {path.name for path in agent_root.glob("*.toml")}
    if actual_agents != EXPECTED_AGENTS:
        findings.append(
            {
                "path": "plugins/agentic-course-redesign/assets/project-template/.codex/agents",
                "kind": "agent_set_mismatch",
                "detail": f"expected={sorted(EXPECTED_AGENTS)} actual={sorted(actual_agents)}",
            }
        )
    public_agent_root = (
        PUBLIC_PLUGIN / "assets" / "project-template" / ".codex" / "agents"
    )
    actual_public_agents = {path.name for path in public_agent_root.glob("*.toml")}
    if actual_public_agents != EXPECTED_AGENTS:
        findings.append(
            {
                "path": "openai-submission/source/agentic-course-redesign/assets/project-template/.codex/agents",
                "kind": "public_agent_set_mismatch",
                "detail": f"expected={sorted(EXPECTED_AGENTS)} actual={sorted(actual_public_agents)}",
            }
        )

    ignore_path = root / ".gitignore"
    if not ignore_path.is_file():
        findings.append({"path": ".gitignore", "kind": "missing_gitignore"})
    else:
        ignore_lines = {
            line.strip() for line in ignore_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        for required in {"dist/", "__pycache__/", ".pytest_cache/", ".venv/", "~$*"}:
            if required not in ignore_lines:
                findings.append({"path": ".gitignore", "kind": f"missing_ignore:{required}"})
        if any(line in ignore_lines for line in {".agents/", ".codex/", "**/.agents/", "**/.codex/"}):
            findings.append({"path": ".gitignore", "kind": "control_directory_ignored"})

    return {
        "schema_version": 1,
        "pass": not findings,
        "source_file_count": inspected_file_count,
        "skill_count": len(actual_skills),
        "public_skill_count": len(actual_public_skills),
        "agent_count": len(actual_agents),
        "public_agent_count": len(actual_public_agents),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = scan()
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
