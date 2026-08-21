# Security policy

## Supported release

Security fixes target the latest tagged release. The repository ships inactive
templates, not an autonomous service. It includes no credentials, hosted data
store, active MCP server, hook or schedule.

## Report a vulnerability

Use GitHub private vulnerability reporting if it is enabled for this
repository. Do not put credentials, personal data, student records or exploit
details in a public issue. For a non-sensitive defect, open a GitHub issue with
the affected version, platform and minimal synthetic reproduction.

## Threat model

The main risks are prompt injection in course files, unintended egress of
protected material, answer-key leakage, overly broad filesystem writes,
stale approval lineage, adapter drift, malicious dependencies and accidental
publication. The workflow therefore starts with Gate 0A before requesting or
inspecting a source path, treats course content as untrusted evidence, records
exact eligibility and source/access lineage, restricts writes to approved
targets, separates audiences and requires human decisions at gates.

In a personal or otherwise unmanaged environment, Gate 0A permits source
processing only when the lecturer has both a valid material basis—private
ownership, rightsholder authorisation or an appropriate licence/public-use
basis—and authority to process it with the selected provider. Public
availability alone is insufficient. Institution-internal or restricted
material is route-only until the exact approved environment, scope and policy
reference are confirmed. Mixed or uncertain collections fail closed.

Users remain responsible for institutional policy, lawful processing, storage,
copyright, platform permissions and reviewing executable scripts before use.
