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
from unittest import mock


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


def approved_eligibility_record() -> dict:
    value = json.loads(
        (
            PLUGIN
            / "assets/project-template/01_Control/material-processing-eligibility.template.json"
        ).read_text(encoding="utf-8")
    )
    value.update(
        {
            "eligibility_id": "ELIG-SYNTHETIC-001",
            "status": "approved",
            "lecturer_declaration_reference": "REPLY-ELIGIBILITY-001",
            "recorded_at": "2026-08-21T09:55:00Z",
            "reconfirmation_required": False,
        }
    )
    value["environment"].update(
        {
            "category": "personal_or_unmanaged",
            "exact_environment_reference": "SYNTHETIC-PERSONAL-ENVIRONMENT",
        }
    )
    value["material_scope"].update(
        {
            "declared_category": "privately_owned_or_rightsholder_authorised",
            "ai_processing_authority_confirmed": True,
            "contains_institution_internal_or_restricted_material": False,
            "contains_student_personal_data": False,
            "sensitivity_classification": "non_sensitive",
            "assessment_security_classification": "no_protected_assessment_material",
            "assessment_security_handling_authorised": True,
        }
    )
    value["decision"].update(
        {
            "outcome": "proceed",
            "reason": "synthetic authorised fixture",
            "approved_processing_scope": "synthetic course fixture only",
        }
    )
    value["fingerprint"] = manifest.canonical_eligibility_fingerprint(value)
    return value


setup = load("setup_course_project", "scripts/setup_course_project.py")
manifest = load("source_manifest", "scripts/source_manifest.py")
state_validator = load("validate_state", "scripts/validate_state.py")
migration = load("migrate_state_v7_to_v8", "scripts/migrate_state_v7_to_v8.py")
fingerprinter = load("fingerprint_file", "scripts/fingerprint_file.py")
release_evidence = load_path(
    "validate_release_evidence",
    PLUGIN.parents[1] / "validation/validate_release_evidence.py",
)


def downgrade_v8_to_v7(state: dict) -> dict:
    result = copy.deepcopy(state)
    result["schema_version"] = 7
    result["plugin_version"] = "0.2.2"
    result.pop("adaptive_course_scope", None)
    result.pop("material_processing_eligibility", None)
    result.pop("schema_8_migration_hold", None)
    for field in (
        "educational_context_type",
        "discipline_or_subject",
        "qualification_or_framework",
        "adaptation_inputs_confirmed",
    ):
        result.get("course", {}).pop(field, None)
    result.get("source_access_policy", {}).pop(
        "material_processing_eligibility_fingerprint", None
    )
    activation = result["activation"]
    activation["required_before_active"] = [
        item
        for item in activation["required_before_active"]
        if item not in {"gate_0a_recorded", "matching_course_run_terminal_complete_dormant"}
    ]
    update = activation["system_update"]
    update["prerequisites"] = [
        item
        for item in update["prerequisites"]
        if item != "matching_run_terminal_complete_dormant_and_not_active"
    ]
    update["completed_reply_requirements"] = [
        item
        for item in update["completed_reply_requirements"]
        if item != "material_processing_eligibility_fingerprint"
    ]
    update["approval"].pop("material_processing_eligibility_fingerprint", None)
    result.get("schedule_registration", {}).pop(
        "required_material_processing_eligibility", None
    )
    return result


def completed_run_state(template: dict) -> tuple[dict, dict]:
    state = copy.deepcopy(template)
    eligibility = state["material_processing_eligibility"]
    eligibility.update(
        {
            "eligibility_id": "ELIG-SYNTHETIC-001",
            "status": "approved",
            "lecturer_declaration_reference": "REPLY-ELIGIBILITY-001",
            "recorded_at": "2026-08-21T09:55:00Z",
            "reconfirmation_required": False,
        }
    )
    eligibility["environment"].update(
        {
            "category": "personal_or_unmanaged",
            "exact_environment_reference": "SYNTHETIC-PERSONAL-ENVIRONMENT",
        }
    )
    eligibility["material_scope"].update(
        {
            "declared_category": "privately_owned_or_rightsholder_authorised",
            "ai_processing_authority_confirmed": True,
            "contains_institution_internal_or_restricted_material": False,
            "contains_student_personal_data": False,
            "sensitivity_classification": "non_sensitive",
            "assessment_security_classification": "no_protected_assessment_material",
            "assessment_security_handling_authorised": True,
        }
    )
    eligibility["decision"].update(
        {
            "outcome": "proceed",
            "reason": "synthetic authorised fixture",
            "approved_processing_scope": "synthetic course fixture only",
        }
    )
    eligibility["fingerprint"] = state_validator._canonical_eligibility_fingerprint(
        eligibility
    )
    eligibility_fingerprint = eligibility["fingerprint"]
    run = copy.deepcopy(state["run_template"])
    run.update(
        {
            "template_only": False,
            "run_id": "RUN-SYNTHETIC-001",
            "task_chat_reference": "TASK-SYNTHETIC-001",
            "mode": "manual",
            "status": "complete_dormant",
            "started_at": "2026-08-21T09:56:00Z",
            "current_gate": "RUN_CLOSED",
            "plan_version": 3,
            "next_permitted_action": "none_course_run_complete_dormant_wait_for_fresh_trigger",
        }
    )
    run["trigger"].update(
        {
            "trigger_id": "TRIGGER-SYNTHETIC-001",
            "trigger_type": "manual",
            "created_at": "2026-08-21T09:56:00Z",
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
        }
    )
    run["contract"].update(
        {
            "status": "approved",
            "contract_id": "RC-SYNTHETIC-001",
            "version": 1,
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
            "source_access_policy_version": "SAP-SYNTHETIC-v1",
            "source_access_policy_fingerprint": "POLICY-FINGERPRINT-001",
        }
    )
    run["shared_context"].update(
        {
            "version": 2,
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
            "source_access_policy_version": "SAP-SYNTHETIC-v1",
            "source_access_policy_fingerprint": "POLICY-FINGERPRINT-001",
        }
    )
    run["source_manifest_verification"].update(
        {
            "source_manifest_fingerprint": "MANIFEST-FINGERPRINT-001",
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
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
        "material_processing_eligibility_fingerprint": eligibility_fingerprint,
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

    run["approvals"]["gate_0a"].update(
        {
            "approval_id": "GATE0A-SYNTHETIC-001",
            "status": "approved",
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
            "lecturer_declaration_reference": "REPLY-ELIGIBILITY-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T09:55:00Z",
        }
    )

    manifest_path = "01_Control/source-hashes.csv"
    state["source_manifest"] = manifest_path
    state["source_access_policy"].update(
        {
            "status": "approved",
            "version": "SAP-SYNTHETIC-v1",
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
            "fingerprint": "POLICY-FINGERPRINT-001",
            "lecturer_approval_reference": "REPLY-GATE0-001",
            "recorded_at": "2026-08-21T09:59:00Z",
        }
    )
    run["source_manifest_verification"]["manifest_path"] = manifest_path
    run["contract"]["lecturer_approval"].update(
        {
            "status": "approved",
            "lecturer_reply": "REPLY-GATE1-001",
            "recorded_at": "2026-08-21T10:00:00Z",
        }
    )

    gate0 = run["approvals"]["gate_0"]
    gate0.update(
        {
            "approval_id": "GATE0-SYNTHETIC-001",
            "status": "approved",
            "basis": "approved exact manifest and source-access policy",
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
            "source_manifest_fingerprint": "MANIFEST-FINGERPRINT-001",
            "source_access_policy_version": "SAP-SYNTHETIC-v1",
            "source_access_policy_fingerprint": "POLICY-FINGERPRINT-001",
            "lecturer_reply": "REPLY-GATE0-001",
            "recorded_at": "2026-08-21T09:59:00Z",
        }
    )
    gate0["approval_receipt"].update(
        {
            **lineage,
            "reply_reference": "REPLY-GATE0-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T09:59:00Z",
        }
    )
    gate1 = run["approvals"]["gate_1"]
    gate1.update(
        {
            "approval_id": "GATE1-SYNTHETIC-001",
            "status": "approved",
            "basis": "approved synthetic course brief and run contract",
            "run_contract_id": run["contract"]["contract_id"],
            "run_contract_version": run["contract"]["version"],
            "material_processing_eligibility_fingerprint": eligibility_fingerprint,
            "source_manifest_fingerprint": "MANIFEST-FINGERPRINT-001",
            "source_access_policy_version": "SAP-SYNTHETIC-v1",
            "source_access_policy_fingerprint": "POLICY-FINGERPRINT-001",
            "lecturer_reply": "REPLY-GATE1-001",
            "recorded_at": "2026-08-21T10:00:00Z",
        }
    )
    gate1["approval_receipt"].update(
        {
            **lineage,
            "reply_reference": "REPLY-GATE1-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:00:00Z",
        }
    )

    coordination = run["coordination"]
    for index, role in enumerate(coordination["stage_a_role_statuses"], start=1):
        role.update(
            {
                "status": "complete_accepted",
                "accepted_return_id": f"RETURN-SYNTHETIC-{index:02d}",
            }
        )
    coordination.update(
        {
            "all_five_stage_a_complete": True,
            "preliminary_summary_exchange_complete": True,
            "live_alignment_ledger_started": True,
            "cross_review_complete": True,
            "assessment_final_integration_complete": True,
            "red_team_complete": True,
        }
    )
    gate2a = run["approvals"]["gate_2a"]
    gate2a.update(
        {
            "approval_id": "GATE2A-SYNTHETIC-001",
            "status": "approved",
            "lecturer_reply": "REPLY-GATE2A-001",
            "mission_interpretation": "synthetic course-specific mission",
            "approved_focus": ["synthetic focus"],
            "role_contracts": [{"role_goal": "synthetic bounded role goal"}],
            "recorded_at": "2026-08-21T10:01:00Z",
        }
    )
    gate2a["approval_receipt"].update(
        {
            **lineage,
            "reply_reference": "REPLY-GATE2A-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:01:00Z",
        }
    )
    gate2b = run["approvals"]["gate_2b"]
    research_root = "03_Research/2026-08-21_RUN-SYNTHETIC-001"
    gate2b.update(
        {
            "approval_id": "GATE2B-SYNTHETIC-001",
            "status": "approved",
            "lecturer_reply": "REPLY-GATE2B-001",
            "selected_change_cards": ["CHANGE-SYNTHETIC-001"],
            "approved_research_targets": [
                {
                    "target_type": "research_dossier",
                    "relative_path": f"{research_root}/Research_Dossier.md",
                    "run_id": run["run_id"],
                    "approved_at": "2026-08-21T10:02:00Z",
                },
                {
                    "target_type": "research_handoff",
                    "relative_path": f"{research_root}/Research_Handoff.md",
                    "run_id": run["run_id"],
                    "approved_at": "2026-08-21T10:02:00Z",
                },
            ],
            "recorded_at": "2026-08-21T10:02:00Z",
        }
    )
    gate2b["approval_receipt"].update(
        {
            **lineage,
            "reply_reference": "REPLY-GATE2B-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:02:00Z",
        }
    )
    working_target = "04_Working_Copies/RUN-SYNTHETIC-001/Redesigned_Material.md"
    gate3 = run["approvals"]["gate_3"]
    gate3.update(
        {
            "approval_id": "GATE3-SYNTHETIC-001",
            "status": "approved",
            "lecturer_reply": "REPLY-GATE3-001",
            "approved_blueprint_reference": "BLUEPRINT-SYNTHETIC-001",
            "approved_material_targets": [
                {
                    "target_type": "working_copy",
                    "relative_path": working_target,
                    "audience_classification": "student_facing",
                    "run_id": run["run_id"],
                    "approved_at": "2026-08-21T10:03:00Z",
                }
            ],
            "recorded_at": "2026-08-21T10:03:00Z",
        }
    )
    gate3["approval_receipt"].update(
        {
            **lineage,
            "reply_reference": "REPLY-GATE3-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:03:00Z",
        }
    )
    artefact = run["approvals"]["artefact_gate"]
    artefact.update(
        {
            "approval_id": "ARTEFACT-GATE-SYNTHETIC-001",
            "status": "complete",
            "artefacts": [
                {
                    "artefact_id": "ARTEFACT-SYNTHETIC-001",
                    "target": working_target,
                    "decision": "accepted",
                    "acceptance_reference": "REPLY-ARTEFACT-001",
                    "qa_reference": "QA-SYNTHETIC-001",
                    "recorded_at": "2026-08-21T10:04:00Z",
                }
            ],
        }
    )
    artefact["approval_receipt"].update(
        {
            **lineage,
            "reply_reference": "REPLY-ARTEFACT-001",
            "validation_status": "passed",
            "recorded_at": "2026-08-21T10:04:00Z",
        }
    )

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
            "question_scope_presented": copy.deepcopy(
                state_validator.REQUIRED_SYSTEM_REVIEW_SCOPE
            ),
            "question_text": state_validator.MANDATORY_SYSTEM_REVIEW_QUESTION,
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
    run["termination"].update(
        {
            "status": "complete_dormant",
            "reason": "accepted materials and explicit system-review response recorded",
            "recorded_at": "2026-08-21T10:07:00Z",
            "system_improvement_response_reference": "REPLY-OFFER-001",
            "active_run_id_cleared_at": "2026-08-21T10:07:00Z",
        }
    )
    guidance = run["approvals"]["trigger_guidance_offer"]
    guidance["status"] = "offered"
    guidance["offer"].update(
        {
            "offer_id": "trigger-guidance:RUN-SYNTHETIC-001:REPLY-OFFER-001",
            "run_id": "RUN-SYNTHETIC-001",
            "system_improvement_response_reference": "REPLY-OFFER-001",
            "offer_reference": "TRIGGER-GUIDANCE-OFFER-001",
            "offered_at": "2026-08-21T10:08:00Z",
            "validation_status": "passed",
        }
    )
    state["active_run_id"] = None
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
            eligibility_path = Path(temporary) / "eligibility.json"
            eligibility_path.write_text(
                json.dumps(approved_eligibility_record()), encoding="utf-8"
            )
            preview = setup.build_report(target)
            self.assertFalse(preview["target_contents_inspected"])
            self.assertIsNone(preview["target_existing_top_level_entries"])
            with self.assertRaises(PermissionError):
                setup.install(target, allow_nonempty=False)
            with self.assertRaises(FileExistsError):
                setup.install(
                    target,
                    allow_nonempty=False,
                    eligibility_record=eligibility_path,
                )
            result = setup.install(
                target,
                allow_nonempty=True,
                eligibility_record=eligibility_path,
            )
            self.assertTrue(result["installed"])
            self.assertEqual((target / "lecturer-note.txt").read_text(), "keep")

    def test_allow_nonempty_is_documented_as_conditional_and_never_overwrites(self):
        system_root = PLUGIN.parents[1]
        guide = (system_root / "PORTABLE_SETUP_WINDOWS.md").read_text(encoding="utf-8")
        self.assertIn("--allow-nonempty", guide)
        self.assertIn("does not permit overwriting", guide)


class EligibilityGeneratorTests(unittest.TestCase):
    def command(self, project: Path, *extra: str) -> list[str]:
        return [
            sys.executable,
            str(PLUGIN / "scripts/create_material_processing_eligibility.py"),
            "--project",
            str(project.resolve()),
            "--eligibility-id",
            "ELIG-SYNTHETIC-GENERATOR-001",
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
            "Synthetic authorised material in one declared environment.",
            "--approved-processing-scope",
            "Synthetic one-course project only.",
            "--lecturer-declaration-reference",
            "SYNTHETIC-REPLY-GATE0A-001",
            "--recorded-at",
            "2026-08-22T12:00:00+02:00",
            *extra,
        ]

    def test_preview_is_deterministic_and_writes_nothing(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "synthetic" / "one-course"
            (project / "01_Control").mkdir(parents=True)
            first = subprocess.run(
                self.command(project), check=False, capture_output=True, text=True
            )
            second = subprocess.run(
                self.command(project), check=False, capture_output=True, text=True
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
                (project / "01_Control/material-processing-eligibility.json").exists()
            )

    def test_apply_creates_only_exact_target_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "synthetic" / "one-course"
            control = project / "01_Control"
            control.mkdir(parents=True)
            first = subprocess.run(
                self.command(project, "--apply"),
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
            target = control / "material-processing-eligibility.json"
            original = target.read_bytes()
            self.assertTrue(manifest.validate_eligibility(target)["ok"])
            second = subprocess.run(
                self.command(project, "--apply"),
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("refusing to overwrite", second.stdout)
            self.assertEqual(target.read_bytes(), original)
            self.assertEqual([path.name for path in control.iterdir()], [target.name])

    def test_refuses_redirected_control_directory_when_symlinks_are_supported(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "synthetic" / "one-course"
            project.mkdir(parents=True)
            outside = Path(temporary) / "outside-control"
            outside.mkdir()
            control = project / "01_Control"
            try:
                control.symlink_to(outside, target_is_directory=True)
            except OSError as exc:
                self.skipTest(f"directory symlinks are unavailable: {exc}")

            preview = subprocess.run(
                self.command(project), check=False, capture_output=True, text=True
            )
            self.assertNotEqual(
                preview.returncode, 0, preview.stdout + preview.stderr
            )
            self.assertIn("redirected project control directory", preview.stdout)
            self.assertFalse(
                (outside / "material-processing-eligibility.json").exists()
            )


class ManifestTests(unittest.TestCase):
    def test_gate_0a_owned_public_internal_mixed_and_institutional_cases(self):
        with tempfile.TemporaryDirectory() as temporary:
            record_path = Path(temporary) / "eligibility.json"

            owned = approved_eligibility_record()
            record_path.write_text(json.dumps(owned), encoding="utf-8")
            self.assertTrue(manifest.validate_eligibility(record_path)["ok"])

            public_only = copy.deepcopy(owned)
            public_only["material_scope"].update(
                {
                    "declared_category": "appropriately_licensed_or_public_with_explicit_ai_processing_authority",
                    "ai_processing_authority_confirmed": False,
                }
            )
            public_only["fingerprint"] = manifest.canonical_eligibility_fingerprint(
                public_only
            )
            record_path.write_text(json.dumps(public_only), encoding="utf-8")
            errors = manifest.validate_eligibility(record_path)["errors"]
            self.assertTrue(any("explicit AI-processing authority" in item for item in errors))

            internal_personal = copy.deepcopy(owned)
            internal_personal["material_scope"].update(
                {
                    "declared_category": "institution_internal_or_restricted",
                    "contains_institution_internal_or_restricted_material": True,
                    "sensitivity_classification": "institution_internal_or_restricted",
                }
            )
            internal_personal["fingerprint"] = manifest.canonical_eligibility_fingerprint(
                internal_personal
            )
            record_path.write_text(json.dumps(internal_personal), encoding="utf-8")
            errors = manifest.validate_eligibility(record_path)["errors"]
            self.assertTrue(any("route-only" in item for item in errors))

            mixed = copy.deepcopy(owned)
            mixed["material_scope"]["declared_category"] = "mixed"
            mixed["fingerprint"] = manifest.canonical_eligibility_fingerprint(mixed)
            record_path.write_text(json.dumps(mixed), encoding="utf-8")
            errors = manifest.validate_eligibility(record_path)["errors"]
            self.assertTrue(any("segregated or clarified" in item for item in errors))

            institutional = copy.deepcopy(owned)
            institutional["environment"].update(
                {
                    "category": "approved_institutional_exact_environment",
                    "exact_environment_reference": "ENV-SYNTHETIC-001",
                    "institutional_policy_reference": "POLICY-SYNTHETIC-001",
                    "approved_scope": "synthetic internal course only",
                    "policy_expires_at": "2099-12-31T23:59:59+01:00[Europe/Zurich]",
                }
            )
            institutional["material_scope"].update(
                {
                    "declared_category": "institution_internal_or_restricted",
                    "contains_institution_internal_or_restricted_material": True,
                    "sensitivity_classification": "institution_internal_or_restricted",
                }
            )
            institutional["fingerprint"] = manifest.canonical_eligibility_fingerprint(
                institutional
            )
            record_path.write_text(json.dumps(institutional), encoding="utf-8")
            self.assertTrue(manifest.validate_eligibility(record_path)["ok"])

    def test_create_verify_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "Course"
            (project / "00_Source_Materials").mkdir(parents=True)
            (project / "00_Context").mkdir()
            (project / "00_Source_Materials/workbook.txt").write_text("course", encoding="utf-8")
            (project / "00_Source_Materials/test_answer_key.txt").write_text("secret", encoding="utf-8")
            (project / "00_Context/policy.txt").write_text("policy", encoding="utf-8")
            path = Path("01_Control/source-hashes.csv")
            eligibility_path = project / "01_Control/material-processing-eligibility.json"
            eligibility_path.parent.mkdir()
            eligibility_path.write_text(
                json.dumps(approved_eligibility_record()), encoding="utf-8"
            )
            created = manifest.create(
                project, path, replace=False, eligibility_record=eligibility_path
            )
            self.assertTrue(created["ok"])
            verified = manifest.verify(project, path, eligibility_record=eligibility_path)
            self.assertTrue(verified["ok"])
            with (project / path).open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            key = next(row for row in rows if "answer_key" in row["relative_path"])
            self.assertEqual(key["audience_classification"], "lecturer_only_candidate")
            (project / "00_Source_Materials/workbook.txt").write_text("coursf", encoding="utf-8")
            failed = manifest.verify(project, path, eligibility_record=eligibility_path)
            self.assertFalse(failed["ok"])
            self.assertIn("hash-mismatch", {item["status"] for item in failed["results"]})

    def test_gate_0a_failure_prevents_source_enumeration(self):
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary) / "Course"
            project.mkdir()
            invalid = project / "01_Control/material-processing-eligibility.json"
            invalid.parent.mkdir()
            invalid.write_text(
                json.dumps({"status": "route_only", "fingerprint": None}),
                encoding="utf-8",
            )
            with mock.patch.object(manifest, "enumerate_files") as enumerate_files:
                result = manifest.create(
                    project,
                    Path("01_Control/source-hashes.csv"),
                    replace=False,
                    eligibility_record=invalid,
                )
            self.assertFalse(result["ok"])
            self.assertFalse(result["source_enumeration_started"])
            enumerate_files.assert_not_called()


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
        template = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        state, run = completed_run_state(template)
        approvals = run["approvals"]
        self.assertEqual(state_validator.validate(state), [])
        approvals["gate_2b"]["approved_research_targets"][0]["relative_path"] = (
            "04_Working_Copies/RUN-SYNTHETIC-001/Research_Dossier.md"
        )
        approvals["gate_3"]["approved_material_targets"][0]["relative_path"] = (
            "03_Research/2026-08-21_RUN-SYNTHETIC-001/Redesigned_Material.md"
        )
        errors = state_validator.validate(state)
        self.assertTrue(any("Gate 2B research target 0" in item for item in errors))
        self.assertIn("Gate 3 material target 0 violates its required prefix", errors)

    def test_schema_8_records_match_canonical_shapes(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        run = state["run_template"]
        self.assertEqual(state["schema_version"], 8)
        self.assertEqual(state["plugin_version"], "0.2.4")
        self.assertEqual(
            state["umbrella_entry_routing"]["initial_gate"],
            "GATE_0A_AWAITING_MATERIAL_ENVIRONMENT_ELIGIBILITY",
        )
        self.assertEqual(
            state["material_processing_eligibility"]["status"],
            "awaiting_lecturer_declaration",
        )
        self.assertEqual(
            state["adaptive_course_scope"]["supported_contexts"],
            [
                "school",
                "vocational_education_and_training",
                "professional_learning",
                "higher_education",
                "other_lecturer_defined",
            ],
        )
        self.assertIn("complete_dormant", run["allowed_run_statuses"])
        self.assertEqual(
            run["resume_protocol"], state_validator.EXPECTED_RESUME_PROTOCOL
        )
        self.assertIn(
            "schedule_contracts",
            run["approvals"]["system_improvement_review_offer"]["required_question_scope"],
        )
        self.assertTrue(
            run["approvals"]["trigger_guidance_offer"]["informational_only"]
        )

    def test_adaptive_course_scope_accepts_diverse_synthetic_profiles(self):
        template = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(
                encoding="utf-8"
            )
        )
        profiles = (
            ("school", "Biology", "Year 8", "English"),
            ("vocational_education_and_training", "Welding", "Apprenticeship", "German"),
            ("professional_learning", "Clinical supervision", "Continuing education", "French"),
            ("higher_education", "Literature", "Bachelor", "English"),
            ("other_lecturer_defined", "Community media", "Adult learners", "Spanish"),
        )
        for context, discipline, level, language in profiles:
            with self.subTest(context=context):
                state = copy.deepcopy(template)
                state["course"].update(
                    {
                        "title": f"Synthetic {discipline}",
                        "context": "synthetic regression fixture",
                        "level_and_programme": level,
                        "learner_profile": "synthetic learners",
                        "course_language": language,
                        "educational_context_type": context,
                        "discipline_or_subject": discipline,
                        "adaptation_inputs_confirmed": True,
                    }
                )
                self.assertEqual(state_validator.validate(state), [])

    def test_v7_migration_preview_is_non_mutating_and_preserving(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        source = downgrade_v8_to_v7(state)
        source["run_template"]["contract"]["permitted_tools"] = ["local_read_only"]
        before = copy.deepcopy(source)
        report = migration.preview_migration(source, source="synthetic-v7")
        self.assertEqual(source, before)
        self.assertTrue(report["ok"])
        self.assertFalse(report["would_write"])
        candidate = report["candidate_state"]
        self.assertEqual(candidate["status"], "candidate_not_active")
        self.assertEqual(candidate["schedules"], source["schedules"])
        self.assertEqual(candidate["schema_version"], 8)
        self.assertTrue(report["reconfirmation_required"])
        self.assertTrue(all(report["preservation_checks"].values()))

    def test_v7_migration_cli_never_writes_source(self):
        state = json.loads(
            (PLUGIN / "assets/project-template/01_Control/state.json").read_text(encoding="utf-8")
        )
        source = downgrade_v8_to_v7(state)
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "state-v7.json"
            original = json.dumps(source, indent=2)
            path.write_text(original, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(PLUGIN / "scripts/migrate_state_v7_to_v8.py"), str(path)],
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
        self.assertEqual(run["status"], "complete_dormant")
        self.assertEqual(run["termination"]["status"], "complete_dormant")
        self.assertIsNone(complete["active_run_id"])
        self.assertTrue(run["termination"]["never_resume_after_terminal"])
        self.assertEqual(run["approvals"]["trigger_guidance_offer"]["status"], "offered")
        closeout_transition = next(
            item
            for item in run["manual_stage_authority"]["transition_rules"]
            if item["trigger"] == "explicit_system_improvement_review_response"
        )
        self.assertEqual(
            closeout_transition["silence_behavior"], "remain_waiting_without_decision"
        )
        self.assertTrue(closeout_transition["requires_explicit_response"])

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
    def test_v024_manifest_and_marketplace_metadata(self):
        system_root = PLUGIN.parents[1]
        plugin_manifest = json.loads(
            (PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        marketplace = json.loads(
            (system_root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8")
        )
        interface = plugin_manifest["interface"]
        self.assertEqual(plugin_manifest["version"], "0.2.4")
        self.assertEqual(
            plugin_manifest["repository"],
            "https://github.com/gpochs/Agentic-Course-Redesign-System",
        )
        self.assertEqual(plugin_manifest["author"]["name"], "GIAN PETER OCHSNER")
        self.assertEqual(interface["developerName"], "GIAN PETER OCHSNER")
        self.assertEqual(
            interface["websiteURL"],
            "https://github.com/gpochs/Agentic-Course-Redesign-System",
        )
        self.assertEqual(
            interface["privacyPolicyURL"],
            "https://github.com/gpochs/Agentic-Course-Redesign-System/blob/v0.2.4/docs/PRIVACY.md",
        )
        self.assertEqual(
            interface["termsOfServiceURL"],
            "https://github.com/gpochs/Agentic-Course-Redesign-System/blob/v0.2.4/docs/TERMS.md",
        )
        self.assertNotIn("supportURL", interface)
        self.assertEqual(interface["category"], "Education & Research")
        self.assertEqual(interface["displayName"], "Agentic Course Redesign")
        self.assertLessEqual(len(interface["displayName"]), 30)
        self.assertLessEqual(len(interface["shortDescription"]), 30)
        description = interface["longDescription"]
        self.assertLessEqual(len(description), 2400)
        self.assertGreaterEqual(description.count("\n- "), 10)
        self.assertNotRegex(description, r"\bWork\b")
        required_listing_markers = (
            "LECTURER / TEACHER CONTROL",
            "Course Redesign Orchestrator",
            "Course Mapper and Learning-Outcomes Auditor",
            "Active-Learning Researcher",
            "AI Integration and AI-Competence Researcher",
            "Student Experience, Accessibility and Workload Proxy Critic",
            "Assessment and Constructive-Alignment Designer",
            "Source Verification and Citation Auditor",
            "Evidence and Feasibility Red Team",
            "Learning Designer",
            "Learning Material Designer",
            "Artefact Accessibility and Visual QA Auditor",
            "Gate 0A:",
            "Gate 0:",
            "Gate 1:",
            "HITL 1",
            "HITL 2",
            "HITL 3",
            "Research",
            "red-team review",
            "Material production",
            "assessment-security QA",
            "production handoff",
            "final system review",
            "complete and dormant",
            "One unresolved question at a time",
            "Use a card only if the live host can show the complete option set plus custom answer",
            "Verified current Codex in Plan mode: 2–3 explicit choices plus automatic Other",
            "If capacity is unknown, unavailable or exceeded",
            "ordinary chat with every valid numbered option plus Other, then wait",
            "Never prune, hide or combine valid options to fit a card",
            "dependency-based chunks with every option visible",
            "lecturer may split, merge, reorder or rename them",
        )
        listing_copy = (
            system_root / "openai-submission/review/LISTING_COPY.md"
        ).read_text(encoding="utf-8")
        for marker in required_listing_markers:
            self.assertIn(marker, description)
            self.assertIn(marker, listing_copy)
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
        for marker in (
            "live host contract can show the complete option set plus a custom answer",
            "verified Codex supports exactly two or three explicit choices plus automatic Other",
            "capacity is unknown, unavailable or exceeded",
            "show every valid numbered option plus Other",
            "Never prune, hide or combine valid choices to fit cards",
            "keep every option visible in dependency chunks",
            "let the lecturer control grouping",
        ):
            self.assertIn(marker, metadata)
        self.assertIn("### Umbrella entry, Gate 0A and Gate 0", skill)
        self.assertIn("course-redesign-setup", skill)
        self.assertIn("course-redesign-system", skill)
        self.assertIn("fail closed on mixed/uncertain material", skill)
        self.assertIn("No gate, permission, target, or lecturer decision carries", skill)
        self.assertIn("DECLARE PRODUCTION COMPLETE", skill)
        self.assertIn("APPROVE PRODUCTION HANDOFF", skill)
        self.assertIn("Do not open HITL 3 until", skill)
        self.assertIn(state_validator.MANDATORY_SYSTEM_REVIEW_QUESTION, skill)
        self.assertIn("Before any course-source path", skill)
        self.assertIn("complete_dormant", skill)
        self.assertIn("read-only system review", skill)
        self.assertIn("it does not authorise system-file changes", skill)
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

    def test_all_skills_enforce_complete_host_adaptive_dialogue_contract(self):
        markers = (
            "Ask one unresolved",
            "Before using a native choice card, follow the live host tool contract",
            "complete, mutually exclusive option set and a custom-answer path without omission",
            "Never prune, hide or combine valid choices merely to fit a card",
            "If a native card is unavailable or unsupported, its capacity is unknown",
            "complete set exceeds that capacity",
            "ordinary chat with every valid numbered option plus `Other - type your answer`, then wait",
            "Every valid option remains visible",
            "adaptive dependency-based",
            "keep every valid option visible",
            "lecturer split, merge, reorder or rename",
            "Preserve a custom answer exactly",
            "Show an editable recap",
            "skipped or blank response leaves a required question unresolved",
            "never preselected",
            "select only if true",
            "dialogue choice never substitutes",
        )
        for skill_path in sorted((PLUGIN / "skills").glob("*/SKILL.md")):
            text = " ".join(skill_path.read_text(encoding="utf-8").split())
            for marker in markers:
                with self.subTest(skill=skill_path.parent.name, marker=marker):
                    self.assertIn(marker, text)

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
        self.assertEqual(cases["version"], "0.2.4")
        self.assertEqual(prompts["version"], "0.2.4")
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
            archive = root / "Agentic-Course-Redesign-System_v0.2.4.zip"
            archive.write_bytes(b"candidate archive fixture")
            matching = {
                "schema_version": 1,
                "pass": True,
                "archive": archive.name,
                "archive_sha256": release_evidence.sha256(archive),
                "archive_bytes": archive.stat().st_size,
                "findings": [],
            }
            self.assertEqual(release_evidence.validate(matching, archive, "0.2.4"), [])
            stale = dict(matching)
            stale["archive"] = "Agentic-Course-Redesign-System_v0.2.1.zip"
            stale["archive_sha256"] = "0" * 64
            errors = release_evidence.validate(stale, archive, "0.2.4")
            self.assertTrue(any("archive name" in item for item in errors))
            self.assertTrue(any("expected version" in item for item in errors))
            self.assertTrue(any("SHA-256" in item for item in errors))


class FingerprintTests(unittest.TestCase):
    def test_policy_fingerprint_is_canonical_and_excludes_approval_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            control = Path(temporary) / "01_Control"
            control.mkdir()
            eligibility = control / "material-processing-eligibility.json"
            eligibility.write_text(
                json.dumps(approved_eligibility_record()), encoding="utf-8"
            )
            policy_path = control / "source-access-policy.json"
            policy = json.loads(
                (PLUGIN / "assets/project-template/01_Control/source-access-policy.template.json").read_text(
                    encoding="utf-8"
                )
            )
            policy.update(
                {
                    "fingerprint": "OLD",
                    "lecturer_decision": "approved",
                    "approved_at": "now",
                }
            )
            policy_path.write_text(json.dumps(policy), encoding="utf-8")
            digest_one, payload_one = fingerprinter.fingerprint(
                policy_path, "policy", eligibility_record=eligibility
            )
            policy.update(
                {"fingerprint": None, "lecturer_decision": None, "approved_at": "later"}
            )
            policy_path.write_text(json.dumps(policy, indent=2), encoding="utf-8")
            digest_two, payload_two = fingerprinter.fingerprint(
                policy_path, "policy", eligibility_record=eligibility
            )
            self.assertEqual(digest_one, digest_two)
            self.assertEqual(payload_one, payload_two)
            canonical_policy = json.loads(payload_one)
            self.assertNotIn("approved_at", canonical_policy)
            self.assertNotIn("fingerprint", canonical_policy)

    def test_course_source_fingerprint_changes_with_formatting_and_raw_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            control = root / "01_Control"
            control.mkdir()
            eligibility = control / "material-processing-eligibility.json"
            eligibility.write_text(
                json.dumps(approved_eligibility_record()), encoding="utf-8"
            )
            first = root / "first.json"
            second = root / "second.json"
            first.write_text('{"a":1}', encoding="utf-8")
            second.write_text('{ "a": 1 }', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mode must be"):
                fingerprinter.fingerprint(first, "raw")
            self.assertNotEqual(
                fingerprinter.fingerprint(
                    first, "course-source", eligibility_record=eligibility
                )[0],
                fingerprinter.fingerprint(
                    second, "course-source", eligibility_record=eligibility
                )[0],
            )


if __name__ == "__main__":
    unittest.main()
