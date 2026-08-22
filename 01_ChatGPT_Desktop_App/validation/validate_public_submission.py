#!/usr/bin/env python3
"""Validate the separate OpenAI skills-only source and review materials."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parent.parent
CUSTOM_PLUGIN = ROOT / "plugins" / "agentic-course-redesign"
PUBLIC_PLUGIN = ROOT / "openai-submission" / "source" / "agentic-course-redesign"
REVIEW = ROOT / "openai-submission" / "review"
EXPECTED_REPOSITORY = "https://github.com/gpochs/Agentic-Course-Redesign-System"
EXPECTED_PUBLISHER = "GIAN PETER OCHSNER"
EXPECTED_WEBSITE = EXPECTED_REPOSITORY
EXPECTED_PRIVACY = f"{EXPECTED_REPOSITORY}/blob/v0.2.4/docs/PRIVACY.md"
EXPECTED_TERMS = f"{EXPECTED_REPOSITORY}/blob/v0.2.4/docs/TERMS.md"
EXPECTED_SKILLS = {
    "course-redesign-assessment",
    "course-redesign-materials",
    "course-redesign-orchestrator",
    "course-redesign-research",
    "course-redesign-setup",
    "course-redesign-system",
}
RUNTIME_TREES = (".codex-plugin", "assets", "scripts", "skills")
DISALLOWED_MANIFEST_KEYS = {
    "apps",
    "mcpServers",
    "hooks",
    "connectors",
    "authentication",
    "permissions",
}
DISALLOWED_FILES = {".app.json", ".mcp.json"}
REQUIRED_OWNER_MARKERS = {
    "[VERIFIED_PUBLISHER_NAME]",
    "[OPENAI_ORGANIZATION_AND_PROJECT]",
    "[APPS_MANAGEMENT_WRITE_SUBMITTER]",
    "[PUBLIC_WEBSITE_HTTPS_URL]",
    "[PUBLIC_SUPPORT_HTTPS_URL]",
    "[PUBLIC_PRIVACY_POLICY_HTTPS_URL]",
    "[PUBLIC_TERMS_HTTPS_URL]",
    "[SUPPORTED_COUNTRIES_OR_REGIONS]",
    "[POLICY_ATTESTATION_OWNER]",
}
OWNER_BLOCKERS = [
    "re-confirm the verified publisher identity and update manifest publisher fields only if needed",
    "re-confirm the owning OpenAI organization/project and Apps Management Write submitter",
    "re-confirm that the published website, support, privacy-policy, and terms HTTPS pages remain accurate",
    "re-confirm supported countries or regions",
    "complete the v0.2.4 policy attestations",
    "run the OpenAI v0.2.4 skill safety/security scans and complete review",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def tree_records(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): digest(path)
        for path in sorted(root.rglob("*"))
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    }


def runtime_records(plugin: Path) -> dict[str, str]:
    records: dict[str, str] = {}
    for name in RUNTIME_TREES:
        subtree = plugin / name
        if not subtree.exists():
            continue
        for relative, value in tree_records(subtree).items():
            records[f"{name}/{relative}"] = value
    return records


def svg_dimensions(path: Path) -> tuple[float, float]:
    root = ElementTree.parse(path).getroot()
    if root.tag.rsplit("}", 1)[-1] != "svg":
        raise ValueError("root element is not svg")
    width = root.attrib.get("width")
    height = root.attrib.get("height")
    if width is not None and height is not None:
        return float(width), float(height)
    view_box = root.attrib.get("viewBox", "").split()
    if len(view_box) == 4:
        return float(view_box[2]), float(view_box[3])
    raise ValueError("numeric width/height or viewBox missing")


def validate_archive(path: Path) -> list[str]:
    failures: list[str] = []
    if not path.is_file():
        return ["requested skills-only ZIP is missing"]
    expected = {
        f"agentic-course-redesign/{relative}"
        for relative in tree_records(PUBLIC_PLUGIN)
    }
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        names = {name for name in archive.namelist() if not name.endswith("/")}
        if bad:
            failures.append(f"ZIP CRC failure: {bad}")
        roots = {name.split("/", 1)[0] for name in names}
        if roots != {"agentic-course-redesign"}:
            failures.append(f"ZIP must have exactly one plugin root, found {sorted(roots)}")
        unsafe = [
            name
            for name in names
            if name.startswith("/") or ".." in PurePosixPath(name).parts
        ]
        if unsafe:
            failures.append(f"unsafe ZIP paths: {unsafe}")
        if names != expected:
            failures.append(
                "ZIP membership differs from public source: "
                f"missing={sorted(expected - names)} extra={sorted(names - expected)}"
            )
        for relative, expected_hash in tree_records(PUBLIC_PLUGIN).items():
            member = f"agentic-course-redesign/{relative}"
            if member in names:
                actual = hashlib.sha256(archive.read(member)).hexdigest().upper()
                if actual != expected_hash:
                    failures.append(f"ZIP content hash mismatch: {relative}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    failures: list[str] = []
    checks: list[dict[str, object]] = []

    def check(label: str, condition: bool, detail: str | None = None) -> None:
        checks.append({"check": label, "pass": condition, **({"detail": detail} if detail else {})})
        if not condition:
            failures.append(detail or label)

    manifest_path = PUBLIC_PLUGIN / ".codex-plugin" / "plugin.json"
    check("public manifest exists", manifest_path.is_file())
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.is_file() else {}
    interface = manifest.get("interface", {})

    check("stable package name", manifest.get("name") == "agentic-course-redesign")
    check("v0.2.4 semantic version", manifest.get("version") == "0.2.4")
    check(
        "valid package name syntax",
        bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", str(manifest.get("name", "")))),
    )
    check("repository URL matches requested release", manifest.get("repository") == EXPECTED_REPOSITORY)
    check("published publisher identity", manifest.get("author", {}).get("name") == EXPECTED_PUBLISHER)
    check("skills path declared", manifest.get("skills") == "./skills/")
    check(
        "no MCP/app/hook/connector/authentication/permission manifest keys",
        not (set(manifest) & DISALLOWED_MANIFEST_KEYS),
    )
    check("no screenshots in skills-only interface", "screenshots" not in interface)
    check("directory category", interface.get("category") == "Education & Research")
    check("umbrella plugin display name", interface.get("displayName") == "Agentic Course Redesign")
    check("display name length", 0 < len(interface.get("displayName", "")) <= 30)
    check("short description length", 0 < len(interface.get("shortDescription", "")) <= 30)
    long_description = interface.get("longDescription", "")
    check("long description present", 0 < len(long_description) <= 4000)
    listing_markers = (
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
    check(
        "compact scannable public description",
        len(long_description) <= 2400
        and long_description.count("\n- ") >= 10
        and all(heading in long_description for heading in ("SPECIALIST TEAM (10)", "GATED WORKFLOW", "DECISION DIALOGUE", "BOUNDARY")),
    )
    check(
        "public description preserves roles, lifecycle and dialogue contract",
        all(marker in long_description for marker in listing_markers),
    )
    check(
        "public description makes no unsupported Work cardinality claim",
        re.search(r"\bWork\b", long_description) is None,
    )
    listing_copy = (REVIEW / "LISTING_COPY.md").read_text(encoding="utf-8")
    normalized_listing_copy = " ".join(listing_copy.split())
    check(
        "listing copy preserves manifest description markers",
        all(marker in normalized_listing_copy for marker in listing_markers),
    )
    check("published developer identity", interface.get("developerName") == EXPECTED_PUBLISHER)
    check("website URL matches repository root", interface.get("websiteURL") == EXPECTED_WEBSITE)
    check("privacy URL is pinned to v0.2.4", interface.get("privacyPolicyURL") == EXPECTED_PRIVACY)
    check("terms URL is pinned to v0.2.4", interface.get("termsOfServiceURL") == EXPECTED_TERMS)
    capabilities = interface.get("capabilities", [])
    check("capability count and shape", isinstance(capabilities, list) and len(capabilities) <= 20 and all(isinstance(item, str) and 0 < len(item) <= 120 for item in capabilities))

    prompts_path = REVIEW / "starter-prompts.json"
    prompts_payload = json.loads(prompts_path.read_text(encoding="utf-8"))
    review_prompts = prompts_payload["prompts"]
    manifest_prompts = interface.get("defaultPrompt", [])
    prompts_valid = (
        manifest_prompts == review_prompts
        and 1 <= len(manifest_prompts) <= 3
        and len(set(item.strip() for item in manifest_prompts)) == len(manifest_prompts)
        and all(isinstance(item, str) and "@" not in item and "\n" not in item and 0 < len(item) <= 128 for item in manifest_prompts)
    )
    check("starter prompts match and meet final limits", prompts_valid)
    check("starter prompt version matches manifest", prompts_payload.get("version") == manifest.get("version"))

    for field in ("logo", "composerIcon"):
        declared = interface.get(field, "")
        asset = PUBLIC_PLUGIN / declared.removeprefix("./")
        valid = declared.startswith("./assets/") and asset.is_file() and asset.suffix.casefold() == ".svg"
        detail = None
        if valid:
            try:
                width, height = svg_dimensions(asset)
                valid = width == height and 48 <= width <= 4096
            except (ValueError, ElementTree.ParseError):
                valid = False
        if not valid:
            detail = f"{field} must be a readable square SVG between 48 and 4096 units"
        check(f"{field} asset", valid, detail)

    disallowed_paths = [
        path.relative_to(PUBLIC_PLUGIN).as_posix()
        for path in PUBLIC_PLUGIN.rglob("*")
        if path.is_file()
        and (path.name in DISALLOWED_FILES or "hooks" in path.relative_to(PUBLIC_PLUGIN).parts)
    ]
    check("no MCP, app, or hook payload", not disallowed_paths, str(disallowed_paths) if disallowed_paths else None)
    check("review-only tests excluded from upload source", not (PUBLIC_PLUGIN / "tests").exists())

    actual_skills = {
        path.parent.name for path in (PUBLIC_PLUGIN / "skills").glob("*/SKILL.md")
    }
    check("exact six public skills", actual_skills == EXPECTED_SKILLS, f"actual={sorted(actual_skills)}")
    check(
        "custom and public runtime trees are byte-identical",
        runtime_records(CUSTOM_PLUGIN) == runtime_records(PUBLIC_PLUGIN),
    )
    umbrella_metadata = (
        PUBLIC_PLUGIN
        / "skills"
        / "course-redesign-orchestrator"
        / "agents"
        / "openai.yaml"
    ).read_text(encoding="utf-8")
    umbrella_skill = (
        PUBLIC_PLUGIN
        / "skills"
        / "course-redesign-orchestrator"
        / "SKILL.md"
    ).read_text(encoding="utf-8")
    system_skill = (
        PUBLIC_PLUGIN / "skills/course-redesign-system/SKILL.md"
    ).read_text(encoding="utf-8")
    all_skill_text = [
        path.read_text(encoding="utf-8")
        for path in sorted((PUBLIC_PLUGIN / "skills").glob("*/SKILL.md"))
    ]
    normalized_skill_text = [" ".join(text.split()) for text in all_skill_text]
    check(
        "flattened picker has one full-workflow umbrella entry",
        'display_name: "Agentic Course Redesign"' in umbrella_metadata
        and "$course-redesign-orchestrator" in umbrella_metadata
        and "### Umbrella entry, Gate 0A and Gate 0" in umbrella_skill
        and "course-redesign-setup" in umbrella_skill
        and "public availability alone is" in umbrella_skill
        and "complete_dormant" in umbrella_skill
        and all(
            status in umbrella_skill
            for status in ("offered_awaiting_response", "requested", "declined")
        )
        and "APPROVE SYSTEM FILES" in system_skill
        and "A token-only reply is" in system_skill,
    )
    strong_prompt_markers = (
        "live host contract can show the complete option set plus a custom answer",
        "verified Codex supports exactly two or three explicit choices plus automatic Other",
        "capacity is unknown, unavailable or exceeded",
        "show every valid numbered option plus Other",
        "Never prune, hide or combine valid choices to fit cards",
        "keep every option visible in dependency chunks",
        "let the lecturer control grouping",
    )
    check(
        "public umbrella prompt preserves every option and lecturer-controlled grouping",
        all(marker in umbrella_metadata for marker in strong_prompt_markers),
    )
    dialogue_markers = (
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
    check(
        "all six skills carry the complete lecturer dialogue contract",
        len(all_skill_text) == 6
        and all(
            all(marker in text for marker in dialogue_markers)
            for text in normalized_skill_text
        ),
    )
    check(
        "deterministic preview-first Gate-0A generator is bundled",
        (PUBLIC_PLUGIN / "scripts/create_material_processing_eligibility.py").is_file()
        and "refusing to overwrite existing eligibility record"
        in (
            PUBLIC_PLUGIN / "scripts/create_material_processing_eligibility.py"
        ).read_text(encoding="utf-8")
        and "--apply" in (
            PUBLIC_PLUGIN / "scripts/create_material_processing_eligibility.py"
        ).read_text(encoding="utf-8"),
    )
    public_state = json.loads(
        (
            PUBLIC_PLUGIN
            / "assets/project-template/01_Control/state.json"
        ).read_text(encoding="utf-8")
    )
    offer_gate = public_state.get("run_template", {}).get("approvals", {}).get(
        "system_improvement_review_offer", {}
    )
    check("public template uses state schema 8", public_state.get("schema_version") == 8)
    check("public template remains inactive", public_state.get("status") == "candidate_not_active")
    check("public template registers no schedule", public_state.get("schedules") == [])
    eligibility = public_state.get("material_processing_eligibility", {})
    check(
        "pre-source Gate 0A blocks every source-detail operation",
        eligibility.get("status") == "awaiting_lecturer_declaration"
        and eligibility.get("gate") == "GATE_0A_MATERIAL_ENVIRONMENT_ELIGIBILITY"
        and set(eligibility.get("must_precede", []))
        == {
            "course_source_path_or_filename_disclosure",
            "course_source_listing",
            "course_source_read",
            "course_source_copy",
            "course_source_hash",
            "course_source_or_context_intake",
        }
        and eligibility.get("material_scope", {}).get(
            "public_availability_alone_is_insufficient"
        )
        is True
        and eligibility.get("material_scope", {}).get(
            "allowed_sensitivity_classifications"
        )
        == [
            "non_sensitive",
            "institution_internal_or_restricted",
            "student_personal_data",
            "institution_internal_or_restricted_and_student_personal_data",
            "mixed_or_uncertain",
        ]
        and eligibility.get("material_scope", {}).get(
            "allowed_assessment_security_classifications"
        )
        == [
            "no_protected_assessment_material",
            "contains_protected_assessment_or_answer_key_material",
            "mixed_or_uncertain",
        ],
    )
    adaptive = public_state.get("adaptive_course_scope", {})
    check(
        "course-independent adaptive scope is explicit",
        adaptive.get("adapt_to_supplied_material_context_level_learners_objectives_assessment_language_and_constraints")
        is True
        and adaptive.get("subject_level_qualification_and_institutional_policy_assumptions_forbidden")
        is True
        and len(adaptive.get("supported_contexts", [])) == 5,
    )
    check(
        "preview-only migration helper is bundled",
        public_state.get("schema_compatibility", {}).get("migration_mode") == "preview_only"
        and (
            PUBLIC_PLUGIN / "scripts/migrate_state_v7_to_v8.py"
        ).is_file(),
    )
    check(
        "complete post-HITL3 review question and proposal-only authority",
        offer_gate.get("ask_exactly_once") is True
        and "schedule_contracts" in offer_gate.get("required_question_scope", [])
        and set(offer_gate.get("authority_on_request", {}).get("authorises", []))
        == {
            "read_only_review_of_current_system_and_successful_run_evidence",
            "prepare_one_versioned_system_improvement_proposal",
        }
        and "register_or_modify_schedule"
        in offer_gate.get("authority_on_request", {}).get("does_not_authorise", []),
    )
    run_template = public_state.get("run_template", {})
    closeout = next(
        (
            item
            for item in run_template.get("manual_stage_authority", {}).get(
                "transition_rules", []
            )
            if item.get("trigger") == "explicit_system_improvement_review_response"
        ),
        {},
    )
    trigger_guidance = run_template.get("approvals", {}).get(
        "trigger_guidance_offer", {}
    )
    check(
        "explicit response closes terminal and guidance never automates",
        closeout.get("requires_explicit_response") is True
        and closeout.get("silence_behavior") == "remain_waiting_without_decision"
        and "complete_dormant" in run_template.get("allowed_run_statuses", [])
        and run_template.get("termination", {}).get("never_resume_after_terminal") is True
        and trigger_guidance.get("informational_only") is True
        and trigger_guidance.get("optional_schedule_guidance", {}).get(
            "no_immediate_run"
        )
        is True,
    )

    cases = json.loads((REVIEW / "test-cases.json").read_text(encoding="utf-8"))
    positives = cases.get("positive_cases", [])
    negatives = cases.get("negative_cases", [])
    positive_fields = {"id", "user_prompt", "expected_skill_or_workflow", "expected_behavior", "expected_result_shape", "fixture_data"}
    negative_fields = {"id", "user_prompt", "expected_safe_behavior", "why_not_complete", "fixture_data"}
    check("at least five complete positive cases", len(positives) >= 5 and all(positive_fields <= set(case) for case in positives))
    check("at least three complete negative cases", len(negatives) >= 3 and all(negative_fields <= set(case) for case in negatives))
    ids = [case["id"] for case in positives + negatives]
    check("unique reviewer case IDs", len(ids) == len(set(ids)))
    check("reviewer case version matches manifest", cases.get("version") == manifest.get("version"))
    check(
        "reviewer cases cover final sequence and authority",
        {
            "P07_PRODUCTION_CLOSE_AND_HITL3",
            "P08_POST_HITL3_SYSTEM_REVIEW_OFFER",
            "N07_SKIP_PRODUCTION_HANDOFF",
            "N08_REVIEW_YES_IS_NOT_WRITE_AUTHORITY",
            "P09_GATE0A_PRIVATE_AUTHORISED",
            "P10_APPROVED_INSTITUTIONAL_ENVIRONMENT",
            "P11_ADAPTIVE_COURSE_SCOPE",
            "N09_PUBLIC_ACCESS_ALONE",
            "N10_INTERNAL_PERSONAL_ROUTE_ONLY",
            "N11_MIXED_OR_UNCERTAIN_GATE0A",
            "P12_NATIVE_CARD_DIALOGUE",
            "P13_COMPLETE_NUMBERED_DIALOGUE",
            "P14_DEPENDENCY_CLUSTER_AND_CUSTOM_ANSWER",
            "N12_SKIP_OR_OPTION_PRUNING",
        }.issubset(ids),
    )

    checklist = (REVIEW / "LISTING_METADATA_CHECKLIST.md").read_text(encoding="utf-8")
    check("all owner markers are explicit", all(marker in checklist for marker in REQUIRED_OWNER_MARKERS))
    check(
        "no fabricated support URL in candidate manifest",
        "supportURL" not in manifest and "supportURL" not in interface,
    )

    if args.archive:
        archive_failures = validate_archive(args.archive.resolve())
        check("skills-only ZIP matches public source", not archive_failures, "; ".join(archive_failures) if archive_failures else None)

    result = {
        "schema_version": 1,
        "pass": not failures,
        "package_validation": "passed" if not failures else "failed",
        "submission_ready": False,
        "public_source_file_count": len(tree_records(PUBLIC_PLUGIN)),
        "skill_count": len(actual_skills),
        "positive_case_count": len(positives),
        "negative_case_count": len(negatives),
        "checks": checks,
        "failures": failures,
        "owner_submission_blockers": OWNER_BLOCKERS,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
