---
name: add-feature
description: Implement a new CAVE API feature (button, chart, map, slider, pane, etc.). Use when asked to add, change, or build out app functionality.
---

# Adding a Feature

Default assumption: this is an API change in `cave_api/`, not a server change — see the layer table and escalation criteria at the top of `docs/DEVELOPMENT.md`.

Workflow:

1. Identify the relevant `session_data` top-level key(s) (`panes`, `mapFeatures`, `maps`, `groupedOutputs`, ...) — see [api-reference](../api-reference/SKILL.md) for the key table, the props schema, and how to find the matching doc in `docs/cave_api_docs/`.
2. Find the closest existing example in `cave_api/examples/` and use it as a reference — don't build a prop schema from memory. See the [examples](../examples/SKILL.md) skill for a categorized guide to picking one.
3. Implement in `cave_api/src/` (add a module alongside `app.py` if needed) and wire it into `cave_api/api.py`'s `execute_command` router.
4. If the feature adds a new command, write a test first — see [add-test](../add-test/SKILL.md).
5. Run [test](../test/SKILL.md) — at minimum `cave test init.py`; also `cave test examples.py` if you touched `cave_api/examples/`.
6. If tests fail, diagnose whether the issue is the new code, a new test, or an existing test/example — fix and rerun.
7. Once tests pass, run [lint](../lint/SKILL.md) (`cave prettify`).
8. If something isn't rendering as expected, see [debug](../debug/SKILL.md).

Report back with a summary of what changed and which tests were run.
