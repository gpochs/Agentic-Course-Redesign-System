from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


VALIDATION_DIR = Path(__file__).resolve().parent
ADAPTER_ROOT = VALIDATION_DIR.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("antigravity_adapter_validator", VALIDATION_DIR / "validate_adapter.py")
installer = load_module(
    "antigravity_overlay_installer", ADAPTER_ROOT / "scripts" / "install_workspace_overlay.py"
)


class AdapterValidationTests(unittest.TestCase):
    def test_static_adapter_passes(self) -> None:
        result = validator.validate()
        self.assertTrue(result["ok"], result["errors"])

    def test_skill_frontmatter_is_discriminating(self) -> None:
        skills_root = ADAPTER_ROOT / "workspace-overlay" / ".agents" / "skills"
        for skill_dir in skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            frontmatter = validator.parse_frontmatter(skill_dir / "SKILL.md")
            self.assertEqual(frontmatter["name"], skill_dir.name)
            self.assertGreater(len(frontmatter["description"]), 20)

    def test_custom_agents_are_native_and_read_only(self) -> None:
        agents_root = ADAPTER_ROOT / "workspace-overlay" / ".agents" / "agents"
        self.assertEqual(
            {path.name for path in agents_root.glob("*.md")},
            set(validator.EXPECTED_AGENTS),
        )
        for filename, role in validator.EXPECTED_AGENTS.items():
            path = agents_root / filename
            frontmatter = validator.parse_agent_frontmatter(path)
            self.assertEqual(frontmatter["tools"], ["view_file", "grep_search"])
            self.assertFalse(frontmatter["mainAgent"])
            self.assertTrue(frontmatter["subagent"])
            self.assertEqual(frontmatter["commandExecutionPolicy"], "off")
            self.assertFalse(frontmatter["inheritMcp"])
            self.assertEqual(frontmatter["mcpServers"], [])
            self.assertEqual(frontmatter["plugins"], [])
            self.assertEqual(validator.validate_agent_definition(path, role), [])

    def test_write_capable_custom_agent_is_rejected(self) -> None:
        source = (
            ADAPTER_ROOT
            / "workspace-overlay"
            / ".agents"
            / "agents"
            / "course-mapper.md"
        ).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "course-mapper.md"
            path.write_text(
                source.replace("  - grep_search", "  - replace_file_content", 1),
                encoding="utf-8",
            )
            errors = validator.validate_agent_definition(path, "course_mapper")
            self.assertTrue(any("tools must be exactly" in item for item in errors))

    def test_secret_detector_catches_private_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "bad.txt").write_text(
                "-----BEGIN " + "PRIVATE KEY-----\nnot-a-real-key\n", encoding="utf-8"
            )
            findings = validator.find_secret_like_material(root)
            self.assertTrue(any(item.startswith("private-key:") for item in findings))

    def test_active_or_scheduled_state_is_rejected(self) -> None:
        state_path = ADAPTER_ROOT / "workspace-overlay" / "01_Control" / "state.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["status"] = "active"
        state["schedules"] = [{"id": "forbidden-test"}]
        errors = validator.validate_state_fields(state)
        self.assertTrue(any("candidate_not_active" in item for item in errors))
        self.assertTrue(any("no registered schedules" in item for item in errors))

    def test_installer_preview_apply_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "one" / "course" / "workspace"
            preview = installer.build_report(target)
            self.assertEqual(preview["mode"], "preview")
            self.assertFalse(target.exists())
            self.assertGreater(preview["planned_file_count"], 20)
            applied = installer.install(target, allow_nonempty=False)
            self.assertTrue(applied["installed"])
            self.assertEqual(applied["planned_file_count"], applied["verified_copy_count"])
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / ".agents" / "skills").is_dir())
            with self.assertRaises(FileExistsError):
                installer.install(target, allow_nonempty=False)

    def test_installer_refuses_home_and_adapter_targets(self) -> None:
        self.assertTrue(installer.target_is_forbidden(Path.home()))
        self.assertTrue(installer.target_is_forbidden(ADAPTER_ROOT / "nested"))


if __name__ == "__main__":
    unittest.main()
