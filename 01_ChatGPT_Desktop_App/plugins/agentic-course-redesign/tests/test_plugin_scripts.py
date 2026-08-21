from __future__ import annotations

import csv
import copy
import importlib.util
import json
import os
import subprocess
import sys
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


def load_path(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


setup = load("setup_course_project", "scripts/setup_course_project.py")
manifest = load("source_manifest", "scripts/source_manifest.py")
state_validator = load("validate_state", "scripts/validate_state.py")
migration = load("migrate_state_v6_to_v7", "scripts/migrate_state_v6_to_v7.py")
fingerprinter = load("fingerprint_file", "scripts/fingerprint_file.py")
release_evidence = load_path(
    "validate_release_evidence",
    PLUGIN.parents[1] / "validation/validate_release_evidence.py",
)


def downgrade_v7_to_v6(state: dict) -> dict:
    result = copy.deepcopy(state)
    result["schema_version"] = 6
    result["plugin_version"] = "0.2.1"
    result.pop("umbrella_entry_routing")
    result.pop("schema_compatibility")
    for run in [result["run_template"], *result["runs"]]:
        run["approvals"].pop("hitl_3")
        run["approvals"].pop("system_improvement_review_offer")
        run.pop("resume_protocol")
        rules = run["manual_stage_authority"]["transition_rules"]
        first = next(
            index
            for index, rule in enumerate(rules)
            if rule["trigger"] == "fresh_hitl3_acceptance_after_verified_production_handoff"
        )
        rules[first : first + 2] = [
            {
                "trigger": "fresh_hitl3_acceptance_and_system_review_request_after_verified_production_handoff",
                "authorises_through": "SYSTEM_GATE",
                "purpose": "reusable_system_proposal_and_system_gate_only",
                "does_not_authorise_candidate_activation": True,
            }
        ]
    activation = result["activation"]
    activation["required_before_active"] = [
        item
        for item in activation["required_before_active"]
        if item not in {"hitl_3_accepted", "system_improvement_review_offer_requested"}
    ]
    update = activation["system_update"]
    update.pop("allowed_statuses")
    update.pop("prerequisites")
    update["completed_reply_requirements"] = [
        item
        for item in update["completed_reply_requirements"]
        if item not in {"run_id", "system_improvement_review_offer_reference"}
    ]
    update["approval"].pop("run_id")
    update["approval"].pop("system_improvement_review_offer_reference")
    return result


def completed_run_state(template: dict) -> tuple[dict, dict]:
    state = copy.deepcopy(template)
    run = copy.deepcopy(state["run_template"])
    run.update(
        {
            "template_only": False,
            "run_id": "RUN-SYNTHETIC-001",
            "task_chat_reference": "TASK-SYNTHETIC-001",
            "status": "waiting_at_gate",
            "current_gate": "SYSTEM_GATE",
            "plan_version": 3,
        }
    )
    run["contract"].update(
        {
            "status": "approved",
            "contract_id": "RC-SYNTHETIC-001",
            "version": 1,
            "source_access_policy_version": "SAP-SYNTHETIC-v1",
            "source_access_policy_fingerprint": "POLICY-FINGERPRINT-001",
        }
    )
    run["shared_context"].update(
        {
            "version": 2,
            "source_access_policy_version": "SAP-SYNTHETIC-v1",
            "source_access_policy_fingerprint": "POLICY-FINGERPRINT-001",
        }
    )
    run["source_manifest_verification"].update(
        {
            "source_manifest_fingerprint": "MANIFEST-FINGERPRINT-001",
            "source_access_policy_version": "SAP-SYNTHETIC-v1",
            "source_access_policy_fingerprint": "POLICY-FINGERPRINT-001",
            "status": "passed",
            "verified_at": "2026-08-21T10:00:00Z",
        }
    )
    lineage = {
        "run_id": run["run_id"],
        "run_contract_id": run["contract"]["contract_id"],
        "run_contract_version": run["contract"]["version"],
        "task_chat_reference": run["task_chat_reference"],
        "shared_context_version": run["shared_context"]["version"],
        "source_manifest_fingerprint": run["source_manifest_verification"][
            "source_manifest_fingerprint"
        ],
        "source_access_policy_version": run["source_manifest_verification"][
            "source_access_policy_version"
        ],
        "source_access_policy_fingerprint": run["source_manifest_verification"][
            "source_access_policy_fingerprint"
        ],
        "plan_version": run["plan_version"],
    }
    production = run["approvals"]["production_completion"]
    production["status"] = "complete"
    production["declaration"]["completed_reply"].update(
        {
            **lineage,
            "standalone_line": "DECLARE PRODUCTION COMPLETE",
            "reply_reference": "REPLY-PRODUCTION-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:01:00Z",
        }
    )
    handoff_target = "04_Working_Copies/RUN-SYNTHETIC-001/Production_Handoff.md"
    production["handoff_approval"]["exact_handoff_target"] = handoff_target
    production["handoff_approval"]["completed_reply"].update(
        {
            **lineage,
            "repeated_exact_handoff_target": handoff_target,
            "standalone_line": "APPROVE PRODUCTION HANDOFF",
            "reply_reference": "REPLY-HANDOFF-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:02:00Z",
        }
    )
    production["handoff_verified_at"] = "2026-08-21T10:03:00Z"
    hitl3 = run["approvals"]["hitl_3"]
    hitl3["status"] = "accepted"
    hitl3["decision"].update(
        {
            **lineage,
            "decision": "accept",
            "final_acceptance_reference": "HITL3-ACCEPT-001",
            "reply_reference": "REPLY-HITL3-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:04:00Z",
        }
    )
    offer_gate = run["approvals"]["system_improvement_review_offer"]
    offer_gate["status"] = "requested"
    offer_gate["offer"].update(
        {
            "offer_id": "system-review-offer:RUN-SYNTHETIC-001:HITL3-ACCEPT-001",
            **lineage,
            "hitl_3_final_acceptance_reference": "HITL3-ACCEPT-001",
            "question_scope_presented": copy.deepcopy(migration.REQUIRED_SYSTEM_REVIEW_SCOPE),
            "question_text": migration.MANDATORY_SYSTEM_REVIEW_QUESTION,
            "offer_reference": "OFFER-001",
            "offered_at": "2026-08-21T10:05:00Z",
            "validation_status": "passed",
        }
    )
    offer_gate["response"].update(
        {
            **lineage,
            "decision": "request_read_only_system_improvement_review_and_versioned_proposal",
            "reply_reference": "REPLY-OFFER-001",
            "responded_at": "2026-08-21T10:06:00Z",
            "validation_status": "passed",
        }
    )
    state["active_run_id"] = run["run_id"]
    state["runs"] = [run]
    return state, run


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

    def test_schema_7_records_match_canonical_migration_shapes(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        run = state["run_template"]
        self.assertEqual(state["schema_version"], 7)
        self.assertEqual(state["plugin_version"], "0.2.2")
        self.assertEqual(state["umbrella_entry_routing"], migration.umbrella_entry_routing())
        self.assertEqual(run["approvals"]["hitl_3"], migration.hitl3_record())
        self.assertEqual(
            run["approvals"]["system_improvement_review_offer"],
            migration.system_improvement_review_offer_record(),
        )
        self.assertEqual(run["resume_protocol"], migration.resume_protocol())
        self.assertIn(
            "schedule_contracts",
            run["approvals"]["system_improvement_review_offer"]["required_question_scope"],
        )

    def test_v6_migration_preview_is_non_mutating_and_valid(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        source = downgrade_v7_to_v6(state)
        source["run_template"]["contract"]["permitted_tools"] = ["local_read_only"]
        before = copy.deepcopy(source)
        report = migration.preview_migration(source, source="synthetic-v6")
        self.assertEqual(source, before)
        self.assertTrue(report["ok"])
        self.assertFalse(report["would_write"])
        candidate = report["candidate_state"]
        self.assertEqual(candidate["status"], "candidate_not_active")
        self.assertEqual(candidate["schedules"], source["schedules"])
        self.assertEqual(state_validator.validate(candidate), [])

    def test_v6_migration_cli_never_writes_source(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        source = downgrade_v7_to_v6(state)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "state-v6.json"
            original = json.dumps(source, indent=2)
            path.write_text(original, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(PLUGIN / "scripts/migrate_state_v6_to_v7.py"), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["mode"], "preview_only")
            self.assertFalse(report["would_write"])
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_validator_enforces_final_sequence_and_proposal_only_offer(self):
        template = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        complete, run = completed_run_state(template)
        self.assertEqual(state_validator.validate(complete), [])

        premature = copy.deepcopy(complete)
        premature_run = premature["runs"][0]
        premature_run["approvals"]["production_completion"]["status"] = (
            "declared_awaiting_handoff_approval"
        )
        premature_run["approvals"]["production_completion"]["handoff_verified_at"] = None
        errors = state_validator.validate(premature)
        self.assertTrue(any("HITL3 cannot open before" in error for error in errors), errors)

        expanded = copy.deepcopy(complete)
        gate = expanded["runs"][0]["approvals"]["system_improvement_review_offer"]
        gate["required_question_scope"].remove("schedule_contracts")
        gate["authority_on_request"]["authorises"].append("modify_system_files")
        errors = state_validator.validate(expanded)
        self.assertTrue(any("question scope is incomplete" in error for error in errors), errors)
        self.assertTrue(any("authorise only review and proposal" in error for error in errors), errors)

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
    def test_v022_manifest_and_marketplace_metadata(self):
        system_root = PLUGIN.parents[1]
        plugin_manifest = json.loads(
            (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (system_root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        interface = plugin_manifest["interface"]
        self.assertEqual(plugin_manifest["version"], "0.2.2")
        self.assertEqual(
            plugin_manifest["repository"],
            "https://github.com/gpochs/Agentic-Course-Redesign-System",
        )
        self.assertEqual(interface["category"], "Education & Research")
        self.assertEqual(interface["displayName"], "Agentic Course Redesign")
        self.assertLessEqual(len(interface["displayName"]), 30)
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        self.assertEqual(len(interface["defaultPrompt"]), 3)
        self.assertTrue(all("@" not in item and len(item) <= 128 for item in interface["defaultPrompt"]))
        self.assertTrue((PLUGIN / interface["logo"].removeprefix("./")).is_file())
        self.assertTrue((PLUGIN / interface["composerIcon"].removeprefix("./")).is_file())
        self.assertEqual(marketplace["name"], "agentic-course-redesign-system")
        self.assertEqual(marketplace["plugins"][0]["source"]["path"], "./plugins/agentic-course-redesign")
        self.assertEqual(marketplace["plugins"][0]["policy"]["authentication"], "ON_INSTALL")

    def test_orchestrator_is_full_workflow_umbrella_entry(self):
        orchestrator = PLUGIN / "skills/course-redesign-orchestrator"
        metadata = (orchestrator / "agents/openai.yaml").read_text(encoding="utf-8")
        skill = (orchestrator / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('display_name: "Agentic Course Redesign"', metadata)
        self.assertIn("$course-redesign-orchestrator", metadata)
        self.assertIn("## Umbrella entry routing", skill)
        self.assertIn("$course-redesign-setup", skill)
        self.assertIn("$course-redesign-system", skill)
        self.assertIn("Fail closed on a missing, stale, contradictory, or invalid", skill)
        self.assertIn("never authorises crossing lecturer-in-the-loop gates", skill)
        self.assertIn("DECLARE PRODUCTION COMPLETE", skill)
        self.assertIn("APPROVE PRODUCTION HANDOFF", skill)
        self.assertIn("HITL 3 remains forbidden", skill)
        self.assertIn(migration.MANDATORY_SYSTEM_REVIEW_QUESTION, skill)
        self.assertIn("read-only system-improvement", skill)
        self.assertIn("It does not authorise system-file changes", skill)
        for status in ("offered_awaiting_response", "requested", "declined"):
            self.assertIn(status, skill)
        system_skill = (
            PLUGIN / "skills/course-redesign-system/SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("APPROVE SYSTEM FILES", system_skill)
        self.assertIn("A token-only reply is", system_skill)

        display_names = []
        for yaml_path in sorted((PLUGIN / "skills").glob("*/agents/openai.yaml")):
            for line in yaml_path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("display_name:"):
                    display_names.append(line.split(":", 1)[1].strip().strip('"'))
                    break
        self.assertEqual(len(display_names), 6)
        self.assertEqual(display_names.count("Agentic Course Redesign"), 1)
        self.assertEqual(len(set(display_names)), 6)

    def test_public_source_is_skills_only_and_matches_runtime(self):
        system_root = PLUGIN.parents[1]
        public = system_root / "openai-submission/source/agentic-course-redesign"
        self.assertFalse((public / ".mcp.json").exists())
        self.assertFalse((public / ".app.json").exists())
        self.assertFalse((public / "hooks").exists())
        self.assertFalse((public / "tests").exists())
        public_manifest = json.loads(
            (public / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertFalse(
            set(public_manifest)
            & {"apps", "mcpServers", "hooks", "connectors", "authentication", "permissions"}
        )
        self.assertEqual(
            public_manifest,
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
        self.assertEqual(cases["version"], "0.2.2")
        self.assertEqual(prompts["version"], "0.2.2")
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

    def test_release_evidence_rejects_stale_report(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "Agentic-Course-Redesign-System_v0.2.2.zip"
            archive.write_bytes(b"candidate archive fixture")
            matching = {
                "schema_version": 1,
                "pass": True,
                "archive": archive.name,
                "archive_sha256": release_evidence.sha256(archive),
                "archive_bytes": archive.stat().st_size,
                "findings": [],
            }
            self.assertEqual(release_evidence.validate(matching, archive, "0.2.2"), [])
            stale = dict(matching)
            stale["archive"] = "Agentic-Course-Redesign-System_v0.2.1.zip"
            stale["archive_sha256"] = "0" * 64
            errors = release_evidence.validate(stale, archive, "0.2.2")
            self.assertTrue(any("archive name" in item for item in errors))
            self.assertTrue(any("expected version" in item for item in errors))
            self.assertTrue(any("SHA-256" in item for item in errors))


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
