from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


VALIDATE_RELEASE = load_module(
    "validate_release_under_test", ROOT / "05_Validation" / "validate_release.py"
)
BUILD_RELEASE = load_module(
    "build_release_under_test", ROOT / "05_Validation" / "build_release.py"
)


class ReleaseValidationTests(unittest.TestCase):
    def make_archive(
        self,
        directory: Path,
        filename_version: str,
        inventory_version: str,
        *,
        inventory_updates: dict | None = None,
        raw_inventory: bytes | None = None,
    ) -> Path:
        archive_path = directory / f"Agentic-Course-Redesign-System_v{filename_version}.zip"
        member_name = "Agentic-Course-Redesign-System/README.md"
        member_data = b"synthetic fixture\n"
        inventory = {
            "schema_version": 1,
            "bundle_root_name": "Agentic-Course-Redesign-System",
            "version": inventory_version,
            "file_count": 1,
            "files": [
                {
                    "relative_path": "README.md",
                    "bytes": len(member_data),
                    "sha256": hashlib.sha256(member_data).hexdigest().upper(),
                }
            ],
        }
        if inventory_updates:
            inventory.update(inventory_updates)
        inventory_data = (
            raw_inventory
            if raw_inventory is not None
            else json.dumps(inventory).encode("utf-8")
        )
        with zipfile.ZipFile(archive_path, "w") as archive:
            archive.writestr(member_name, member_data)
            archive.writestr(
                "Agentic-Course-Redesign-System/package-inventory.json",
                inventory_data,
            )
        digest = hashlib.sha256(archive_path.read_bytes()).hexdigest().upper()
        archive_path.with_suffix(".sha256.txt").write_text(
            f"{digest}  {archive_path.name}\n", encoding="ascii"
        )
        return archive_path

    def run_validator(self, archive: Path, report: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(ROOT / "05_Validation" / "validate_release.py"),
                str(archive),
                "--expected-version",
                "0.2.2",
                "--report",
                str(report),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_matching_archive_inventory_report_and_expected_version_pass(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            archive = self.make_archive(directory, "0.2.2", "0.2.2")
            result = VALIDATE_RELEASE.validate(
                archive,
                expected_version="0.2.2",
                report_path=directory / "system-release-validation-v0.2.2.json",
            )
            self.assertTrue(result["pass"], result["findings"])
            self.assertEqual(result["release_version"], "0.2.2")
            self.assertEqual(result["inventory_version"], "0.2.2")

    def test_stale_inventory_version_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            archive = self.make_archive(Path(raw), "0.2.2", "0.2.1")
            result = VALIDATE_RELEASE.validate(archive, expected_version="0.2.2")
            self.assertFalse(result["pass"])
            self.assertIn(
                "inventory_archive_version_mismatch",
                {item["kind"] for item in result["findings"]},
            )

    def test_stale_report_name_fails(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            archive = self.make_archive(directory, "0.2.2", "0.2.2")
            result = VALIDATE_RELEASE.validate(
                archive,
                report_path=directory / "system-release-validation-v0.2.1.json",
            )
            self.assertFalse(result["pass"])
            self.assertIn(
                "report_archive_version_mismatch",
                {item["kind"] for item in result["findings"]},
            )

    def test_build_rejects_version_other_than_canonical_core(self):
        canonical = BUILD_RELEASE.current_version()
        wrong = "9.9.9" if canonical != "9.9.9" else "9.9.8"
        with self.assertRaisesRegex(ValueError, "canonical core version"):
            BUILD_RELEASE.build(wrong)

    def test_malformed_inventory_returns_structured_finding(self):
        with tempfile.TemporaryDirectory() as raw:
            archive = self.make_archive(
                Path(raw), "0.2.2", "0.2.2", raw_inventory=b"{not-json"
            )
            result = VALIDATE_RELEASE.validate(archive, expected_version="0.2.2")
            self.assertFalse(result["pass"])
            self.assertIn(
                "invalid_embedded_inventory_json",
                {item["kind"] for item in result["findings"]},
            )

    def test_inventory_schema_count_record_and_path_invariants_fail_closed(self):
        member_data = b"synthetic fixture\n"
        valid_record = {
            "relative_path": "README.md",
            "bytes": len(member_data),
            "sha256": hashlib.sha256(member_data).hexdigest().upper(),
        }
        cases = (
            ({"schema_version": 2}, "inventory_schema_version_mismatch"),
            ({"file_count": 99}, "inventory_file_count_mismatch"),
            ({"file_count": 1, "files": ["not-an-object"]}, "invalid_inventory_file_record"),
            ({"file_count": 0, "files": {}}, "invalid_inventory_file_records"),
            (
                {"file_count": 2, "files": [valid_record, dict(valid_record)]},
                "duplicate_inventory_relative_path",
            ),
            (
                {
                    "file_count": 1,
                    "files": [{**valid_record, "relative_path": "../README.md"}],
                },
                "unsafe_inventory_relative_path",
            ),
            (
                {
                    "file_count": 1,
                    "files": [{**valid_record, "bytes": "18", "sha256": "bad"}],
                },
                "invalid_inventory_byte_count",
            ),
        )
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            for updates, expected_kind in cases:
                with self.subTest(expected_kind=expected_kind):
                    archive = self.make_archive(
                        directory,
                        "0.2.2",
                        "0.2.2",
                        inventory_updates=updates,
                    )
                    result = VALIDATE_RELEASE.validate(archive, expected_version="0.2.2")
                    self.assertFalse(result["pass"])
                    kinds = {item["kind"] for item in result["findings"]}
                    self.assertIn(expected_kind, kinds)
                    if expected_kind == "invalid_inventory_byte_count":
                        self.assertIn("invalid_inventory_sha256", kinds)

    def test_cli_creates_new_versioned_report_exclusively(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            archive = self.make_archive(directory, "0.2.2", "0.2.2")
            report = directory / "system-release-validation-v0.2.2.json"
            completed = self.run_validator(archive, report)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertTrue(payload["pass"])
            self.assertTrue(payload["report_output_safe"])
            self.assertEqual(payload["archive"], archive.name)
            evidence = subprocess.run(
                [
                    sys.executable,
                    str(
                        ROOT
                        / "01_ChatGPT_Desktop_App"
                        / "validation"
                        / "validate_release_evidence.py"
                    ),
                    "--report",
                    str(report),
                    "--archive",
                    str(archive),
                    "--expected-version",
                    "0.2.2",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(evidence.returncode, 0, evidence.stdout + evidence.stderr)

    def test_cli_never_overwrites_archive_sidecar_inventory_source_or_report(self):
        with tempfile.TemporaryDirectory() as raw:
            directory = Path(raw)
            archive = self.make_archive(directory, "0.2.2", "0.2.2")
            sidecar = archive.with_suffix(".sha256.txt")
            inventory = directory / "package-inventory.json"
            source = directory / "README.md"
            existing_report = directory / "system-release-validation-v0.2.2.json"
            inventory.write_bytes(b"external inventory sentinel\n")
            source.write_bytes(b"source sentinel\n")
            existing_report.write_bytes(b"existing report sentinel\n")
            protected = (archive, sidecar, inventory, source, existing_report)
            expected = {path: path.read_bytes() for path in protected}

            for target in protected:
                with self.subTest(target=target.name):
                    completed = self.run_validator(archive, target)
                    self.assertNotEqual(completed.returncode, 0)
                    for path, content in expected.items():
                        self.assertEqual(path.read_bytes(), content, path)

    def test_report_output_refuses_non_dist_source_tree_path(self):
        with tempfile.TemporaryDirectory() as raw:
            archive = self.make_archive(Path(raw), "0.2.2", "0.2.2")
            proposed = ROOT / "system-release-validation-v0.2.2.json"
            findings = VALIDATE_RELEASE.validate_report_output_path(
                proposed, archive, "0.2.2"
            )
            self.assertIn(
                "report_output_inside_source_tree",
                {item["kind"] for item in findings},
            )


if __name__ == "__main__":
    unittest.main()
