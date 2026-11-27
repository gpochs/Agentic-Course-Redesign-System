"""Build a self-contained native edition from the shared release (Python 3.11+)."""

import argparse
import hashlib
import json
import os
import stat
import subprocess
import tempfile
import tomllib
from functools import cache
from pathlib import Path

ADAPTERS = Path(__file__).resolve().parent
ROOT = ADAPTERS.parent
CORE = ROOT / "03_Shared_Workflow_Core"
PORTABLE = ADAPTERS / "00_Portable_Core_Adapter/overlay/.claude/skills/course-redesign"
ROLES = ROOT / "01_ChatGPT_Desktop_App/plugins/agentic-course-redesign/assets/project-template/.codex/agents"
NAME = "agentic-course-redesign"
HOSTS = {"claude": "02_Claude_Code", "opencode": "03_OpenCode",
         "antigravity": "04_Google_Antigravity", "copilot": "01_GitHub_Copilot", "copilot-project": "01_GitHub_Copilot"}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


# New canonical references are named explicitly for a maintainer running the
# builder before staging this release. All other copied paths must be recorded.
NEW_GUIDES = ("course-redesign-materials/references/artifact-review.md",
              "course-redesign-orchestrator/references/role-evidence.md",
              "course-redesign-orchestrator/references/second-opinion.md",
              "course-redesign-orchestrator/references/model-plan.md",
              "course-redesign-orchestrator/references/tool-fit.md")
ROLE_GUIDE = Path(NEW_GUIDES[1])
NATIVE_GUIDE = ROLE_GUIDE.with_name("native-intake.md")


def link_review_entry(content, skill):
    """Place the host guide at the entry used for the next source or draft."""
    guide = ("references/native-intake.md" if skill == "course-redesign-orchestrator"
             else "../course-redesign-orchestrator/references/native-intake.md")
    heading = "## In conversation\n"
    if content.count(heading) != 1:
        raise ValueError(f"Expected a single conversation section in {skill}")
    instruction = f"Use [this app's review guide]({guide}) to select a course tab or files and open a saved draft with the teacher."
    return content.replace(heading, heading + "\n" + instruction + "\n", 1)


def link_native_intake(content):
    section = b"### Asking about course context"
    if content.count(section) != 1:
        raise ValueError("Expected one course-context section in the role guide")
    link = b"\n\nWhen preparing the next context question or preview in this host, use its [native intake guidance](native-intake.md)."
    return content.replace(section, section + link, 1)


@cache
def reviewed_files():
    if (ROOT / ".git").exists():
        records = subprocess.run(["git", "ls-files", "--cached", "-z"], cwd=ROOT,
                                 check=True, capture_output=True).stdout.split(b"\0")
        names = {os.fsdecode(record): None for record in records if record}
        for guide in NEW_GUIDES:
            for base in (CORE / "agent-skills", ADAPTERS / HOSTS["copilot"] / "plugin" / NAME / "skills"):
                names[(base / guide).relative_to(ROOT).as_posix()] = None
        quick_start = ADAPTERS / HOSTS["copilot"] / "plugin" / NAME / "assets/PARTICIPANT_QUICK_START.md"
        names[quick_start.relative_to(ROOT).as_posix()] = None
        for folder in set(HOSTS.values()):
            guide = ADAPTERS / folder / "native-intake.md"
            if guide.is_file():
                names[guide.relative_to(ROOT).as_posix()] = None
        copilot_guide = ADAPTERS / HOSTS["copilot"] / "plugin" / NAME / "skills" / NATIVE_GUIDE
        if copilot_guide.is_file():
            names[copilot_guide.relative_to(ROOT).as_posix()] = None
    else:
        snapshot = json.loads((ROOT / "package-inventory.json").read_text(encoding="utf-8"))
        names = {entry["relative_path"]: entry["sha256"] for entry in snapshot["files"]}
    return names


def read_reviewed(path):
    relative = path.relative_to(ROOT)
    name = relative.as_posix()
    records = reviewed_files()
    if name not in records or ".." in relative.parts:
        raise ValueError(f"Unreviewed package input: {name}")
    current = ROOT
    for part in relative.parts:
        current = current / part
        info = current.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f"Linked package input: {relative}")
    if not stat.S_ISREG(info.st_mode):
        raise ValueError(f"Expected regular file: {relative}")
    content = path.read_bytes()
    expected = records[name]
    if expected and hashlib.sha256(content).hexdigest() != expected.lower():
        raise ValueError(f"Packaged source digest mismatch: {relative}")
    return content


def copy_file(source, target):
    data = read_reviewed(source)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)


def selected_files(directory):
    prefix = directory.relative_to(ROOT).as_posix() + "/"
    return sorted(ROOT / name for name in reviewed_files() if name.startswith(prefix))


def copy_tree(source, target):
    for path in selected_files(source):
        copy_file(path, target / path.relative_to(source))


def render(host, output):
    edition = ADAPTERS / HOSTS[host]
    if host == "copilot":
        copy_tree(edition / "plugin" / NAME, output)
        return
    output.mkdir(parents=True, exist_ok=True)
    copy_file(ROOT / "LICENSE", output / "LICENSE")
    copy_file(edition / "README.md", output / "README.md")
    if host in {"opencode", "copilot-project"}:
        bundle = output / "skills/course-redesign"
        copy_tree(PORTABLE, bundle)
        stage_root = bundle / "stages"
    else:
        bundle = output
        stage_root = bundle / "skills"
        metadata = {
            "name": NAME, "version": read_reviewed(CORE / "VERSION").decode().strip(),
            "description": "Revise a course, compare teaching options and try draft materials before choosing what to use."
        }
        if host == "claude":
            metadata.update(name="gpochs-course-redesign", author={"name": "Gian Peter Ochsner"}, license="MIT")
            write(output / "SKILL.md", "---\nname: gpochs-course-redesign\ndescription: Improve a lesson, activity, assessment or complete course. Start with your teaching goal or choose materials to review.\n---\n\nStart with the bundled [orchestrator](skills/course-redesign-orchestrator/SKILL.md).")
        if host == "antigravity":
            (output / "assets").mkdir(exist_ok=True)
            copy_file(ROLES.parents[2] / "logo.svg", output / "assets/logo.svg")
            metadata["logo"] = "assets/logo.svg"
            metadata["displayName"] = "Agentic Course Redesign"
            metadata["suggestedPrompts"] = ["Help me improve a lesson. I can describe it or choose materials to work from."]
        manifest_dir = ".claude-plugin" if host == "claude" else ".antigravity-plugin"
        write(output / manifest_dir / "plugin.json", json.dumps(metadata, indent=2))
    copy_tree(CORE / "agent-skills", stage_root)
    for skill in ("course-redesign-orchestrator", "course-redesign-setup", "course-redesign-materials", "course-redesign-assessment"):
        entry = stage_root / skill / "SKILL.md"
        if host == "copilot-project":
            copy_file(edition / "plugin" / NAME / "skills" / skill / "SKILL.md", entry)
        else:
            write(entry, link_review_entry(entry.read_text(encoding="utf-8"), skill))
    if host == "antigravity":
        # Antigravity reads a maximum of 24,000 bytes from a skill body.
        # Keep the opening conversation in the entry point and preserve the
        # complete procedure beside it so relative reference links still work.
        entry = stage_root / "course-redesign-orchestrator/SKILL.md"
        before, heading, rest = entry.read_text(encoding="utf-8").partition("### Gate 1: course brief and run contract")
        if not heading:
            raise ValueError("Cannot locate course-brief handover in the shared orchestrator")
        write(entry.with_name("STAGES.md"), heading + rest)
        write(entry, before.rstrip() + "\n\nBefore confirming the course brief or resuming any later step, read the [remaining workflow](STAGES.md). Follow its rules for research, design choices, drafts, acceptance and handover.")
    intake = edition / "native-intake.md"
    if intake.is_file():
        copy_file(intake, stage_root / NATIVE_GUIDE)
        (stage_root / ROLE_GUIDE).write_bytes(link_native_intake(read_reviewed(CORE / "agent-skills" / ROLE_GUIDE)))
        starter = bundle / "SKILL.md"
        if starter.is_file():
            native_path = (stage_root / NATIVE_GUIDE).relative_to(bundle).as_posix()
            starter_text = starter.read_text(encoding="utf-8")
            write(starter, starter_text.rstrip() + f"\n\nFor the next course question, choice or preview, use [the example for this app]({native_path}).")
    if host in {"opencode", "copilot-project"}:
        for guide in stage_root.glob("*/SKILL.md"):
            guide.rename(guide.with_name("GUIDE.md"))
    copy_tree(CORE / "scripts", bundle / "scripts")
    copy_tree(CORE / "course-project-template", bundle / "assets/project-template")
    for target in ("PARTICIPANT_QUICK_START.md", "VERSION"):
        source = edition / "plugin" / NAME if host == "copilot-project" and target == "VERSION" else CORE
        copy_file(source / target, bundle / target)
        if target.endswith(".md"):
            copy_file(CORE / target, bundle / "assets" / target)
    agents_path = {
        "claude": edition / "overlay/.claude/agents",
        "opencode": edition / "overlay/.opencode/agents",
        "copilot-project": edition / "plugin" / NAME / "agents",
        "antigravity": edition / "workspace-overlay/.agents/agents"
    }[host]
    if host == "copilot-project":
        copy_tree(agents_path, output / "agents")
        return
    for source in selected_files(agents_path):
        header = read_reviewed(source).decode().replace("\r\n", "\n").split("\n---\n", 1)[0]
        if host == "claude":
            header = header.replace("skills:\n  - course-redesign", "model: inherit")
        role = tomllib.loads(read_reviewed(ROLES / (source.stem + ".toml")).decode())
        body = role["developer_instructions"].strip()
        write(output / "agents" / source.name, header + "\n---\n\n" + body)


def build(host, target):
    if target.resolve().is_relative_to(ROOT):
        raise ValueError("Choose an output directory outside the release source tree")
    if target.exists():
        raise FileExistsError(f"Choose a new output directory: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as tmp:
        prepared = Path(tmp) / "package"
        render(host, prepared)
        prepared.rename(target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host", choices=HOSTS)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    build(args.host, args.output.absolute())
