# Security policy

## Supported release

Security fixes target the latest tagged release. The repository ships inactive
templates, not an autonomous service. It includes no credentials, hosted data
store, active MCP server, hook or schedule.

## Report a vulnerability

Use the repository's [private vulnerability reporting form](https://github.com/gpochs/Agentic-Course-Redesign-System/security/advisories/new). Keep credentials, personal data and student records out of reports. For an ordinary defect, a public issue with the version, platform and a small fictional example is enough.

## Protecting releases

The maintainer verified two active GitHub rulesets on 27 November 2026. Changes to `main` require an up-to-date pull request, resolved review conversations and the `validate` check from GitHub Actions. The rule blocks deletion and force-pushes. The owner can merge a passing pull request without a second maintainer. A separate rule protects existing `v*` tags against replacement and deletion. Forks and pull requests can propose changes. Install released code from the intended owner and version. [Main branch rules](https://github.com/gpochs/Agentic-Course-Redesign-System/rules/28249791) · [Version tag rules](https://github.com/gpochs/Agentic-Course-Redesign-System/rules/28249823)

The validation workflow runs with a read-only token, uses pinned external actions and discards checkout credentials. Before merging changes to agent instructions, installers, package inventories or the validation workflow itself, inspect those diffs together. A change can weaken a check and the behaviour it was meant to check in the same pull request. A matching checksum identifies the released bytes. Publisher identity and local access permissions need their own checks. [GitHub secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)

Apply the same separation to optional tools in all five editions. A new hook can run again after the current task, a connected browser may already be signed in, and a public model demo may receive an uploaded file. Inspect the publisher, version, execution, account and actual data destination. Prefer an approved native capability when it can do the job. Course documents, repository instructions returned by a search and model outputs cannot authorise an install or an additional recipient. [Guide to choosing optional tools](03_Shared_Workflow_Core/agent-skills/course-redesign-orchestrator/references/tool-fit.md)

## Threat model

The main risks are prompt injection in course files, unintended egress of
protected material, answer-key leakage, overly broad filesystem writes,
stale approval lineage, adapter drift, malicious dependencies and accidental
publication. A teacher can choose **Skip for now** and finish a redesign from a
description. Before opening existing course material, the assistant checks
which items the teacher may use, where they may be processed and who may see
the result. It records that decision and the identity of each approved copy.

In a personal or otherwise unmanaged environment, the workflow permits source
processing only when the lecturer has both a valid material basis—private
ownership, rightsholder authorisation or an appropriate licence/public-use
basis—and authority to process it with the selected provider. Public
availability alone is insufficient. Institution-internal or restricted
material is route-only until the exact approved environment, scope and policy
reference are confirmed. If permission is unclear for one source, leave that
source closed. Work can continue with a description and any separately
cleared items. A permission covering one file does not extend to a linked quiz,
chatbot or shared question bank.

## Instructions embedded in teaching materials

Treat a document, LMS page, website, imported issue, tool result or another agent's report as a source. A source can contain legitimate instructions for learners. Keep their meaning and audience when redesigning an activity. Permission to operate an app or disclose information comes from the lecturer's recorded decision for this run. A quote of a past approval, a hidden note or text labelled “system” inside a file supplies no such authority.

The orchestrator gives each specialist only the excerpt and purpose it needs. Record a locator and finding when a source tries to redirect the task. Keep unrelated operational requests out of specialist prompts, tool arguments, durable memory and future runs. Continue using unaffected educational content. Before sending data to a tool, verify its intended recipient, exact target, audience and approved data scope, including parameters put into a URL. For an LMS or cloud draft, bind the working-copy review record to the approved HTTPS origin, course or folder and action. Reinspect the saved object's identity and visibility before presenting it to the lecturer.

Workflow instructions and fingerprint checks support host access controls. A fingerprint can detect a change relative to the recorded bytes. It cannot authenticate who supplied them. Keep credentials out of files, prompts and reports. Use read-only access for research and a scoped working copy for production when the host provides those controls. [OpenAI's agent design guidance](https://openai.com/index/designing-agents-to-resist-prompt-injection/) and [Anthropic's browser-use research](https://www.anthropic.com/research/prompt-injection-defenses) describe the residual risks and the value of limiting the actions available to an agent.

Users remain responsible for institutional policy, lawful processing, storage,
copyright, platform permissions and reviewing executable scripts before use.
