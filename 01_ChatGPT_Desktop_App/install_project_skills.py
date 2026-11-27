#!/usr/bin/env python3
"""Preview or install the six repo-scoped Codex skills and their local dependencies."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


ADAPTER = Path(__file__).resolve().parent
sys.path.insert(0, str(ADAPTER / "validation"))
from release_inputs import verified_public_payload

PACKAGE = ADAPTER / "openai-submission/source/agentic-course-redesign"
COMPONENTS = ("skills", "scripts", "assets")


def hash_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def install(project: Path, apply: bool) -> dict:
    project = project.expanduser().resolve(strict=True)
    if not project.is_dir() or project in {Path(project.anchor), Path.home().resolve()}:
        raise ValueError("Select a dedicated project directory.")
    target = project / ".agents"
    pending = []
    conflicts = []
    expected = {}
    payload = verified_public_payload(PACKAGE)
    for name, content in payload.items():
        relative = Path(name)
        if relative.parts[0] not in COMPONENTS:
            continue
        dest = target / relative
        expected[name] = hashlib.sha256(content).hexdigest()
        parents = [parent for parent in dest.parents if parent.is_relative_to(target)]
        if any(parent.is_symlink() or (parent.exists() and not parent.is_dir()) for parent in parents):
            conflicts.append(name)
        elif dest.is_symlink() or not dest.resolve(strict=False).is_relative_to(target):
            conflicts.append(name)
        elif dest.is_file() and hash_file(dest) == expected[name]:
            continue
        elif dest.exists():
            conflicts.append(name)
        else:
            pending.append(relative)
    if apply and not conflicts:
        for relative in pending:
            dest = target / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            dst = dest.open("xb")
            try:
                with dst:
                    dst.write(payload[relative.as_posix()])
            except OSError:
                dest.unlink(missing_ok=True)
                raise
        for relative, digest in expected.items():
            if hash_file(target / relative) != digest:
                raise ValueError(f"Installed bytes differ at {relative}")
    return {
        "project": str(project),
        "apply": apply,
        "ok": not conflicts,
        "package_files": len(expected),
        "new_files": [p.as_posix() for p in pending],
        "conflicts": conflicts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--apply", action="store_true", help="Create previewed files without overwriting existing files.")
    args = parser.parse_args()
    try:
        result = install(args.project, args.apply)
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
