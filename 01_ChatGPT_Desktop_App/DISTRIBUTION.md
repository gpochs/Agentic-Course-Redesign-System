# Distribution and publication boundaries

## Current candidate and release state

- Current repository package and plugin release: `0.2.2`, published with
  matching archive, checksum, inventory and validation evidence; inactive by
  default and not thereby installed, activated, or scheduled.
- Public repository:
  <https://github.com/gpochs/Agentic-Course-Redesign-System>.
- GitHub repository verified public: **yes**.
- Current repository release: `v0.2.2`.
- `v0.2.1` tag, release assets and checksums remain published. The live release
  reports `immutable=false`; its attached system validation JSON names and
  hashes a v0.2.0 archive, so that attachment is not matching v0.2.1 evidence.
- `v0.2.2` tag and matching release assets: **published**. Installation and its
  fresh-task picker smoke test remain separate host actions and are not implied
  by publication.
- User-level ChatGPT Desktop/Codex `0.2.1` picker smoke test: **complete** — a
  new supported Codex task loaded the installed cache and invoked the
  `@Agentic Course Redesign` umbrella; all six bundled skills were available.
  This is historical evidence for v0.2.1 only, not evidence that v0.2.2 has
  been installed or loaded.
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

The v0.2.2 custom and public release runtime trees are kept byte-identical;
the public source is at
`openai-submission/source/agentic-course-redesign/`. Reviewer material is kept
outside that source at `openai-submission/review/`, so it is not accidentally
included as runtime instruction.

## Required workshop wording

Describe the current state as:

> a published v0.2.2 skills-only repository plugin for supported custom-
> marketplace surfaces, with an inactive-by-default template, explicit
> production handoff, HITL 3 and proposal-only system-review controls

Do not describe v0.2.2 as installed until the exact host installation and
fresh-task picker verification are complete, or as available in the universal
Plugins Directory until the separate submission, review and publication steps
are complete.

Before uploading any later release, run `validation/validate_release_evidence.py`
against the exact report and archive. Archive name/version, byte count and
SHA-256 must all match; a passing report for another archive is a failure.

## Official references

- <https://developers.openai.com/plugins/build/plugins>
- <https://developers.openai.com/plugins/deploy/connect-chatgpt>
- <https://developers.openai.com/plugins/deploy/submission>
- <https://developers.openai.com/plugins/deploy/submission-errors>
- <https://learn.chatgpt.com/docs/plugins>
