---
name: lint
description: Format cave_api/, cave_app/, and cave_core/ with autoflake + black via the cave CLI. Use when asked to format, lint, clean up style, prettify, or before committing Python changes.
---

# Formatting

Run:

```
cave prettify
```

This runs autoflake (strips unused imports) followed by black over `cave_api/`, `cave_app/`, and `cave_core/` (see `utils/prettify.sh`). `cave_api/api.py` is excluded from unused-import stripping — it intentionally imports example/template modules that may not all be referenced at once (see the Option 1/2/3 entry-point pattern in `docs/DEVELOPMENT.md`).

Run it before committing any Python changes. Rerun the relevant test afterward (`cave test init.py` at minimum) to confirm nothing broke. If a test fails only after formatting, flag it to the user and stop — wait for further instructions before proceeding.
