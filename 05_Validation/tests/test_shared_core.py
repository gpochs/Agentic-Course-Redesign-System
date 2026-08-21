from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "03_Shared_Workflow_Core"
STATE_PATH = CORE / "course-project-template" / "01_Control" / "state.json"
SETUP_PATH = CORE / "scripts" / "setup_course_project.py"
MIGRATION_PATH = CORE / "scripts" / "migrate_state_v6_to_v7.py"
VALIDATOR_PATH = CORE / "scripts" / "validate_state.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def downgrade_v7_to_v6(state: dict) -> dict:
    """Create a synthetic schema-6 fixture from the canonical schema-7 state."""

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


class SharedCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.setup = load_module("shared_setup", SETUP_PATH)
        cls.migration = load_module("shared_migration_v7", MIGRATION_PATH)
        cls.validator = load_module("shared_validate_v7", VALIDATOR_PATH)
        cls.state = json.loads(STATE_PATH.read_text(encoding="utf-8"))

    def completed_run_state(self) -> tuple[dict, dict]:
        state = copy.deepcopy(self.state)
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
                "question_scope_presented": copy.deepcopy(
                    self.migration.REQUIRED_SYSTEM_REVIEW_SCOPE
                ),
                "question_text": self.migration.MANDATORY_SYSTEM_REVIEW_QUESTION,
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

    def test_shared_state_is_schema_7_inactive_and_unscheduled(self) -> None:
        self.assertEqual(self.state["schema_version"], 7)
        self.assertEqual(self.state["plugin_version"], "0.2.2")
        self.assertEqual(self.state["status"], "candidate_not_active")
        self.assertEqual(self.state["schedules"], [])
        self.assertEqual(
            self.state["umbrella_entry_routing"], self.migration.umbrella_entry_routing()
        )

    def test_schema_records_match_preview_migration_canonical_shapes(self) -> None:
        run = self.state["run_template"]
        self.assertEqual(run["approvals"]["hitl_3"], self.migration.hitl3_record())
        self.assertEqual(
            run["approvals"]["system_improvement_review_offer"],
            self.migration.system_improvement_review_offer_record(),
        )
        self.assertEqual(run["resume_protocol"], self.migration.resume_protocol())
        self.assertEqual(
            run["approvals"]["system_improvement_review_offer"]["required_question_scope"],
            self.migration.REQUIRED_SYSTEM_REVIEW_SCOPE,
        )
        question = self.migration.MANDATORY_SYSTEM_REVIEW_QUESTION
        for required_phrase in (
            "workflow skills and umbrella entry routing",
            "plugin or platform adapter",
            "AGENTS.md and agent configurations",
            "project template, state schema and migration",
            "validators, tests and QA",
            "documentation",
            "memory or other workflow-owned durable instruction stores",
            "schedule contracts",
            "permissions, tools, external egress and automatic behaviour",
            "risks, residual risks and rollback",
        ):
            self.assertIn(required_phrase, question)
        for relative_path in (
            "agent-skills/course-redesign-orchestrator/SKILL.md",
            "agent-skills/course-redesign-system/SKILL.md",
            "course-project-template/AGENTS.md",
        ):
            self.assertIn(
                question,
                (CORE / relative_path).read_text(encoding="utf-8"),
                relative_path,
            )

    def test_v6_migration_preview_is_non_mutating_idempotent_and_preserving(self) -> None:
        source = downgrade_v7_to_v6(self.state)
        source["run_template"]["contract"]["permitted_tools"] = ["local_read_only"]
        before = copy.deepcopy(source)
        first = self.migration.preview_migration(source, source="synthetic-v6")
        self.assertEqual(source, before)
        self.assertTrue(first["ok"])
        self.assertFalse(first["would_write"])
        candidate = first["candidate_state"]
        self.assertEqual(candidate["status"], "candidate_not_active")
        self.assertEqual(candidate["schedules"], source["schedules"])
        self.assertEqual(
            candidate["run_template"]["contract"]["permitted_tools"],
            ["local_read_only"],
        )
        second = self.migration.preview_migration(candidate, source="synthetic-v7")
        self.assertEqual(second["changed_paths"], [])
        self.assertEqual(second["candidate_state"], candidate)

    def test_schema_7_preview_rejects_incomplete_preserved_legacy_activation(self) -> None:
        source = downgrade_v7_to_v6(self.state)
        source["status"] = "suspended"
        source["schedules"] = [{"schedule_id": "EXISTING-DO-NOT-CHANGE"}]
        before = copy.deepcopy(source)
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "schema-7 state failed full validation",
        ):
            self.migration.preview_migration(source, source="incomplete-legacy-v6")
        self.assertEqual(source, before)

    def test_schema_7_preview_rejects_expanded_system_review_authority(self) -> None:
        state = copy.deepcopy(self.state)
        state["run_template"]["approvals"]["system_improvement_review_offer"][
            "authority_on_request"
        ]["authorises"].append("modify_system_files")
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "system-review request authority is divergent",
        ):
            self.migration.preview_migration(state, source="unsafe-schema-v7")

    def test_v6_migration_cli_never_writes_source(self) -> None:
        source = downgrade_v7_to_v6(self.state)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state-v6.json"
            original = json.dumps(source, indent=2)
            path.write_text(original, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(MIGRATION_PATH), str(path)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["mode"], "preview_only")
            self.assertFalse(report["would_write"])
            self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_v6_migration_preserves_existing_run_lineage_and_permissions(self) -> None:
        state, _ = self.completed_run_state()
        source = downgrade_v7_to_v6(state)
        source_run = source["runs"][0]
        source_run["contract"]["permitted_tools"] = ["local_read_only"]
        source_run["contract"]["permitted_actions"] = ["inspect_approved_sources"]
        report = self.migration.preview_migration(source, source="synthetic-run-v6")
        migrated = report["candidate_state"]["runs"][0]
        for field in ("run_id", "task_chat_reference", "plan_version"):
            self.assertEqual(migrated[field], source_run[field])
        self.assertEqual(migrated["contract"]["contract_id"], source_run["contract"]["contract_id"])
        self.assertEqual(migrated["contract"]["permitted_tools"], ["local_read_only"])
        self.assertEqual(
            migrated["contract"]["permitted_actions"], ["inspect_approved_sources"]
        )
        self.assertEqual(migrated["approvals"]["production_completion"]["status"], "complete")
        self.assertEqual(migrated["approvals"]["hitl_3"]["status"], "not_started")
        self.assertEqual(
            migrated["approvals"]["system_improvement_review_offer"]["status"],
            "not_offered",
        )

    def test_v6_migration_fails_closed_on_unsupported_or_conflicting_input(self) -> None:
        unsupported = downgrade_v7_to_v6(self.state)
        unsupported["schema_version"] = 5
        with self.assertRaises(self.migration.MigrationError):
            self.migration.preview_migration(unsupported)
        conflicting = downgrade_v7_to_v6(self.state)
        conflicting["run_template"]["approvals"]["hitl_3"] = {}
        with self.assertRaises(self.migration.MigrationError):
            self.migration.preview_migration(conflicting)

    def test_validator_accepts_canonical_template(self) -> None:
        self.assertEqual(self.validator.validate(copy.deepcopy(self.state)), [])

    def test_validator_accepts_fully_sequenced_current_lineage_run(self) -> None:
        state, _ = self.completed_run_state()
        self.assertEqual(self.validator.validate(state), [])

    def test_validator_rejects_hitl3_before_verified_handoff(self) -> None:
        state, run = self.completed_run_state()
        production = run["approvals"]["production_completion"]
        production["status"] = "declared_awaiting_handoff_approval"
        production["handoff_verified_at"] = None
        errors = self.validator.validate(state)
        self.assertTrue(any("HITL3 cannot open before" in error for error in errors), errors)

    def test_validator_rejects_offer_before_hitl3_acceptance(self) -> None:
        state, run = self.completed_run_state()
        run["approvals"]["hitl_3"]["status"] = "awaiting_lecturer_decision"
        errors = self.validator.validate(state)
        self.assertTrue(any("offer cannot precede accepted HITL3" in error for error in errors), errors)

    def test_validator_rejects_stale_offer_lineage(self) -> None:
        state, run = self.completed_run_state()
        run["approvals"]["system_improvement_review_offer"]["offer"][
            "run_contract_id"
        ] = "STALE-CONTRACT"
        errors = self.validator.validate(state)
        self.assertTrue(any("system-review offer has stale or mismatched" in error for error in errors), errors)

    def test_validator_rejects_stale_production_and_hitl3_lineage(self) -> None:
        state, run = self.completed_run_state()
        run["approvals"]["production_completion"]["declaration"]["completed_reply"][
            "plan_version"
        ] = 2
        run["approvals"]["hitl_3"]["decision"]["source_manifest_fingerprint"] = (
            "STALE-MANIFEST"
        )
        errors = self.validator.validate(state)
        self.assertTrue(any("production declaration has stale or mismatched" in error for error in errors), errors)
        self.assertTrue(any("HITL3 decision has stale or mismatched" in error for error in errors), errors)

    def test_validator_rejects_handoff_approval_without_valid_declaration(self) -> None:
        state, run = self.completed_run_state()
        run["approvals"]["production_completion"]["declaration"]["completed_reply"][
            "validation_status"
        ] = "rejected"
        errors = self.validator.validate(state)
        self.assertTrue(any("declaration must be validated before handoff" in error for error in errors), errors)

    def test_system_update_cannot_begin_after_declined_review_offer(self) -> None:
        state, run = self.completed_run_state()
        offer_gate = run["approvals"]["system_improvement_review_offer"]
        offer_gate["status"] = "declined"
        offer_gate["response"]["decision"] = "decline_system_improvement_review"
        update = state["activation"]["system_update"]
        update["status"] = "proposal_requested"
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
        update["approval"].update(
            {
                **lineage,
                "system_improvement_review_offer_reference": offer_gate["offer"][
                    "offer_reference"
                ],
            }
        )
        errors = self.validator.validate(state)
        self.assertTrue(any("cannot begin before the source run requests review" in error for error in errors), errors)

    def test_validator_rejects_incomplete_question_scope_or_expanded_authority(self) -> None:
        state, run = self.completed_run_state()
        gate = run["approvals"]["system_improvement_review_offer"]
        gate["required_question_scope"].remove("schedule_contracts")
        gate["authority_on_request"]["authorises"].append("modify_system_files")
        errors = self.validator.validate(state)
        self.assertTrue(any("question scope is incomplete" in error for error in errors), errors)
        self.assertTrue(any("authorise only review and proposal" in error for error in errors), errors)

    def test_validator_requires_separate_production_and_handoff_replies(self) -> None:
        state, run = self.completed_run_state()
        production = run["approvals"]["production_completion"]
        production["handoff_approval"]["completed_reply"]["reply_reference"] = production[
            "declaration"
        ]["completed_reply"]["reply_reference"]
        errors = self.validator.validate(state)
        self.assertTrue(
            any("must use distinct reply references" in error for error in errors),
            errors,
        )

    def test_validator_binds_handoff_to_current_run(self) -> None:
        state, run = self.completed_run_state()
        production = run["approvals"]["production_completion"]
        wrong_target = "04_Working_Copies/OTHER-RUN/Production_Handoff.md"
        production["handoff_approval"]["exact_handoff_target"] = wrong_target
        production["handoff_approval"]["completed_reply"][
            "repeated_exact_handoff_target"
        ] = wrong_target
        errors = self.validator.validate(state)
        self.assertTrue(any("must belong to the current run" in error for error in errors), errors)

    def test_validator_requires_separate_hitl3_and_review_response_replies(self) -> None:
        state, run = self.completed_run_state()
        run["approvals"]["system_improvement_review_offer"]["response"][
            "reply_reference"
        ] = run["approvals"]["hitl_3"]["decision"]["reply_reference"]
        errors = self.validator.validate(state)
        self.assertTrue(
            any("HITL3 decision and system-review response" in error for error in errors),
            errors,
        )

    def test_validator_rejects_validated_system_update_without_system_gate(self) -> None:
        state, _ = self.completed_run_state()
        state["activation"]["system_update"]["status"] = "validated"
        errors = self.validator.validate(state)
        for phrase in (
            "standalone APPROVE SYSTEM FILES",
            "must name at least one exact target",
            "approval completed reply must be validated",
        ):
            self.assertTrue(any(phrase in error for error in errors), (phrase, errors))

    def test_validator_rejects_unapproved_activation_and_schedule(self) -> None:
        state = copy.deepcopy(self.state)
        state["status"] = "active"
        state["schedules"] = [{"schedule_id": "UNAPPROVED"}]
        errors = self.validator.validate(state)
        for phrase in (
            "requires a separate approved activation decision",
            "invalid registered schedule status",
        ):
            self.assertTrue(any(phrase in error for error in errors), (phrase, errors))

    def test_validator_rejects_schedule_receipts_before_approval(self) -> None:
        state = copy.deepcopy(self.state)
        registration = state["schedule_registration"]
        registration["approved_standing_contract_ids"] = ["SCHEDULE-001"]
        registration["approved_standing_contract_versions"] = ["v1"]
        registration["no_write_simulation_result"] = "passed-without-run"
        registration["approval"]["line_1"] = "APPROVE SCHEDULES"
        registration["approval"]["validation_status"] = "passed"
        errors = self.validator.validate(state)
        for phrase in (
            "cannot list approved contracts",
            "approval receipt cannot exist",
            "not-run schedule simulation cannot contain",
        ):
            self.assertTrue(any(phrase in error for error in errors), (phrase, errors))

    def test_validator_rejects_passed_simulation_for_blank_contract(self) -> None:
        state = copy.deepcopy(self.state)
        registration = state["schedule_registration"]
        registration["no_write_simulation_status"] = "passed"
        registration["no_write_simulation_result"] = "passed"
        registration["no_write_simulation_recorded_at"] = "2026-08-21T12:00:00Z"
        errors = self.validator.validate(state)
        self.assertTrue(
            any("simulated proposal.project is missing project_id" in error for error in errors),
            errors,
        )

    def test_validator_rejects_incomplete_malformed_or_drifted_active_contract(self) -> None:
        state = copy.deepcopy(self.state)
        contract = copy.deepcopy(state["standing_schedule_contract_template"])
        contract.update(
            {
                "schedule_id": "SCHEDULE-001",
                "contract_id": "CONTRACT-001",
                "contract_version": "v1",
                "status": "active",
                "timezone": "Europe/Zurich",
                "recurrence": ["annual-may-31"],
                "activation_time": "2099-05-01T09:00:00+02:00[Europe/Zurich]",
                "expires_at": "not-a-date Europe/Zurich",
                "approved_at": "2099-04-30T09:00:00Z",
                "approved_contract_snapshot_reference": "sha256:stale",
                "write_authority": "write_anywhere",
            }
        )
        approval_values = {
            "line_1": "APPROVE SCHEDULES",
            "line_2": "Schedule contract: CONTRACT-001 v1",
            "line_3": "Expires: not-a-date Europe/Zurich",
            "parsed_contract_id": "CONTRACT-001",
            "parsed_contract_version": "v1",
            "parsed_expiry_local_with_iana_timezone": "not-a-date Europe/Zurich",
            "completed_reply_reference": "REPLY-SCHEDULE-001",
            "validation_status": "passed",
            "recorded_at": "2099-04-30T09:01:00Z",
        }
        contract["lecturer_approval"].update({"status": "approved", **approval_values})
        state["status"] = "active"
        state["schedules"] = [contract]
        registration = state["schedule_registration"]
        registration.update(
            {
                "status": "approved",
                "no_write_simulation_status": "passed",
                "no_write_simulation_result": "passed",
                "no_write_simulation_recorded_at": "2099-04-30T08:59:00Z",
                "approved_standing_contract_ids": ["CONTRACT-001"],
                "approved_standing_contract_versions": ["v1"],
            }
        )
        registration["approval"].update(approval_values)
        errors = self.validator.validate(state)
        for phrase in (
            "safety field write_authority diverges",
            "baseline_approvals is missing gate_0_approval_id",
            "expires_at must use canonical offset[IANA/Timezone] format",
            "snapshot reference must match its canonical SHA-256",
        ):
            self.assertTrue(any(phrase in error for error in errors), (phrase, errors))

    def test_validator_rejects_fake_timezone_and_date_specific_offset_mismatch(self) -> None:
        self.assertFalse(self.validator._valid_iana_timezone("Fake/Nowhere"))
        fake_errors: list[str] = []
        self.assertIsNone(
            self.validator._parse_zoned_datetime(
                "2099-05-31T09:00:00+09:00[Fake/Nowhere]",
                "Fake/Nowhere",
                "fake-zone",
                fake_errors,
            )
        )
        self.assertTrue(any("unavailable IANA timezone" in error for error in fake_errors))
        offset_errors: list[str] = []
        self.assertIsNone(
            self.validator._parse_zoned_datetime(
                "2099-05-31T09:00:00+09:00[Europe/Zurich]",
                "Europe/Zurich",
                "wrong-offset",
                offset_errors,
            )
        )
        self.assertTrue(any("offset does not match" in error for error in offset_errors))

    def test_validator_rejects_duplicate_offer_idempotency_key(self) -> None:
        state, first = self.completed_run_state()
        second = copy.deepcopy(first)
        second["run_id"] = "RUN-SYNTHETIC-002"
        second["task_chat_reference"] = "TASK-SYNTHETIC-002"
        for gate_name in ("production_completion", "hitl_3", "system_improvement_review_offer"):
            gate = second["approvals"][gate_name]
            serialized = json.dumps(gate).replace("RUN-SYNTHETIC-001", "RUN-SYNTHETIC-002")
            second["approvals"][gate_name] = json.loads(serialized)
        second["approvals"]["system_improvement_review_offer"]["offer"][
            "offer_id"
        ] = first["approvals"]["system_improvement_review_offer"]["offer"]["offer_id"]
        state["runs"].append(second)
        errors = self.validator.validate(state)
        self.assertTrue(any("duplicate system-review offer idempotency key" in error for error in errors), errors)

    def test_umbrella_route_is_enforced(self) -> None:
        state = copy.deepcopy(self.state)
        state["umbrella_entry_routing"]["initial_gate"] = "GATE_1"
        errors = self.validator.validate(state)
        self.assertTrue(any("umbrella entry" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
