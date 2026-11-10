---
name: cave-cli
description: Use the cave CLI to manage this app's Docker environment — starting the dev server, resetting the database, listing/killing containers, upgrading the template, etc. Use when asked to run, start, stop, reset, or upgrade the app, or any other Docker-lifecycle task outside of testing (see test) or formatting (see lint).
---

# The `cave` CLI

This app runs in Docker, managed entirely through the `cave` CLI — not `docker` directly. Dedicated skills exist for specialized workflows:
- [run](../run/SKILL.md) for starting the live dev server and monitoring logs
- [task](../task/SKILL.md) for inspecting and managing background tasks and the task runner
- [test](../test/SKILL.md) for running automated test suites
- [lint](../lint/SKILL.md) for code formatting (`cave prettify`)
- [debug](../debug/SKILL.md) for diagnosing server errors, task failures, and validation issues

The background task runner executes tasks (`cave test`, `cave prettify`, `cave task start`) sequentially in an isolated container environment, allowing tests and tasks to run concurrently alongside `cave run` without container or port conflicts.

> [!CAUTION]
> **No Raw Docker or Host Python Commands:**
> - **Never invoke raw `docker` or `docker compose` commands** (`docker ps`, `docker exec`, `docker run`, `docker logs`, etc.). Use the corresponding `cave` commands:
>   - Instead of `docker ps`: use `cave list`
>   - Instead of `docker logs`: use `cave logs`
>   - Instead of `docker exec <cmd>`: use `cave test <file>`, `cave prettify`, or `cave task start <cmd>`
> - **Never run project Python code or imports on the host machine**: All project dependencies (`cave_utils`, `pamda`, `django`, etc.) are installed exclusively inside Docker. Running `python` directly on the host will fail with `ModuleNotFoundError`. Always execute code and tests via `cave test <file>`, `cave prettify`, or `cave task start`.

**Flags and behavior can change between CLI versions.** The tables below are a map of what exists, not a substitute for checking. Before running an unfamiliar command, confirm its current flags with `cave <command> -h` (or `cave -h` for the full command list) rather than relying on memorized options.

---

## Safe — routine dev loop

| Command | What it does |
|---|---|
| `cave run` | Build and run the CAVE app. Add `ip:port` to host on LAN. Use `-it` to open bash inside the container, or `--all` to output raw logs instead of launching the TUI dashboard. Writes rotating server logs to `run.log` (configurable via `--log-lines LINES`, default 500, or `--no-log-history`). See [run](../run/SKILL.md). |
| `cave logs` (`cave log`) | Inspect, follow (`-f`), locate path (`-p`), clear (`-c`), or filter live server logs (`-e` errors, `-w` warnings, `-n N` tail lines). Inspect background task logs with `-t [ID]`. See [debug](../debug/SKILL.md). |
| `cave task` | Inspect, attach to, cancel, and manage background tasks and the task runner (`list`/`-l`, `list-all`/`-la`, `-n N` limit, `attach`/`-a`, `clean`, `kill`/`-k`, `stop`, `reset`). See [task](../task/SKILL.md). |
| `cave test <file>` | Run automated tests sequentially in the task runner container (supports detached mode `-d`, pytest arguments). Always run `cave prettify` before testing. See [test](../test/SKILL.md). |
| `cave prettify` | Format code with autoflake and black in the task runner container (supports detached mode `-d`). Run before tests and commits. See [lint](../lint/SKILL.md). |
| `cave list` (`-a` for full names) | List running CAVE app containers and task runner containers |
| `cave list-versions` (`cave lv`) | List available `cave_app` template versions (git tags); `--pattern` to filter, `--all` for the full history |
| `cave doctor` | Check the health of the CAVE environment (Docker, dependencies, etc.) |
| `cave version` | Print CLI version info |
| `cave theme <name>` | Set the CLI's own color theme (`dark`, `light`, `solarized`, `monokai`) — cosmetic, not app-related |
| `cave completion` (`--install`) | Generate or install shell completion script for bash/zsh |

---

## Token Efficiency Best Practices for Agents

To prevent token bloat and repetitive cycles when interacting with the CLI:

1. **Filter Server Logs**:
   - Run `cave logs -e` (errors only) or `cave logs -e -n 50` rather than streaming unbounded log outputs into chat context.
   - Use `cave logs -n 20` when inspecting recent activity.
2. **Inspect Background Tasks Non-Interactively**:
   - Limit task listings with `cave task -la -n 10`.
   - Read specific task outputs using `cave logs -t [ID] -n 50` rather than attaching interactively.
3. **Format Before Testing**:
   - Always run `cave prettify` before `cave test <file>`. Skipping this leads to a waste of execution time and tokens (code edit → test → prettify → re-test).
4. **Clean Stale Task Logs**:
   - Use `cave task clean` periodically to purge completed task logs.

---

## Destructive / State Modifying — always get explicit user confirmation before running

Every command below changes or removes local state (Docker containers/volumes, project files, or the CLI itself). Don't run any of these because a step in your own workflow seems to call for it (e.g. "tests are failing, might as well reset the DB") — state what you want to run and why, and wait for a yes.

| Command | What it does | Why it's risky |
|---|---|---|
| `cave reset` (`cave reset-db`) | Remove Docker containers and volumes, then rebuild from scratch | Wipes the local database and any container-local state |
| `cave kill [app-name]` (`-a` for all, `-t` for task server) | Stop Docker containers for a CAVE app, all apps (`-a`), or task server containers (`-t`) | Stops a dev session or task server that may be in use |
| `cave task reset` | Tear down the task server, remove task database/redis volumes, and rebuild container image | Wipes task history and task database state |
| `cave task stop` | Stop task server containers and clean up completed task logs | Terminates active task execution |
| `cave purge <app-path>` | Remove a CAVE app and all its Docker resources | Irreversible deletion of container/volume resources |
| `cave upgrade` | Upgrade the CAVE app template in the current directory to a different `--version` | Can rewrite or conflict with project files; touches `.env` unless `--skip-env-upgrade` is provided |
| `cave sync --url <url>` | Merge files from another repository into this app | Can overwrite existing files |
| `cave uninstall` | Remove the CAVE CLI itself | Removes the tool, not just app state |

---

## Setup-only — rarely relevant inside an existing app

| Command | What it does |
|---|---|
| `cave create <app-name>` | Create a brand-new CAVE app from the template repository |
| `cave update` | Update the CAVE CLI itself (not this app) |
