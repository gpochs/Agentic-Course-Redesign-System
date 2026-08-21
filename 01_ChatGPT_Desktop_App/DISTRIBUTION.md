# Distribution and publication boundaries

## Current release state

- Current repository package and plugin release: `0.2.3`, published with
  matching archive, checksum, inventory and validation evidence; inactive by
  default and not thereby installed, activated, or scheduled.
- Public repository:
  <https://github.com/gpochs/Agentic-Course-Redesign-System>.
- GitHub repository verified public: **yes**.
- Current repository release: `v0.2.3`.
- `v0.2.1` tag, release assets and checksums remain published. The live release
  reports `immutable=false`; its attached system validation JSON names and
  hashes a v0.2.0 archive, so that attachment is not matching v0.2.1 evidence.
- `v0.2.2` tag and matching release assets: **published**. On the tested host it
  was subsequently installed and enabled at user level and passed a desktop-
  restart fresh-task picker/umbrella smoke test with all six skills. Publication
  alone did not cause that host action.
- User-level ChatGPT Desktop/Codex `0.2.2` picker smoke test: **complete on the
  tested host** — after restart, a fresh supported task loaded the installed
  cache and invoked the `@Agentic Course Redesign` umbrella; all six bundled
  skills were available. It is not evidence that v0.2.3 or another host is
  installed or loaded.
- `v0.2.3` tag and matching release assets: **published**. Exact-version host
  installation and fresh-task smoke evidence is recorded only after it occurs.
- Submitted to OpenAI: **no**.
- OpenAI safety/security scan completed: **no**.
- OpenAI review or approval: **no**.
- Published in the universal Plugins Directory: **no**.

## What the repository can enable

A verified checkout or the public GitHub repository can provide:

- the custom repo marketplace at `.agents/plugins/marketplace.json`;
- installation in Work mode or Codex in the ChatGPT desktop app when that source
  is available and workspace policy allows it;
- marketplace discovery and enablement through Codex CLI;
- source review, pinned Git refs, releases, checksums, issues, and pull requests;
- workspace-only sharing by an authorised workspace admin; and
- the portable project-template fallback.

GitHub cannot by itself create an OpenAI-reviewed public listing or certify
publisher identity, policy compliance, support readiness, or directory approval.

## Custom marketplace versus universal directory

Local and repository marketplaces are custom distribution sources and may be
private, team-scoped or public. Their availability can vary by app version,
account and workspace policy. OpenAI's universal public directory is a separate
catalog shared by ChatGPT and Codex.

For a skills-only public listing, the owner must still:

1. supply and confirm the verified individual or business publisher identity;
2. give the submitter Apps Management Write permission;
3. publish matching website, support, privacy-policy, and terms HTTPS pages;
4. choose supported countries or regions;
5. upload the final skills-only bundle through the OpenAI Platform;
6. provide starter prompts, at least five positive tests, at least three
   negative tests, release notes, and policy attestations;
7. pass skill safety/security scans and OpenAI review; and
8. after approval, explicitly publish the approved version.

The repository includes prepared review assets, but it deliberately does not
invent the publisher identity, support contact, legal URLs, territory choices,
or attestations. Those unresolved fields live only in the submission checklist,
not as fake manifest values.

## Package contents

The custom plugin and public-submission source contain six skills plus their
referenced scripts and project template. They contain no MCP server, connector,
credential, external-service entitlement, lifecycle hook, screenshot, personal
memory, or standing automation. Installation alone performs no course action.
The custom marketplace retains the pre-existing
`policy.authentication: ON_INSTALL` host install-policy metadata. It is not a
plugin/provider authentication capability or bundled credential surface, and
  v0.2.3 adds no authentication mechanism.

The v0.2.3 release custom and public-source runtime trees are byte-identical;
the public source is at
`openai-submission/source/agentic-course-redesign/`. Reviewer material is kept
outside that source at `openai-submission/review/`, so it is not accidentally
included as runtime instruction.

## Required workshop wording

Describe the current state as:

> a published v0.2.3 skills-only repository plugin with adaptive pre-source
> Gate 0A, schema 8 and terminal complete-dormant closeout, plus preserved
> v0.2.2 rollback evidence; neither release registers automation by publication

Describe either version as installed only for an exact verified host. Do not
describe either version as available in the universal Plugins Directory until
its separate submission, review and publisher publication steps are complete.

Before uploading any later release, run `validation/validate_release_evidence.py`
against the exact report and archive. Archive name/version, byte count and
SHA-256 must all match; a passing report for another archive is a failure.

## Official references

- <https://developers.openai.com/plugins/build/plugins>
- <https://developers.openai.com/plugins/deploy/connect-chatgpt>
- <https://developers.openai.com/plugins/deploy/submission>
- <https://developers.openai.com/plugins/deploy/submission-errors>
- <https://learn.chatgpt.com/docs/plugins>
