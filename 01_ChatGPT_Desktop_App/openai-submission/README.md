# OpenAI skills-only submission workspace

This directory prepares, but does not perform, a public-directory submission.

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

Build from the repository root:

```text
python openai-submission/build_skills_only_zip.py
```

This produces a local candidate archive and SHA-256 sidecar under `dist/`. A
passing local build does not mean the plugin has passed OpenAI's skill scan or
review. Do not upload until every unresolved field in
`review/LISTING_METADATA_CHECKLIST.md` is supplied and revalidated.
