from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from validate_native_plugin import DEFAULT_ROOT, validate


class NativePluginMutationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        copies = (
            ".github/plugin",
            "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/"
            "assets/project-template/.codex/agents",
            "02_Other_Agentic_Systems/01_GitHub_Copilot",
            "03_Shared_Workflow_Core/agent-skills",
            "03_Shared_Workflow_Core/scripts",
            "03_Shared_Workflow_Core/course-project-template",
        )
        for relative in copies:
            source = DEFAULT_ROOT / relative
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def kinds(self) -> set[str]:
        return {finding["kind"] for finding in validate(self.root)}

    def test_baseline_passes(self) -> None:
        self.assertEqual(validate(self.root), [])

    def test_source_escape_fails(self) -> None:
        path = self.root / ".github" / "plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["plugins"][0]["source"] = "../outside"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("unsafe_or_unexpected_marketplace_source", self.kinds())

    def test_forbidden_integration_fails(self) -> None:
        path = (
            self.root
            / "02_Other_Agentic_Systems"
            / "01_GitHub_Copilot"
            / "plugin"
            / "agentic-course-redesign"
            / "plugin.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        data["mcpServers"] = {".": {"command": "forbidden"}}
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("forbidden_manifest_integration", self.kinds())

    def test_forbidden_marketplace_integration_fails(self) -> None:
        path = self.root / ".github" / "plugin" / "marketplace.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["plugins"][0]["mcpServers"] = {
            "forbidden": {"command": "forbidden"}
        }
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("forbidden_marketplace_integration", self.kinds())

    def test_skill_drift_fails(self) -> None:
        path = (
            self.root
            / "02_Other_Agentic_Systems"
            / "01_GitHub_Copilot"
            / "plugin"
            / "agentic-course-redesign"
            / "skills"
            / "course-redesign-orchestrator"
            / "SKILL.md"
        )
        path.write_text(path.read_text("utf-8") + "\ndrift\n", encoding="utf-8")
        self.assertIn("canonical_skill_drift", self.kinds())

    def test_agent_tool_widening_fails(self) -> None:
        path = (
            self.root
            / "02_Other_Agentic_Systems"
            / "01_GitHub_Copilot"
            / "plugin"
            / "agentic-course-redesign"
            / "agents"
            / "course-mapper.agent.md"
        )
        text = path.read_text(encoding="utf-8").replace(
            'tools: ["read", "search"]',
            'tools: ["read", "search", "execute"]',
        )
        path.write_text(text, encoding="utf-8")
        self.assertIn("agent_boundary_mismatch", self.kinds())

    def test_package_version_drift_fails(self) -> None:
        path = (
            self.root
            / "02_Other_Agentic_Systems"
            / "01_GitHub_Copilot"
            / "plugin"
            / "agentic-course-redesign"
            / "plugin.json"
        )
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = "9.9.9"
        path.write_text(json.dumps(data), encoding="utf-8")
        self.assertIn("manifest_version_mismatch", self.kinds())


if __name__ == "__main__":
    unittest.main()
