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
publication. The workflow therefore starts read-only, treats course content as
untrusted evidence, records exact source/access lineage, restricts writes to
approved targets, separates audiences and requires human decisions at gates.

Users remain responsible for institutional policy, lawful processing, storage,
copyright, platform permissions and reviewing executable scripts before use.

