from __future__ import annotations

import csv
import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


PLUGIN = Path(__file__).resolve().parent.parent


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, PLUGIN / relative)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


setup = load("setup_course_project", "scripts/setup_course_project.py")
manifest = load("source_manifest", "scripts/source_manifest.py")
state_validator = load("validate_state", "scripts/validate_state.py")
fingerprinter = load("fingerprint_file", "scripts/fingerprint_file.py")


class SetupTests(unittest.TestCase):
    def test_documented_windows_target_and_broad_target_refusal(self):
        system_root = PLUGIN.parents[1]
        guide = (system_root / "PORTABLE_SETUP_WINDOWS.md").read_text(encoding="utf-8")
        documented = r"C:\CourseProjects\Biology\Year2"
        self.assertIn(documented, guide)
        self.assertTrue(setup.target_is_dangerously_broad(Path.home()))
        with self.assertRaises(ValueError):
            setup.install(Path.home(), allow_nonempty=False)
        if os.name == "nt":
            self.assertFalse(setup.target_is_dangerously_broad(Path(documented)))

    def test_preview_apply_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "OneCourse"
            preview = setup.build_report(target)
            self.assertFalse(preview["would_overwrite"])
            self.assertGreater(preview["planned_file_count"], 10)
            result = setup.install(target, allow_nonempty=False)
            self.assertTrue(result["installed"])
            self.assertEqual(json.loads((target / "01_Control/state.json").read_text())["status"], "candidate_not_active")
            second = setup.build_report(target)
            self.assertTrue(second["would_overwrite"])
            with self.assertRaises(FileExistsError):
                setup.install(target, allow_nonempty=True)

    def test_nonempty_requires_explicit_flag(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "OneCourse"
            target.mkdir()
            (target / "lecturer-note.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                setup.install(target, allow_nonempty=False)
            result = setup.install(target, allow_nonempty=True)
            self.assertTrue(result["installed"])
            self.assertEqual((target / "lecturer-note.txt").read_text(), "keep")

    def test_allow_nonempty_is_documented_as_conditional_and_never_overwrites(self):
        system_root = PLUGIN.parents[1]
        guide = (system_root / "PORTABLE_SETUP_WINDOWS.md").read_text(encoding="utf-8")
        self.assertIn("--allow-nonempty", guide)
        self.assertIn("does not permit overwriting", guide)


class ManifestTests(unittest.TestCase):
    def test_create_verify_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "Course"
            (project / "00_Source_Materials").mkdir(parents=True)
            (project / "00_Context").mkdir()
            (project / "00_Source_Materials/workbook.txt").write_text("course", encoding="utf-8")
            (project / "00_Source_Materials/test_answer_key.txt").write_text("secret", encoding="utf-8")
            (project / "00_Context/policy.txt").write_text("policy", encoding="utf-8")
            path = Path("01_Control/source-hashes.csv")
            created = manifest.create(project, path, replace=False)
            self.assertTrue(created["ok"])
            verified = manifest.verify(project, path)
            self.assertTrue(verified["ok"])
            with (project / path).open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            key = next(row for row in rows if "answer_key" in row["relative_path"])
            self.assertEqual(key["audience_classification"], "lecturer_only_candidate")
            (project / "00_Source_Materials/workbook.txt").write_text("coursf", encoding="utf-8")
            failed = manifest.verify(project, path)
            self.assertFalse(failed["ok"])
            self.assertIn("hash-mismatch", {item["status"] for item in failed["results"]})


class StateTests(unittest.TestCase):
    def test_template_state_fail_closed_invariants(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state_validator.validate(state), [])
        state["standing_schedule_contract_template"]["no_immediate_run"] = False
        self.assertIn(
            "standing schedule must forbid immediate runs", state_validator.validate(state)
        )

    def test_retry_and_stage_a_regressions_fail(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        state["run_template"]["retry_policy"]["max_retries_per_specialist_per_stage"] = 2
        state["run_template"]["coordination"]["stage_a_role_statuses"].pop()
        errors = state_validator.validate(state)
        self.assertIn("retry ceiling must be exactly one per specialist per stage", errors)
        self.assertIn("Stage A must track exactly all five core roles", errors)

    def test_schedule_skill_and_research_folder_regressions_fail(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        standing = state["standing_schedule_contract_template"]
        standing["runtime_versions"]["skill_name"] = "course-redesign"
        standing["unique_output_naming_rule"] = "new_unique_dated_02_Research_folder"
        errors = state_validator.validate(state)
        self.assertIn("standing schedule must invoke course-redesign-orchestrator", errors)
        self.assertIn(
            "scheduled research output must use a unique dated 03_Research run folder",
            errors,
        )

    def test_gate_2b_research_and_gate_3_material_target_boundaries(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        approvals = state["run_template"]["approvals"]
        approvals["gate_2b"]["status"] = "approved"
        approvals["gate_2b"]["approved_research_targets"] = [
            {
                "target_type": "research_dossier",
                "relative_path": "03_Research/2030-01-02_RUN-001/Research_Dossier.md",
            },
            {
                "target_type": "research_handoff",
                "relative_path": "03_Research/2030-01-02_RUN-001/Research_Handoff.md",
            },
        ]
        approvals["gate_3"]["status"] = "approved"
        approvals["gate_3"]["approved_material_targets"] = [
            {
                "target_type": "working_copy",
                "relative_path": "04_Working_Copies/RUN-001/Workbook.docx",
            },
            {
                "target_type": "approved_release",
                "relative_path": "05_Approved/RUN-001/Workbook.docx",
            },
        ]
        self.assertEqual(state_validator.validate(state), [])
        approvals["gate_2b"]["approved_research_targets"][0]["relative_path"] = (
            "04_Working_Copies/RUN-001/Research_Dossier.md"
        )
        approvals["gate_3"]["approved_material_targets"][0]["relative_path"] = (
            "03_Research/2030-01-02_RUN-001/Workbook.docx"
        )
        errors = state_validator.validate(state)
        self.assertTrue(any("Gate 2B research target 0" in item for item in errors))
        self.assertIn("Gate 3 material target 0 violates its required prefix", errors)

    def test_each_skill_default_prompt_explicitly_invokes_itself(self):
        skill_root = PLUGIN / "skills"
        skill_names = sorted(path.name for path in skill_root.iterdir() if path.is_dir())
        self.assertEqual(len(skill_names), 6)
        for skill_name in skill_names:
            metadata = (skill_root / skill_name / "agents/openai.yaml").read_text(
                encoding="utf-8"
            )
            self.assertIn(f"${skill_name}", metadata, skill_name)


class DistributionTests(unittest.TestCase):
    def test_v020_manifest_and_marketplace_metadata(self):
        system_root = PLUGIN.parents[1]
        plugin_manifest = json.loads(
            (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (system_root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        interface = plugin_manifest["interface"]
        self.assertEqual(plugin_manifest["version"], "0.2.0")
        self.assertEqual(
            plugin_manifest["repository"],
            "https://github.com/gpochs/Agentic-Course-Redesign-System",
        )
        self.assertEqual(interface["category"], "Education & Research")
        self.assertLessEqual(len(interface["displayName"]), 30)
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertEqual(len(interface["defaultPrompt"]), 3)
        self.assertTrue(all("@" not in item and len(item) <= 128 for item in interface["defaultPrompt"]))
        self.assertTrue((PLUGIN / interface["logo"].removeprefix("./")).is_file())
        self.assertTrue((PLUGIN / interface["composerIcon"].removeprefix("./")).is_file())
        self.assertEqual(marketplace["name"], "agentic-course-redesign-system")
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/agentic-course-redesign")
        self.assertEqual(marketplace["plugins"][0]["policy"]["authentication"], "ON_INSTALL")

    def test_public_source_is_skills_only_and_matches_runtime(self):
        system_root = PLUGIN.parents[1]
        public = system_root / "openai-submission/source/agentic-course-redesign"
        self.assertFalse((public / ".mcp.json").exists())
        self.assertFalse((public / ".app.json").exists())
        self.assertFalse((public / "hooks").exists())
        self.assertFalse((public / "tests").exists())
        self.assertEqual(
            json.loads((public / ".codex-plugin/plugin.json").read_text(encoding="utf-8")),
            json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")),
        )
        for relative in ("assets", "scripts", "skills"):
            custom_files = {
                path.relative_to(PLUGIN / relative).as_posix(): path.read_bytes()
                for path in (PLUGIN / relative).rglob("*")
                if path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix != ".pyc"
            }
            public_files = {
                path.relative_to(public / relative).as_posix(): path.read_bytes()
                for path in (public / relative).rglob("*")
                if path.is_file()
                and "__pycache__" not in path.parts
                and path.suffix != ".pyc"
            }
            self.assertEqual(custom_files, public_files, relative)

    def test_review_material_minimums_and_owner_placeholders(self):
        system_root = PLUGIN.parents[1]
        review = system_root / "openai-submission/review"
        cases = json.loads((review / "test-cases.json").read_text(encoding="utf-8"))
        prompts = json.loads((review / "starter-prompts.json").read_text(encoding="utf-8"))
        checklist = (review / "LISTING_METADATA_CHECKLIST.md").read_text(encoding="utf-8")
        self.assertGreaterEqual(len(cases["positive_cases"]), 5)
        self.assertGreaterEqual(len(cases["negative_cases"]), 3)
        self.assertEqual(len(prompts["prompts"]), 3)
        for marker in (
            "[VERIFIED_PUBLISHER_NAME]",
            "[PUBLIC_WEBSITE_HTTPS_URL]",
            "[PUBLIC_SUPPORT_HTTPS_URL]",
            "[PUBLIC_PRIVACY_POLICY_HTTPS_URL]",
            "[PUBLIC_TERMS_HTTPS_URL]",
            "[SUPPORTED_COUNTRIES_OR_REGIONS]",
        ):
            self.assertIn(marker, checklist)

    def test_template_version_matches_plugin(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        manifest_data = json.loads(
            (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(state["plugin_version"], manifest_data["version"])


class FingerprintTests(unittest.TestCase):
    def test_policy_fingerprint_is_canonical_and_excludes_approval_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.json"
            second = Path(temporary) / "second.json"
            first.write_text(
                '{"policy_version":1,"per_source_entries":[],"fingerprint":"OLD",'
                '"lecturer_decision":"approved","approved_at":"now"}',
                encoding="utf-8",
            )
            second.write_text(
                '{\n  "approved_at": "later", "lecturer_decision": null, '
                '"per_source_entries": [], "policy_version": 1, "fingerprint": null\n}',
                encoding="utf-8",
            )
            digest_one, payload_one = fingerprinter.fingerprint(first, "policy")
            digest_two, payload_two = fingerprinter.fingerprint(second, "policy")
            self.assertEqual(digest_one, digest_two)
            self.assertEqual(payload_one, payload_two)
            self.assertNotIn(b"approved_at", payload_one)
            self.assertNotIn(b"fingerprint", payload_one)

    def test_raw_fingerprint_changes_with_formatting(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.json"
            second = Path(temporary) / "second.json"
            first.write_text('{"a":1}', encoding="utf-8")
            second.write_text('{ "a": 1 }', encoding="utf-8")
            self.assertNotEqual(
                fingerprinter.fingerprint(first, "raw")[0],
                fingerprinter.fingerprint(second, "raw")[0],
            )


if __name__ == "__main__":
    unittest.main()
