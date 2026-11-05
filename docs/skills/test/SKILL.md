---
name: test
description: Run the cave_api test suite via the cave CLI (cave test <file>), always running cave prettify first. Use when asked to run tests, verify an API change, or check that init/examples/replay logic is valid.
---

# Running Tests

Tests live in `tests/`. Do not run them directly with `python` — always go through the `cave` CLI, which runs them inside the app's Docker container.

> [!IMPORTANT]
> **Always run linting before tests:** Run [lint](../lint/SKILL.md) (`cave prettify`) before running any tests. Workflows frequently make changes, run tests, run `cave prettify`, and then have to run tests again. Running `cave prettify` first ensures code formatting and unused import cleanup are applied upfront, avoiding redundant test cycles.
>
> Running `cave test` without specifying a test file will result in a `Test not found` error. You must always pass a test file.

```sh
# Always run linting before tests:
cave prettify
cave test <test_file.py>
```

## Task Runner, Concurrency & Detached Execution

- **Dedicated Task Runner**: `cave test` runs tests sequentially as tasks inside a dedicated background task runner container.
- **Concurrent with `cave run`**: The task runner operates in an isolated environment separate from the dev server. You can run tests while `cave run` is actively serving in the browser without container or port conflicts.
- **Sequential Queueing**: If multiple tests or tasks are scheduled, they queue and run in sequence.
- **Detached Execution (`-d` / `--detached`)**: By default, `cave test` attaches to test output and streams logs. Pass `-d` to run the test in the background and return immediately:
  ```sh
  cave test init.py -d
  ```
- **Live Attachment**: Use `cave task attach` to view logs for running tests. While attached, press `Esc` to detach (test keeps running in the background) or `Ctrl+C` to cancel the test.

---

## Test CLI Flags & Options

| Command / Flag | Purpose |
|---|---|
| `cave test <test_file.py>` | Run specified test file sequentially in the task runner |
| `cave test -d` / `--detached` | Run test task in detached background mode |
| `cave test -v` / `-q` | Verbose debug output (`-v`) or quiet mode (`-q`) |
| `cave test --loglevel <LEVEL>` | Set log level: `DEBUG`, `INFO`, `WARN`, `ERROR`, `SILENT` |
| `cave test -y` / `--yes` | Automatically answer confirmation prompts with yes |
| `cave test --docker-args <ARGS>` | Additional arguments to pass to `docker run` |
| `[remaining ...]` | Additional test files or pytest arguments |

---

## Managing Tests & The Task Runner via `cave task`

Queue inspection, cancellation, stopping, and resetting are managed through the [task](../task/SKILL.md) command:

| Goal | Command |
|---|---|
| View active test queue & status | `cave task list` (or `cave task -l`) |
| View test history (active, completed, failed) | `cave task list-all` (or `cave task -la`) |
| Attach to running test logs | `cave task attach [ID]` (or `cave task -a [ID]`) |
| Cancel a running or queued test | `cave task kill <ID>` (or `cave task -k <ID>`) |
| Cancel all queued and running tests | `cave task kill-all` (or `cave task --kill-all`) |
| Stop background task server | `cave task stop` (or `cave task --stop`, `cave kill -t`) |
| Reset & rebuild task environment | `cave task reset` (or `cave task --reset`) |

> [!NOTE]
> Previously, flags like `--reset`, `-c`, and `--keep-alive` were attached directly to `cave test`. These have been superseded by `cave task` commands (`cave task reset`, `cave task kill-all`, `cave task stop`).

---

## Default Available Test Files

| File | Purpose | When to run |
|---|---|---|
| `init.py` | Calls `execute_command` with `command="init"` and validates the output. **Primary test.** | After any `cave_api/` change |
| `examples.py` | Runs `init` on every example under `cave_api/examples/` and validates each. | After touching any file in `cave_api/examples/` |
| `database.py` | Checks DB state (a user exists and has a personal team). Server-layer only. | After Django model or auth changes |
| `cache_and_session.py` | Tests cache, session state, and WebSocket broadcasting. Server-layer only. | After cache, session, or WebSocket changes |
| `replay.py` | Replays a recorded mutation log (`tests/mutation_logs/`) through `execute_command` and validates the resulting session state. | After capturing a mutation log, or to regression-test a specific session |

```sh
# Example test runs (preceded by linting):
cave prettify
cave test init.py          # validate your app's init command (most common)
cave test examples.py      # validate all bundled examples
cave test database.py      # server-layer DB check
cave test cache_and_session.py # server-layer cache & session check
cave test replay.py        # replay a mutation log and validate session state
```

> [!TIP]
> **Fast Single-Example Testing**: Validating all bundled examples via `cave test examples.py` tests 25+ files. When actively iterating on a single example, uncomment it under Option 3 in `cave_api/api.py` and run `cave prettify && cave test init.py` to validate only that file in seconds. Run `cave test examples.py` for full regression coverage once finished.

---

## Standard Pattern

`tests/init.py` ships configured to match whatever you are seeing in your live application:

```python
from cave_api.api import execute_command
from cave_utils import Socket, Validator

def test_init():
    init_session_data = execute_command(session_data={}, socket=Socket(), command="init")

    validator = Validator(init_session_data, ignore_keys=["meta"])
    validator.log.print_logs()
    assert len(validator.log.log) == 0

if __name__ == "__main__":
    test_init()
```

For command-specific tests beyond `init`, or extending replay coverage, see [add-test](../add-test/SKILL.md).
