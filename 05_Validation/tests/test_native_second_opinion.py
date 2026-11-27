"""Exercise each installed host guide through its native package layout."""

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "native_review_builder", ROOT / "02_Other_Agentic_Systems/build_host_package.py"
)
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class NativeSecondOpinionTests(unittest.TestCase):
    def test_built_native_review_has_the_host_route_and_final_teacher_choice(self):
        features = {
            "claude": ("Side chat", "Computer use"),
            "opencode": ("Review", "OpenCode Browse"),
            "antigravity": ("Walkthrough", "Artifacts", "empty workspace", "verify the reviewer’s file and tool access", "manual text-only handover"),
            "copilot": ("Canvas", "Computer Use"),
            "copilot-project": ("Canvas", "Computer Use"),
        }
        with tempfile.TemporaryDirectory() as directory:
            for host, expected in features.items():
                with self.subTest(host=host):
                    target = Path(directory) / host
                    builder.build(host, target)
                    guides = list(target.rglob("native-intake.md"))
                    self.assertEqual(len(guides), 1)
                    source = builder.ADAPTERS / builder.HOSTS[host] / "native-intake.md"
                    self.assertEqual(source.read_bytes(), guides[0].read_bytes())
                    guide = guides[0].read_text(encoding="utf-8")
                    selection = guide.partition("Model choice for this course")[2].split("\n##", 1)[0]
                    for mode in ("Match models to tasks", "Keep the current model", "Choose at each step"):
                        self.assertIn(mode, selection)
                    self.assertIn("](model-plan.md)", selection)
                    self.assertTrue(guides[0].with_name("model-plan.md").is_file())
                    self.assertIn("](tool-fit.md)", selection)
                    self.assertTrue(guides[0].with_name("tool-fit.md").is_file())
                    host_controls = {
                        "claude": ("Agent", "/tasks"),
                        "opencode": ("provider/model#variant", "subagent"),
                        "antigravity": ("inherit", "flash", "pro"),
                        "copilot": ("task", "Auto", "Fusion"),
                        "copilot-project": ("task", "Auto", "Fusion"),
                    }
                    for control in host_controls[host]:
                        self.assertIn(control, selection)
                    for agent in (target / "agents").glob("*.md"):
                        frontmatter = agent.read_text(encoding="utf-8").split("---", 2)[1]
                        for line in frontmatter.splitlines():
                            if line.startswith("model:"):
                                self.assertEqual(line, "model: inherit")
                    heading = "Step 10 · Would you like a second opinion?"
                    self.assertEqual(guide.count(heading), 1)
                    section = guide.partition(heading)[2].split("\n##", 1)[0]
                    for term in (*expected, "Skip", "Prepare a review", "Explore a different model", "Send this packet",
                                 "original", "account", "model", "audience", "cost", "slide",
                                 "unused family", "least-involved family", "limited second look",
                                 "same-model self-check"):
                        self.assertIn(term, section)
