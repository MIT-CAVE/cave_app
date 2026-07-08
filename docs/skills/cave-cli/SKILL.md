---
name: cave-cli
description: Use the cave CLI to manage this app's Docker environment — starting the dev server, resetting the database, listing/killing containers, upgrading the template, etc. Use when asked to run, start, stop, reset, or upgrade the app, or any other Docker-lifecycle task outside of testing (see test) or formatting (see lint).
---

# The `cave` CLI

This app runs in Docker, managed entirely through the `cave` CLI — not `docker` directly. `cave test` and `cave prettify` have their own skills ([test](../test/SKILL.md), [lint](../lint/SKILL.md)); this skill covers everything else.

**Flags and behavior can change between CLI versions.** The tables below are a map of what exists, not a substitute for checking. Before running an unfamiliar command, confirm its current flags with `cave <command> -h` (or `cave -h` for the full command list) rather than relying on memorized options.

## Safe — routine dev loop

| Command | What it does |
|---|---|
| `cave run` | Build and run the CAVE app. Add `ip:port` to host on LAN. Use `-it` to open bash inside the container, or `--all` to output raw logs instead of launching the TUI dashboard. See [run](../run/SKILL.md). |
| `cave list` (`-a` for full names) | List running CAVE app containers |
| `cave list-versions` (`cave lv`) | List available `cave_app` template versions (git tags); `--pattern` to filter, `--all` for the full history |
| `cave doctor` | Check the health of the CAVE environment (Docker, dependencies, etc.) |
| `cave version` | Print CLI version info |
| `cave theme <name>` | Set the CLI's own color theme (`dark`, `light`, `solarized`, `monokai`) — cosmetic, not app-related |

## Destructive — always get explicit user confirmation before running

Every command below changes or removes local state (Docker containers/volumes, project files, or the CLI itself). Don't run any of these because a step in your own workflow seems to call for it (e.g. "tests are failing, might as well reset the DB") — state what you want to run and why, and wait for a yes.

| Command | What it does | Why it's risky |
|---|---|---|
| `cave reset` (`cave reset-db`) | Remove Docker containers and volumes, then rebuild from scratch | Wipes the local database and any container-local state |
| `cave kill [app-name]` (`-a` for all) | Stop Docker containers for a CAVE app, or every running CAVE app | Stops a dev session that may be in use |
| `cave purge <app-path>` | Remove a CAVE app and all its Docker resources | Irreversible |
| `cave upgrade` | Upgrade the CAVE app template in the current directory to a different `--version` | Can rewrite or conflict with project files; touches `.env` unless `--skip-env-upgrade` is provided |
| `cave sync --url <url>` | Merge files from another repository into this app | Can overwrite existing files |
| `cave uninstall` | Remove the CAVE CLI itself | Removes the tool, not just app state |

## Setup-only — rarely relevant inside an existing app

| Command | What it does |
|---|---|
| `cave create <app-name>` | Create a brand-new CAVE app from the template repository |
| `cave update` | Update the CAVE CLI itself (not this app) |
