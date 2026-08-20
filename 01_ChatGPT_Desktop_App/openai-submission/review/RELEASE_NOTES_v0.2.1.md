# Release notes for proposed v0.2.1 submission

Version 0.2.1 preserves the validated six-skill, lecturer-in-the-loop course
redesign workflow and its inactive-by-default project template.

This patch presents `course-redesign-orchestrator` as **Agentic Course
Redesign**, the single full-workflow umbrella entry. It routes a new course to
protected setup and an existing course to its next verified gate, so lecturers
do not have to invoke six specialist skills manually on surfaces that flatten a
skills-only plugin.

The patch also enforces portable Git line endings for deterministic manifest
validation. It adds no MCP server, connector, app, hook, credential, telemetry,
runtime activation, or schedule. Specialist skills remain directly selectable
for bounded expert tasks.
