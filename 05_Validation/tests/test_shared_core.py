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
MIGRATION_PATH = CORE / "scripts" / "migrate_state_v7_to_v8.py"
VALIDATOR_PATH = CORE / "scripts" / "validate_state.py"
SOURCE_MANIFEST_PATH = CORE / "scripts" / "source_manifest.py"
FINGERPRINT_PATH = CORE / "scripts" / "fingerprint_file.py"
V022_STATE_SPEC = (
    "v0.2.2:03_Shared_Workflow_Core/course-project-template/01_Control/state.json"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def downgrade_v8_to_v7(state: dict) -> dict:
    """Create a safe synthetic schema-7 fixture for the preview-only migration."""

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


def load_tagged_v022_state() -> dict:
    """Load the published schema-7 template, not a schema-8 approximation."""

    result = subprocess.run(
        ["git", "show", V022_STATE_SPEC],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise AssertionError(f"published v0.2.2 fixture is unavailable: {result.stderr}")
    state = json.loads(result.stdout)
    if state.get("schema_version") != 7 or state.get("plugin_version") != "0.2.2":
        raise AssertionError("published v0.2.2 fixture has unexpected schema/version")
    return state


class SharedCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.setup = load_module("shared_setup", SETUP_PATH)
        cls.migration = load_module("shared_migration_v8", MIGRATION_PATH)
        cls.validator = load_module("shared_validate_v8", VALIDATOR_PATH)
        cls.source_manifest = load_module("shared_source_manifest", SOURCE_MANIFEST_PATH)
        cls.fingerprinter = load_module("shared_fingerprint", FINGERPRINT_PATH)
        cls.state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
        cls.v022_state = load_tagged_v022_state()

    def legacy_failed_safe_state(self) -> tuple[dict, dict]:
        state = copy.deepcopy(self.v022_state)
        run = copy.deepcopy(state["run_template"])
        run.update(
            {
                "template_only": False,
                "run_id": "RUN-LEGACY-FAILED-SAFE-001",
                "task_chat_reference": "TASK-LEGACY-001",
                "mode": "manual",
                "status": "failed_safe",
                "started_at": "2026-08-20T10:00:00Z",
                "current_gate": "RUN_TERMINATED",
                "next_permitted_action": "none",
            }
        )
        run["termination"].update(
            {
                "status": "failed_safe",
                "reason": "synthetic fail-safe terminal history",
                "recorded_at": "2026-08-20T10:01:00Z",
            }
        )
        state["active_run_id"] = None
        state["runs"] = [run]
        return state, run

    def legacy_schedule_history_state(self, status: str = "paused") -> tuple[dict, dict]:
        """Populate the actual published v0.2.2 schedule shape as inactive history."""

        state = copy.deepcopy(self.v022_state)
        schedule = copy.deepcopy(state["standing_schedule_contract_template"])
        schedule.update(
            {
                "contract_id": "CONTRACT-LEGACY-SCHEDULE-001",
                "contract_version": "v1",
                "status": status,
                "project": {
                    "project_id": "PROJECT-LEGACY-001",
                    "project_root": "C:/Synthetic/LegacyCourseProject",
                },
                "course": {
                    "course_id": "COURSE-LEGACY-001",
                    "course_title": "Synthetic legacy course",
                },
                "main_goal": "synthetic bounded scheduled review",
                "success_criteria": ["synthetic criterion"],
                "stop_conditions": ["stop at Gate 2B"],
                "constraints": ["synthetic only"],
                "permitted_tools": ["local_read_only"],
                "permitted_actions": ["bounded_scheduled_review"],
                "data_egress_boundary": "no external egress",
                "permitted_source_classes": ["student_safe"],
                "permitted_output_audiences": ["lecturer_only"],
                "source_access_policy_version": "SAP-LEGACY-v1",
                "source_access_policy_fingerprint": "POLICY-LEGACY-001",
                "assessment_security_boundary": "no answer leakage",
                "timezone": "UTC",
                "recurrence": ["annual-synthetic-review"],
                "approved_contract_snapshot_reference": "sha256:LEGACY-SNAPSHOT-001",
                "approved_at": "2024-12-31T12:00:00Z",
                "activation_time": "2025-01-01T00:00:00+00:00[UTC]",
                "expires_at": "2025-12-31T23:59:59+00:00[UTC]",
                "last_reconfirmed_at": "2024-12-31T12:00:00Z",
            }
        )
        schedule["runtime_versions"].update(
            {
                "prompt_version": "v0.2.2",
                "skill_version": "0.2.2",
                "validated_system_proposal_id": "ACR-SYS-LEGACY",
                "validated_system_proposal_version": "v0.2.2",
                "activation_decision_reference": "ACTIVATE-LEGACY-001",
            }
        )
        schedule["baseline_approvals"].update(
            {
                "gate_0_approval_id": "GATE0-LEGACY-001",
                "gate_1_approval_id": "GATE1-LEGACY-001",
                "source_manifest_path": "01_Control/source-hashes.csv",
                "source_manifest_fingerprint": "MANIFEST-LEGACY-001",
                "source_access_policy_version": "SAP-LEGACY-v1",
                "source_access_policy_fingerprint": "POLICY-LEGACY-001",
                "verified_still_valid_at": "2024-12-31T11:59:00Z",
                "verification_result": "passed",
            }
        )
        schedule["lecturer_approval"].update(
            {
                "status": "approved",
                "line_1": "APPROVE SCHEDULES",
                "line_2": "Schedule contract: CONTRACT-LEGACY-SCHEDULE-001 v1",
                "line_3": "Expires: 2025-12-31T23:59:59+00:00[UTC]",
                "completed_reply_reference": "REPLY-SCHEDULE-LEGACY-001",
                "validation_status": "passed",
                "recorded_at": "2024-12-31T12:00:00Z",
            }
        )
        if status == "paused":
            schedule["pause"].update(
                {
                    "lecturer_direction_reference": "PAUSE-LEGACY-001",
                    "paused_at": "2025-06-01T00:00:00Z",
                }
            )
        if status == "cancelled":
            schedule["rollback"].update(
                {
                    "status": "completed",
                    "rollback_reference": "CANCEL-LEGACY-001",
                    "rolled_back_at": "2025-06-01T00:00:00Z",
                }
            )
        state["schedules"] = [schedule]
        return state, schedule

    def accepted_before_review_state(
        self, *, run_status: str = "waiting_at_gate", keep_active: bool = True
    ) -> tuple[dict, dict]:
        state, run = self.completed_run_state()
        run["approvals"]["system_improvement_review_offer"] = copy.deepcopy(
            self.state["run_template"]["approvals"]["system_improvement_review_offer"]
        )
        run["approvals"]["trigger_guidance_offer"] = copy.deepcopy(
            self.state["run_template"]["approvals"]["trigger_guidance_offer"]
        )
        run["termination"] = copy.deepcopy(self.state["run_template"]["termination"])
        run["status"] = run_status
        run["current_gate"] = "SYSTEM_REVIEW_OFFER"
        run["next_permitted_action"] = (
            "persist_and_present_mandatory_system_improvement_review_offer_once"
        )
        if run_status in {"completed", "handed_off"}:
            run["termination"].update(
                {
                    "status": run_status,
                    "reason": "synthetic premature terminal closeout",
                    "recorded_at": "2026-08-21T10:05:00Z",
                }
            )
        state["active_run_id"] = run["run_id"] if keep_active else None
        return state, run

    def historical_schedule_state(
        self,
        status: str,
        *,
        base_state: dict | None = None,
        triggered_run_id: str | None = None,
    ) -> tuple[dict, dict]:
        state = copy.deepcopy(base_state if base_state is not None else self.state)
        contract = copy.deepcopy(state["standing_schedule_contract_template"])
        current_fingerprint = state["material_processing_eligibility"].get("fingerprint")
        eligibility_fingerprint = current_fingerprint or "ELIGIBILITY-HISTORICAL-001"
        contract.update(
            {
                "schedule_id": "SCHEDULE-HISTORICAL-001",
                "contract_id": "CONTRACT-HISTORICAL-001",
                "contract_version": "v1",
                "status": status,
                "project": {
                    "project_id": "PROJECT-HISTORICAL-001",
                    "project_root": "C:/Synthetic/CourseProject",
                },
                "course": {
                    "course_id": "COURSE-HISTORICAL-001",
                    "course_title": "Synthetic historical course",
                },
                "main_goal": "synthetic bounded scheduled review",
                "success_criteria": ["synthetic criterion"],
                "stop_conditions": ["stop at Gate 2B"],
                "constraints": ["synthetic only"],
                "permitted_tools": ["local_read_only"],
                "permitted_actions": ["bounded_scheduled_review"],
                "data_egress_boundary": "no external egress",
                "permitted_source_classes": ["student_safe"],
                "permitted_output_audiences": ["lecturer_only"],
                "material_processing_eligibility_fingerprint": eligibility_fingerprint,
                "source_access_policy_version": "SAP-HISTORICAL-v1",
                "source_access_policy_fingerprint": "POLICY-HISTORICAL-001",
                "assessment_security_boundary": "no answer leakage",
                "timezone": "UTC",
                "recurrence": ["annual-synthetic-review"],
                "activation_time": "2025-01-01T00:00:00+00:00[UTC]",
                "expires_at": "2025-12-31T23:59:59+00:00[UTC]",
                "approved_at": "2024-12-31T12:00:00Z",
                "last_reconfirmed_at": "2024-12-31T12:00:00Z",
            }
        )
        contract["baseline_approvals"].update(
            {
                "gate_0a_approval_id": "GATE0A-HISTORICAL-001",
                "gate_0_approval_id": "GATE0-HISTORICAL-001",
                "gate_1_approval_id": "GATE1-HISTORICAL-001",
                "material_processing_eligibility_fingerprint": eligibility_fingerprint,
                "source_manifest_path": "01_Control/source-hashes.csv",
                "source_manifest_fingerprint": "MANIFEST-HISTORICAL-001",
                "source_access_policy_version": "SAP-HISTORICAL-v1",
                "source_access_policy_fingerprint": "POLICY-HISTORICAL-001",
                "verified_still_valid_at": "2024-12-31T11:59:00Z",
                "verification_result": "passed",
            }
        )
        contract["runtime_versions"].update(
            {
                "prompt_version": "v0.2.3",
                "skill_version": "0.2.3",
                "validated_system_proposal_id": "ACR-SYS-HISTORICAL",
                "validated_system_proposal_version": "v0.2.3",
                "activation_decision_reference": "ACTIVATE-HISTORICAL-001",
            }
        )
        contract["lecturer_approval"].update(
            {
                "status": "approved",
                "line_1": "APPROVE SCHEDULES",
                "line_2": "Schedule contract: CONTRACT-HISTORICAL-001 v1",
                "line_3": "Expires: 2025-12-31T23:59:59+00:00[UTC]",
                "parsed_contract_id": "CONTRACT-HISTORICAL-001",
                "parsed_contract_version": "v1",
                "parsed_expiry_local_with_iana_timezone": (
                    "2025-12-31T23:59:59+00:00[UTC]"
                ),
                "completed_reply_reference": "REPLY-SCHEDULE-HISTORICAL-001",
                "validation_status": "passed",
                "recorded_at": "2024-12-31T12:00:00Z",
            }
        )
        contract["approved_contract_snapshot_reference"] = (
            self.validator._expected_contract_snapshot_reference(contract)
        )
        receipt = contract["status_transition_receipt"]
        receipt.update(
            {
                "status": status,
                "reason": f"synthetic {status} transition",
                "decision_or_detection_reference": f"TRANSITION-{status.upper()}-001",
                "recorded_at": "2026-01-01T00:00:00Z",
                "future_triggers_disabled": True,
                "no_course_action": True,
                "triggered_run_id": triggered_run_id,
                "preserved_contract_snapshot_reference": contract[
                    "approved_contract_snapshot_reference"
                ],
            }
        )
        contract["status_history"] = [copy.deepcopy(receipt)]
        state["status"] = "candidate_not_active"
        state["schedules"] = [contract]
        state["schedule_registration"] = copy.deepcopy(
            self.state["schedule_registration"]
        )
        return state, contract

    def terminal_scheduled_history_run_state(
        self,
        *,
        run_status: str,
        contract_status_at_trigger: str,
        trigger_created_at: str,
    ) -> tuple[dict, dict, dict]:
        """Build a terminal scheduled-run receipt against later-expired history."""

        base, _ = self.completed_run_state()
        base["runs"] = []
        base["active_run_id"] = None
        run_id = f"RUN-SCHEDULE-{run_status.upper().replace('_', '-')}-001"
        state, contract = self.historical_schedule_state(
            "expired",
            base_state=base,
            triggered_run_id=run_id if run_status == "expired" else None,
        )
        run = copy.deepcopy(state["run_template"])
        eligibility_fingerprint = state["material_processing_eligibility"]["fingerprint"]
        run.update(
            {
                "template_only": False,
                "run_id": run_id,
                "task_chat_reference": f"TASK-SCHEDULE-{run_status.upper()}-001",
                "mode": "scheduled",
                "status": run_status,
                "started_at": trigger_created_at,
                "current_gate": "RUN_TERMINATED",
                "next_permitted_action": f"none_{run_status}",
            }
        )
        reference = {
            "schedule_id": contract["schedule_id"],
            "contract_id": contract["contract_id"],
            "contract_version": contract["contract_version"],
            "approved_contract_snapshot_reference": contract[
                "approved_contract_snapshot_reference"
            ],
            "contract_status_at_trigger": contract_status_at_trigger,
        }
        run["trigger"].update(
            {
                "trigger_id": f"TRIGGER-SCHEDULE-{run_status.upper()}-001",
                "trigger_type": "scheduled",
                "created_at": trigger_created_at,
                "material_processing_eligibility_fingerprint": eligibility_fingerprint,
                "standing_schedule_contract_reference": reference,
            }
        )
        run["execution_authority"]["standing_contract_reference"] = copy.deepcopy(
            reference
        )
        run["contract"]["material_processing_eligibility_fingerprint"] = (
            eligibility_fingerprint
        )
        run["contract"]["contract_id"] = f"RC-SCHEDULE-{run_status.upper()}-001"
        run["source_manifest_verification"][
            "material_processing_eligibility_fingerprint"
        ] = eligibility_fingerprint
        run["approvals"]["gate_0a"].update(
            {
                "status": "approved",
                "approval_id": f"GATE0A-SCHEDULE-{run_status.upper()}-001",
                "material_processing_eligibility_fingerprint": eligibility_fingerprint,
                "lecturer_declaration_reference": "REPLY-ELIGIBILITY-001",
                "validation_status": "passed",
                "recorded_at": trigger_created_at,
            }
        )
        run["termination"].update(
            {
                "status": run_status,
                "reason": f"synthetic terminal {run_status} schedule history",
                "recorded_at": trigger_created_at,
            }
        )
        state["runs"] = [run]
        return state, run, contract

    def completed_run_state(self) -> tuple[dict, dict]:
        state = copy.deepcopy(self.state)
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
        eligibility["fingerprint"] = self.validator._canonical_eligibility_fingerprint(
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
                    self.validator.REQUIRED_SYSTEM_REVIEW_SCOPE
                ),
                "question_text": self.validator.MANDATORY_SYSTEM_REVIEW_QUESTION,
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

    def test_shared_state_is_schema_8_inactive_unscheduled_and_pre_source(self) -> None:
        self.assertEqual(self.state["schema_version"], 8)
        self.assertEqual(self.state["plugin_version"], "0.2.4")
        self.assertEqual(self.state["status"], "candidate_not_active")
        self.assertEqual(self.state["schedules"], [])
        self.assertEqual(
            self.state["umbrella_entry_routing"], self.validator.EXPECTED_UMBRELLA_ROUTING
        )
        self.assertEqual(
            self.state["material_processing_eligibility"]["status"],
            "awaiting_lecturer_declaration",
        )
        self.assertIsNone(self.state["material_processing_eligibility"]["fingerprint"])

    def test_gate_0a_rejects_public_only_without_explicit_ai_processing_authority(self) -> None:
        state = copy.deepcopy(self.state)
        eligibility = state["material_processing_eligibility"]
        eligibility.update(
            {
                "eligibility_id": "ELIG-PUBLIC-ONLY",
                "status": "approved",
                "lecturer_declaration_reference": "REPLY-PUBLIC-ONLY",
                "recorded_at": "2026-08-21T11:00:00Z",
            }
        )
        eligibility["environment"]["category"] = "personal_or_unmanaged"
        eligibility["material_scope"].update(
            {
                "declared_category": "appropriately_licensed_or_public_with_explicit_ai_processing_authority",
                "ai_processing_authority_confirmed": False,
                "contains_institution_internal_or_restricted_material": False,
                "contains_student_personal_data": False,
                "sensitivity_classification": "non_sensitive",
                "assessment_security_classification": "no_protected_assessment_material",
                "assessment_security_handling_authorised": True,
            }
        )
        eligibility["decision"].update(
            {"outcome": "proceed", "reason": "public only", "approved_processing_scope": "none"}
        )
        eligibility["fingerprint"] = self.validator._canonical_eligibility_fingerprint(
            eligibility
        )
        errors = self.validator.validate(state)
        self.assertTrue(
            any("explicit AI-processing authority" in error for error in errors), errors
        )

    def test_gate_0a_routes_internal_material_out_of_personal_environment(self) -> None:
        state = copy.deepcopy(self.state)
        eligibility = state["material_processing_eligibility"]
        eligibility.update(
            {
                "eligibility_id": "ELIG-INTERNAL-PERSONAL",
                "status": "approved",
                "lecturer_declaration_reference": "REPLY-INTERNAL-PERSONAL",
                "recorded_at": "2026-08-21T11:00:00Z",
            }
        )
        eligibility["environment"]["category"] = "personal_or_unmanaged"
        eligibility["material_scope"].update(
            {
                "declared_category": "institution_internal_or_restricted",
                "ai_processing_authority_confirmed": True,
                "contains_institution_internal_or_restricted_material": True,
                "contains_student_personal_data": False,
                "sensitivity_classification": "institution_internal_or_restricted",
                "assessment_security_classification": "no_protected_assessment_material",
                "assessment_security_handling_authorised": True,
            }
        )
        eligibility["decision"].update(
            {"outcome": "proceed", "reason": "unsafe synthetic case", "approved_processing_scope": "none"}
        )
        eligibility["fingerprint"] = self.validator._canonical_eligibility_fingerprint(
            eligibility
        )
        errors = self.validator.validate(state)
        self.assertTrue(any("must be route-only" in error for error in errors), errors)

    def test_gate_0a_requires_total_status_decision_outcome_consistency(self) -> None:
        for status, outcome in (
            ("route_only", "proceed"),
            ("failed_closed", "proceed"),
            ("failed_closed", "route_only"),
        ):
            with self.subTest(status=status, outcome=outcome):
                state, _ = self.completed_run_state()
                eligibility = state["material_processing_eligibility"]
                eligibility["status"] = status
                eligibility["decision"]["outcome"] = outcome
                eligibility["fingerprint"] = (
                    self.validator._canonical_eligibility_fingerprint(eligibility)
                )
                errors = self.validator.validate(state)
                self.assertTrue(
                    any(
                        "status/decision outcome combination is invalid" in error
                        for error in errors
                    ),
                    errors,
                )

    def test_gate_0a_reconfirmation_blocks_state_and_manifest_intake(self) -> None:
        state, _ = self.completed_run_state()
        eligibility = state["material_processing_eligibility"]
        eligibility["reconfirmation_required"] = True
        eligibility["fingerprint"] = self.validator._canonical_eligibility_fingerprint(
            eligibility
        )
        errors = self.validator.validate(state)
        self.assertTrue(any("reconfirmation is required" in error for error in errors), errors)
        with tempfile.TemporaryDirectory() as temp:
            record = Path(temp) / "material-processing-eligibility.json"
            record.write_text(json.dumps(eligibility), encoding="utf-8")
            intake = self.source_manifest.validate_eligibility(record)
        self.assertFalse(intake["ok"])
        self.assertTrue(
            any("reconfirmation is required" in error for error in intake["errors"]),
            intake,
        )

    def test_gate_0a_institutional_record_requires_explicit_security_declarations(self) -> None:
        state = copy.deepcopy(self.state)
        eligibility = state["material_processing_eligibility"]
        eligibility.update(
            {
                "eligibility_id": "ELIG-MISSING-SECURITY",
                "status": "approved",
                "lecturer_declaration_reference": "REPLY-001",
                "recorded_at": "2026-08-21T12:00:00Z",
                "reconfirmation_required": False,
            }
        )
        eligibility["environment"].update(
            {
                "category": "approved_institutional_exact_environment",
                "exact_environment_reference": "SYNTHETIC-INST-ENV",
                "institutional_policy_reference": "SYNTHETIC-POLICY",
                "approved_scope": "all synthetic",
                "policy_expires_at": "2099-12-31T23:59:59+01:00[Europe/Zurich]",
            }
        )
        eligibility["material_scope"].update(
            {
                "declared_category": None,
                "ai_processing_authority_confirmed": True,
                "contains_institution_internal_or_restricted_material": None,
                "contains_student_personal_data": None,
                "sensitivity_classification": None,
                "assessment_security_classification": None,
                "assessment_security_handling_authorised": None,
            }
        )
        eligibility["decision"].update(
            {
                "outcome": "proceed",
                "reason": "synthetic missing declarations",
                "approved_processing_scope": "synthetic",
            }
        )
        eligibility["fingerprint"] = self.validator._canonical_eligibility_fingerprint(
            eligibility
        )
        errors = self.validator.validate(state)
        for phrase in (
            "allowed material category",
            "sensitivity classification",
            "assessment-security classification",
            "assessment_security_handling_authorised as boolean",
        ):
            self.assertTrue(any(phrase in error for error in errors), (phrase, errors))
        with tempfile.TemporaryDirectory() as temp:
            record = Path(temp) / "material-processing-eligibility.json"
            record.write_text(json.dumps(eligibility), encoding="utf-8")
            intake = self.source_manifest.validate_eligibility(record)
        self.assertFalse(intake["ok"])
        self.assertTrue(any("allowed material category" in error for error in intake["errors"]))

    def test_gate_0a_personal_environment_excludes_student_personal_data(self) -> None:
        state, _ = self.completed_run_state()
        eligibility = state["material_processing_eligibility"]
        eligibility["material_scope"].update(
            {
                "contains_student_personal_data": True,
                "sensitivity_classification": "student_personal_data",
            }
        )
        eligibility["fingerprint"] = self.validator._canonical_eligibility_fingerprint(
            eligibility
        )
        errors = self.validator.validate(state)
        self.assertTrue(any("must exclude student personal data" in error for error in errors), errors)
        with tempfile.TemporaryDirectory() as temp:
            record = Path(temp) / "material-processing-eligibility.json"
            record.write_text(json.dumps(eligibility), encoding="utf-8")
            intake = self.source_manifest.validate_eligibility(record)
        self.assertFalse(intake["ok"])
        self.assertTrue(any("student personal data" in error for error in intake["errors"]))

    def test_manifest_validates_gate_0a_before_project_resolution(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            invalid_record = root / "invalid-eligibility.json"
            invalid_record.write_text("{}", encoding="utf-8")
            missing_project = root / "course-source-root-must-not-be-resolved"
            created = self.source_manifest.create(
                missing_project,
                Path("01_Control/source-hashes.csv"),
                False,
                invalid_record,
            )
            verified = self.source_manifest.verify(
                missing_project,
                Path("01_Control/source-hashes.csv"),
                invalid_record,
            )
        for result in (created, verified):
            self.assertFalse(result["ok"])
            self.assertFalse(result["source_enumeration_started"])
            self.assertTrue(any("Gate-0A" in error for error in result["errors"]), result)

    def test_fingerprinter_has_no_ungated_raw_or_disguised_control_mode(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            arbitrary = root / "course-source.json"
            arbitrary.write_text('{"schema_version": 1}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "mode must be"):
                self.fingerprinter.fingerprint(arbitrary, "raw")
            with self.assertRaisesRegex(ValueError, "restricted to 01_Control"):
                self.fingerprinter.fingerprint(arbitrary, "eligibility")

    def test_fingerprinter_validates_gate_0a_before_course_source_read(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            invalid_record = root / "invalid-eligibility.json"
            invalid_record.write_text("{}", encoding="utf-8")
            missing_source = root / "must-not-be-inspected.txt"
            with self.assertRaisesRegex(PermissionError, "Gate-0A does not permit"):
                self.fingerprinter.fingerprint(
                    missing_source,
                    "course-source",
                    eligibility_record=invalid_record,
                )

    def test_fingerprinter_allows_only_structured_gate_0a_bootstrap(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            control = Path(temp) / "01_Control"
            control.mkdir()
            record = control / "material-processing-eligibility.json"
            record.write_text(
                json.dumps(self.state["material_processing_eligibility"]),
                encoding="utf-8",
            )
            digest, _ = self.fingerprinter.fingerprint(record, "eligibility")
        self.assertEqual(
            digest,
            self.validator._canonical_eligibility_fingerprint(
                self.state["material_processing_eligibility"]
            ),
        )

    def test_course_scope_accepts_diverse_synthetic_profiles(self) -> None:
        profiles = (
            ("school", "Biology", "Year 8", "English"),
            ("vocational_education_and_training", "Welding", "Apprenticeship", "German"),
            ("professional_learning", "Clinical supervision", "Continuing education", "French"),
            ("higher_education", "Literature", "Bachelor", "English"),
            ("other_lecturer_defined", "Community media", "Mixed adult learners", "Spanish"),
        )
        for context, discipline, level, language in profiles:
            with self.subTest(context=context):
                state = copy.deepcopy(self.state)
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
                self.assertEqual(self.validator.validate(state), [])

    def test_setup_skill_collects_course_specific_adaptation_inputs(self) -> None:
        text = (
            CORE / "agent-skills" / "course-redesign-setup" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "course title, discipline, level, programme, language, learner profile, and group size",
            "current/deployed learning objectives",
            "current assessment files, stakes, grading system, pass rule",
            "constraints, accessibility, workload, and style expectations",
        ):
            self.assertIn(phrase, text)

    def test_schedule_template_is_gate_0a_bound_expiring_and_future_only(self) -> None:
        contract = self.state["standing_schedule_contract_template"]
        self.assertTrue(contract["activation_requires_non_null_expires_at"])
        self.assertTrue(contract["no_immediate_run"])
        self.assertIn(
            "gate_0a_approval_id", contract["baseline_approvals"]
        )
        self.assertIn(
            "material_processing_eligibility_fingerprint",
            contract["baseline_approvals"],
        )
        self.assertTrue(contract["terminal_rules"]["on_or_after_expiry"].startswith("return_expired"))

    def test_schema_records_match_preview_migration_canonical_shapes(self) -> None:
        run = self.state["run_template"]
        self.assertEqual(run["resume_protocol"], self.validator.EXPECTED_RESUME_PROTOCOL)
        self.assertEqual(
            run["approvals"]["system_improvement_review_offer"]["required_question_scope"],
            self.validator.REQUIRED_SYSTEM_REVIEW_SCOPE,
        )
        question = self.validator.MANDATORY_SYSTEM_REVIEW_QUESTION
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

    def test_v7_migration_preview_is_non_mutating_idempotent_and_preserving(self) -> None:
        source = downgrade_v8_to_v7(self.state)
        source["run_template"]["contract"]["permitted_tools"] = ["local_read_only"]
        before = copy.deepcopy(source)
        first = self.migration.preview_migration(source, source="synthetic-v7")
        self.assertEqual(source, before)
        self.assertTrue(first["ok"])
        self.assertFalse(first["would_write"])
        candidate = first["candidate_state"]
        self.assertEqual(candidate["status"], "candidate_not_active")
        self.assertEqual(candidate["schedules"], source["schedules"])
        self.assertEqual(candidate["run_template"]["contract"]["permitted_tools"], [])
        self.assertTrue(all(first["preservation_checks"].values()))
        self.assertTrue(first["reconfirmation_required"])
        self.assertEqual(candidate["schema_version"], 8)
        second = self.migration.preview_migration(candidate, source="synthetic-v8")
        self.assertEqual(second["changed_paths"], [])
        self.assertEqual(second["candidate_state"], candidate)
        self.assertTrue(second["reconfirmation_required"])
        self.assertFalse(second["candidate_activation_ready"])
        self.assertEqual(
            second["required_before_use"], first["required_before_use"]
        )

    def test_schema_8_preview_rejects_invalid_existing_state(self) -> None:
        source = copy.deepcopy(self.state)
        source["umbrella_entry_routing"]["initial_gate"] = "GATE_1"
        before = copy.deepcopy(source)
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "schema-8 state is invalid",
        ):
            self.migration.preview_migration(source, source="unsafe-schema-v8")
        self.assertEqual(source, before)

    def test_schema_8_preview_rejects_expanded_system_review_authority(self) -> None:
        state = copy.deepcopy(self.state)
        state["run_template"]["approvals"]["system_improvement_review_offer"][
            "authority_on_request"
        ]["authorises"].append("modify_system_files")
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "schema-8 state is invalid",
        ):
            self.migration.preview_migration(state, source="unsafe-schema-v8")

    def test_v7_migration_cli_never_writes_source(self) -> None:
        source = downgrade_v8_to_v7(self.state)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "state-v7.json"
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

    def test_v7_migration_preserves_existing_run_lineage_and_permissions(self) -> None:
        source, source_run = self.legacy_failed_safe_state()
        source_run = source["runs"][0]
        source_run["contract"]["permitted_tools"] = ["local_read_only"]
        source_run["contract"]["permitted_actions"] = ["inspect_approved_sources"]
        source_before = copy.deepcopy(source)
        report = self.migration.preview_migration(source, source=V022_STATE_SPEC)
        migrated = report["candidate_state"]["runs"][0]
        self.assertEqual(source, source_before)
        self.assertEqual(migrated, source_run)
        for field in ("run_id", "task_chat_reference", "plan_version"):
            self.assertEqual(migrated[field], source_run[field])
        self.assertEqual(migrated["contract"]["contract_id"], source_run["contract"]["contract_id"])
        self.assertEqual(migrated["contract"]["permitted_tools"], ["local_read_only"])
        self.assertEqual(
            migrated["contract"]["permitted_actions"], ["inspect_approved_sources"]
        )
        self.assertEqual(migrated["status"], "failed_safe")
        self.assertEqual(migrated["termination"]["status"], "failed_safe")
        receipt = report["candidate_state"]["legacy_preserved_run_history"]["receipts"][0]
        self.assertEqual(receipt["run_index"], 0)
        self.assertEqual(receipt["run_id"], source_run["run_id"])
        self.assertEqual(receipt["terminal_status"], "failed_safe")
        self.assertEqual(
            receipt["canonical_json_sha256"],
            self.migration._canonical_json_sha256(source_run),
        )
        self.assertEqual(self.validator.validate(report["candidate_state"]), [])

    def test_v7_migration_rejects_malformed_or_tampered_legacy_history(self) -> None:
        malformed, _ = self.legacy_failed_safe_state()
        malformed["runs"][0]["termination"]["reason"] = None
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "unsafe schema-7 run history",
        ):
            self.migration.preview_migration(malformed, source=V022_STATE_SPEC)

        source, _ = self.legacy_failed_safe_state()
        candidate = self.migration.preview_migration(
            source, source=V022_STATE_SPEC
        )["candidate_state"]
        candidate["runs"][0]["termination"]["reason"] = "tampered after receipt"
        errors = self.validator.validate(candidate)
        self.assertTrue(any("canonical SHA-256" in error for error in errors), errors)

    def test_v7_migration_rejects_nonterminal_history_without_rewriting_it(self) -> None:
        source = copy.deepcopy(self.v022_state)
        run = copy.deepcopy(source["run_template"])
        run.update(
            {
                "template_only": False,
                "run_id": "RUN-LEGACY-ACTIVE-001",
                "mode": "manual",
                "status": "waiting_at_gate",
                "started_at": "2026-08-20T10:00:00Z",
            }
        )
        source["active_run_id"] = run["run_id"]
        source["runs"] = [run]
        before = copy.deepcopy(source)
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "not terminal schema-7 history",
        ):
            self.migration.preview_migration(source, source=V022_STATE_SPEC)
        self.assertEqual(source, before)

    def test_v7_migration_preserves_inactive_actual_v022_schedule_history(self) -> None:
        for status in ("paused", "expired", "cancelled"):
            with self.subTest(status=status):
                source, source_schedule = self.legacy_schedule_history_state(status)
                before = copy.deepcopy(source)
                report = self.migration.preview_migration(
                    source, source=V022_STATE_SPEC
                )
                candidate = report["candidate_state"]
                self.assertEqual(source, before)
                self.assertEqual(candidate["schedules"], [source_schedule])
                marker = candidate["legacy_preserved_schedule_history"]
                self.assertEqual(
                    marker["validation_profile"],
                    "schema_7_inactive_schedule_history_v0_2_2",
                )
                receipt = marker["receipts"][0]
                self.assertEqual(receipt["schedule_index"], 0)
                self.assertEqual(receipt["contract_id"], source_schedule["contract_id"])
                self.assertEqual(receipt["status"], status)
                self.assertEqual(
                    receipt["canonical_json_sha256"],
                    self.migration._canonical_json_sha256(source_schedule),
                )
                self.assertTrue(
                    candidate["schema_8_migration_hold"][
                        "schedule_reconfirmation_required"
                    ]
                )
                self.assertEqual(self.validator.validate(candidate), [])
                repeated = self.migration.preview_migration(
                    candidate, source="schema-8-schedule-history-preview"
                )
                self.assertEqual(repeated["candidate_state"], candidate)
                self.assertTrue(repeated["reconfirmation_required"])

    def test_v7_migration_rejects_malformed_or_operational_schedule_history(self) -> None:
        malformed = copy.deepcopy(self.v022_state)
        malformed["schedules"] = [{"schedule_id": "MALFORMED-LEGACY"}]
        before = copy.deepcopy(malformed)
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "unsafe schema-7 schedule history",
        ):
            self.migration.preview_migration(malformed, source=V022_STATE_SPEC)
        self.assertEqual(malformed, before)

        operational, _ = self.legacy_schedule_history_state("paused")
        operational["schedules"][0]["status"] = "active"
        operational["schedule_registration"]["status"] = "approved"
        before = copy.deepcopy(operational)
        with self.assertRaisesRegex(
            self.migration.MigrationError,
            "currently registered schedules must be disabled",
        ):
            self.migration.preview_migration(operational, source=V022_STATE_SPEC)
        self.assertEqual(operational, before)

    def test_v7_migration_detects_tampered_schedule_after_receipt(self) -> None:
        source, _ = self.legacy_schedule_history_state("paused")
        candidate = self.migration.preview_migration(
            source, source=V022_STATE_SPEC
        )["candidate_state"]
        candidate["schedules"][0]["constraints"].append("tampered after receipt")
        errors = self.validator.validate(candidate)
        self.assertTrue(
            any("canonical SHA-256" in error for error in errors),
            errors,
        )

    def test_v7_migration_rejects_active_or_suspended_runtime_without_rewriting(self) -> None:
        for status in ("active", "suspended"):
            with self.subTest(status=status):
                source = copy.deepcopy(self.v022_state)
                source["status"] = status
                source["activation"]["activated_at"] = "2026-08-20T10:00:00Z"
                before = copy.deepcopy(source)
                with self.assertRaisesRegex(
                    self.migration.MigrationError,
                    "explicitly inactive",
                ):
                    self.migration.preview_migration(source, source=V022_STATE_SPEC)
                self.assertEqual(source, before)

    def test_v7_migration_fails_closed_on_unsupported_or_conflicting_input(self) -> None:
        unsupported = downgrade_v8_to_v7(self.state)
        unsupported["schema_version"] = 6
        with self.assertRaises(self.migration.MigrationError):
            self.migration.preview_migration(unsupported)
        conflicting = downgrade_v8_to_v7(self.state)
        conflicting.pop("activation")
        with self.assertRaises(self.migration.MigrationError):
            self.migration.preview_migration(conflicting)

    def test_validator_accepts_canonical_template(self) -> None:
        self.assertEqual(self.validator.validate(copy.deepcopy(self.state)), [])

    def test_validator_accepts_fully_sequenced_current_lineage_run(self) -> None:
        state, _ = self.completed_run_state()
        self.assertEqual(self.validator.validate(state), [])

    def test_validator_rejects_each_skipped_prerequisite_gate(self) -> None:
        skipped_statuses = {
            "gate_0a": "pending",
            "gate_0": "pending",
            "gate_1": "pending",
            "gate_2a": "not_started",
            "gate_2b": "not_started",
            "gate_3": "not_started",
            "artefact_gate": "not_started",
        }
        for gate_name, skipped_status in skipped_statuses.items():
            with self.subTest(gate=gate_name):
                state, run = self.completed_run_state()
                run["approvals"][gate_name]["status"] = skipped_status
                errors = self.validator.validate(state)
                self.assertTrue(
                    any(f"cannot advance past {gate_name}" in error for error in errors),
                    errors,
                )

    def test_validator_rejects_stale_intermediate_gate_lineage(self) -> None:
        state, run = self.completed_run_state()
        run["approvals"]["gate_2b"]["approval_receipt"]["plan_version"] = 999
        errors = self.validator.validate(state)
        self.assertTrue(
            any("gate_2b approval has stale or mismatched plan_version" in error for error in errors),
            errors,
        )

    def test_validator_rejects_self_asserted_or_drifted_source_controls(self) -> None:
        mutations = (
            (
                "missing manifest",
                lambda state, run: state.update({"source_manifest": None}),
                "current top-level source manifest",
            ),
            (
                "pending policy",
                lambda state, run: state["source_access_policy"].update(
                    {"status": "pending_lecturer_confirmation"}
                ),
                "current approved source-access policy",
            ),
            (
                "policy drift",
                lambda state, run: state["source_access_policy"].update(
                    {"fingerprint": "DRIFTED-POLICY"}
                ),
                "does not match current top-level policy",
            ),
            (
                "manifest spoof",
                lambda state, run: run["source_manifest_verification"].update(
                    {"manifest_path": "01_Control/other-source-hashes.csv"}
                ),
                "does not match the current top-level manifest",
            ),
        )
        for name, mutate, phrase in mutations:
            with self.subTest(case=name):
                state, run = self.completed_run_state()
                mutate(state, run)
                errors = self.validator.validate(state)
                self.assertTrue(any(phrase in error for error in errors), errors)

    def test_validator_rejects_premature_terminal_closeout_after_hitl3(self) -> None:
        for terminal_status in ("completed", "handed_off"):
            with self.subTest(terminal_status=terminal_status):
                state, _ = self.accepted_before_review_state(
                    run_status=terminal_status, keep_active=False
                )
                errors = self.validator.validate(state)
                self.assertTrue(
                    any(
                        "accepted HITL3 must remain non-terminal until the mandatory review offer has an explicit response"
                        in error
                        for error in errors
                    ),
                    errors,
                )

    def test_validator_rejects_active_run_loss_before_review_response(self) -> None:
        state, _ = self.accepted_before_review_state(
            run_status="waiting_at_gate", keep_active=False
        )
        errors = self.validator.validate(state)
        self.assertTrue(
            any(
                "accepted HITL3 must remain active until the mandatory review offer has an explicit response"
                in error
                for error in errors
            ),
            errors,
        )

    def test_validator_allows_only_nonterminal_active_wait_before_offer_is_recorded(self) -> None:
        state, _ = self.accepted_before_review_state()
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
            "material_processing_eligibility_fingerprint": run["trigger"][
                "material_processing_eligibility_fingerprint"
            ],
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

    def test_validator_rejects_truncated_or_fabricated_schedule_history(self) -> None:
        state = copy.deepcopy(self.state)
        state["schedules"] = [
            {
                "schedule_id": "S-FAKE",
                "contract_id": "C-FAKE",
                "contract_version": "v1",
                "status": "expired",
            }
        ]
        errors = self.validator.validate(state)
        for phrase in (
            "safety field allowed_statuses diverges",
            "approved contract snapshot reference",
            "status_transition_receipt must be an object",
        ):
            self.assertTrue(any(phrase in error for error in errors), (phrase, errors))

    def test_validator_preserves_complete_paused_expired_and_cancelled_schedule_history(self) -> None:
        for status in ("paused", "expired", "cancelled"):
            with self.subTest(status=status):
                state, _ = self.historical_schedule_state(status)
                self.assertEqual(self.validator.validate(state), [])

    def test_validator_accepts_expired_trigger_receipt_without_course_action(self) -> None:
        base, _ = self.completed_run_state()
        base["runs"] = []
        base["active_run_id"] = None
        run_id = "RUN-SCHEDULE-EXPIRED-001"
        state, contract = self.historical_schedule_state(
            "expired", base_state=base, triggered_run_id=run_id
        )
        run = copy.deepcopy(state["run_template"])
        eligibility_fingerprint = state["material_processing_eligibility"]["fingerprint"]
        run.update(
            {
                "template_only": False,
                "run_id": run_id,
                "task_chat_reference": "TASK-SCHEDULE-EXPIRED-001",
                "mode": "scheduled",
                "status": "expired",
                "started_at": "2026-01-01T00:00:00Z",
                "current_gate": "RUN_TERMINATED",
                "next_permitted_action": "none_expired_without_course_action",
            }
        )
        reference = {
            "schedule_id": contract["schedule_id"],
            "contract_id": contract["contract_id"],
            "contract_version": contract["contract_version"],
            "approved_contract_snapshot_reference": contract[
                "approved_contract_snapshot_reference"
            ],
            "contract_status_at_trigger": "expired",
        }
        run["trigger"].update(
            {
                "trigger_id": "TRIGGER-SCHEDULE-EXPIRED-001",
                "trigger_type": "scheduled",
                "created_at": "2026-01-01T00:00:00Z",
                "material_processing_eligibility_fingerprint": eligibility_fingerprint,
                "standing_schedule_contract_reference": reference,
            }
        )
        run["execution_authority"]["standing_contract_reference"] = copy.deepcopy(
            reference
        )
        run["contract"]["material_processing_eligibility_fingerprint"] = (
            eligibility_fingerprint
        )
        run["contract"]["contract_id"] = "RC-SCHEDULE-EXPIRED-001"
        run["source_manifest_verification"][
            "material_processing_eligibility_fingerprint"
        ] = eligibility_fingerprint
        run["approvals"]["gate_0a"].update(
            {
                "status": "approved",
                "approval_id": "GATE0A-SCHEDULE-EXPIRED-001",
                "material_processing_eligibility_fingerprint": eligibility_fingerprint,
                "lecturer_declaration_reference": "REPLY-ELIGIBILITY-001",
                "validation_status": "passed",
                "recorded_at": "2026-01-01T00:00:00Z",
            }
        )
        run["termination"].update(
            {
                "status": "expired",
                "reason": "contract expired before course action",
                "recorded_at": "2026-01-01T00:00:00Z",
            }
        )
        state["runs"] = [run]
        self.assertEqual(self.validator.validate(state), [])

        run["trigger"]["created_at"] = "2025-06-01T00:00:00Z"
        errors = self.validator.validate(state)
        self.assertTrue(
            any("expired scheduled trigger precedes contract expiry" in error for error in errors),
            errors,
        )

    def test_validator_binds_scheduled_trigger_time_to_immutable_contract_window(self) -> None:
        state, run, _ = self.terminal_scheduled_history_run_state(
            run_status="failed_safe",
            contract_status_at_trigger="active",
            trigger_created_at="2025-06-01T00:00:00Z",
        )
        self.assertEqual(self.validator.validate(state), [])

        for created_at, phrase in (
            ("not-a-time", "must be a valid offset timestamp"),
            ("2024-12-31T23:59:59Z", "outside its contract window"),
            ("2026-01-01T00:00:00Z", "outside its contract window"),
            ("2099-01-01T00:00:00Z", "cannot be in the future"),
        ):
            with self.subTest(created_at=created_at):
                run["trigger"]["created_at"] = created_at
                errors = self.validator.validate(state)
                self.assertTrue(any(phrase in error for error in errors), errors)

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

    def test_validator_rejects_duplicate_trigger_id_across_schema_8_runs(self) -> None:
        state, first = self.completed_run_state()
        second = json.loads(
            json.dumps(first)
            .replace("RUN-SYNTHETIC-001", "RUN-SYNTHETIC-002")
            .replace("TASK-SYNTHETIC-001", "TASK-SYNTHETIC-002")
        )
        self.assertEqual(
            second["trigger"]["trigger_id"], first["trigger"]["trigger_id"]
        )
        state["runs"].append(second)
        errors = self.validator.validate(state)
        self.assertTrue(any("duplicate trigger_id" in error for error in errors), errors)

    def test_validator_rejects_duplicate_run_contract_and_gate_approval_ids(self) -> None:
        state, first = self.completed_run_state()
        second = json.loads(
            json.dumps(first)
            .replace("RUN-SYNTHETIC-001", "RUN-SYNTHETIC-002")
            .replace("TASK-SYNTHETIC-001", "TASK-SYNTHETIC-002")
        )
        second["trigger"]["trigger_id"] = "TRIGGER-SYNTHETIC-002"
        second["approvals"]["system_improvement_review_offer"]["offer"][
            "offer_id"
        ] = "system-review-offer:RUN-SYNTHETIC-002:HITL3-ACCEPT-001"
        second["approvals"]["trigger_guidance_offer"]["offer"][
            "offer_id"
        ] = "trigger-guidance:RUN-SYNTHETIC-002:REPLY-OFFER-001"
        for gate_name in (
            "gate_0a",
            "gate_0",
            "gate_1",
            "gate_2a",
            "gate_2b",
            "gate_3",
            "artefact_gate",
        ):
            gate = second["approvals"][gate_name]
            if gate.get("approval_id"):
                gate["approval_id"] = gate["approval_id"].replace("001", "002")
        second["approvals"]["gate_0"]["approval_id"] = first["approvals"]["gate_0"][
            "approval_id"
        ]
        second["approvals"]["gate_1"]["approval_id"] = first["approvals"]["gate_1"][
            "approval_id"
        ]
        state["runs"].append(second)
        errors = self.validator.validate(state)
        self.assertTrue(any("duplicate run contract_id" in error for error in errors), errors)
        for approval_id in (
            first["approvals"]["gate_0"]["approval_id"],
            first["approvals"]["gate_1"]["approval_id"],
        ):
            self.assertTrue(
                any(f"duplicate gate approval_id {approval_id}" in error for error in errors),
                errors,
            )

    def test_validator_rejects_unregistered_scheduled_run_and_manual_schedule_reference(self) -> None:
        scheduled, run = self.accepted_before_review_state()
        run["mode"] = "scheduled"
        run["trigger"]["trigger_type"] = "scheduled"
        run["trigger"]["standing_schedule_contract_reference"] = None
        errors = self.validator.validate(scheduled)
        for phrase in (
            "scheduled run requires a non-null standing schedule contract reference",
            "scheduled run requires an active validated runtime",
        ):
            self.assertTrue(any(phrase in error for error in errors), (phrase, errors))

        manual, manual_run = self.accepted_before_review_state()
        reference = {
            "schedule_id": "SCHEDULE-UNAUTHORISED",
            "contract_id": "CONTRACT-UNAUTHORISED",
            "contract_version": "v1",
        }
        manual_run["trigger"]["standing_schedule_contract_reference"] = reference
        manual_run["execution_authority"]["standing_contract_reference"] = reference
        errors = self.validator.validate(manual)
        self.assertTrue(
            any("manual run must not carry a standing schedule contract" in error for error in errors),
            errors,
        )

    def test_umbrella_route_is_enforced(self) -> None:
        state = copy.deepcopy(self.state)
        state["umbrella_entry_routing"]["initial_gate"] = "GATE_1"
        errors = self.validator.validate(state)
        self.assertTrue(any("umbrella entry" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
