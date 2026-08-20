# Portable core adapter

Adapter release: `0.2.0`. Validated semantic base: `0.1.0`.

This adapter is the platform-neutral safety and workflow layer for a local,
lecturer-guided course-redesign project. It is a semantic adaptation of the
validated candidate `ACR-SYS-20260820-001` version `0.1.0`; it is not that
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

## Safe composition

1. Review the target project and this overlay without changing either.
2. Compose this overlay first and exactly one platform overlay second.
3. Treat every collision as a manual merge decision. Do not overwrite an
   existing instruction, skill, or agent file automatically.
4. Commit the reviewed files to the project repository if the repository owner
   wants them shared.
5. Copying files does not approve Gate 0, activate a reusable runtime, enable a
   schedule, authorize network use, or authorize any write to course materials.

No copy/install script is supplied intentionally: the adapter must not mutate a
project or turn itself on merely because the public repository was cloned.

## Static validation

From `02_Other_Agentic_Systems/`, validate all four adapters without invoking a
host application:

```text
python 00_Portable_Core_Adapter/validation/validate_adapters.py
```

Pass the validated canonical source root as the optional sole argument to also
recompute every recorded source SHA-256. The validator checks manifests,
root-relative inventories, the portable skill contract, all ten native role
sets, thin-wrapper references, fail-closed escalation, read-only tool or
permission declarations, absence of an executable OpenCode plugin, and private
absolute-path leakage.

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
