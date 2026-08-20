#!/usr/bin/env python3
"""Fail closed on public-source, workflow and adapter regressions."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_TOP_LEVEL = {
    "01_ChatGPT_Desktop_App",
    "02_Other_Agentic_Systems",
    "03_Shared_Workflow_Core",
    "04_Documentation",
    "05_Validation",
}
EXPECTED_SKILLS = {
    "course-redesign-assessment",
    "course-redesign-materials",
    "course-redesign-orchestrator",
    "course-redesign-research",
    "course-redesign-setup",
    "course-redesign-system",
}
REQUIRED_ROOT_FILES = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
}
TEXT_SUFFIXES = {
    "",
    ".csv",
    ".html",
    ".json",
    ".jsonc",
    ".md",
    ".py",
    ".svg",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}
EXCLUDED_PARTS = {".git", "dist"}
DISALLOWED_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
}
DISALLOWED_SUFFIXES = {
    ".cer",
    ".crt",
    ".jks",
    ".key",
    ".keystore",
    ".p12",
    ".pem",
    ".pfx",
    ".pyc",
}
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


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDED_PARTS for part in rel.parts):
            continue
        files.append(path)
    return sorted(files, key=lambda item: relative(item).casefold())


def parse_skill_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML delimiter")
    try:
        end = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValueError("missing closing YAML delimiter") from exc
    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"unsupported frontmatter line: {line}")
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    if not "\n".join(lines[end + 1 :]).strip():
        raise ValueError("empty skill instructions")
    return metadata


def validate_adapter_manifest(path: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [{"path": relative(path), "kind": "invalid_adapter_manifest", "detail": str(exc)}]
    for field in ("schema_version", "platform", "adapter_version", "status"):
        if field not in data:
            findings.append({"path": relative(path), "kind": f"missing_adapter_field:{field}"})
    if data.get("status") not in {"candidate_not_active", "template_not_installed", "validated_template"}:
        findings.append({"path": relative(path), "kind": "unsafe_adapter_status"})
    if data.get("adapter_version") != "0.2.0":
        findings.append({"path": relative(path), "kind": "adapter_release_version_mismatch"})
    # `source_files` may describe the external validated base and is not
    # expected to exist inside an adapter. Verify only frozen adapter outputs.
    records = data.get("files") or data.get("generated_files") or []
    if records and not isinstance(records, list):
        findings.append({"path": relative(path), "kind": "invalid_adapter_file_records"})
    for record in records if isinstance(records, list) else []:
        if not isinstance(record, dict):
            findings.append({"path": relative(path), "kind": "invalid_adapter_file_record"})
            continue
        rel_path = record.get("path") or record.get("relative_path")
        expected = record.get("sha256")
        if not rel_path or not expected:
            continue
        target = path.parent / str(rel_path)
        if not target.is_file():
            findings.append({"path": relative(path), "kind": "adapter_record_missing", "detail": str(rel_path)})
        elif sha256(target) != str(expected).upper():
            findings.append({"path": relative(path), "kind": "adapter_record_hash_mismatch", "detail": str(rel_path)})
    return findings


def load_private_denylist(path: Path | None) -> list[str]:
    if path is None:
        return []
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def scan(private_denylist: list[str] | None = None) -> dict[str, object]:
    findings: list[dict[str, str]] = []
    files = source_files()
    denylist = private_denylist or []

    for name in sorted(EXPECTED_TOP_LEVEL):
        if not (ROOT / name).is_dir():
            findings.append({"path": name, "kind": "missing_top_level_directory"})
    for name in sorted(REQUIRED_ROOT_FILES):
        if not (ROOT / name).is_file():
            findings.append({"path": name, "kind": "missing_required_root_file"})

    for path in files:
        rel = relative(path)
        parts = set(path.relative_to(ROOT).parts)
        if path.is_symlink():
            findings.append({"path": rel, "kind": "symlink_not_portable"})
        if parts & DISALLOWED_PARTS:
            findings.append({"path": rel, "kind": "cache_or_environment_artifact"})
        if path.name.startswith("~$"):
            findings.append({"path": rel, "kind": "office_lock_file"})
        if path.name.casefold().startswith(".env") or path.suffix.casefold() in DISALLOWED_SUFFIXES:
            findings.append({"path": rel, "kind": "secret_key_or_bytecode_file"})
        if path.suffix.casefold() == ".json":
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if path.name == "state.json":
                    if data.get("status") != "candidate_not_active":
                        findings.append({"path": rel, "kind": "state_not_inactive"})
                    if data.get("schedules") not in ([], None):
                        findings.append({"path": rel, "kind": "schedule_present"})
            except Exception as exc:
                findings.append({"path": rel, "kind": "invalid_json", "detail": str(exc)})
        if path.suffix.casefold() == ".toml":
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:
                findings.append({"path": rel, "kind": "invalid_toml", "detail": str(exc)})
        if path.suffix.casefold() in TEXT_SUFFIXES:
            text = path.read_text(encoding="utf-8", errors="replace")
            if "\ufffd" in text:
                findings.append({"path": rel, "kind": "replacement_character"})
            for marker in denylist:
                if marker.casefold() in text.casefold():
                    findings.append({"path": rel, "kind": "pilot_specific_content", "detail": marker})
            for kind, pattern in CONTENT_PATTERNS.items():
                if pattern.search(text):
                    findings.append({"path": rel, "kind": kind})

    skill_root = ROOT / "03_Shared_Workflow_Core" / "agent-skills"
    actual_skills = {path.parent.name for path in skill_root.glob("*/SKILL.md")}
    if actual_skills != EXPECTED_SKILLS:
        findings.append(
            {
                "path": relative(skill_root),
                "kind": "shared_skill_set_mismatch",
                "detail": f"expected={sorted(EXPECTED_SKILLS)} actual={sorted(actual_skills)}",
            }
        )
    for path in ROOT.rglob("SKILL.md"):
        if any(part in EXCLUDED_PARTS for part in path.relative_to(ROOT).parts):
            continue
        try:
            metadata = parse_skill_frontmatter(path)
            name = metadata.get("name", "")
            description = metadata.get("description", "")
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                findings.append({"path": relative(path), "kind": "invalid_skill_name"})
            if not description or len(description) > 1024:
                findings.append({"path": relative(path), "kind": "invalid_skill_description"})
        except Exception as exc:
            findings.append({"path": relative(path), "kind": "invalid_skill", "detail": str(exc)})

    adapter_manifests = sorted(ROOT.glob("02_Other_Agentic_Systems/**/adapter-manifest.json"))
    if len(adapter_manifests) < 4:
        findings.append(
            {
                "path": "02_Other_Agentic_Systems",
                "kind": "insufficient_adapter_manifests",
                "detail": f"found={len(adapter_manifests)}",
            }
        )
    for manifest in adapter_manifests:
        findings.extend(validate_adapter_manifest(manifest))

    root_marketplace = ROOT / ".agents" / "plugins" / "marketplace.json"
    if not root_marketplace.is_file():
        findings.append({"path": ".agents/plugins/marketplace.json", "kind": "missing_root_marketplace"})
    else:
        marketplace = json.loads(root_marketplace.read_text(encoding="utf-8"))
        plugins = marketplace.get("plugins", [])
        if len(plugins) != 1 or plugins[0].get("name") != "agentic-course-redesign":
            findings.append({"path": relative(root_marketplace), "kind": "unexpected_root_marketplace_plugins"})
        else:
            plugin_path = plugins[0].get("source", {}).get("path", "")
            target = ROOT / str(plugin_path).removeprefix("./")
            if not (target / ".codex-plugin" / "plugin.json").is_file():
                findings.append({"path": relative(root_marketplace), "kind": "root_marketplace_target_missing"})

    chatgpt_manifest = (
        ROOT
        / "01_ChatGPT_Desktop_App"
        / "plugins"
        / "agentic-course-redesign"
        / ".codex-plugin"
        / "plugin.json"
    )
    if not chatgpt_manifest.is_file():
        findings.append({"path": relative(chatgpt_manifest), "kind": "missing_chatgpt_plugin_manifest"})
    else:
        plugin_data = json.loads(chatgpt_manifest.read_text(encoding="utf-8"))
        if plugin_data.get("name") != "agentic-course-redesign" or plugin_data.get("version") != "0.2.0":
            findings.append({"path": relative(chatgpt_manifest), "kind": "chatgpt_plugin_identity_mismatch"})

    antigravity_overlay = ROOT / "02_Other_Agentic_Systems" / "04_Google_Antigravity" / "workspace-overlay"
    for forbidden in (
        antigravity_overlay / ".agents" / "hooks.json",
        antigravity_overlay / ".agents" / "mcp_config.json",
        antigravity_overlay / ".agents" / "plugins",
    ):
        if forbidden.exists():
            findings.append({"path": relative(forbidden), "kind": "privileged_antigravity_component_auto_discovered"})

    ignore_path = ROOT / ".gitignore"
    if ignore_path.is_file():
        ignore_text = ignore_path.read_text(encoding="utf-8")
        for forbidden in (".agents/", ".codex/", ".claude/", ".opencode/", ".github/"):
            if re.search(rf"(?m)^\s*{re.escape(forbidden)}\s*$", ignore_text):
                findings.append({"path": ".gitignore", "kind": "control_directory_ignored", "detail": forbidden})

    return {
        "schema_version": 1,
        "pass": not findings,
        "repository": "Agentic-Course-Redesign-System",
        "source_file_count": len(files),
        "shared_skill_count": len(actual_skills),
        "adapter_manifest_count": len(adapter_manifests),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--private-denylist",
        type=Path,
        help="Optional local-only newline-delimited course markers; never commit this file.",
    )
    args = parser.parse_args()
    result = scan(load_private_denylist(args.private_denylist))
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
