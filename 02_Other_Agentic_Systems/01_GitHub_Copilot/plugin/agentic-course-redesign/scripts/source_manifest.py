#!/usr/bin/env python3
"""Create or verify a deterministic protected-source manifest for one course."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import stat
from datetime import datetime, timezone
from pathlib import Path


HEADERS = [
    "relative_path",
    "source_class",
    "audience_classification",
    "assessment_security",
    "size_bytes",
    "sha256",
]
DEFAULT_ROOTS = ("00_Source_Materials", "00_Context")
ALLOWED_MATERIAL_CATEGORIES = {
    "privately_owned_or_rightsholder_authorised",
    "appropriately_licensed_or_public_with_explicit_ai_processing_authority",
    "institution_internal_or_restricted",
    "mixed",
    "uncertain",
}
ALLOWED_SENSITIVITY_CLASSIFICATIONS = [
    "non_sensitive",
    "institution_internal_or_restricted",
    "student_personal_data",
    "institution_internal_or_restricted_and_student_personal_data",
    "mixed_or_uncertain",
]
ALLOWED_ASSESSMENT_SECURITY_CLASSIFICATIONS = [
    "no_protected_assessment_material",
    "contains_protected_assessment_or_answer_key_material",
    "mixed_or_uncertain",
]
ELIGIBILITY_EXCLUDED_FIELDS = frozenset(
    {"fingerprint", "lecturer_declaration_reference", "recorded_at"}
)


def canonical_eligibility_fingerprint(value: dict) -> str:
    payload = {
        key: item for key, item in value.items() if key not in ELIGIBILITY_EXCLUDED_FIELDS
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()


def _nonexpired(value: object) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        parsed = datetime.fromisoformat(value.split("[", 1)[0])
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.astimezone(timezone.utc) > datetime.now(
        timezone.utc
    )


def validate_eligibility(record_path: Path) -> dict[str, object]:
    """Validate trusted Gate-0A control before enumerating any course source."""

    if not record_path.is_file():
        return {"ok": False, "errors": ["approved Gate-0A eligibility record missing"]}
    try:
        value = json.loads(record_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [f"invalid Gate-0A eligibility record: {exc}"]}
    if not isinstance(value, dict):
        return {"ok": False, "errors": ["Gate-0A eligibility record must be an object"]}
    errors: list[str] = []
    environment = value.get("environment", {})
    material = value.get("material_scope", {})
    decision = value.get("decision", {})
    if not all(isinstance(item, dict) for item in (environment, material, decision)):
        return {"ok": False, "errors": ["Gate-0A eligibility sections must be objects"]}
    expected_fingerprint = canonical_eligibility_fingerprint(value)
    actual_fingerprint = str(value.get("fingerprint") or "").upper()
    category = material.get("declared_category")
    environment_category = environment.get("category")
    outcome = decision.get("outcome")
    if value.get("status") != "approved" or outcome != "proceed":
        errors.append("Gate-0A must be approved with outcome proceed before source intake")
    if value.get("reconfirmation_required") is not False:
        errors.append("Gate-0A reconfirmation is required before source intake")
    if actual_fingerprint != expected_fingerprint:
        errors.append("Gate-0A eligibility fingerprint is missing or mismatched")
    if not value.get("lecturer_declaration_reference") or not value.get("recorded_at"):
        errors.append("Gate-0A lecturer declaration receipt is incomplete")
    if material.get("public_availability_alone_is_insufficient") is not True:
        errors.append("Gate-0A must state that public availability alone is insufficient")
    if material.get("ai_processing_authority_confirmed") is not True:
        errors.append("explicit AI-processing authority is not confirmed")
    if material.get(
        "allowed_sensitivity_classifications"
    ) != ALLOWED_SENSITIVITY_CLASSIFICATIONS:
        errors.append("Gate-0A sensitivity classifications are missing or reordered")
    if material.get(
        "allowed_assessment_security_classifications"
    ) != ALLOWED_ASSESSMENT_SECURITY_CLASSIFICATIONS:
        errors.append("Gate-0A assessment-security classifications are missing or reordered")
    if category not in ALLOWED_MATERIAL_CATEGORIES:
        errors.append("Gate-0A must name one allowed material category")
    for field in (
        "contains_institution_internal_or_restricted_material",
        "contains_student_personal_data",
        "assessment_security_handling_authorised",
    ):
        if not isinstance(material.get(field), bool):
            errors.append(f"Gate-0A material scope must answer {field} as boolean")
    sensitivity = material.get("sensitivity_classification")
    assessment_security = material.get("assessment_security_classification")
    if sensitivity not in ALLOWED_SENSITIVITY_CLASSIFICATIONS:
        errors.append("Gate-0A must name one allowed sensitivity classification")
    if assessment_security not in ALLOWED_ASSESSMENT_SECURITY_CLASSIFICATIONS:
        errors.append("Gate-0A must name one allowed assessment-security classification")
    expected_sensitivity = {
        (False, False): "non_sensitive",
        (True, False): "institution_internal_or_restricted",
        (False, True): "student_personal_data",
        (True, True): "institution_internal_or_restricted_and_student_personal_data",
    }.get(
        (
            material.get("contains_institution_internal_or_restricted_material"),
            material.get("contains_student_personal_data"),
        )
    )
    if sensitivity == "mixed_or_uncertain":
        if category not in {"mixed", "uncertain"}:
            errors.append("mixed/uncertain sensitivity requires a mixed or uncertain material category")
    elif expected_sensitivity is not None and sensitivity != expected_sensitivity:
        errors.append("Gate-0A sensitivity classification contradicts its material-scope flags")
    if material.get("assessment_security_handling_authorised") is not True:
        errors.append("explicit assessment-security handling authority is not confirmed")
    if sensitivity == "mixed_or_uncertain" or assessment_security == "mixed_or_uncertain":
        errors.append("mixed or uncertain security classifications must fail closed")
    if category in {"mixed", "uncertain"}:
        errors.append("mixed or uncertain material must be segregated or clarified")
    if environment_category == "personal_or_unmanaged":
        if category not in {
            "privately_owned_or_rightsholder_authorised",
            "appropriately_licensed_or_public_with_explicit_ai_processing_authority",
        }:
            errors.append(
                "personal/unmanaged processing is limited to owned/authorised or explicitly AI-processable licensed/public material"
            )
        if material.get("contains_institution_internal_or_restricted_material") is not False:
            errors.append(
                "institution-internal/restricted material is route-only in a personal/unmanaged environment"
            )
        if material.get("contains_student_personal_data") is not False:
            errors.append(
                "student personal data requires a separately approved institutional workflow"
            )
    elif environment_category == "approved_institutional_exact_environment":
        for field in (
            "exact_environment_reference",
            "institutional_policy_reference",
            "approved_scope",
        ):
            if not environment.get(field):
                errors.append(f"approved institutional environment is missing {field}")
        if not _nonexpired(environment.get("policy_expires_at")):
            errors.append("approved institutional policy expiry is missing, invalid or expired")
    else:
        errors.append("Gate-0A processing environment category is invalid")
    return {
        "ok": not errors,
        "errors": errors,
        "fingerprint": actual_fingerprint if not errors else None,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def is_redirecting_link(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        is_junction = getattr(path, "is_junction", None)
        if callable(is_junction) and is_junction():
            return True
        attributes = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
        if attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0):
            return os.path.normcase(os.path.abspath(path)) != os.path.normcase(
                os.path.abspath(path.resolve(strict=False))
            )
    except OSError:
        return True
    return False


def classify(relative: str) -> tuple[str, str, str]:
    text = relative.casefold()
    if relative.startswith("00_Context/"):
        source_class = "context"
    elif any(token in text for token in ("test", "exam", "assessment", "rubric")):
        source_class = "assessment"
    else:
        source_class = "course_material"
    if any(token in text for token in ("answer", "key", "marking", "solution", "teacher")):
        return source_class, "lecturer_only_candidate", "teacher_only_review_required"
    if source_class == "assessment":
        return source_class, "unconfirmed", "assessment_review_required"
    return source_class, "unconfirmed", "none_identified_filename_only"


def enumerate_files(project: Path, roots: tuple[str, ...]) -> tuple[list[Path], list[str]]:
    files: list[Path] = []
    errors: list[str] = []
    for root_name in roots:
        root = project / root_name
        if not root.is_dir():
            errors.append(f"missing protected root: {root_name}")
            continue
        if is_redirecting_link(root):
            errors.append(f"redirecting link/junction forbidden: {root_name}")
            continue
        for current, directories, names in os.walk(root, followlinks=False):
            current_path = Path(current)
            for directory in list(directories):
                candidate = current_path / directory
                if is_redirecting_link(candidate):
                    errors.append(
                        f"redirecting link/junction forbidden: {candidate.relative_to(project).as_posix()}"
                    )
                    directories.remove(directory)
            for name in names:
                candidate = current_path / name
                if name.casefold() == "readme.txt":
                    continue
                if is_redirecting_link(candidate):
                    errors.append(
                        f"redirecting link/junction forbidden: {candidate.relative_to(project).as_posix()}"
                    )
                elif candidate.is_file():
                    files.append(candidate)
    return sorted(files, key=lambda p: p.relative_to(project).as_posix().casefold()), errors


def create(project: Path, output: Path, replace: bool, eligibility_record: Path) -> dict:
    eligibility_record = (
        eligibility_record
        if eligibility_record.is_absolute()
        else project / eligibility_record
    )
    eligibility = validate_eligibility(eligibility_record)
    if not eligibility["ok"]:
        return {
            "ok": False,
            "mode": "create",
            "source_enumeration_started": False,
            "errors": eligibility["errors"],
        }
    project = project.resolve(strict=True)
    output = output if output.is_absolute() else project / output
    files, errors = enumerate_files(project, DEFAULT_ROOTS)
    if errors:
        return {"ok": False, "errors": errors}
    if output.exists() and not replace:
        return {"ok": False, "errors": ["manifest exists; use --replace only after approval"]}
    rows = []
    for path in files:
        relative = path.relative_to(project).as_posix()
        source_class, audience, security = classify(relative)
        rows.append(
            {
                "relative_path": relative,
                "source_class": source_class,
                "audience_classification": audience,
                "assessment_security": security,
                "size_bytes": str(path.stat().st_size),
                "sha256": sha256(path),
            }
        )
    if not rows:
        return {"ok": False, "errors": ["no source files found"]}
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    if output.exists():
        output.unlink()
    temporary.replace(output)
    return {
        "ok": True,
        "mode": "create",
        "project": str(project),
        "manifest": str(output),
        "row_count": len(rows),
        "manifest_fingerprint": sha256(output),
        "material_processing_eligibility_fingerprint": eligibility["fingerprint"],
        "classification_requires_lecturer_confirmation": True,
    }


def verify(project: Path, manifest: Path, eligibility_record: Path) -> dict:
    eligibility_record = (
        eligibility_record
        if eligibility_record.is_absolute()
        else project / eligibility_record
    )
    eligibility = validate_eligibility(eligibility_record)
    if not eligibility["ok"]:
        return {
            "ok": False,
            "mode": "verify",
            "source_enumeration_started": False,
            "errors": eligibility["errors"],
        }
    project = project.resolve(strict=True)
    manifest = manifest if manifest.is_absolute() else project / manifest
    errors: list[str] = []
    results = []
    if not manifest.is_file():
        return {"ok": False, "errors": ["manifest missing"]}
    with manifest.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != HEADERS:
            return {"ok": False, "errors": [f"invalid headers: {reader.fieldnames}"]}
        rows = list(reader)
    actual_files, enumeration_errors = enumerate_files(project, DEFAULT_ROOTS)
    errors.extend(enumeration_errors)
    actual_map = {p.relative_to(project).as_posix(): p for p in actual_files}
    seen: set[str] = set()
    for number, row in enumerate(rows, 2):
        relative = (row.get("relative_path") or "").strip().replace("\\", "/")
        if not relative or relative.startswith("/") or ".." in Path(relative).parts:
            results.append({"row": number, "path": relative, "status": "invalid-path"})
            continue
        if relative in seen:
            results.append({"row": number, "path": relative, "status": "duplicate"})
            continue
        seen.add(relative)
        path = actual_map.get(relative)
        if path is None:
            results.append({"row": number, "path": relative, "status": "missing"})
            continue
        try:
            expected_size = int(row.get("size_bytes") or "")
        except ValueError:
            expected_size = -1
        expected_hash = (row.get("sha256") or "").strip().upper()
        actual_hash = sha256(path)
        valid_classification = all(
            (row.get(field) or "").strip()
            for field in ("source_class", "audience_classification", "assessment_security")
        )
        status = "ok"
        if not valid_classification:
            status = "missing-classification"
        elif expected_size != path.stat().st_size:
            status = "size-mismatch"
        elif re.fullmatch(r"[0-9A-F]{64}", expected_hash) is None:
            status = "invalid-sha256"
        elif expected_hash != actual_hash:
            status = "hash-mismatch"
        results.append({"row": number, "path": relative, "status": status})
    for relative in sorted(set(actual_map) - seen):
        results.append({"path": relative, "status": "unlisted"})
    ok = bool(rows) and not errors and all(item["status"] == "ok" for item in results)
    return {
        "ok": ok,
        "mode": "verify",
        "project": str(project),
        "manifest": str(manifest),
        "manifest_fingerprint": sha256(manifest),
        "material_processing_eligibility_fingerprint": eligibility["fingerprint"],
        "errors": errors,
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("create", "verify"):
        sub = subparsers.add_parser(name)
        sub.add_argument("--project", required=True, type=Path)
        sub.add_argument(
            "--manifest", type=Path, default=Path("01_Control/source-hashes.csv")
        )
        sub.add_argument(
            "--eligibility-record",
            type=Path,
            default=Path("01_Control/material-processing-eligibility.json"),
            help="approved fingerprinted Gate-0A control; validated before source enumeration",
        )
        if name == "create":
            sub.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    result = (
        create(args.project, args.manifest, args.replace, args.eligibility_record)
        if args.command == "create"
        else verify(args.project, args.manifest, args.eligibility_record)
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
