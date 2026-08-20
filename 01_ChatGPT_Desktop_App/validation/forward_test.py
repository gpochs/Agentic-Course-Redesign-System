#!/usr/bin/env python3
"""Run a disposable end-to-end structural test of the portable plugin bundle."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import tempfile
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "agentic-course-redesign"


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
fingerprinter = load("fingerprint_file", "scripts/fingerprint_file.py")
public_scrub = load_path("public_scrub", ROOT / "validation" / "public_scrub.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def check(condition: bool, label: str, evidence: object = None) -> dict[str, object]:
    return {"check": label, "pass": bool(condition), "evidence": evidence}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    checks: list[dict[str, object]] = []

    plugin_manifest = json.loads(
        (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
    )
    marketplace = json.loads(
        (ROOT / ".agents" / "plugins" / "marketplace.json").read_text(encoding="utf-8")
    )
    cases = json.loads(
        (ROOT / "validation" / "plugin-test-cases.json").read_text(encoding="utf-8")
    )
    checks.append(check(plugin_manifest.get("name") == "agentic-course-redesign", "plugin manifest identity"))
    checks.append(check(marketplace["plugins"][0]["name"] == plugin_manifest["name"], "marketplace identity match"))
    checks.append(check(len(cases.get("positive_cases", [])) >= 5, "at least five positive cases"))
    checks.append(check(len(cases.get("negative_cases", [])) >= 3, "at least three negative cases"))

    skills = sorted(PLUGIN.glob("skills/*/SKILL.md"))
    skill_names = {path.parent.name for path in skills}
    checks.append(check(skill_names == public_scrub.EXPECTED_SKILLS, "exact six bounded plugin skills", sorted(skill_names)))
    non_ascii_skills = [path.relative_to(PLUGIN).as_posix() for path in skills if not path.read_text(encoding="utf-8").isascii()]
    checks.append(check(not non_ascii_skills, "validator-portable ASCII skill files", non_ascii_skills))
    checks.append(check((PLUGIN / "assets/PARTICIPANT_QUICK_START.md").is_file(), "participant onboarding asset present"))
    prompt_errors = []
    for skill_path in skills:
        skill_name = skill_path.parent.name
        metadata = (skill_path.parent / "agents" / "openai.yaml").read_text(encoding="utf-8")
        if f"${skill_name}" not in metadata:
            prompt_errors.append(f"{skill_name}: default prompt does not invoke ${skill_name}")
    checks.append(check(not prompt_errors, "each skill default prompt explicitly invokes itself", prompt_errors))

    toml_paths = sorted((PLUGIN / "assets/project-template/.codex/agents").glob("*.toml"))
    agent_definitions = []
    for path in toml_paths:
        with path.open("rb") as handle:
            agent_definitions.append((path, tomllib.load(handle)))
    config_path = PLUGIN / "assets/project-template/.codex/config.toml"
    with config_path.open("rb") as handle:
        config = tomllib.load(handle)
    checks.append(check(len(toml_paths) == 10, "ten agent definitions parse", len(toml_paths)))
    checks.append(check(config.get("agents", {}).get("max_concurrent_threads_per_session") == 5, "five specialist threads configured"))
    required_agent_tokens = (
        "return_id",
        "run_contract_id",
        "source_access_policy_fingerprint",
        "dependencies_overlaps_conflicts",
        "lecturer_only_questions",
        "ESCALATE_TO_ORCHESTRATOR:",
        "Only one bounded corrective retry",
    )
    agent_errors = []
    for path, data in agent_definitions:
        instructions = data.get("developer_instructions", "")
        if data.get("sandbox_mode") != "read-only":
            agent_errors.append(f"{path.name}: sandbox is not read-only")
        for token in required_agent_tokens:
            if token not in instructions:
                agent_errors.append(f"{path.name}: missing {token}")
    checks.append(check(not agent_errors, "agent lineage, envelope, escalation and retry controls", agent_errors))

    state_path = PLUGIN / "assets/project-template/01_Control/state.json"
    state_text = state_path.read_text(encoding="utf-8")
    state = json.loads(state_text)
    state_errors = state_validator.validate(state)
    checks.append(check(not state_errors, "state fail-closed invariants", state_errors))
    checks.append(check(state.get("status") == "candidate_not_active", "template runtime inactive"))
    checks.append(check(state.get("schedules") == [], "template registers no schedules"))
    standing = state.get("standing_schedule_contract_template", {})
    checks.append(
        check(
            standing.get("runtime_versions", {}).get("skill_name") == "course-redesign-orchestrator",
            "schedule invokes the orchestrator skill",
        )
    )
    approvals = state.get("run_template", {}).get("approvals", {})
    checks.append(
        check(
            "approved_research_targets" in approvals.get("gate_2b", {})
            and "approved_exact_targets" not in approvals.get("gate_2b", {}),
            "Gate 2B uses typed research targets",
        )
    )
    checks.append(
        check(
            "approved_material_targets" in approvals.get("gate_3", {})
            and "approved_exact_targets" not in approvals.get("gate_3", {}),
            "Gate 3 uses typed material targets",
        )
    )
    legacy_prompt_tokens = tuple(
        token
        for number in range(1, 6)
        for token in (f"prompt_{number}", f"prompt {number}")
    )
    checks.append(
        check(
            not any(token in state_text.casefold() for token in legacy_prompt_tokens),
            "state uses conversational gates rather than numbered prompts",
        )
    )
    warning = (PLUGIN / "assets/project-template/00_NOT_ACTIVE_UNTIL_VALIDATED.txt").read_text(encoding="utf-8")
    checks.append(check("ready for a lecturer-guided first run" in warning, "inactive warning permits guided first run"))
    checks.append(check("no standing schedule is registered" in warning, "inactive warning forbids schedule activation"))

    policy_path = PLUGIN / "assets/project-template/01_Control/source-access-policy.template.json"
    digest_one, payload_one = fingerprinter.fingerprint(policy_path, "policy")
    policy_copy = json.loads(policy_path.read_text(encoding="utf-8"))
    policy_copy["fingerprint"] = "IGNORED"
    policy_copy["lecturer_decision"] = "approved"
    policy_copy["approved_at"] = "2099-01-01T00:00:00Z"

    with tempfile.TemporaryDirectory(prefix="agentic-course-redesign-forward-") as temporary:
        temporary_root = Path(temporary)
        altered = temporary_root / "policy.json"
        altered.write_text(json.dumps(policy_copy, indent=4), encoding="utf-8")
        digest_two, payload_two = fingerprinter.fingerprint(altered, "policy")
        checks.append(check(digest_one == digest_two and payload_one == payload_two, "canonical policy fingerprint stable", digest_one))

        project = temporary_root / "One_Course_Project"
        preview = setup.build_report(project)
        checks.append(check(not preview["would_overwrite"], "setup preview is non-destructive"))
        installed = setup.install(project, allow_nonempty=False)
        checks.append(check(installed["installed"], "template installed in disposable project"))
        copied_state = json.loads((project / "01_Control/state.json").read_text(encoding="utf-8"))
        checks.append(check(copied_state["status"] == "candidate_not_active", "copied project remains inactive"))

        (project / "00_Source_Materials" / "workbook.txt").write_text("safe course content", encoding="utf-8")
        (project / "00_Source_Materials" / "test_answer_key.txt").write_text("teacher only", encoding="utf-8")
        (project / "00_Context" / "programme-policy.txt").write_text("local policy", encoding="utf-8")
        manifest_path = Path("01_Control/source-hashes.csv")
        created = manifest.create(project, manifest_path, replace=False)
        verified = manifest.verify(project, manifest_path)
        checks.append(check(created["ok"] and verified["ok"], "source manifest create and verify", created.get("manifest_fingerprint")))
        (project / "00_Source_Materials" / "workbook.txt").write_text("tampered", encoding="utf-8")
        tampered = manifest.verify(project, manifest_path)
        checks.append(check(not tampered["ok"], "source tampering fails verification"))

        synthetic_home = "C:" + "\\Users\\SampleLecturer\\OneDrive\\Course\\file.txt"
        synthetic_email = "owner" + "@" + "example.org"
        synthetic_findings = public_scrub.inspect_text(
            "synthetic-private-fixture.txt", synthetic_home + "\n" + synthetic_email
        )
        detected_kinds = {item["kind"] for item in synthetic_findings}
        checks.append(
            check(
                {"windows_user_home", "windows_onedrive_absolute", "email_address"}
                <= detected_kinds,
                "synthetic leakage fixture is detected",
                sorted(detected_kinds),
            )
        )

    scrub_result = public_scrub.scan(ROOT)
    checks.append(
        check(
            scrub_result["pass"],
            "public source scrub",
            scrub_result["findings"],
        )
    )

    result = {
        "schema_version": 1,
        "plugin": plugin_manifest["name"],
        "plugin_version": plugin_manifest["version"],
        "plugin_manifest_sha256": sha256(PLUGIN / ".codex-plugin/plugin.json"),
        "pass": all(item["pass"] for item in checks),
        "checks": checks,
        "limitations": [
            "This structural forward test does not prove that every attendee's desktop build exposes marketplace installation.",
            "Workspace policy, product access, and app version can restrict the documented Work and Codex custom-marketplace route.",
            "The macOS project-template route has not yet been independently executed on a macOS machine.",
            "Public Plugins Directory publication requires separate publisher submission, OpenAI review, approval, and publisher release.",
            "No runtime or standing schedule is activated by this test."
        ]
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
