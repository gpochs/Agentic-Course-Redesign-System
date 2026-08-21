from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR_PATH = ROOT / "05_Validation" / "validate_repository.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("repository_semantics", VALIDATOR_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepositorySemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def test_all_orchestration_entries_have_complete_ordered_terminal_contract(self) -> None:
        for rel_path in self.validator.ORCHESTRATION_ENTRY_PATHS:
            path = ROOT / rel_path
            self.assertEqual(
                self.validator.validate_orchestration_entry(path),
                [],
                rel_path,
            )

    def test_all_system_lifecycle_entries_keep_separate_gates(self) -> None:
        for rel_path in self.validator.SYSTEM_LIFECYCLE_PATHS:
            path = ROOT / rel_path
            self.assertEqual(
                self.validator.validate_system_lifecycle_entry(path),
                [],
                rel_path,
            )

    def test_missing_review_scope_fails_closed(self) -> None:
        source = (
            ROOT
            / "03_Shared_Workflow_Core"
            / "agent-skills"
            / "course-redesign-orchestrator"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "SKILL.md"
            path.write_text(source.replace("schedule contracts; ", ""), encoding="utf-8")
            kinds = {
                item["kind"]
                for item in self.validator.validate_orchestration_entry(path)
            }
            self.assertIn("system_review_question_scope_incomplete", kinds)

    def test_terminal_gate_mutations_fail_closed(self) -> None:
        source = (
            ROOT
            / "03_Shared_Workflow_Core"
            / "agent-skills"
            / "course-redesign-orchestrator"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        mutations = (
            (
                "current-lineage",
                "optional-lineage",
                "two completed current-lineage replies",
            ),
            (
                " as a standalone line",
                "",
                "both approval tokens are standalone lines",
            ),
            (
                "second, separate completed current-lineage reply",
                "completed current-lineage reply",
                "two completed current-lineage replies",
            ),
            (
                "exact",
                "named",
                "second reply repeats the exact target",
            ),
            (
                "Save and independently verify",
                "Save without reopening",
                "handoff is independently reopened or verified",
            ),
            (
                "Do not open HITL 3 until",
                "Open HITL 3 before",
                "HITL3 remains closed until handoff verification",
            ),
            (
                "current-\nlineage final acceptance",
                "final closure",
                "unconditional current-lineage HITL3 acceptance precedes the offer",
            ),
            (
                "A token-only, combined, stale-lineage or changed-target reply is\ninvalid.",
                "A token-only reply is valid.",
                "token-only or combined approval fails closed",
            ),
        )
        with tempfile.TemporaryDirectory() as raw:
            for index, (old, new, expected_detail) in enumerate(mutations):
                with self.subTest(expected_detail=expected_detail):
                    self.assertIn(old, source)
                    path = Path(raw) / f"orchestrator-{index}.md"
                    path.write_text(source.replace(old, new), encoding="utf-8")
                    findings = self.validator.validate_orchestration_entry(path)
                    details = {
                        item.get("detail")
                        for item in findings
                        if item["kind"] == "terminal_gate_contract_incomplete"
                    }
                    self.assertIn(expected_detail, details, findings)

    def test_missing_system_gate_token_fails_closed(self) -> None:
        source = (
            ROOT
            / "03_Shared_Workflow_Core"
            / "agent-skills"
            / "course-redesign-system"
            / "SKILL.md"
        ).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "SKILL.md"
            path.write_text(source.replace("APPROVE SYSTEM FILES", "APPROVE FILES"), encoding="utf-8")
            kinds = {
                item["kind"]
                for item in self.validator.validate_system_lifecycle_entry(path)
            }
            self.assertIn("system_lifecycle_stage_missing_or_out_of_order", kinds)

    def test_candidate_control_record_is_bound_to_id_version_and_inactive_status(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            path = Path(raw) / "proposal.md"
            path.write_text(
                "Proposal ID: WRONG\nProposal version: 9.9.9\nStatus: active\n",
                encoding="utf-8",
            )
            expected = (
                "proposal id: `acr-sys-20260820-004`",
                "proposal version: `0.2.2`",
                "system-file candidate approved; repository publication separately authorised",
            )
            findings = self.validator.validate_candidate_control_record(path, expected)
            self.assertEqual(
                {item["kind"] for item in findings},
                {"candidate_control_record_mismatch"},
            )
            self.assertEqual(len(findings), 3)

    def test_root_manifest_gate_forbids_connector_expansion(self) -> None:
        self.assertIn("connectors", self.validator.FORBIDDEN_PLUGIN_INTEGRATION_KEYS)
        self.assertEqual(
            set(self.validator.FORBIDDEN_PLUGIN_INTEGRATION_KEYS),
            {
                "apps",
                "mcpServers",
                "connectors",
                "hooks",
                "permissions",
                "authentication",
                "schedules",
            },
        )


if __name__ == "__main__":
    unittest.main()
