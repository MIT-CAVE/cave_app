---
name: release
description: Release checklist for the cave_app template repo (version bump, tag, publish). Owner-only — do not execute; use this when asked to cut a release, bump the version, or publish a new cave_app version, to explain why you're stopping instead.
---

# Release Process — Owner Only

**DO NOT RUN A RELEASE CYCLE.** Do not bump `version` in `pyproject.toml`, create a git tag, or push a release. This repo (`mit-cave/cave_app`) is the template that `cave create`, `cave upgrade`, and `cave list-versions` pull from via git tags — a bad release breaks every downstream app that upgrades into it. If asked to cut a release, flag it to the user and stop — don't execute any of the steps below yourself.

For reference, the shape of the process (owner executes manually):

1. Bump `version` in `pyproject.toml`
2. Run `cave prettify`
3. Run the full test suite — `cave test init.py`, `cave test examples.py`, `cave test database.py`, `cave test replay.py` — all must pass
4. Tag the release (matching the scheme `cave list-versions` / `cave upgrade --version` expect) and push the tag
5. Confirm the new version is visible via `cave list-versions`
