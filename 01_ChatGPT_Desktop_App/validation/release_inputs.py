"""Select reviewed package members before opening any release input."""
from __future__ import annotations

import hashlib
import json
import stat
from pathlib import Path, PurePosixPath

ADAPTER = Path(__file__).resolve().parents[1]
REVIEW = ADAPTER / "openai-submission/review"


def reviewed_file(root: Path, name: str) -> Path:
    relative = PurePosixPath(name)
    if relative.is_absolute() or relative.as_posix() != name or not relative.parts:
        raise ValueError(f"Invalid release path {name!r}")
    if any(part in {".", ".."} or "\\" in part or ":" in part for part in relative.parts):
        raise ValueError(f"Invalid release path {name!r}")
    path = root / relative
    if not path.is_relative_to(ADAPTER):
        raise ValueError(f"Release input outside adapter: {name}")
    for component in (path, *(p for p in path.parents if p.is_relative_to(ADAPTER))):
        info = component.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Redirected release input: {name}")
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError(f"Release input is not a regular file: {name}")
    return path


def public_manifest() -> dict[str, str]:
    path = reviewed_file(REVIEW, "public-package-digests.json")
    return json.loads(path.read_text(encoding="utf-8"))


def verified_public_payload(root: Path) -> dict[str, bytes]:
    payload = {}
    for name, expected in public_manifest().items():
        content = reviewed_file(root, name).read_bytes()
        if hashlib.sha256(content).hexdigest().upper() != expected:
            raise ValueError(f"Release bytes differ from approved input: {name}")
        payload[name] = content
    return payload


def portable_sources() -> list[Path]:
    inventory = reviewed_file(REVIEW, "portable-files.json")
    names = json.loads(inventory.read_text(encoding="utf-8"))
    if not isinstance(names, list) or len(names) != len(set(names)):
        raise ValueError("The portable release inventory must have unique members.")
    return [reviewed_file(ADAPTER, name) for name in names]
