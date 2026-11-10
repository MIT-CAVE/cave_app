# CAVE App — Developer Guide

## How to Approach Changes

**Default assumption: every feature request is an API change.**

The CAVE App is split into two layers:

| Layer | Location | Who touches it |
|---|---|---|
| **API** (your app logic) | `cave_api/` | You, almost always |
| **Server** (Django/WebSocket infra) | `cave_core/`, `cave_app/` | Rarely, only for auth/admin/server-level needs |

When a user asks to "add a button", "show a chart", "display a map", "create a slider", "change what the app does" — that is an **API change**. It lives in `cave_api/` and is implemented by modifying `execute_command`.

Only escalate to server-level changes if the request is clearly about:
- Django admin configuration
- Authentication or user management
- URL routing
- WebSocket session infrastructure
- Static files, templates, or deployment

If in doubt, it is an API change. For the concrete implementation workflow, see the [add-feature](.claude/skills/add-feature/SKILL.md) skill.


---

## Skills

> [!NOTE]
> **Skills & Documentation Architecture**:
> All skills and project documentation are stored canonically in `docs/` (`docs/skills/` and `docs/DEVELOPMENT.md`).
> The agent directories `.agents/skills` and `.claude/skills` are symlinks targeting `../docs/skills/`, and both `AGENTS.md` and `CLAUDE.md` in the repository root are symlinks to `docs/DEVELOPMENT.md`.
> **Never edit files inside `.agents/` or `.claude/` directly** — only edit files in `docs/` and all agent environments will automatically receive the updates.

| Skill | Use when |
|---|---|
| [run](.claude/skills/run/SKILL.md) | Launching the app with `cave run`, monitoring logs (`cave logs`), and verifying it's serving |
| [add-feature](.claude/skills/add-feature/SKILL.md) | Implementing a new API feature — buttons, charts, maps, sliders, panes |
| [examples](.claude/skills/examples/SKILL.md) | Picking the closest reference example in `cave_api/examples/` before writing new API code |
| [api-reference](.claude/skills/api-reference/SKILL.md) | Looking up `execute_command`, `session_data` keys, props schema, or field-level API docs |
| [test](.claude/skills/test/SKILL.md) | Running the test suite via the `cave` CLI (`cave test <file>`), running `cave prettify` first |
| [task](.claude/skills/task/SKILL.md) | Inspecting, scheduling, attaching to, cancelling, and managing background tasks and the task runner (`cave task`) |
| [add-test](.claude/skills/add-test/SKILL.md) | Adding a test for a custom command, or a replay/mutation-log regression test |
| [lint](.claude/skills/lint/SKILL.md) | Formatting `cave_api/`, `cave_app/`, `cave_core/` with `cave prettify` (run before testing or committing) |
| [debug](.claude/skills/debug/SKILL.md) | Diagnosing validation errors, live server exceptions (`cave logs -e`), task failures, or blank screens |
| [cave-cli](.claude/skills/cave-cli/SKILL.md) | Running, resetting, upgrading, or otherwise managing the app's Docker environment via the `cave` CLI |
| [cave-upgrade](.claude/skills/cave-upgrade/SKILL.md) | Upgrading the CAVE framework version via the CLI and migrating custom API/test code to the new version's schema |
| [release](.claude/skills/release/SKILL.md) | Owner-only — explains why to stop and flag instead of executing a release |


---

## The `cave` CLI

This app runs in Docker, managed entirely through the `cave` CLI. See the [cave-cli](.claude/skills/cave-cli/SKILL.md) skill for the full command reference — including which commands are destructive and require user confirmation before running.

> [!CAUTION]
> **No Raw Docker or Host Python Commands:**
> - **Never use raw `docker` or `docker compose` commands** (e.g. `docker ps`, `docker exec`, `docker run`, `docker logs`). Container lifecycle, inspection, and execution must go through the `cave` CLI (`cave list`, `cave logs`, `cave test`, `cave task`, `cave doctor`, `cave run`).
> - **Never run Python or test commands directly on the host machine** (e.g. `python -c ...`, `python tests/init.py`, `pytest`). Project dependencies (`cave_utils`, `pamda`, `django`, etc.) are installed exclusively inside the Docker environment. Running Python on the host will fail with `ModuleNotFoundError`. Always execute code and tests via the `cave` CLI (`cave test <file>`, `cave prettify`, `cave task ...`).

---
## Testing, Background Tasks & Logs

Tests live in `tests/` and run only through the `cave` CLI (`cave test <file>`) — never directly with `python`. Always run `cave prettify` (see the [lint](.claude/skills/lint/SKILL.md) skill) before running tests to prevent redundant test-lint-test cycles and save conversational tokens.

`cave test` dispatches test tasks sequentially to a dedicated background task runner, supports detached background execution (`cave test <file> -d`), and runs concurrently alongside `cave run` without container or port conflicts.

### Server Logs & Monitoring (`cave logs`)
Inspect live server logs or background task logs without interrupting running containers:
- `cave logs -e`: Scan for errors and exceptions in the running server (token-efficient).
- `cave logs -e -w`: Scan for errors and warnings.
- `cave logs -n 20`: Tail the last 20 lines of the server log.
- `cave logs -f`: Follow log output in real time (`Ctrl+C` to detach).
- `cave logs -p`: Print absolute path to the active log file (`run.log`).
- `cave logs -c`: Clear the log file before reproducing an issue.
- `cave logs -t [ID] -n 50`: Inspect task execution logs directly (e.g. latest test run or a specific task ID) non-interactively.

### Task Management (`cave task`)
Task runner lifecycle, queue inspection, log attachment, and cancellation are handled through the `cave task` command:
- `cave task list` (`-l`): View active/queued tasks
- `cave task list-all` (`-la`): View history of all tasks (use `-n <limit>` to avoid token bloat, e.g. `cave task -la -n 10`)
- `cave task attach [ID]` (`-a`): Attach to live streaming logs (`Esc` to detach, `Ctrl+C` to cancel)
- `cave task clean` (`--clean`): Clean completed task logs and remove completed tasks from registry
- `cave task kill <ID>` (`-k`): Cancel a specific task
- `cave task kill-all`: Cancel all active and queued tasks
- `cave task stop`: Stop task server containers (also `cave kill -t`)
- `cave task reset`: Reset task runner database and rebuild container image

See the [test](.claude/skills/test/SKILL.md) skill for available test files, the [task](.claude/skills/task/SKILL.md) skill for task management, [debug](.claude/skills/debug/SKILL.md) for troubleshooting with logs, and [add-test](.claude/skills/add-test/SKILL.md) for writing new command tests or replay-based regression tests.

---

## API Reference

The CAVE API is a single function, `execute_command(session_data, socket, command="init", **kwargs)`, that receives and returns a `session_data` dict built from 10 top-level keys (`settings`, `panes`, `mapFeatures`, `maps`, `groupedOutputs`, ...) and `props` (the shared schema behind every slider, dropdown, and map feature). Full details — the `execute_command` signature, the session_data key table, the props schema, and how to navigate the field-level docs in `docs/cave_api_docs/` — are in the [api-reference](.claude/skills/api-reference/SKILL.md) skill. Read it before building or modifying any panes, map features, or session_data structure.

---

## Entry Point & Custom Code

`cave_api/api.py` is the hardcoded entry point — it must define or import `execute_command`. Three options are pre-configured (comment/uncomment to switch):

- **Option 1 (default):** Example selector — browse all bundled examples from within the running app. Not a coding template.
- **Option 2:** `cave_api/src/app.py` — the minimal starting template. **Use this when building a custom app.**
- **Option 3:** Load a specific example directly for quick reference or testing.

Recommended workflow: explore with Option 1 → switch to Option 2 to start building → keep `cave_api/examples/` intact for reference throughout.

Write your app in `cave_api/src/` (add modules alongside `app.py` freely, e.g. `src/model.py`), keeping `api.py` itself as a thin router into `src/`. Put static data files in `cave_api/data/` and load them via `importlib.resources`:

```python
import json
from importlib import resources

data_folder = resources.files("cave_api.data")
with open(data_folder.joinpath("my_data.json").__str__()) as f:
    data = json.load(f)
```

Add Python dependencies under `[project.optional-dependencies.api]` in `pyproject.toml`, then (re)start with `cave run` — see [cave-cli](.claude/skills/cave-cli/SKILL.md).

---

## Examples

`cave_api/examples/` contains 25+ working examples — the best reference for how to construct any specific feature. See the [examples](.claude/skills/examples/SKILL.md) skill for a categorized guide to picking the right one before writing new API code.

---

## Hot Reload

Python file changes in `cave_api/` reload automatically while `cave run` is active. Restart required for: CSV/JSON data files, `pyproject.toml` changes, `Dockerfile` changes.

---

## Project Structure (Full)

```
cave_api/             ← API project folder (your app logic lives here)
  api.py              ← entry point (Option 1/2/3)
  src/                ← custom app code goes here
    app.py            ← minimal starting template
  examples/           ← 25+ reference examples (keep intact)
    selector/         ← example browser UI (infrastructure, not a template)
  data/               ← static data files
tests/                ← test files
  mutation_logs/      ← CSV/JSON mutation logs for replay testing

cave_core/            ← Django app: models, views, WebSockets, auth
cave_app/             ← Django project: settings, ASGI, URLs
templates/            ← Django HTML templates
static/               ← static assets
media/                ← user-uploaded media
utils/                ← server utilities (run_server.sh, reset_db.sh, etc.)
pyproject.toml        ← project dependencies (add API deps under [project.optional-dependencies.api])
Dockerfile            ← container definition
```

### Server-layer files (only modify for infrastructure needs)

- `cave_core/models/` — database models and model-level logic
- `cave_core/auth.py` — authentication backends
- `cave_core/views/` — HTTP views and endpoints
- `cave_core/websockets/` — WebSocket session logic
- `cave_core/utils/` — cache, session, emailing, timing utilities
- `cave_app/` — Django project settings, ASGI, URL routing

---

## Ignore

Gitignored paths are not relevant: `__pycache__`, `venv`, `.claude`, `*.egg-info`, `build`, `dist`.
