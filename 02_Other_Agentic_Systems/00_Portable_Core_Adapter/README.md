# Portable core adapter

Adapter release: `0.2.4`. Shared semantic base: inactive candidate
`ACR-SYS-20260822-007` version `0.2.4`.

This adapter is the platform-neutral safety and workflow layer for a local,
lecturer-guided course-redesign project. It is a semantic adaptation of the
approved inactive candidate `ACR-SYS-20260822-007` version `0.2.4`; it is not that
candidate's runtime, installer, or activation mechanism.

The `overlay/` directory is laid out relative to a future project root:

```text
<project-root>/
├── AGENTS.md
└── .claude/
    └── skills/
        └── course-redesign/
            ├── SKILL.md
            └── references/
                ├── control-contract.md
                ├── role-contracts.md
                └── workflow.md
```

`AGENTS.md` is the shared always-on safety envelope. The skill holds the shared
workflow contract and uses the portable Agent Skills format. The
`.claude/skills/` location is deliberately reused because current Claude Code,
GitHub Copilot, and OpenCode documentation all describe project skill discovery
there. Platform folders beside this adapter add only native instruction and
agent wrappers.

Release `0.2.4` retains the pre-source Gate 0A processing-eligibility hard stop,
course-independent ownership and institutional-routing semantics, and schema-8
lineage vocabulary. It adds the host-neutral one-decision interaction contract,
adaptive dependency clusters with every valid option visible, a four-or-more
full-option chat fallback that leaves card mode, no pruning/hiding/combining to
fit a card, verbatim custom-answer
mapping, pre-gate recaps, and deterministic preview-first Gate-0A candidate
generation with a generic no-overwrite host fallback. After
HITL 3, silence waits; an explicit requested or declined system-improvement
response closes the course run. Only a fresh manual trigger or a separately
authorised scheduled trigger creates another run. One informational trigger-
guidance offer creates no automation. The portable overlay does not duplicate a
project state template or migration; when a composed project has control state,
use canonical schema 8 or the canonical preview-only v7-to-v8 migration before
continuing.

## Safe composition

1. Review the target project and this overlay without changing either.
2. Compose this overlay first and exactly one platform overlay second.
3. Treat every collision as a manual merge decision. Do not overwrite an
   existing instruction, skill, or agent file automatically.
4. Commit the reviewed files to the project repository if the repository owner
   wants them shared.
5. Copying files does not approve Gate 0A or Gate 0, activate a reusable
   runtime, enable a schedule, authorize network use, or authorize any write to
   course materials.

No copy/install script is supplied intentionally: the adapter must not mutate a
project or turn itself on merely because the public repository was cloned.

## Static validation

Repository maintainers can preview deterministic shared-core mirror and
manifest reconciliation without writing:

```text
python 00_Portable_Core_Adapter/validation/reconcile_adapters.py
```

After reviewing the exact mirror list, `--apply` updates only declared
Antigravity shared-core mirrors and the five adapter manifests. It never copies
an overlay into a course project, activates a runtime, or registers automation.

From `02_Other_Agentic_Systems/`, validate all four adapters without invoking a
host application:

```text
python 00_Portable_Core_Adapter/validation/validate_adapters.py
```

Pass the validated canonical source root as the optional sole argument to also
recompute every recorded source SHA-256. The validator checks manifests,
root-relative inventories, the portable skill contract, the twenty Claude Code
and OpenCode native role
sets, thin-wrapper references, fail-closed escalation, read-only tool or
permission declarations, absence of an executable OpenCode plugin, and private
absolute-path leakage. It also checks the production-handoff-before-HITL3
order, terminal dormant lifecycle, the interaction contract and Gate-0A helper
fallback, and the full post-HITL3 review offer and proposal-only authority.

Each manifest's top-level `files` array freezes every file under that adapter
root except `adapter-manifest.json` itself. The self-exclusion is explicit in
`file_inventory.manifest_self_excluded`; excluding the manifest avoids an
impossible recursive self-hash.

## Source and specification references

- [Agent Skills specification](https://agentskills.io/specification)
- [GitHub Copilot repository custom instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)
- [GitHub Copilot skills](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills)
- [Claude Code memory and project instructions](https://code.claude.com/docs/en/memory)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenCode V2 instructions](https://opencode.ai/v2/docs/instructions)
- [OpenCode V2 skills](https://opencode.ai/v2/docs/skills)

See `CAPABILITIES.md` for the deliberately narrow capability boundary and
`adapter-manifest.json` for provenance and the root-relative inventory.
