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


def create(project: Path, output: Path, replace: bool) -> dict:
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
        "classification_requires_lecturer_confirmation": True,
    }


def verify(project: Path, manifest: Path) -> dict:
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
        if name == "create":
            sub.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    result = (
        create(args.project, args.manifest, args.replace)
        if args.command == "create"
        else verify(args.project, args.manifest)
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
