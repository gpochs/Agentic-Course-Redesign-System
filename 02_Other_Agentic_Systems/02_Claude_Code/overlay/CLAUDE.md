# Course-redesign bridge for Claude Code

@AGENTS.md

Use `.claude/skills/course-redesign/SKILL.md` and its references as the only
course-redesign workflow contract. The project subagents under
`.claude/agents/` are read-only specialist wrappers over those shared
contracts. Do not infer that the presence of these files activates a runtime,
authorizes a gate, permits network access, or grants a write target.

If the import or skill cannot be resolved, state that limitation and read the
project files directly. Never replace the portable safety boundary with a
weaker implicit default.

