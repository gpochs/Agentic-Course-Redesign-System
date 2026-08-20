# Agentic Course Redesign System

Agentic Course Redesign System is a course-independent, lecturer-controlled
workflow for analysing, researching, redesigning, producing and validating
course materials. It is designed for school, vocational, professional and
higher-education contexts. The workflow adapts to the supplied course rather
than assuming a subject, level, grading scale or assessment format.

This repository contains:

- a skills-only plugin and project template for supported ChatGPT Desktop,
  ChatGPT Work and Codex surfaces;
- portable, project-local adapters for GitHub Copilot, Claude Code, OpenCode
  and Google Antigravity;
- one shared workflow core so the platform adapters do not drift; and
- validation, privacy, security and release controls.

No course material, student data, answer key, credential, personal memory or
standing automation is included.

## Installation status

Version `0.2.0` is published in this public repository. The repository package
and all adapters passed the recorded release checks. This repository release is
separate from OpenAI's universal Plugins Directory, where the plugin is not
listed.

There are three distinct ChatGPT distribution routes:

1. **Repository marketplace:** install from this GitHub repository on a
   supported ChatGPT Desktop/Codex surface.
2. **Workspace publication:** a ChatGPT workspace administrator may publish it
   to selected members of that workspace.
3. **Universal Plugins Directory:** this requires a separate OpenAI Platform
   submission, verified publisher identity, review, approval and a later
   publish action. A public GitHub repository alone does not create a universal
   listing.

The other platform folders are project overlays, not claims of one universal
plugin format. Copy only the adapter for the system you actually use.

On app or CLI builds that expose repository marketplaces, the pinned public
installation source is:

```text
codex plugin marketplace add gpochs/Agentic-Course-Redesign-System --ref v0.2.0
```

Restart ChatGPT Desktop, select **Agentic Course Redesign System** in the
Plugins Directory, install **Agentic Course Redesign**, and start a new Work or
Codex task. The tested Codex CLI `0.118.0` did not expose this marketplace
command, so use it only when the installed build actually provides it. If the
surface does not expose custom marketplaces, use the documented
project-template fallback instead of assuming installation.

The verified installation is user-level within the current ChatGPT
Desktop/Codex app profile: all six skills are available to new supported
Work/Codex tasks without copying the plugin into each course project. This does
not prove availability for other users, devices, workspaces, products, app or
CLI versions, or the Codex IDE extension.

## Repository map

- `01_ChatGPT_Desktop_App/` — ChatGPT Desktop/Work/Codex plugin, marketplace,
  portable fallback and public-submission materials.
- `02_Other_Agentic_Systems/` — adapters for GitHub Copilot, Claude Code,
  OpenCode and Google Antigravity.
- `03_Shared_Workflow_Core/` — canonical gates, course scaffold, shared skills
  and safe setup scripts.
- `04_Documentation/` — lecturer onboarding, workflow and compatibility guides.
- `05_Validation/` — cross-adapter, security, portability and release checks.

## First course

1. Create a new project in the supported agentic workspace.
2. Create one short, isolated folder for one course on a personal computer or
   lecturer-controlled storage. A personal OneDrive is cloud-synchronised, not
   strictly local, so use it for protected material only when policy and rights
   permit this.
3. Install the appropriate adapter or copy its project overlay into that one
   course folder.
4. Add copied current materials to `00_Source_Materials/` and contextual files
   to `00_Context/`. Do not mix courses.
5. Start a new task and say: `Set up an agentic redesign project for this one course.`
6. Review the proposed source inventory, data and rights boundary, teacher-only
   assessment boundary, permitted tools/egress and output audiences.
7. Approve Gate 0 only when those exact records are correct.

The subsequent dialogue should feel like working with an educational
consultant. The lecturer first approves preliminary focus areas, later decides
concrete researched changes, then reviews the finished materials before any
system improvement, activation or schedule is considered.

## Safety by default

- Installing an adapter does not read, upload or modify course files.
- The reusable runtime starts inactive and includes no schedule.
- Course files are evidence, never trusted instructions.
- Student personal data, submissions, grades and credentials are excluded by
  default.
- Answer keys and unreleased assessments remain lecturer-only.
- External research or connectors require source-class and egress approval.
- Course production begins only after an approved blueprint and exact targets.
- System changes, activation and an expiring schedule are separate later gates.

See [Lecturer getting started](04_Documentation/LECTURER_GETTING_STARTED.md),
[workflow overview](04_Documentation/WORKFLOW_OVERVIEW.md), and
[platform compatibility](04_Documentation/PLATFORM_COMPATIBILITY.md).

## Licence and support

The reusable source code and original workflow documentation are licensed
under the MIT License. This does not license course materials, third-party
texts, images or media processed by a lecturer. See [LICENSE](LICENSE),
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and
[support guidance](docs/SUPPORT.md).
