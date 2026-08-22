from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
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

PACKAGE_VERSION = "0.2.4-copilot.1"
BASE_VERSION = "0.2.4"
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
        self.assertEqual(
            adapter_manifest["native_plugin"]["rollback_package_version"],
            "0.2.3-copilot.1",
        )

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

    def test_all_six_skills_preserve_core_with_exact_copilot_override(self) -> None:
        installed = {
            skill_name(path): path
            for path in sorted((PLUGIN / "skills").glob("*/SKILL.md"))
        }
        self.assertEqual(set(installed), EXPECTED_SKILLS)
        for name, plugin_path in installed.items():
            canonical = CORE / "agent-skills" / name / "SKILL.md"
            expected = (
                canonical.read_text(encoding="utf-8").rstrip()
                + "\n\n"
                + COPILOT_CHOICE_CAPACITY_OVERRIDE
            )
            self.assertEqual(
                plugin_path.read_text(encoding="utf-8").rstrip(),
                expected,
                f"Copilot skill drift: {name}",
            )

    def test_all_helpers_are_byte_identical_to_canonical_core(self) -> None:
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

    def test_ten_agents_preserve_codex_role_contracts_and_dialogue_boundary(
        self,
    ) -> None:
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
            canonical_body = source["developer_instructions"].strip()
            replacement = COPILOT_AGENT_BODY_REPLACEMENTS.get(name)
            if replacement is not None:
                old, new = replacement
                self.assertEqual(canonical_body.count(old), 1)
                canonical_body = canonical_body.replace(old, new, 1)
            expected_body = (
                canonical_body + "\n\n\n" + COPILOT_AGENT_DIALOGUE_SUFFIX
            )
            self.assertEqual(
                body.strip(),
                expected_body,
                f"Copilot agent role-contract drift: {name}",
            )
            normalized_body = " ".join(body.split())
            self.assertIn("## Copilot lecturer-question boundary", normalized_body)
            self.assertIn(
                "one unresolved consequential question at a time", normalized_body
            )
            self.assertIn("native `ask_user` card", normalized_body)
            self.assertIn("complete valid option set", normalized_body)
            self.assertIn(
                "at least five explicit choices plus a custom-answer field",
                normalized_body,
            )
            self.assertIn("observed capability, not a maximum", normalized_body)
            self.assertIn(
                "Do not state or assume an unsupported maximum", normalized_body
            )
            self.assertIn(
                "Never prune, hide or combine valid choices merely to fit a card.",
                normalized_body,
            )
            self.assertIn(
                "host rejects or cannot present the complete valid set",
                normalized_body,
            )
            self.assertIn(
                "every valid numbered option plus `Other`", normalized_body
            )
            self.assertIn("dependency chunks", normalized_body)
            self.assertIn(
                "Keep every valid option visible across chunks", normalized_body
            )
            self.assertIn("never preselect", normalized_body)
            self.assertIn("uncertainty fails closed", normalized_body)
            if name == "learning-designer":
                self.assertNotIn("offer two or three feasible options", body)
                self.assertIn(
                    "present every materially distinct feasible option",
                    normalized_body,
                )
                self.assertIn(
                    "cluster long sets only by shared evidence or dependency while "
                    "keeping every option visible",
                    normalized_body,
                )
                self.assertIn(
                    "Do not reopen a settled choice unless a newly surfaced conflict "
                    "requires lecturer escalation",
                    normalized_body,
                )

    def test_project_template_mirrors_core_and_is_copilot_aware(self) -> None:
        template = PLUGIN / "assets" / "project-template"
        for source in sorted((CORE / "course-project-template").rglob("*")):
            if not source.is_file():
                continue
            relative = source.relative_to(CORE / "course-project-template")
            target = template / relative
            self.assertTrue(target.is_file(), f"missing template file: {relative}")
            if relative.as_posix() in {"AGENTS.md", "01_Control/GATES.md"}:
                expected = (
                    source.read_text(encoding="utf-8").rstrip()
                    + "\n\n"
                    + COPILOT_CHOICE_CAPACITY_OVERRIDE
                )
                self.assertEqual(
                    target.read_text(encoding="utf-8").rstrip(),
                    expected,
                    str(relative),
                )
            else:
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
        self.assertIn(
            "../../scripts/create_material_processing_eligibility.py", setup
        )

    def test_all_six_skills_enforce_shared_dialogue_contract(self) -> None:
        required = (
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
        for path in sorted((PLUGIN / "skills").glob("*/SKILL.md")):
            text = " ".join(path.read_text(encoding="utf-8").split())
            for phrase in required:
                self.assertIn(phrase, text, f"{path.name}: {phrase}")

    def _eligibility_command(self, project: Path) -> list[str]:
        helper = PLUGIN / "scripts" / "create_material_processing_eligibility.py"
        return [
            sys.executable,
            str(helper),
            "--project",
            str(project),
            "--eligibility-id",
            "ELIGIBILITY-TEST-001",
            "--environment-category",
            "personal_or_unmanaged",
            "--material-category",
            "privately_owned_or_rightsholder_authorised",
            "--ai-processing-authority-confirmed",
            "true",
            "--contains-institution-internal-or-restricted-material",
            "false",
            "--contains-student-personal-data",
            "false",
            "--sensitivity-classification",
            "non_sensitive",
            "--assessment-security-classification",
            "no_protected_assessment_material",
            "--assessment-security-handling-authorised",
            "true",
            "--decision-reason",
            "Lecturer declarations permit this scope.",
            "--approved-processing-scope",
            "One isolated course project.",
            "--lecturer-declaration-reference",
            "TEST-DECLARATION-001",
            "--recorded-at",
            "2026-08-22T12:00:00+02:00",
        ]

    def test_gate0a_helper_previews_applies_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary).resolve() / "course-project"
            (project / "01_Control").mkdir(parents=True)
            target = project / "01_Control" / "material-processing-eligibility.json"
            command = self._eligibility_command(project)

            preview = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            preview_data = json.loads(preview.stdout)
            self.assertEqual(preview_data["mode"], "preview")
            self.assertFalse(preview_data["created"])
            self.assertFalse(preview_data["would_overwrite"])
            self.assertEqual(Path(preview_data["output"]), target)
            self.assertFalse(target.exists())

            applied = subprocess.run(
                [*command, "--apply"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            applied_data = json.loads(applied.stdout)
            self.assertTrue(applied_data["created"])
            self.assertTrue(target.is_file())
            self.assertEqual(
                json.loads(target.read_text(encoding="utf-8")),
                preview_data["record"],
            )

            overwrite = subprocess.run(
                [*command, "--apply"], capture_output=True, text=True, encoding="utf-8"
            )
            self.assertNotEqual(overwrite.returncode, 0)
            self.assertIn("refusing to overwrite", overwrite.stdout)

    def test_gate0a_helper_rejects_ambiguous_relative_project_target(self) -> None:
        command = self._eligibility_command(Path("relative-course-project"))
        result = subprocess.run(
            command, capture_output=True, text=True, encoding="utf-8"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("project must be an absolute path", result.stdout)

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

    def test_adapter_docs_and_instructions_cover_dialogue_and_byok_path(self) -> None:
        instruction_paths = (
            ADAPTER / "overlay" / ".github" / "copilot-instructions.md",
            ADAPTER
            / "overlay"
            / ".github"
            / "instructions"
            / "course-redesign.instructions.md",
            PLUGIN
            / "assets"
            / "project-template"
            / ".github"
            / "copilot-instructions.md",
            PLUGIN
            / "assets"
            / "project-template"
            / ".github"
            / "instructions"
            / "course-redesign.instructions.md",
        )
        for path in instruction_paths:
            text = " ".join(path.read_text(encoding="utf-8").split())
            for phrase in (
                "one unresolved consequential question",
                "native `ask_user` card",
                "complete valid option set",
                "at least five explicit choices plus a custom-answer field",
                "observed capability, not a maximum",
                "unsupported maximum",
                "host rejects or cannot present the complete valid set",
                "every valid numbered option plus `Other`",
                "dependency chunks",
                "every valid option visible across chunks",
                "never preselect",
                "uncertainty fails closed",
                "blank or `Skip`",
                "authority gates",
            ):
                self.assertIn(phrase, text, f"{path}: {phrase}")

        interaction_surfaces = (
            ADAPTER / "README.md",
            ADAPTER / "CAPABILITIES.md",
            ADAPTER / "PARTICIPANT_INSTALLATION.md",
            PLUGIN / "README.md",
            PLUGIN / "PARTICIPANT_QUICK_START.md",
            *instruction_paths,
        )
        for path in interaction_surfaces:
            text = " ".join(path.read_text(encoding="utf-8").split()).casefold()
            for phrase in COPILOT_CARD_CAPACITY_PHRASES:
                self.assertIn(phrase, text, f"{path}: {phrase}")

        compatibility_paths = (
            ADAPTER / "README.md",
            ADAPTER / "CAPABILITIES.md",
            ADAPTER / "PARTICIPANT_INSTALLATION.md",
            PLUGIN / "README.md",
            PLUGIN / "PARTICIPANT_QUICK_START.md",
            instruction_paths[0],
            instruction_paths[2],
        )
        for path in compatibility_paths:
            text = " ".join(path.read_text(encoding="utf-8").split())
            for phrase in (
                "Copilot 1.0.80",
                "PowerShell/Python",
                "apply_patch",
                "expected function",
                "type=custom",
                "fresh task",
                "GitHub-hosted GPT-5.4",
                "default Claude",
            ):
                self.assertIn(phrase, text, f"{path}: {phrase}")

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
        normalized_guide = " ".join(guide.split())
        for phrase in (
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
        ):
            self.assertIn(phrase, normalized_guide)
        for path in (
            ADAPTER / "PARTICIPANT_INSTALLATION.md",
            PLUGIN / "PARTICIPANT_QUICK_START.md",
        ):
            text = " ".join(path.read_text(encoding="utf-8").split())
            for phrase in (
                "--project <absolute project directory>",
                "derives",
                "01_Control/material-processing-eligibility.json",
                "redirected `01_Control`",
                "refuses overwrite",
            ):
                self.assertIn(phrase, text, f"{path}: {phrase}")
            self.assertNotIn("absolute target ending in", text)


if __name__ == "__main__":
    unittest.main()
