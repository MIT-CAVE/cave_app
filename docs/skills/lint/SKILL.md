---
name: lint
description: Format cave_api/, cave_app/, and cave_core/ with autoflake + black via the cave CLI. Run before running any tests and before committing Python changes. Use when asked to format, lint, clean up style, or prettify.
---

# Formatting

Run:

```
cave prettify
```

This runs autoflake (strips unused imports) followed by black over `cave_api/`, `cave_app/`, and `cave_core/` (see `utils/prettify.sh`). `cave_api/api.py` is excluded from unused-import stripping — it intentionally imports example/template modules that may not all be referenced at once (see the Option 1/2/3 entry-point pattern in `docs/DEVELOPMENT.md`).

Always run `cave prettify` before running tests (see [test](../test/SKILL.md)) and before committing any Python changes. Running linting before testing avoids redundant test-lint-test cycles (make changes → test → prettify → test again) by ensuring tests execute directly on the clean, formatted code. If a test fails after formatting, flag it to the user and stop — wait for further instructions before proceeding.
