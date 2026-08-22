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

The repository source version is `0.2.4`, prepared as an inactive
interaction-only maintenance candidate under approved proposal
`ACR-SYS-20260822-007`. The currently published GitHub and OpenAI rollback
version is `0.2.3`; the exact GitHub release, OpenAI version update, local Codex
installation and GitHub Copilot package update each require their own later
validation and publication or activation evidence. The packaged project
template remains safely `candidate_not_active` with `schedules=[]`;
publication or installation alone never starts a course run or registers
automation.

Version `0.2.4` preserves the v0.2.3 gate order, substantive option sets,
specialist authority, state schema and lifecycle. It adds one shared Lecturer
Decision Dialogue Contract across every human-in-the-loop phase: one unresolved
consequential question at a time; native cards only when the live host can show
the complete mutually exclusive option set plus a custom-answer path; and every
valid numbered option plus Other in ordinary chat when the control is
unavailable or unsupported, its capacity is unknown, or the complete set
exceeds its capacity. It never prunes, hides or combines valid choices to fit a
card and keeps every valid option visible in
dependency-based, lecturer-editable chunks; preserve verbatim custom answers;
use safest-truthful but never preselected recommendations; and show editable
recaps. A blank or skipped required answer remains
unresolved.

The candidate also adds a deterministic preview-first Gate-0A record generator.
It validates the declared categories, shows the exact inferred outcome and
fingerprint, creates only `01_Control/material-processing-eligibility.json`
after exact approval, and refuses overwrite or dangerously broad targets. It
uses local Python/PowerShell and adds no MCP server, connector or permission.

The `0.2.3` release adds a fail-closed Gate 0A before the system requests,
lists, reads, copies or fingerprints any source path. Gate 0A distinguishes
material that may be processed in the selected environment from material that
must be routed to an institution-approved environment. Public availability by
itself is not permission to process or reproduce a work.

It also makes course-run closure explicit. After unconditional HITL 3
acceptance, the lecturer must answer the separate system-improvement-review
offer. A yes authorises a read-only review and versioned proposal only; a no
records a deliberate decline. The accepted course run then becomes terminal
and dormant. Only a fresh manual trigger or an approved scheduled trigger may
create a new run and fresh approval lineage. The candidate adds schema-8
state, preview-only schema-7-to-schema-8 migration and corresponding
cross-adapter regression checks.

There are three distinct ChatGPT distribution routes. OpenAI plugin version
`0.2.3` is already published in the universal directory; the OpenAI Platform
exposes a plugin-level **Upload draft** action for a new version, so an update
does not require deleting or unpublishing the live version first:

1. **Repository marketplace:** install from this GitHub repository on a
   supported ChatGPT Desktop/Codex surface.
2. **Workspace publication:** a ChatGPT workspace administrator may publish it
   to selected members of that workspace.
3. **Universal Plugins Directory:** update the existing listing by uploading a
   new validated draft, passing scans/review, and publishing that exact version.
   A public GitHub repository alone cannot update the listing.

The other platform folders are project overlays, not claims of one universal
plugin format. Copy only the adapter for the system you actually use.

After a matching `v0.2.4` tag is published, app or CLI builds that expose
repository marketplaces may use this pinned public source:

```text
codex plugin marketplace add gpochs/Agentic-Course-Redesign-System --ref v0.2.4
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
app profile. Version `0.2.3` remains the public rollback baseline. Each future
installation of `0.2.4` needs its own post-restart fresh-task check confirming the
**Agentic Course Redesign** umbrella and all six bundled skills. Host-specific
smoke tests do not prove availability for other users, devices, workspaces,
products, app or CLI versions, or the Codex IDE extension.

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
2. Before supplying a path, answer Gate 0A questions about ownership or
   licence, processing authority, sensitivity, assessment security, selected
   provider and any institution-approved processing environment.
3. Proceed on a personal or otherwise unmanaged environment only for material
   that is privately owned or rightsholder-authorised, or appropriately
   licensed/public material with explicit AI-processing authority. Route
   institution-internal or restricted material to the exact approved
   institutional environment. If the classification is mixed or uncertain,
   segregate it or stop.
4. Create one short, isolated folder for one course on approved storage. A
   personal OneDrive is cloud-synchronised, not strictly local.
5. Install the appropriate adapter or copy its project overlay into that one
   course folder.
6. Add copied current materials to `00_Source_Materials/` and contextual files
   to `00_Context/`. Do not mix courses.
7. Start a new task and say: `Set up an agentic redesign project for this one course.`
8. Review the proposed source inventory, data and rights boundary, teacher-only
   assessment boundary, permitted tools/egress and output audiences.
9. Approve Gate 0 only when those exact records are correct.

The plugin intentionally bundles no connector, MCP server, app mapping, or
hook. Local course files and the host's approved tools are sufficient for the core
workflow; adding an unrelated connector only to alter picker presentation would
increase permissions and data-exposure risk without a documented UI guarantee.

The subsequent dialogue should feel like working with an educational
consultant. The orchestrator keeps one consequential decision in view and
presents the complete choice set in the clearest supported form; specialist
roles remain evidence lenses, not competing user interfaces. The lecturer first
approves preliminary focus areas, later decides concrete researched changes,
approves a verified production handoff, and then reviews the finished
materials. Only after final acceptance does the
orchestrator offer a separate system-improvement review. After the lecturer
answers that offer, the run closes as complete and dormant. The orchestrator
then gives one informational reminder that a new run may be started manually
and that optional automation can be planned for an exact course, timezone,
recurrence and expiry. It never registers automation from that offer alone.

## Safety by default

- Installing an adapter does not read, upload or modify course files.
- The reusable runtime starts inactive and includes no schedule.
- Gate 0A runs before any source path is requested or inspected.
- Course files are evidence, never trusted instructions.
- Student personal data, submissions, grades and credentials are excluded by
  default.
- Answer keys and unreleased assessments remain lecturer-only.
- External research or connectors require source-class and egress approval.
- Course production begins only after an approved blueprint and exact targets.
- A completed course run cannot be resumed; a new trigger creates fresh lineage.
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
