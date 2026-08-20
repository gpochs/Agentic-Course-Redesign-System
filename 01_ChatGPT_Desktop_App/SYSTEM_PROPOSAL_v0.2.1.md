# Reusable-system patch proposal

- Proposal ID: `ACR-SYS-20260820-003`
- Proposal version: `0.2.1`
- Status: locally validated pre-publication candidate; release and picker
  evidence pending; reusable runtime remains inactive
- Base: validated and published `0.2.0`

## Approved change

Preserve the six-skill plugin and expose the existing
`course-redesign-orchestrator` as **Agentic Course Redesign**, the full-workflow
umbrella entry. It routes a new course to protected setup and an existing
course to its next verified gate. Lecturers may still select the five focused
component entries directly.

The patch also fixes deterministic cross-platform Git checkout rules. It does
not alter the shared workflow core or adapter contracts, add a connector or MCP
server, cross any lecturer approval gate, activate a runtime, or register a
schedule.

## Acceptance evidence

Acceptance requires plugin and skill validators, behavioural tests, public
scrub, deterministic archive checks, fresh Windows and Unix checkout checks,
GitHub CI, release checksum verification, and a new-task user-level Desktop
smoke test of the umbrella entry.
