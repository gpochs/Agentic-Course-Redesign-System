from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CORE = Path(__file__).resolve().parents[1]
SCRIPT = CORE / "scripts" / "create_material_processing_eligibility.py"
SOURCE_MANIFEST = CORE / "scripts" / "source_manifest.py"


def load_source_manifest():
    spec = importlib.util.spec_from_file_location("_test_source_manifest", SOURCE_MANIFEST)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class EligibilityGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.project = Path(self.temporary.name) / "synthetic" / "one-course"
        (self.project / "01_Control").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def command(self, *extra: str, recorded_at: str = "2026-08-22T12:00:00+02:00") -> list[str]:
        return [
            sys.executable,
            str(SCRIPT),
            "--project",
            str(self.project.resolve()),
            "--eligibility-id",
            "ELIG-SYNTHETIC-001",
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
            "Synthetic authorised material in the declared local environment.",
            "--approved-processing-scope",
            "This synthetic one-course project only.",
            "--lecturer-declaration-reference",
            "synthetic-chat-receipt-001",
            "--recorded-at",
            recorded_at,
            *extra,
        ]

    def run_command(self, command: list[str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(command, check=False, capture_output=True, text=True)

    def test_preview_is_deterministic_and_writes_nothing(self) -> None:
        first = self.run_command(self.command())
        second = self.run_command(
            self.command(recorded_at="2026-08-22T13:00:00+02:00")
        )
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
        first_report = json.loads(first.stdout)
        second_report = json.loads(second.stdout)
        self.assertEqual(
            first_report["record"]["fingerprint"],
            second_report["record"]["fingerprint"],
        )
        self.assertFalse(first_report["created"])
        self.assertFalse(
            (self.project / "01_Control" / "material-processing-eligibility.json").exists()
        )

    def test_apply_creates_exact_valid_target_and_refuses_overwrite(self) -> None:
        first = self.run_command(self.command("--apply"))
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        target = self.project / "01_Control" / "material-processing-eligibility.json"
        self.assertTrue(target.is_file())
        source_manifest = load_source_manifest()
        self.assertTrue(source_manifest.validate_eligibility(target)["ok"])
        original = target.read_bytes()

        second = self.run_command(self.command("--apply"))
        self.assertNotEqual(second.returncode, 0)
        self.assertEqual(target.read_bytes(), original)
        self.assertEqual(
            sorted(path.name for path in (self.project / "01_Control").iterdir()),
            ["material-processing-eligibility.json"],
        )

    def test_personal_restricted_material_records_route_only(self) -> None:
        command = self.command()
        replacements = {
            "privately_owned_or_rightsholder_authorised": "institution_internal_or_restricted",
            "non_sensitive": "institution_internal_or_restricted",
        }
        command = [replacements.get(item, item) for item in command]
        flag_index = command.index("--contains-institution-internal-or-restricted-material")
        command[flag_index + 1] = "true"
        result = self.run_command(command)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["record"]["status"], "route_only")
        self.assertEqual(report["record"]["decision"]["outcome"], "route_only")
        self.assertFalse(report["source_intake_permitted"])
        self.assertFalse(
            (self.project / "01_Control" / "material-processing-eligibility.json").exists()
        )

    def test_refuses_dangerously_broad_project(self) -> None:
        command = self.command()
        project_index = command.index("--project")
        command[project_index + 1] = str(Path(self.project.anchor))
        result = self.run_command(command)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("dangerously broad", result.stdout)

    def test_refuses_redirected_control_directory_when_symlinks_are_supported(self) -> None:
        outside = Path(self.temporary.name) / "outside-control"
        outside.mkdir()
        control = self.project / "01_Control"
        control.rmdir()
        try:
            control.symlink_to(outside, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"directory symlinks are unavailable: {exc}")

        preview = self.run_command(self.command())
        self.assertNotEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertIn("redirected project control directory", preview.stdout)
        self.assertFalse(
            (outside / "material-processing-eligibility.json").exists()
        )

    def test_rejects_non_boolean_declaration_without_writing(self) -> None:
        command = self.command()
        flag_index = command.index("--contains-student-personal-data")
        command[flag_index + 1] = "unknown"
        result = self.run_command(command)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected exactly true or false", result.stderr)
        self.assertFalse(
            (self.project / "01_Control" / "material-processing-eligibility.json").exists()
        )

    def test_discovers_workspace_overlay_template_from_nested_skill(self) -> None:
        overlay = Path(self.temporary.name) / "adapter" / "workspace-overlay"
        nested_scripts = (
            overlay
            / ".agents"
            / "skills"
            / "course-redesign-setup"
            / "scripts"
        )
        nested_scripts.mkdir(parents=True)
        shutil.copy2(SCRIPT, nested_scripts / SCRIPT.name)
        shutil.copy2(SOURCE_MANIFEST, nested_scripts / SOURCE_MANIFEST.name)
        (overlay / "01_Control").mkdir()
        shutil.copy2(
            CORE
            / "course-project-template"
            / "01_Control"
            / "material-processing-eligibility.template.json",
            overlay / "01_Control" / "material-processing-eligibility.template.json",
        )
        command = self.command()
        command[1] = str(nested_scripts / SCRIPT.name)
        project_index = command.index("--project")
        command[project_index + 1] = str(overlay.resolve())
        result = self.run_command(command)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(
            report["relative_output"],
            "01_Control/material-processing-eligibility.json",
        )


if __name__ == "__main__":
    unittest.main()
