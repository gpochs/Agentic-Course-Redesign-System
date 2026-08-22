#!/usr/bin/env python3
"""Validate the native GitHub Copilot package and repository marketplace."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path, PurePosixPath


SCRIPT = Path(__file__).resolve()
DEFAULT_ROOT = SCRIPT.parents[3]
PACKAGE_VERSION = "0.2.4-copilot.1"
PLUGIN_RELATIVE = PurePosixPath(
    "02_Other_Agentic_Systems/01_GitHub_Copilot/plugin/"
    "agentic-course-redesign"
)
EXPECTED_SKILLS = {
    "course-redesign-assessment",
    "course-redesign-materials",
    "course-redesign-orchestrator",
    "course-redesign-research",
    "course-redesign-setup",
    "course-redesign-system",
}
EXPECTED_AGENTS = {
    "active-learning-researcher",
    "ai-integration-researcher",
    "artefact-accessibility-visual-qa",
    "assessment-alignment-designer",
    "course-mapper",
    "evidence-feasibility-red-team",
    "learning-designer",
    "learning-material-designer",
    "source-verification-citation-auditor",
    "student-experience-critic",
}
EXPECTED_SCRIPTS = {
    "create_material_processing_eligibility.py",
    "fingerprint_file.py",
    "migrate_state_v6_to_v7.py",
    "migrate_state_v7_to_v8.py",
    "setup_course_project.py",
    "source_manifest.py",
    "validate_state.py",
}
FORBIDDEN_KEYS = {
    "apps",
    "commands",
    "connectors",
    "extensions",
    "hooks",
    "mcpServers",
    "lspServers",
    "permissions",
    "authentication",
    "schedules",
}
FORBIDDEN_MARKETPLACE_KEYS = FORBIDDEN_KEYS | {"agents", "skills"}
FORBIDDEN_FILES = {
    ".mcp.json",
    "hooks.json",
    "lsp.json",
    "mcp.json",
    "openai.yaml",
    "config.toml",
}
COPILOT_AGENT_DIALOGUE_SUFFIX = """## Copilot lecturer-question boundary

When this manually selected profile must surface a lecturer-only question, it
must return it through the orchestrator and keep one unresolved consequential
question at a time. Use the native `ask_user` card for the complete valid option
set whenever the live GitHub Copilot host accepts it. A live Copilot host has
demonstrated at least five explicit choices plus a custom-answer field; this is
an observed capability, not a maximum. Do not state or assume an unsupported
maximum. Never prune, hide or combine valid choices merely to fit a card. If the
host rejects or cannot present the complete valid set, ask one ordinary chat
question listing every valid numbered option plus `Other`, then wait.

For very long sets, request dependency chunks only when choices share evidence
or constrain one another. Keep every valid option visible across chunks,
explain the grouping, and let the lecturer split, merge, reorder or rename it.
Preserve custom answers and confirm their interpretation; recap each chunk and
gate. Mark only the safest truthful, evidence-aligned, reversible recommendation
and never preselect it. Select a factual declaration only when true; uncertainty
fails closed. Blank or `Skip` cannot advance. Keep every exact authority gate
separate from design preferences."""
COPILOT_CHOICE_CAPACITY_OVERRIDE = """## GitHub Copilot native `ask_user` capacity override

This Copilot-only host rule applies the shared core's host-capacity contract to the demonstrated GitHub Copilot host; it changes no option, gate, evidence requirement, or workflow meaning. Keep one unresolved consequential question at a time. Use the native `ask_user` card for the complete valid option set whenever the live GitHub Copilot host accepts it. A live Copilot host has demonstrated at least five explicit choices plus a custom-answer field; this is an observed capability, not a maximum. Do not state or assume an unsupported maximum. Never prune, hide or combine valid choices merely to fit a card. If the host rejects or cannot present the complete valid set, ask one ordinary chat question listing every valid numbered option plus `Other`, then wait. For very long sets, dependency chunks are allowed only when choices share evidence or constrain one another; keep every valid option visible across chunks, explain the grouping, and let the lecturer split, merge, reorder or rename it."""
COPILOT_CARD_CAPACITY_PHRASES = (
    "one unresolved consequential question at a time",
    "native `ask_user` card",
    "complete valid option set",
    "at least five explicit choices plus a custom-answer field",
    "observed capability, not a maximum",
    "do not state or assume an unsupported maximum",
    "never prune, hide or combine valid choices merely to fit a card",
    "host rejects or cannot present the complete valid set",
    "every valid numbered option plus `other`",
    "dependency chunks",
    "keep every valid option visible across chunks",
)
COPILOT_AGENT_BODY_REPLACEMENTS = {
    "learning-designer": (
        "offer two or three feasible options with a recommendation, evidence, "
        "workload and trade-offs",
        "present every materially distinct feasible option with a recommendation, "
        "evidence, workload and trade-offs, cluster long sets only by shared "
        "evidence or dependency while keeping every option visible",
    ),
}


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def add(
    findings: list[dict[str, str]],
    root: Path,
    path: Path,
    kind: str,
    detail: str = "",
) -> None:
    item = {"path": relative(path, root), "kind": kind}
    if detail:
        item["detail"] = detail
    findings.append(item)


def read_json(
    findings: list[dict[str, str]], root: Path, path: Path
) -> dict[str, object] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        add(findings, root, path, "invalid_or_missing_json", str(exc))
        return None
    if not isinstance(value, dict):
        add(findings, root, path, "json_root_not_object")
        return None
    return value


def skill_name(path: Path) -> str | None:
    match = re.search(
        r"(?m)^name:[ \t]*([a-z0-9-]+)[ \t]*$",
        path.read_text(encoding="utf-8"),
    )
    return match.group(1) if match else None


def split_agent(path: Path) -> tuple[dict[str, object], str] | None:
    match = re.fullmatch(
        r"---\n(.*?)\n---\n\n(.*)",
        path.read_text(encoding="utf-8"),
        flags=re.DOTALL,
    )
    if not match:
        return None
    header: dict[str, object] = {}
    try:
        for line in match.group(1).splitlines():
            key, raw = line.split(":", 1)
            raw = raw.strip()
            if raw in {"true", "false"}:
                value: object = raw == "true"
            elif raw.startswith(("[", '"')):
                value = json.loads(raw)
            else:
                value = raw
            header[key] = value
    except (ValueError, json.JSONDecodeError):
        return None
    return header, match.group(2)


def validate(root: Path = DEFAULT_ROOT) -> list[dict[str, str]]:
    root = root.resolve()
    findings: list[dict[str, str]] = []
    adapter = root / "02_Other_Agentic_Systems" / "01_GitHub_Copilot"
    plugin = root.joinpath(*PLUGIN_RELATIVE.parts)
    marketplace_path = root / ".github" / "plugin" / "marketplace.json"
    marketplace = read_json(findings, root, marketplace_path)
    manifest = read_json(findings, root, plugin / "plugin.json")
    adapter_manifest_path = adapter / "adapter-manifest.json"
    adapter_manifest = read_json(findings, root, adapter_manifest_path)

    if adapter_manifest is not None:
        native = adapter_manifest.get("native_plugin")
        if (
            adapter_manifest.get("adapter_version") != "0.2.4"
            or adapter_manifest.get("status") != "candidate_not_active"
            or not isinstance(native, dict)
            or native.get("package_version") != PACKAGE_VERSION
            or native.get("base_semantic_version") != "0.2.4"
            or native.get("rollback_package_version") != "0.2.3-copilot.1"
            or native.get("status") != "candidate_not_active"
            or native.get("install_specification")
            != "agentic-course-redesign@agentic-course-redesign-system"
        ):
            add(
                findings,
                root,
                adapter_manifest_path,
                "adapter_release_contract_mismatch",
            )

    if marketplace is not None:
        if marketplace.get("name") != "agentic-course-redesign-system":
            add(findings, root, marketplace_path, "marketplace_name_mismatch")
        owner = marketplace.get("owner")
        if not isinstance(owner, dict) or not owner.get("name"):
            add(findings, root, marketplace_path, "marketplace_owner_missing")
        metadata = marketplace.get("metadata")
        if (
            not isinstance(metadata, dict)
            or metadata.get("version") != PACKAGE_VERSION
        ):
            add(findings, root, marketplace_path, "marketplace_version_mismatch")
        plugins = marketplace.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != 1:
            add(findings, root, marketplace_path, "marketplace_plugin_count")
        else:
            entry = plugins[0]
            if not isinstance(entry, dict):
                add(findings, root, marketplace_path, "marketplace_entry_invalid")
            else:
                if entry.get("name") != "agentic-course-redesign":
                    add(findings, root, marketplace_path, "plugin_name_mismatch")
                if entry.get("version") != PACKAGE_VERSION:
                    add(findings, root, marketplace_path, "plugin_version_mismatch")
                if entry.get("strict") is not True:
                    add(findings, root, marketplace_path, "strict_mode_required")
                for key in sorted(FORBIDDEN_MARKETPLACE_KEYS.intersection(entry)):
                    add(
                        findings,
                        root,
                        marketplace_path,
                        "forbidden_marketplace_integration",
                        key,
                    )
                source = entry.get("source")
                if not isinstance(source, str):
                    add(
                        findings,
                        root,
                        marketplace_path,
                        "marketplace_source_must_be_relative_string",
                    )
                else:
                    pure = PurePosixPath(source)
                    if (
                        pure.is_absolute()
                        or ".." in pure.parts
                        or "\\" in source
                        or pure != PLUGIN_RELATIVE
                    ):
                        add(
                            findings,
                            root,
                            marketplace_path,
                            "unsafe_or_unexpected_marketplace_source",
                            source,
                        )
                    resolved = root.joinpath(*pure.parts).resolve()
                    if root != resolved and root not in resolved.parents:
                        add(
                            findings,
                            root,
                            marketplace_path,
                            "marketplace_source_escapes_repository",
                        )

    if manifest is not None:
        if manifest.get("name") != "agentic-course-redesign":
            add(findings, root, plugin / "plugin.json", "manifest_name_mismatch")
        if manifest.get("version") != PACKAGE_VERSION:
            add(findings, root, plugin / "plugin.json", "manifest_version_mismatch")
        if manifest.get("skills") != "skills/":
            add(findings, root, plugin / "plugin.json", "skills_path_mismatch")
        if manifest.get("agents") != "agents/":
            add(findings, root, plugin / "plugin.json", "agents_path_mismatch")
        for key in sorted(FORBIDDEN_KEYS.intersection(manifest)):
            add(
                findings,
                root,
                plugin / "plugin.json",
                "forbidden_manifest_integration",
                key,
            )

    version_path = plugin / "VERSION"
    if (
        not version_path.is_file()
        or version_path.read_text(encoding="utf-8").strip() != PACKAGE_VERSION
    ):
        add(findings, root, version_path, "package_version_mismatch")

    skill_paths = sorted((plugin / "skills").glob("*/SKILL.md"))
    skill_map = {skill_name(path): path for path in skill_paths}
    if set(skill_map) != EXPECTED_SKILLS:
        add(
            findings,
            root,
            plugin / "skills",
            "skill_set_mismatch",
            repr(sorted(name for name in skill_map if name)),
        )
    for name in sorted(EXPECTED_SKILLS.intersection(skill_map)):
        source = root / "03_Shared_Workflow_Core" / "agent-skills" / name / "SKILL.md"
        expected = (
            source.read_text(encoding="utf-8").rstrip()
            + "\n\n"
            + COPILOT_CHOICE_CAPACITY_OVERRIDE
        ) if source.is_file() else ""
        installed = skill_map[name].read_text(encoding="utf-8").rstrip()
        if not source.is_file() or installed != expected:
            add(findings, root, skill_map[name], "canonical_skill_drift", name)

    scripts = {
        path.name: path for path in sorted((plugin / "scripts").glob("*.py"))
    }
    if set(scripts) != EXPECTED_SCRIPTS:
        add(findings, root, plugin / "scripts", "script_set_mismatch")
    for name in sorted(EXPECTED_SCRIPTS.intersection(scripts)):
        source = root / "03_Shared_Workflow_Core" / "scripts" / name
        if not source.is_file() or scripts[name].read_bytes() != source.read_bytes():
            add(findings, root, scripts[name], "canonical_script_drift", name)

    agent_paths = sorted((plugin / "agents").glob("*.agent.md"))
    agents = {
        path.name.removesuffix(".agent.md"): path for path in agent_paths
    }
    if set(agents) != EXPECTED_AGENTS:
        add(findings, root, plugin / "agents", "agent_set_mismatch")
    codex_agents = (
        root
        / "01_ChatGPT_Desktop_App"
        / "plugins"
        / "agentic-course-redesign"
        / "assets"
        / "project-template"
        / ".codex"
        / "agents"
    )
    for name in sorted(EXPECTED_AGENTS.intersection(agents)):
        parsed = split_agent(agents[name])
        if parsed is None:
            add(findings, root, agents[name], "invalid_agent_frontmatter")
            continue
        header, body = parsed
        allowed = {
            "name",
            "description",
            "tools",
            "disable-model-invocation",
            "user-invocable",
        }
        if set(header) != allowed:
            add(findings, root, agents[name], "unexpected_agent_frontmatter")
        source_path = codex_agents / f"{name}.toml"
        try:
            source = tomllib.loads(source_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError) as exc:
            add(findings, root, source_path, "invalid_agent_source", str(exc))
            continue
        if (
            header.get("name") != name
            or header.get("description") != source.get("description")
            or header.get("tools") != ["read", "search"]
            or header.get("disable-model-invocation") is not True
            or header.get("user-invocable") is not True
        ):
            add(findings, root, agents[name], "agent_boundary_mismatch")
        canonical_body = str(source.get("developer_instructions", "")).strip()
        replacement = COPILOT_AGENT_BODY_REPLACEMENTS.get(name)
        if replacement is not None:
            old, new = replacement
            if canonical_body.count(old) != 1:
                add(
                    findings,
                    root,
                    source_path,
                    "invalid_agent_source",
                    "Copilot replacement source phrase is missing or ambiguous",
                )
                continue
            canonical_body = canonical_body.replace(old, new, 1)
        expected_body = (
            canonical_body + "\n\n\n" + COPILOT_AGENT_DIALOGUE_SUFFIX
        )
        if body.strip() != expected_body:
            add(findings, root, agents[name], "agent_role_contract_drift")
        normalized_body = " ".join(body.split())
        for phrase in (
            "## Copilot lecturer-question boundary",
            "one unresolved consequential question at a time",
            "native `ask_user` card",
            "complete valid option set",
            "at least five explicit choices plus a custom-answer field",
            "observed capability, not a maximum",
            "Do not state or assume an unsupported maximum",
            "Never prune, hide or combine valid choices merely to fit a card.",
            "host rejects or cannot present the complete valid set",
            "every valid numbered option plus `Other`",
            "dependency chunks",
            "Keep every valid option visible across chunks",
            "never preselect",
            "uncertainty fails closed",
        ):
            if phrase not in normalized_body:
                add(
                    findings,
                    root,
                    agents[name],
                    "agent_dialogue_contract_missing",
                    phrase,
                )
        if name == "learning-designer":
            for phrase in (
                "present every materially distinct feasible option",
                "cluster long sets only by shared evidence or dependency while "
                "keeping every option visible",
                "Do not reopen a settled choice unless a newly surfaced conflict "
                "requires lecturer escalation",
            ):
                if phrase not in normalized_body:
                    add(
                        findings,
                        root,
                        agents[name],
                        "agent_dialogue_contract_missing",
                        phrase,
                    )

    dialogue_phrases = (
        "## Lecturer Decision Dialogue Contract",
        "Ask one unresolved",
        "Before using a native choice card",
        "live host tool contract",
        "complete, mutually exclusive option set",
        "custom-answer path without omission",
        "If a native card is unavailable or unsupported",
        "capacity is unknown",
        "every valid numbered option",
        "Never prune, hide or combine valid choices merely to fit a card.",
        "`Other - type your answer`",
        "Every valid option remains visible.",
        "keep every valid option visible",
        "## GitHub Copilot native `ask_user` capacity override",
        "complete valid option set",
        "at least five explicit choices plus a custom-answer field",
        "observed capability, not a maximum",
        "Do not state or assume an unsupported maximum",
        "host rejects or cannot present the complete valid set",
        "every valid numbered option plus `Other`",
        "dependency chunks",
        "keep every valid option visible across chunks",
        "split, merge, reorder or rename",
        "Preserve a custom answer exactly",
        "never preselected",
        "select only if true",
        "uncertainty fails closed",
        "skipped or blank response",
        "Exact authority gates",
    )
    for path in skill_paths:
        text = path.read_text(encoding="utf-8")
        normalized_text = " ".join(text.split())
        for phrase in dialogue_phrases:
            if phrase not in normalized_text:
                add(
                    findings,
                    root,
                    path,
                    "skill_dialogue_contract_missing",
                    phrase,
                )

    template = plugin / "assets" / "project-template"
    core_template = root / "03_Shared_Workflow_Core" / "course-project-template"
    for source in sorted(core_template.rglob("*")):
        if not source.is_file():
            continue
        target = template / source.relative_to(core_template)
        relative_source = source.relative_to(core_template).as_posix()
        if relative_source in {"AGENTS.md", "01_Control/GATES.md"}:
            expected = (
                source.read_text(encoding="utf-8").rstrip()
                + "\n\n"
                + COPILOT_CHOICE_CAPACITY_OVERRIDE
            )
            matches = target.is_file() and (
                target.read_text(encoding="utf-8").rstrip() == expected
            )
        else:
            matches = target.is_file() and target.read_bytes() == source.read_bytes()
        if not matches:
            add(
                findings,
                root,
                target,
                "canonical_project_template_drift",
            )
    for required in (
        template / ".github" / "copilot-instructions.md",
        template
        / ".github"
        / "instructions"
        / "course-redesign.instructions.md",
        plugin / "PARTICIPANT_QUICK_START.md",
        adapter / "PARTICIPANT_INSTALLATION.md",
    ):
        if not required.is_file():
            add(findings, root, required, "required_copilot_file_missing")

    interaction_surfaces = (
        adapter / "README.md",
        adapter / "CAPABILITIES.md",
        adapter / "PARTICIPANT_INSTALLATION.md",
        adapter / "overlay" / ".github" / "copilot-instructions.md",
        adapter
        / "overlay"
        / ".github"
        / "instructions"
        / "course-redesign.instructions.md",
        plugin / "README.md",
        plugin / "PARTICIPANT_QUICK_START.md",
        template / ".github" / "copilot-instructions.md",
        template
        / ".github"
        / "instructions"
        / "course-redesign.instructions.md",
    )
    for path in interaction_surfaces:
        if not path.is_file():
            add(findings, root, path, "required_copilot_file_missing")
            continue
        normalized = " ".join(path.read_text(encoding="utf-8").split()).casefold()
        for phrase in COPILOT_CARD_CAPACITY_PHRASES:
            if phrase not in normalized:
                add(
                    findings,
                    root,
                    path,
                    "copilot_card_capacity_contract_missing",
                    phrase,
                )
    if (template / ".codex").exists():
        add(findings, root, template / ".codex", "codex_host_files_forbidden")

    for path in sorted(plugin.rglob("*")):
        if not path.is_file():
            continue
        if path.name in FORBIDDEN_FILES:
            add(findings, root, path, "forbidden_runtime_config")
        if path.suffix.casefold() in {".md", ".json", ".py", ".txt"}:
            text = path.read_text(encoding="utf-8")
            windows_sep = re.escape(chr(92))
            absolute_user_pattern = (
                rf"(?i)\b[A-Z]:{windows_sep}Users{windows_sep}"
            )
            if re.search(absolute_user_pattern, text):
                add(findings, root, path, "absolute_windows_path_leak")

    participant = adapter / "PARTICIPANT_INSTALLATION.md"
    if participant.is_file():
        text = participant.read_text(encoding="utf-8")
        normalized_participant = " ".join(text.split())
        required_phrases = (
            "agentic-course-redesign@agentic-course-redesign-system",
            "copilot plugin marketplace add gpochs/Agentic-Course-Redesign-System",
            "Begin with Gate 0A only",
            "copilot plugin uninstall agentic-course-redesign",
            "without a support SLA",
            "Copilot 1.0.80 BYOK",
            "create_material_processing_eligibility.py",
            "expected function",
            "type=custom",
            "fresh task",
            "GitHub-hosted GPT-5.4",
            "default Claude model",
            "0.2.3-copilot.1",
            "native `ask_user` card",
            "complete valid option set",
            "at least five explicit choices plus a custom-answer field",
            "observed capability, not a maximum",
            "Do not state or assume an unsupported maximum",
            "Never prune, hide or combine valid choices merely to fit a card.",
            "host rejects or cannot present the complete valid set",
            "every valid numbered option plus `Other`",
            "dependency chunks",
            "Keep every valid option visible across chunks",
        )
        for phrase in required_phrases:
            if phrase not in normalized_participant:
                add(
                    findings,
                    root,
                    participant,
                    "participant_handoff_incomplete",
                    phrase,
                )
    for guide in (
        adapter / "PARTICIPANT_INSTALLATION.md",
        plugin / "PARTICIPANT_QUICK_START.md",
    ):
        if not guide.is_file():
            continue
        text = guide.read_text(encoding="utf-8")
        for phrase in (
            "--project <absolute project directory>",
            "derives",
            "01_Control/material-processing-eligibility.json",
            "redirected `01_Control`",
            "refuses overwrite",
        ):
            if phrase not in text:
                add(
                    findings,
                    root,
                    guide,
                    "gate0a_helper_handoff_inaccurate",
                    phrase,
                )
        if "absolute target ending in" in text:
            add(
                findings,
                root,
                guide,
                "gate0a_helper_handoff_inaccurate",
                "helper accepts a project directory, not an output-file target",
            )
    return findings


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ROOT
    findings = validate(root)
    if findings:
        print(json.dumps({"ok": False, "findings": findings}, indent=2))
        return 1
    print(
        "PASS: native GitHub Copilot plugin "
        f"{PACKAGE_VERSION}, six skills, ten agents, marketplace and "
        "participant handoff are fail-closed and source-consistent"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
