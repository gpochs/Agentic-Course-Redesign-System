# Agentic Course Redesign for GitHub Copilot

This native GitHub Copilot plugin packages the six Agentic Course Redesign
workflow skills and ten manually selected specialist agents. Its workflow
semantics mirror Agentic Course Redesign System `0.2.4`; the Copilot semantic
adapter is `0.2.4` and the packaging revision is `0.2.4-copilot.1`.

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
- Preview-first setup, deterministic no-overwrite Gate-0A record generation,
  state-validation, migration, source-manifest, and fingerprinting helpers.
- A Copilot-aware inactive project template.

No MCP server, connector, API integration, authentication, hook, LSP server,
telemetry, schedule, automation, model provider, or additional permission is
declared by this plugin.

Every packaged skill and specialist profile follows the Copilot dialogue
contract. Keep one unresolved consequential question at a time and use the
native `ask_user` card for the complete valid option set whenever the live
GitHub Copilot host accepts it. A live Copilot host has demonstrated at least
five explicit choices plus a custom-answer field; this is an observed
capability, not a maximum. Do not state or assume an unsupported maximum. Never
prune, hide or combine valid choices merely to fit a card. If the host rejects
or cannot present the complete valid set, ask one ordinary chat question
listing every valid numbered option plus `Other`, then wait. For very long
sets, use dependency chunks only when choices share evidence or constrain one
another. Keep every valid option visible across chunks, preserve custom
answers, and let lecturers reshape the grouping. Recap chunks and gates, never
preselect a recommendation, fail closed on uncertainty, and keep exact
authority decisions separate. Blank or `Skip` never advances a gate.

For Copilot 1.0.80 BYOK, invoke the Gate-0A generator through
PowerShell/Python, not `apply_patch`. If `expected function` follows a prior
`apply_patch` entry recorded as `type=custom`, start a fresh task and prefer
GitHub-hosted GPT-5.4 or the default Claude model. This compatibility path adds
no MCP server, hook, authentication, or permission.

The preserved rollback package is `0.2.3-copilot.1`.

## Support and cost boundary

This open-source plugin is provided free of charge and as-is under the MIT
License, without a support SLA or guaranteed maintenance. It operates inside
the participant's own GitHub Copilot environment. Normal GitHub Copilot plan,
usage, organization-policy, and account conditions remain the participant's
or their organization's responsibility. There is no publisher-operated
server, API key, authentication service, paid hosting, or telemetry.

See `PARTICIPANT_QUICK_START.md` for installation and first-session guidance.
