# Distribution and publication boundaries

## Current release state

- Package version: `0.2.0`.
- Public repository:
  <https://github.com/gpochs/Agentic-Course-Redesign-System>.
- GitHub repository verified public: **yes**.
- Immutable `v0.2.0` tag, release assets and checksums verified: **yes**.
- User-level ChatGPT Desktop/Codex smoke test: **pass** — six skills visible
  in a new supported task.
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

The public source is kept separately at
`openai-submission/source/agentic-course-redesign/`. Reviewer material is kept
outside that source at `openai-submission/review/`, so it is not accidentally
included as runtime instruction.

## Required workshop wording

Describe this release as:

> a publicly released and locally validated v0.2.0 skills-only repository
> plugin, installable from its custom marketplace on supported ChatGPT Desktop
> Work/Codex surfaces, with a separate prepared—but not submitted—OpenAI
> directory candidate

Do not describe it as available in the universal Plugins Directory until OpenAI
has approved it and the verified publisher has published it.

## Official references

- <https://developers.openai.com/plugins/build/plugins>
- <https://developers.openai.com/plugins/deploy/connect-chatgpt>
- <https://developers.openai.com/plugins/deploy/submission>
- <https://developers.openai.com/plugins/deploy/submission-errors>
- <https://learn.chatgpt.com/docs/plugins>
