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
            "antigravity": ("Walkthrough", "Artifacts"),
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
                    heading = "Step 10 · Would you like a second opinion?"
                    self.assertEqual(guide.count(heading), 1)
                    section = guide.partition(heading)[2].split("\n##", 1)[0]
                    for term in (*expected, "Skip", "Prepare a review", "Send this packet",
                                 "original", "account", "model", "audience", "cost", "slide"):
                        self.assertIn(term, section)
