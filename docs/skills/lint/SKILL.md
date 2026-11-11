---
name: lint
description: Format cave_api/, cave_app/, and cave_core/ with autoflake + black via the cave CLI. Run before running any tests and before committing Python changes. Use when asked to format, lint, clean up style, or prettify.
---

# Formatting

Run:

```sh
cave prettify
```

This schedules and runs autoflake (strips unused imports) followed by black over `cave_api/`, `cave_app/`, and `cave_core/` (see `utils/prettify.sh`) inside the background task runner. `cave_api/api.py` is excluded from unused-import stripping — it intentionally imports example/template modules that may not all be referenced at once (see the Option 1/2/3 entry-point pattern in `docs/DEVELOPMENT.md`).

---

## Detached Execution & Task Management

Like tests, code formatting runs as a task on the task runner. You can run formatting in detached background mode:

```sh
cave prettify -d
```

Active or queued prettify tasks can be monitored with `cave task list` (or `cave task -la -n 5`), and output inspected with `cave logs -t -n 50` or attached to with `cave task attach` (see [task](../task/SKILL.md)).

---

## Workflow Rule: Always Prettify Before Testing

Always run `cave prettify` before running tests (see [test](../test/SKILL.md)) and before committing any Python changes.

Running linting before testing avoids redundant test-lint-test cycles (make changes → test → prettify → test again) and saves valuable conversational tokens by ensuring tests execute directly on the clean, formatted code.

If a test fails after formatting, flag it to the user and stop — wait for further instructions before proceeding.
