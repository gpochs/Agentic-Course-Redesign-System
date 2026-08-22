# Agentic Course Redesign for GitHub Copilot

This native GitHub Copilot plugin packages the six Agentic Course Redesign
workflow skills and ten manually selected specialist agents. Its workflow
semantics mirror Agentic Course Redesign System `0.2.3`; the Copilot packaging
revision is `0.2.3-copilot.1`.

The plugin is course-independent. It adapts to a lecturer-supplied course only
after the processing-eligibility and human-approval gates permit that work.
Installing it does not inspect course files, activate a runtime, register a
schedule, or start a redesign.

## Components

- Six full workflow skills, including the umbrella orchestrator.
- Ten read-only specialist agents covering course mapping, active learning,
  AI integration, assessment alignment, student-experience review, learning
  design, materials, source verification, accessibility/visual QA, and an
  evidence-feasibility red team.
- Preview-first setup, state-validation, migration, source-manifest, and
  fingerprinting helpers.
- A Copilot-aware inactive project template.

No MCP server, connector, API integration, authentication, hook, LSP server,
telemetry, schedule, automation, model provider, or additional permission is
declared by this plugin.

## Support and cost boundary

This open-source plugin is provided free of charge and as-is under the MIT
License, without a support SLA or guaranteed maintenance. It operates inside
the participant's own GitHub Copilot environment. Normal GitHub Copilot plan,
usage, organization-policy, and account conditions remain the participant's
or their organization's responsibility. There is no publisher-operated
server, API key, authentication service, paid hosting, or telemetry.

See `PARTICIPANT_QUICK_START.md` for installation and first-session guidance.
