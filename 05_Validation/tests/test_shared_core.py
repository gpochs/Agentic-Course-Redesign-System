from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SETUP_PATH = ROOT / "03_Shared_Workflow_Core" / "scripts" / "setup_course_project.py"


def load_setup_module():
    spec = importlib.util.spec_from_file_location("shared_setup", SETUP_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SharedCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.setup = load_setup_module()

    def test_documented_windows_target_is_not_dangerously_broad(self) -> None:
        target = Path(r"C:\CourseProjects\Biology\Year2")
        self.assertFalse(self.setup.target_is_dangerously_broad(target))

    def test_home_and_drive_root_are_rejected(self) -> None:
        self.assertTrue(self.setup.target_is_dangerously_broad(Path.home()))
        self.assertTrue(self.setup.target_is_dangerously_broad(Path(Path.cwd().anchor)))

    def test_preview_uses_shared_course_template(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "CourseProjects" / "Synthetic" / "Year2"
            report = self.setup.build_report(target)
            self.assertGreater(report["planned_file_count"], 10)
            self.assertFalse(report["would_overwrite"])
            self.assertTrue(str(report["template_root"]).endswith("course-project-template"))

    def test_shared_state_is_inactive_and_unscheduled(self) -> None:
        state = json.loads(
            (ROOT / "03_Shared_Workflow_Core" / "course-project-template" / "01_Control" / "state.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state["status"], "candidate_not_active")
        self.assertEqual(state["schedules"], [])


if __name__ == "__main__":
    unittest.main()

