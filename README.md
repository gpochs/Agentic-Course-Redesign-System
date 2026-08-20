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

System release candidate `0.2.1` packages the `agentic-course-redesign` plugin
`0.2.1`. The patch enforces canonical text line endings so manifest validation
works in Windows and Unix Git checkouts and adds one full-workflow umbrella
entry for picker surfaces that list bundled skills. The candidate package and
all adapters pass the recorded local release checks. Until the immutable
`v0.2.1` tag, CI run, release assets and fresh-clone validation exist, `v0.2.0`
remains the latest published release. Repository publication is separate from
OpenAI's universal Plugins Directory, where the plugin is not listed.

The shared workflow core and four project-local adapters remain at `0.2.0`:
their gate semantics and adapter contracts did not change in this patch.

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

After `v0.2.1` has been published and independently verified, app or CLI builds
that expose repository marketplaces may use this pinned public source:

```text
codex plugin marketplace add gpochs/Agentic-Course-Redesign-System --ref v0.2.1
```

Restart ChatGPT Desktop, select **Agentic Course Redesign System** in the
Plugins Directory, install **Agentic Course Redesign**, and start a new Work or
Codex task. Type `@` and choose **Agentic Course Redesign** to start or continue
the complete gated workflow. On app builds that flatten a skills-only plugin,
this label is the plugin's umbrella orchestrator skill; it routes setup and the
later specialist stages without requiring six manual selections. The tested
Codex CLI `0.118.0` did not expose this marketplace
command, so use it only when the installed build actually provides it. If the
surface does not expose custom marketplaces, use the documented
project-template fallback instead of assuming installation.

The supported installation scope is user-level within a ChatGPT Desktop/Codex
app profile. After version `0.2.1` is loaded in a new supported task, the
expected picker surface is one umbrella entry plus five direct component
entries, without copying the plugin into each course project. The package-level
checks verify that structure; a profile-specific picker smoke test is recorded
only after that profile has loaded the `0.2.1` cache in a new task. This does
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

The plugin intentionally bundles no connector, MCP server, app mapping, or
hook. Local course files and the host's approved tools are sufficient for the core
workflow; adding an unrelated connector only to alter picker presentation would
increase permissions and data-exposure risk without a documented UI guarantee.

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
