# OpenAI skills-only submission workspace

This directory prepares, but does not perform, the v0.2.4 update to the already
published Agentic Course Redesign v0.2.3 public listing.

- `source/agentic-course-redesign/` is the single plugin root to package. It
  contains `.codex-plugin/plugin.json`, six immediate `skills/` children, and
  only the scripts, templates, and assets those skills reference.
- `review/` contains portal copy, starter prompts, reviewer cases, synthetic
  fixtures, release notes, and the owner-completion checklist. It is not part of
  the runtime plugin source.
- `build_skills_only_zip.py` creates a deterministic ZIP with one top-level
  plugin directory and no sibling members.

The source intentionally contains no `.mcp.json`, `.app.json`, `mcpServers`,
`apps`, hook payload, or screenshots. The square SVG logo and composer icon are
512 by 512 and use the image type accepted by OpenAI's current submission
validation rules.

The OpenAI Platform's existing plugin page exposes a plugin-level **Upload**
route. For the later authorised update, keep v0.2.3 published and use **Upload**
to create the v0.2.4 draft under the same plugin. Do not delete or unpublish the
old version first. **Unpublish** is a deliberate delisting control, not the
normal update step.

Build from the repository root:

```text
python openai-submission/build_skills_only_zip.py
```

This produces a local candidate archive and SHA-256 sidecar under `dist/`. A
passing local build does not mean the plugin has passed OpenAI's skill scan or
review. The current source is an inactive candidate and has not been uploaded,
published, installed or activated. Do not upload until every update check in
`review/LISTING_METADATA_CHECKLIST.md` is complete and a separate exact-version
publication decision is recorded.
