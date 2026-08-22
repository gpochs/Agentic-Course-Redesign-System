from __future__ import annotations

import hashlib
import json
import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = ROOT / "02_Other_Agentic_Systems" / "01_GitHub_Copilot"
PLUGIN = ADAPTER / "plugin" / "agentic-course-redesign"
MARKETPLACE = ROOT / ".github" / "plugin" / "marketplace.json"
CORE = ROOT / "03_Shared_Workflow_Core"
CODEX_PLUGIN = (
    ROOT
    / "01_ChatGPT_Desktop_App"
    / "plugins"
    / "agentic-course-redesign"
)

PACKAGE_VERSION = "0.2.3-copilot.1"
BASE_VERSION = "0.2.3"
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
    "fingerprint_file.py",
    "migrate_state_v6_to_v7.py",
    "migrate_state_v7_to_v8.py",
    "setup_course_project.py",
    "source_manifest.py",
    "validate_state.py",
}
FORBIDDEN_MANIFEST_KEYS = {
    "apps",
    "mcpServers",
    "connectors",
    "hooks",
    "permissions",
    "authentication",
    "schedules",
    "lspServers",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def skill_name(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", text)
    if not match:
        raise AssertionError(f"missing skill name: {path}")
    return match.group(1)


def split_agent(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(r"---\n(.*?)\n---\n\n(.*)", text, flags=re.DOTALL)
    if not match:
        raise AssertionError(f"invalid agent frontmatter: {path}")
    header: dict[str, object] = {}
    for line in match.group(1).splitlines():
        key, value = line.split(":", 1)
        value = value.strip()
        if value in {"true", "false"}:
            header[key] = value == "true"
        elif value.startswith(("[", '"')):
            header[key] = json.loads(value)
        else:
            header[key] = value
    return header, match.group(2)


class CopilotPluginTests(unittest.TestCase):
    def test_copilot_package_does_not_reversion_the_semantic_base(self) -> None:
        self.assertEqual(
            (CORE / "VERSION").read_text(encoding="utf-8").strip(),
            BASE_VERSION,
        )
        codex_manifest = json.loads(
            (CODEX_PLUGIN / ".codex-plugin" / "plugin.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(codex_manifest["version"], BASE_VERSION)
        adapter_manifest = json.loads(
            (ADAPTER / "adapter-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(adapter_manifest["adapter_version"], BASE_VERSION)

    def test_marketplace_points_to_repository_relative_native_plugin(self) -> None:
        marketplace = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "agentic-course-redesign-system")
        self.assertEqual(marketplace["metadata"]["version"], PACKAGE_VERSION)
        self.assertEqual(len(marketplace["plugins"]), 1)
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "agentic-course-redesign")
        self.assertEqual(entry["version"], PACKAGE_VERSION)
        self.assertTrue(entry["strict"])
        self.assertEqual(
            entry["source"],
            "02_Other_Agentic_Systems/01_GitHub_Copilot/plugin/"
            "agentic-course-redesign",
        )
        self.assertTrue((ROOT / entry["source"] / "plugin.json").is_file())

    def test_plugin_manifest_is_native_and_declares_no_integration(self) -> None:
        manifest = json.loads((PLUGIN / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "agentic-course-redesign")
        self.assertEqual(manifest["version"], PACKAGE_VERSION)
        self.assertEqual(manifest["skills"], "skills/")
        self.assertEqual(manifest["agents"], "agents/")
        self.assertFalse(FORBIDDEN_MANIFEST_KEYS.intersection(manifest))
        self.assertNotIn("interface", manifest)
        self.assertEqual(
            (PLUGIN / "VERSION").read_text(encoding="utf-8").strip(),
            PACKAGE_VERSION,
        )

    def test_all_six_skills_are_byte_identical_to_canonical_core(self) -> None:
        installed = {
            skill_name(path): path
            for path in sorted((PLUGIN / "skills").glob("*/SKILL.md"))
        }
        self.assertEqual(set(installed), EXPECTED_SKILLS)
        for name, plugin_path in installed.items():
            canonical = CORE / "agent-skills" / name / "SKILL.md"
            self.assertEqual(
                sha256(plugin_path),
                sha256(canonical),
                f"Copilot skill drift: {name}",
            )

    def test_all_six_helpers_are_byte_identical_to_canonical_core(self) -> None:
        installed = {
            path.name: path for path in sorted((PLUGIN / "scripts").glob("*.py"))
        }
        self.assertEqual(set(installed), EXPECTED_SCRIPTS)
        for name, plugin_path in installed.items():
            self.assertEqual(
                sha256(plugin_path),
                sha256(CORE / "scripts" / name),
                f"Copilot helper drift: {name}",
            )

    def test_ten_agents_preserve_codex_role_contracts(self) -> None:
        installed = {
            path.name.removesuffix(".agent.md"): path
            for path in sorted((PLUGIN / "agents").glob("*.agent.md"))
        }
        self.assertEqual(set(installed), EXPECTED_AGENTS)
        source_dir = (
            CODEX_PLUGIN / "assets" / "project-template" / ".codex" / "agents"
        )
        for name, plugin_path in installed.items():
            source = tomllib.loads((source_dir / f"{name}.toml").read_text("utf-8"))
            header, body = split_agent(plugin_path)
            self.assertEqual(header["name"], name)
            self.assertEqual(header["description"], source["description"])
            self.assertEqual(header["tools"], ["read", "search"])
            self.assertTrue(header["disable-model-invocation"])
            self.assertTrue(header["user-invocable"])
            self.assertEqual(body.strip(), source["developer_instructions"].strip())

    def test_project_template_mirrors_core_and_is_copilot_aware(self) -> None:
        template = PLUGIN / "assets" / "project-template"
        for source in sorted((CORE / "course-project-template").rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(CORE / "course-project-template")
            target = template / relative
            self.assertTrue(target.is_file(), f"missing template file: {relative}")
            self.assertEqual(sha256(target), sha256(source), str(relative))
        self.assertTrue((template / ".github" / "copilot-instructions.md").is_file())
        self.assertTrue(
            (
                template
                / ".github"
                / "instructions"
                / "course-redesign.instructions.md"
            ).is_file()
        )
        self.assertFalse((template / ".codex").exists())

    def test_setup_skill_references_resolve_inside_package(self) -> None:
        self.assertTrue((PLUGIN / "PARTICIPANT_QUICK_START.md").is_file())
        self.assertTrue((PLUGIN / "scripts" / "setup_course_project.py").is_file())
        setup = (
            PLUGIN / "skills" / "course-redesign-setup" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("../../PARTICIPANT_QUICK_START.md", setup)
        self.assertIn("../../scripts/setup_course_project.py", setup)

    def test_package_contains_no_host_leak_or_forbidden_runtime_config(self) -> None:
        forbidden_names = {
            ".mcp.json",
            "hooks.json",
            "lsp.json",
            "mcp.json",
            "openai.yaml",
            "config.toml",
        }
        for path in PLUGIN.rglob("*"):
            if not path.is_file():
                continue
            self.assertNotIn(path.name, forbidden_names, str(path))
            if path.suffix.lower() in {".md", ".json", ".py", ".txt"}:
                text = path.read_text(encoding="utf-8")
                windows_sep = re.escape(chr(92))
                absolute_user_pattern = (
                    rf"(?i)\b[A-Z]:{windows_sep}Users{windows_sep}"
                )
                self.assertNotRegex(
                    text,
                    absolute_user_pattern,
                    f"absolute Windows path leaked in {path}",
                )

    def test_participant_handoff_has_install_start_remove_and_support_boundary(
        self,
    ) -> None:
        guide = (ADAPTER / "PARTICIPANT_INSTALLATION.md").read_text("utf-8")
        self.assertIn(
            "agentic-course-redesign@agentic-course-redesign-system", guide
        )
        self.assertIn(
            "copilot plugin marketplace add "
            "gpochs/Agentic-Course-Redesign-System",
            guide,
        )
        self.assertIn("Begin with Gate 0A only", guide)
        self.assertIn("copilot plugin uninstall agentic-course-redesign", guide)
        self.assertIn("without a support SLA", guide)


if __name__ == "__main__":
    unittest.main()
