# Distribution and publication boundaries

## Current release state

- Current GitHub repository and OpenAI Plugins Directory release: `0.2.3`, published with
  matching archive, checksum, inventory and validation evidence; inactive by
  default and not thereby installed, activated, or scheduled.
- Inactive maintenance candidate: `0.2.4` under
  `ACR-SYS-20260822-007`; not committed, uploaded, published, installed,
  activated or scheduled.
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
- `v0.2.3` tag and matching release assets: **published**.
- OpenAI v0.2.3 upload, review and publisher publication: **complete**; the
  OpenAI Platform currently shows `0.2.3` as **Published** with a live
  **View in Directory** link.
- OpenAI v0.2.4 draft upload, scan/review and publication: **not started**.

## What the repository can enable

A verified checkout or the public GitHub repository can provide:

- the custom repo marketplace at `.agents/plugins/marketplace.json`;
- installation in Work mode or Codex in the ChatGPT desktop app when that source
  is available and workspace policy allows it;
- marketplace discovery and enablement through Codex CLI;
- source review, pinned Git refs, releases, checksums, issues, and pull requests;
- workspace-only sharing by an authorised workspace admin; and
- the portable project-template fallback.

GitHub cannot by itself update the separately published OpenAI listing or
certify publisher identity, policy compliance, support readiness, or directory
approval for a later version.

## Custom marketplace versus universal directory

Local and repository marketplaces are custom distribution sources and may be
private, team-scoped or public. Their availability can vary by app version,
account and workspace policy. OpenAI's universal public directory is a separate
catalog shared by ChatGPT and Codex.

For the next skills-only public version, the owner must:

1. supply and confirm the verified individual or business publisher identity;
2. give the submitter Apps Management Write permission;
3. publish matching website, support, privacy-policy, and terms HTTPS pages;
4. choose supported countries or regions;
5. use the existing plugin's **Upload** action to create a new version draft
   and upload the final skills-only bundle;
6. provide starter prompts, at least five positive tests, at least three
   negative tests, release notes, and policy attestations;
7. pass skill safety/security scans and OpenAI review; and
8. after approval, explicitly publish the approved version and verify its live
   directory version.

Do not remove or unpublish v0.2.3 before this process. The plugin-level upload
route permits a new draft while the current version stays published. Use
**Unpublish** only for a deliberate delisting or emergency rollback. The
repository includes prepared review assets, but it does not invent publisher,
support, legal, territory or attestation values for v0.2.4.

## Package contents

The custom plugin and public-submission source contain six skills plus their
referenced scripts and project template. They contain no MCP server, connector,
credential, external-service entitlement, lifecycle hook, screenshot, personal
memory, or standing automation. Installation alone performs no course action.
The custom marketplace retains the pre-existing
`policy.authentication: ON_INSTALL` host install-policy metadata. It is not a
plugin/provider authentication capability or bundled credential surface, and
neither v0.2.3 nor the inactive v0.2.4 candidate adds an authentication
mechanism.

The inactive v0.2.4 candidate custom and public-source runtime trees are kept
byte-identical;
the public source is at
`openai-submission/source/agentic-course-redesign/`. Reviewer material is kept
outside that source at `openai-submission/review/`, so it is not accidentally
included as runtime instruction.

## Required workshop wording

Describe the current state as:

> a published v0.2.3 OpenAI and GitHub skills-only plugin, plus an inactive
> v0.2.4 interaction-only candidate that asks one consequential question at a
> time and uses a card only when the live host contract can present the complete
> option set plus a custom answer. The current verified Codex contract permits
> exactly two or three explicit choices and adds free-form `Other`; Work's exact
> maximum is not independently documented or exposed here. Unknown,
> unavailable or exceeded capacity falls back to the same single ordinary-chat
> question with every valid numbered choice plus `Other`, followed by a wait;
> valid choices are never pruned, hidden or combined to fit a card, and long
> dependency-based chunks keep every option visible and under lecturer control;
> neither version registers
> automation by publication

Describe a version as installed only for an exact verified host. Describe
v0.2.3 as publicly available because its live directory entry is verified; do
not describe v0.2.4 as public until its separate update draft, checks and
publisher publication are complete.

Before uploading any later release, run `validation/validate_release_evidence.py`
against the exact report and archive. Archive name/version, byte count and
SHA-256 must all match; a passing report for another archive is a failure.

## Official references

- <https://developers.openai.com/plugins/build/plugins>
- <https://developers.openai.com/plugins/deploy/connect-chatgpt>
- <https://developers.openai.com/plugins/deploy/submission>
- <https://developers.openai.com/plugins/deploy/submission-errors>
- <https://learn.chatgpt.com/docs/plugins>
