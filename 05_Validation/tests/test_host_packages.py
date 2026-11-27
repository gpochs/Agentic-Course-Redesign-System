"""Check complete native packages and their source boundaries."""

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("host_builder", ROOT / "02_Other_Agentic_Systems/build_host_package.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class HostPackageTests(unittest.TestCase):
    def test_generated_adapter_files_and_manifests_match_their_sources(self):
        script = builder.ADAPTERS / "00_Portable_Core_Adapter/validation/reconcile_adapters.py"
        preview = json.loads(subprocess.check_output([sys.executable, "-B", script], cwd=ROOT))
        self.assertEqual([], preview["mirror_changes"])
        self.assertEqual([], [name for name, changed in preview["manifest_changes"].items() if changed])

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
                    native = builder.ADAPTERS / builder.HOSTS[host] / "native-intake.md"
                    self.assertEqual(native.read_bytes(), (stages / builder.NATIVE_GUIDE).read_bytes())
                    self.assertIn("](native-intake.md)", (stages / builder.ROLE_GUIDE).read_text(encoding="utf-8"))
                    conversation = (stages / "course-redesign-orchestrator" / name).read_text(encoding="utf-8")
                    for phrase in ("1. Start with your course", "Kahoot!", "Mentimeter", "Skip for now",
                                   "multi-select", "The drafts are ready for handover."):
                        self.assertIn(phrase, conversation)
                    if portable:
                        guide = (base / "SKILL.md").read_text(encoding="utf-8")
                        self.assertIn("OpenCode and the project-only GitHub Copilot installation", guide)
                        self.assertIn("stages/course-redesign-<stage>/GUIDE.md", guide)
                    if host == "antigravity":
                        self.assertLessEqual(len(conversation.encode("utf-8")), 24000)
                        self.assertIn("](STAGES.md)", conversation)
                        rest = (stages / "course-redesign-orchestrator/STAGES.md").read_text(encoding="utf-8")
                        canonical = (builder.CORE / "agent-skills/course-redesign-orchestrator/SKILL.md").read_text(encoding="utf-8")
                        self.assertTrue(canonical.rstrip().endswith(rest.rstrip()))
                        self.assertIn("### Production declaration and handoff", rest)
                    self.assertEqual(
                        (builder.CORE / "scripts/validate_state.py").read_bytes(),
                        (base / "scripts/validate_state.py").read_bytes(),
                    )
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
