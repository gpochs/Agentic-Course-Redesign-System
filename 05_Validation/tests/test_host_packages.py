"""Check complete native packages and their source boundaries."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("host_builder", ROOT / "02_Other_Agentic_Systems/build_host_package.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class HostPackageTests(unittest.TestCase):
    def test_every_native_host_has_roles_guides_helpers_and_template(self):
        with tempfile.TemporaryDirectory() as temporary:
            for host in builder.HOSTS:
                with self.subTest(host=host):
                    target = Path(temporary) / host
                    builder.build(host, target)
                    portable = host in {"opencode", "copilot-project"}
                    base = target / "skills/course-redesign" if portable else target
                    stages = base / "stages" if portable else base / "skills"
                    name = "GUIDE.md" if portable else "SKILL.md"
                    self.assertEqual(6, len(list(stages.glob(f"*/{name}"))))
                    self.assertEqual(10, len(list((target / "agents").glob("*.md"))))
                    self.assertIn("--source-free", (stages / "course-redesign-setup" / name).read_text(encoding="utf-8"))
                    for guide in builder.NEW_GUIDES:
                        self.assertTrue((stages / guide).is_file())
                    self.assertTrue((base / "scripts/setup_course_project.py").is_file())
                    state = json.loads((base / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8"))
                    self.assertEqual(8, state["schema_version"])
                    self.assertFalse(list(target.rglob("__pycache__")))

    def test_unrelated_input_is_excluded_and_modified_export_is_rejected(self):
        import hashlib
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            src = root / "source"
            src.mkdir()
            sample = src / "published.md"
            sample.write_bytes(b"public sample")
            (src / "private-notes.md").write_bytes(b"unrelated")
            inventory = {"source/published.md": hashlib.sha256(sample.read_bytes()).hexdigest()}
            with patch.object(builder, "ROOT", root), patch.object(builder, "reviewed_files", return_value=inventory):
                target = root / "output"
                builder.copy_tree(src, target)
                self.assertEqual(["published.md"], [p.name for p in target.iterdir()])
                sample.write_bytes(b"edited")
                with self.assertRaisesRegex(ValueError, "digest mismatch"):
                    builder.copy_tree(src, target)

    def test_output_must_be_new_and_outside_the_source_tree(self):
        with self.assertRaises(ValueError):
            builder.build("claude", ROOT / "02_Other_Agentic_Systems" / "build-test")
        with tempfile.TemporaryDirectory() as existing:
            with self.assertRaises(FileExistsError):
                builder.build("antigravity", Path(existing))
