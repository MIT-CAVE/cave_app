# CAVE App Skills Directory

This directory contains specialized AI assistant skills for the CAVE development environment.

## Architecture & Symlinks

All skills in this directory are the single source of truth for all AI agent harnesses:
- `.agents/skills` is a symlink pointing to `../docs/skills/`
- `.claude/skills` is a symlink pointing to `../docs/skills/`
- `AGENTS.md` and `CLAUDE.md` in the repository root are symlinks pointing to `docs/DEVELOPMENT.md`

> [!IMPORTANT]
> **Always edit skills directly in `docs/skills/<skill-name>/SKILL.md`.**
> Never create or duplicate files inside `.agents/` or `.claude/`. Any changes in `docs/skills/` immediately propagate to all agent tools.

---

## Authoring Guidelines for New Skills

1. **Folder & File Convention**:
   - Each skill lives in its own subdirectory: `docs/skills/<skill-name>/SKILL.md`.
   - File must begin with YAML frontmatter:
     ```markdown
     ---
     name: <skill-name>
     description: <One-sentence trigger condition explaining when the agent should consult or execute this skill.>
     ---
     ```

2. **Design for Token Efficiency**:
   - Prefer commands that limit output size (e.g. `cave logs -e` for errors only, `cave logs -n 20` for tails, `cave task -la -n 10` for task lists, `cave logs -t [ID] -n 50` for task outputs).
   - Discourage commands that dump full unbuffered logs into conversation contexts without bounds.

3. **Enforce Best Practice Order**:
   - Always instruct formatting (`cave prettify`) before test execution (`cave test`) to eliminate repetitive test-prettify-retest cycles.
