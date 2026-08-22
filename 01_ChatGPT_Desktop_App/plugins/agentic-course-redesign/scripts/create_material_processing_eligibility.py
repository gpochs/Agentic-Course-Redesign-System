#!/usr/bin/env python3
"""Preview or atomically create one deterministic Gate-0A eligibility record."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import tempfile
from datetime import datetime
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
OUTPUT_RELATIVE_PATH = Path("01_Control/material-processing-eligibility.json")


def _locate_template_path() -> Path:
    relative = Path("01_Control/material-processing-eligibility.template.json")
    candidates: list[Path] = []
    for ancestor in SCRIPT_PATH.parents:
        candidates.extend(
            (
                ancestor / "course-project-template" / relative,
                ancestor / "assets" / "project-template" / relative,
                ancestor / relative,
            )
        )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(
        "material-processing eligibility template not found in shared-core, "
        "plugin assets or workspace overlay"
    )


TEMPLATE_PATH = _locate_template_path()


def _load_source_manifest_module():
    sibling = SCRIPT_PATH.with_name("source_manifest.py")
    spec = importlib.util.spec_from_file_location("_acr_source_manifest", sibling)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load eligibility semantics from {sibling}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE_MANIFEST = _load_source_manifest_module()


class _MemoryRecord:
    """Minimal read-only Path interface for the existing eligibility validator."""

    def __init__(self, value: dict[str, object]):
        self._text = json.dumps(value, ensure_ascii=False)

    def is_file(self) -> bool:
        return True

    def read_text(self, encoding: str) -> str:
        if encoding.lower().replace("-", "") != "utf8":
            raise ValueError("eligibility validator requested an unexpected encoding")
        return self._text


def parse_bool(value: str) -> bool:
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    raise argparse.ArgumentTypeError("expected exactly true or false")


def target_is_dangerously_broad(path: Path) -> bool:
    resolved = path.resolve(strict=False)
    home = Path.home().resolve(strict=False)
    anchor = Path(resolved.anchor).resolve(strict=False)
    return resolved == anchor or resolved == home or len(resolved.parts) < 4


def _offset_datetime(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.split("[", 1)[0])
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO-8601 date-time") from exc
    if parsed.tzinfo is None:
        raise ValueError(f"{label} must include a UTC offset")
    return parsed


def _require_text(value: str, label: str) -> None:
    if not value.strip():
        raise ValueError(f"{label} must not be blank")


def _infer_outcome(record: dict[str, object]) -> str:
    environment = record["environment"]
    material = record["material_scope"]
    assert isinstance(environment, dict) and isinstance(material, dict)
    category = material["declared_category"]
    sensitivity = material["sensitivity_classification"]
    assessment = material["assessment_security_classification"]

    if category == "mixed":
        return "fail_closed_until_segregated"
    if (
        category == "uncertain"
        or sensitivity == "mixed_or_uncertain"
        or assessment == "mixed_or_uncertain"
    ):
        return "fail_closed_until_clarified"
    if environment["category"] == "personal_or_unmanaged" and (
        category == "institution_internal_or_restricted"
        or material["contains_institution_internal_or_restricted_material"]
        or material["contains_student_personal_data"]
    ):
        return "route_only"
    validation = SOURCE_MANIFEST.validate_eligibility(
        _MemoryRecord(
            {
                **record,
                "status": "approved",
                "reconfirmation_required": False,
                "decision": {**record["decision"], "outcome": "proceed"},
                "fingerprint": None,
            }
        )
    )
    # Fingerprint and receipt errors are expected until the record is finalised.
    substantive = [
        error
        for error in validation["errors"]
        if error not in {
            "Gate-0A eligibility fingerprint is missing or mismatched",
            "Gate-0A lecturer declaration receipt is incomplete",
        }
    ]
    return "proceed" if not substantive else "fail_closed_until_clarified"


def build_record(args: argparse.Namespace) -> tuple[dict[str, object], dict[str, object]]:
    template = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
    if not isinstance(template, dict):
        raise ValueError("eligibility template must be a JSON object")
    for value, label in (
        (args.eligibility_id, "eligibility-id"),
        (args.decision_reason, "decision-reason"),
        (args.approved_processing_scope, "approved-processing-scope"),
        (args.lecturer_declaration_reference, "lecturer-declaration-reference"),
    ):
        _require_text(value, label)
    _offset_datetime(args.recorded_at, "recorded-at")
    if args.policy_expires_at:
        _offset_datetime(args.policy_expires_at, "policy-expires-at")

    environment = template["environment"]
    material = template["material_scope"]
    decision = template["decision"]
    environment.update(
        {
            "category": args.environment_category,
            "exact_environment_reference": args.exact_environment_reference,
            "institutional_policy_reference": args.institutional_policy_reference,
            "approved_scope": args.approved_scope,
            "policy_expires_at": args.policy_expires_at,
        }
    )
    material.update(
        {
            "declared_category": args.material_category,
            "ai_processing_authority_confirmed": args.ai_processing_authority_confirmed,
            "contains_institution_internal_or_restricted_material": args.contains_institution_internal_or_restricted_material,
            "contains_student_personal_data": args.contains_student_personal_data,
            "sensitivity_classification": args.sensitivity_classification,
            "assessment_security_classification": args.assessment_security_classification,
            "assessment_security_handling_authorised": args.assessment_security_handling_authorised,
        }
    )
    template.update(
        {
            "eligibility_id": args.eligibility_id,
            "lecturer_declaration_reference": args.lecturer_declaration_reference,
            "recorded_at": args.recorded_at,
        }
    )
    decision.update(
        {
            "reason": args.decision_reason,
            "approved_processing_scope": args.approved_processing_scope,
        }
    )
    outcome = _infer_outcome(template)
    template["status"] = {
        "proceed": "approved",
        "route_only": "route_only",
        "fail_closed_until_segregated": "failed_closed",
        "fail_closed_until_clarified": "failed_closed",
    }[outcome]
    template["reconfirmation_required"] = outcome != "proceed"
    decision["outcome"] = outcome
    template["fingerprint"] = SOURCE_MANIFEST.canonical_eligibility_fingerprint(template)

    intake_validation = SOURCE_MANIFEST.validate_eligibility(_MemoryRecord(template))
    if outcome == "proceed" and not intake_validation["ok"]:
        raise ValueError(
            "generated proceed record failed the canonical eligibility validator: "
            + "; ".join(intake_validation["errors"])
        )
    if outcome != "proceed" and intake_validation["ok"]:
        raise ValueError("non-proceed record unexpectedly permits source intake")
    if template["fingerprint"] != SOURCE_MANIFEST.canonical_eligibility_fingerprint(template):
        raise ValueError("generated eligibility fingerprint is not canonical")
    return template, intake_validation


def _resolve_output(project: Path) -> Path:
    if not project.is_absolute():
        raise ValueError("project must be an absolute path")
    project = project.resolve(strict=False)
    if target_is_dangerously_broad(project):
        raise ValueError(f"refusing dangerously broad project target: {project}")
    if not project.is_dir():
        raise FileNotFoundError(f"project directory does not exist: {project}")
    control = project / "01_Control"
    if not control.is_dir():
        raise FileNotFoundError(f"project control directory does not exist: {control}")
    resolved_control = control.resolve(strict=True)
    if resolved_control != control or resolved_control.parent != project:
        raise ValueError(
            "refusing redirected project control directory; 01_Control must be "
            f"the literal child of the approved project: {control}"
        )
    return resolved_control / OUTPUT_RELATIVE_PATH.name


def atomic_create(path: Path, payload: bytes) -> None:
    resolved_parent = path.parent.resolve(strict=True)
    if resolved_parent != path.parent:
        raise ValueError(
            "refusing redirected output parent before create: " + str(path.parent)
        )
    if path.exists() or path.is_symlink():
        raise FileExistsError(f"refusing to overwrite existing eligibility record: {path}")
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".material-processing-eligibility.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--project", required=True, type=Path)
    result.add_argument("--eligibility-id", required=True)
    result.add_argument(
        "--environment-category",
        required=True,
        choices=("personal_or_unmanaged", "approved_institutional_exact_environment"),
    )
    result.add_argument(
        "--material-category",
        required=True,
        choices=tuple(sorted(SOURCE_MANIFEST.ALLOWED_MATERIAL_CATEGORIES)),
    )
    result.add_argument(
        "--ai-processing-authority-confirmed", required=True, type=parse_bool
    )
    result.add_argument(
        "--contains-institution-internal-or-restricted-material", required=True, type=parse_bool
    )
    result.add_argument("--contains-student-personal-data", required=True, type=parse_bool)
    result.add_argument(
        "--sensitivity-classification",
        required=True,
        choices=tuple(SOURCE_MANIFEST.ALLOWED_SENSITIVITY_CLASSIFICATIONS),
    )
    result.add_argument(
        "--assessment-security-classification",
        required=True,
        choices=tuple(SOURCE_MANIFEST.ALLOWED_ASSESSMENT_SECURITY_CLASSIFICATIONS),
    )
    result.add_argument(
        "--assessment-security-handling-authorised", required=True, type=parse_bool
    )
    result.add_argument("--exact-environment-reference")
    result.add_argument("--institutional-policy-reference")
    result.add_argument("--approved-scope")
    result.add_argument("--policy-expires-at")
    result.add_argument("--decision-reason", required=True)
    result.add_argument("--approved-processing-scope", required=True)
    result.add_argument("--lecturer-declaration-reference", required=True)
    result.add_argument("--recorded-at", required=True)
    result.add_argument("--apply", action="store_true")
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        output = _resolve_output(args.project)
        record, validation = build_record(args)
        payload = (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        report = {
            "ok": True,
            "mode": "apply" if args.apply else "preview",
            "output": str(output),
            "relative_output": OUTPUT_RELATIVE_PATH.as_posix(),
            "would_overwrite": output.exists() or output.is_symlink(),
            "source_intake_permitted": bool(validation["ok"]),
            "source_intake_validation_errors": validation["errors"],
            "record": record,
        }
        if report["would_overwrite"]:
            raise FileExistsError(f"refusing to overwrite existing eligibility record: {output}")
        if args.apply:
            atomic_create(output, payload)
            report["created"] = True
        else:
            report["created"] = False
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "mode": "apply" if args.apply else "preview",
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
