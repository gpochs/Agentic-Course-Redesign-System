from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


VALIDATION_DIR = Path(__file__).resolve().parent
ADAPTER_ROOT = VALIDATION_DIR.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("antigravity_adapter_validator", VALIDATION_DIR / "validate_adapter.py")
installer = load_module(
    "antigravity_overlay_installer", ADAPTER_ROOT / "scripts" / "install_workspace_overlay.py"
)
STATE_PATH = ADAPTER_ROOT / "workspace-overlay" / "01_Control" / "state.json"
SETUP_SCRIPTS = (
    ADAPTER_ROOT
    / "workspace-overlay"
    / ".agents"
    / "skills"
    / "course-redesign-setup"
    / "scripts"
)
state_validator = load_module(
    "antigravity_state_validator", SETUP_SCRIPTS / "validate_state.py"
)
state_migration = load_module(
    "antigravity_state_migration", SETUP_SCRIPTS / "migrate_state_v6_to_v7.py"
)


def load_state() -> dict:
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def schema6_fixture_from_current_state() -> dict:
    """Invert only the documented schema-7 additions to make a v6 fixture."""

    state = load_state()
    state["schema_version"] = 6
    state.pop("umbrella_entry_routing")
    state.pop("schema_compatibility")
    split_triggers = {
        item["trigger"] for item in state_migration.V7_SPLIT_TRANSITIONS
    }
    for run in [state["run_template"], *state["runs"]]:
        run["approvals"].pop("hitl_3")
        run["approvals"].pop("system_improvement_review_offer")
        run.pop("resume_protocol")
        rules = run["manual_stage_authority"]["transition_rules"]
        first_split = next(
            index for index, rule in enumerate(rules)
            if rule.get("trigger") in split_triggers
        )
        rules[:] = [rule for rule in rules if rule.get("trigger") not in split_triggers]
        rules.insert(
            first_split,
            {
                "trigger": state_migration.V6_COMBINED_TRANSITION_TRIGGER,
                "authorises_through": "SYSTEM_GATE",
                "purpose": "reusable_system_proposal_and_system_gate_only",
                "does_not_authorise_candidate_activation": True,
            },
        )
    system_update = state["activation"]["system_update"]
    system_update.pop("allowed_statuses")
    system_update.pop("prerequisites")
    for field in ("run_id", "system_improvement_review_offer_reference"):
        system_update["completed_reply_requirements"].remove(field)
        system_update["approval"].pop(field)
    for field in ("hitl_3_accepted", "system_improvement_review_offer_requested"):
        state["activation"]["required_before_active"].remove(field)
    return state


class AdapterValidationTests(unittest.TestCase):
    def test_static_adapter_passes(self) -> None:
        result = validator.validate()
        self.assertTrue(result["ok"], result["errors"])

    def test_skill_frontmatter_is_discriminating(self) -> None:
        skills_root = ADAPTER_ROOT / "workspace-overlay" / ".agents" / "skills"
        for skill_dir in skills_root.iterdir():
            if not skill_dir.is_dir():
                continue
            frontmatter = validator.parse_frontmatter(skill_dir / "SKILL.md")
            self.assertEqual(frontmatter["name"], skill_dir.name)
            self.assertGreater(len(frontmatter["description"]), 20)

    def test_custom_agents_are_native_and_read_only(self) -> None:
        agents_root = ADAPTER_ROOT / "workspace-overlay" / ".agents" / "agents"
        self.assertEqual(
            {path.name for path in agents_root.glob("*.md")},
            set(validator.EXPECTED_AGENTS),
        )
        for filename, role in validator.EXPECTED_AGENTS.items():
            path = agents_root / filename
            frontmatter = validator.parse_agent_frontmatter(path)
            self.assertEqual(frontmatter["tools"], ["view_file", "grep_search"])
            self.assertFalse(frontmatter["mainAgent"])
            self.assertTrue(frontmatter["subagent"])
            self.assertEqual(frontmatter["commandExecutionPolicy"], "off")
            self.assertFalse(frontmatter["inheritMcp"])
            self.assertEqual(frontmatter["mcpServers"], [])
            self.assertEqual(frontmatter["plugins"], [])
            self.assertEqual(validator.validate_agent_definition(path, role), [])

    def test_workflow_completeness_controls_pass(self) -> None:
        self.assertEqual(validator.validate_workflow_completeness(), [])

    def test_missing_production_handoff_control_is_rejected(self) -> None:
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in validator.WORKFLOW_CONTROL_PATHS.items()
        }
        documents["orchestrator"] = documents["orchestrator"].replace(
            "APPROVE PRODUCTION HANDOFF", "REMOVED HANDOFF CONTROL", 1
        )
        errors = validator.validate_workflow_completeness(documents)
        self.assertTrue(any("APPROVE PRODUCTION HANDOFF" in item for item in errors))

    def test_system_review_offer_authority_expansion_is_rejected(self) -> None:
        documents = {
            name: path.read_text(encoding="utf-8")
            for name, path in validator.WORKFLOW_CONTROL_PATHS.items()
        }
        documents["system"] = documents["system"].replace(
            "It does not authorise system-file changes",
            "It authorises system-file changes",
            1,
        )
        errors = validator.validate_workflow_completeness(documents)
        self.assertTrue(any("does not authorise system-file changes" in item for item in errors))

    def test_canonical_schema7_state_and_validator_pass(self) -> None:
        state = load_state()
        self.assertEqual(state["schema_version"], 7)
        self.assertEqual(validator.validate_state_fields(state), [])
        self.assertEqual(state_validator.validate(state), [])

    def test_migration_preview_is_idempotent_for_schema7(self) -> None:
        state = load_state()
        original = copy.deepcopy(state)
        report = state_migration.preview_migration(state, source="unit-test")
        self.assertTrue(report["ok"])
        self.assertEqual(report["mode"], "preview_only")
        self.assertFalse(report["would_write"])
        self.assertEqual(report["changed_paths"], [])
        self.assertEqual(report["candidate_state"], original)
        self.assertEqual(state, original)

    def test_schema6_migration_is_preview_only_and_preserves_boundaries(self) -> None:
        state = schema6_fixture_from_current_state()
        original = copy.deepcopy(state)
        report = state_migration.preview_migration(state, source="unit-test-v6")
        candidate = report["candidate_state"]
        self.assertEqual(state, original)
        self.assertEqual(report["mode"], "preview_only")
        self.assertFalse(report["would_write"])
        self.assertEqual(candidate["schema_version"], 7)
        self.assertEqual(candidate["status"], original["status"])
        self.assertEqual(candidate["schedules"], original["schedules"])
        self.assertEqual(
            candidate["run_template"]["contract"]["permitted_tools"],
            original["run_template"]["contract"]["permitted_tools"],
        )
        self.assertTrue(all(report["preservation_checks"].values()))
        self.assertEqual(state_validator.validate(candidate), [])

    def test_migration_and_state_validator_fail_closed(self) -> None:
        with self.assertRaises(state_migration.MigrationError):
            state_migration.preview_migration({"schema_version": 5})
        state = load_state()
        state["run_template"]["approvals"]["system_improvement_review_offer"][
            "authority_on_request"
        ]["authorises"].append("modify_system_files")
        errors = state_validator.validate(state)
        self.assertTrue(any("authorise only review and proposal" in item for item in errors))

    def test_write_capable_custom_agent_is_rejected(self) -> None:
        source = (
            ADAPTER_ROOT
            / "workspace-overlay"
            / ".agents"
            / "agents"
            / "course-mapper.md"
        ).read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "course-mapper.md"
            path.write_text(
                source.replace("  - grep_search", "  - replace_file_content", 1),
                encoding="utf-8",
            )
            errors = validator.validate_agent_definition(path, "course_mapper")
            self.assertTrue(any("tools must be exactly" in item for item in errors))

    def test_secret_detector_catches_private_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "bad.txt").write_text(
                "-----BEGIN " + "PRIVATE KEY-----\nnot-a-real-key\n", encoding="utf-8"
            )
            findings = validator.find_secret_like_material(root)
            self.assertTrue(any(item.startswith("private-key:") for item in findings))

    def test_active_or_scheduled_state_is_rejected(self) -> None:
        state = load_state()
        state["status"] = "active"
        state["schedules"] = [{"id": "forbidden-test"}]
        errors = validator.validate_state_fields(state)
        self.assertTrue(any("candidate_not_active" in item for item in errors))
        self.assertTrue(any("no registered schedules" in item for item in errors))

    def test_installer_preview_apply_and_no_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "one" / "course" / "workspace"
            preview = installer.build_report(target)
            self.assertEqual(preview["mode"], "preview")
            self.assertFalse(target.exists())
            self.assertGreater(preview["planned_file_count"], 20)
            applied = installer.install(target, allow_nonempty=False)
            self.assertTrue(applied["installed"])
            self.assertEqual(applied["planned_file_count"], applied["verified_copy_count"])
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / ".agents" / "skills").is_dir())
            with self.assertRaises(FileExistsError):
                installer.install(target, allow_nonempty=False)

    def test_installer_refuses_home_and_adapter_targets(self) -> None:
        self.assertTrue(installer.target_is_forbidden(Path.home()))
        self.assertTrue(installer.target_is_forbidden(ADAPTER_ROOT / "nested"))


if __name__ == "__main__":
    unittest.main()
