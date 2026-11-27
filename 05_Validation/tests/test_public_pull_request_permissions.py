"""Regression checks for the workflow that executes contributions from forks."""
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


class PublicPullRequestPermissionsTests(unittest.TestCase):
    def test_validation_runs_unprivileged_on_contributed_code(self):
        source = (ROOT / ".github/workflows/validate.yml").read_text(encoding="utf-8")
        workflow = yaml.load(source, Loader=yaml.BaseLoader)
        self.assertIn("pull_request", workflow["on"])
        self.assertNotIn("pull_request_target", workflow["on"])
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertNotRegex(source, r"\bsecrets\s*[.\[]")
        for job in workflow["jobs"].values():
            self.assertEqual(job.get("permissions", workflow["permissions"]), {"contents": "read"})
            self.assertNotIn("self-hosted", str(job["runs-on"]))
            for step in job["steps"]:
                action = step.get("uses")
                if action and not action.startswith("./"):
                    with self.subTest(action=action):
                        self.assertIsNotNone(re.fullmatch(r"[^@]+@[0-9a-f]{40}", action))
                        if action.startswith("actions/checkout@"):
                            self.assertEqual(step.get("with", {}).get("persist-credentials"), "false")
