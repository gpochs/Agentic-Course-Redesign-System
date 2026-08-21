#!/usr/bin/env python3
"""Parse every shipped JSON, TOML, YAML, Python, and SVG source file."""

from __future__ import annotations

import ast
import json
import tomllib
from pathlib import Path
from xml.etree import ElementTree

import yaml


ROOT = Path(__file__).resolve().parent.parent
SKIP_PARTS = {".git", "dist", "__pycache__", ".pytest_cache", ".venv", "venv", "env"}


def main() -> int:
    counts = {"json": 0, "toml": 0, "yaml": 0, "python": 0, "svg": 0}
    failures: list[dict[str, str]] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or set(path.relative_to(ROOT).parts) & SKIP_PARTS:
            continue
        relative = path.relative_to(ROOT).as_posix()
        try:
            if path.suffix.casefold() == ".json":
                json.loads(path.read_text(encoding="utf-8"))
                counts["json"] += 1
            elif path.suffix.casefold() == ".toml":
                with path.open("rb") as handle:
                    tomllib.load(handle)
                counts["toml"] += 1
            elif path.suffix.casefold() in {".yaml", ".yml"}:
                yaml.safe_load(path.read_text(encoding="utf-8"))
                counts["yaml"] += 1
            elif path.suffix.casefold() == ".py":
                ast.parse(path.read_text(encoding="utf-8"), filename=relative)
                counts["python"] += 1
            elif path.suffix.casefold() == ".svg":
                if b"\r" in path.read_bytes():
                    raise ValueError("SVG must use LF line endings for deterministic hashing")
                ElementTree.parse(path)
                counts["svg"] += 1
        except Exception as error:  # report every parser failure in one pass
            failures.append(
                {"path": relative, "error": f"{type(error).__name__}: {error}"}
            )
    result = {
        "schema_version": 1,
        "pass": not failures,
        "parsed": counts,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
