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

```
# Always run linting before tests:
cave prettify
cave test <test_file.py>
```

## Warm Test Server, Concurrency & Queueing

- **Concurrent with `cave run`**: `cave test` runs in a dedicated test environment separate from the dev server. You can run tests while `cave run` is actively serving in the browser without container or port conflicts.
- **Warm test server (instant reruns)**: By default, the test server stays alive in the background for 10 minutes (`--keep-alive 10`) after the last test completes. Subsequent test runs start immediately without rebuilding or restarting containers.
- **Test queueing**: If multiple tests are triggered while one is running, they are queued and run sequentially.

### Test CLI Flags & Options

| Command / Flag | Purpose |
|---|---|
| `cave test <test_file.py>` | Run specified test against warm test server |
| `cave test --keep-alive <MINUTES>` | Minutes to keep test server alive after test finishes (default: `10`, `0` = stop immediately) |
| `cave test --reset <test_file.py>` | Rebuild Docker image and reinitialize database before running this test - Use this if you have made changes to the Docker image, database schema, requirements or something that would require a fresh environment |
| `cave test -c` (or `cave test cancel`) | Cancel currently running test and clear test queue |
| `cave test -k` (or `cave test kill-server`) | Cancel running test, clear test queue, and stop background test server |
| `cave test -q` / `-v` | Run in quiet mode (`-q`) or verbose debug mode (`-v`) |

### Default available test files

| File | Purpose | When to run |
|---|---|---|
| `init.py` | Calls `execute_command` with `command="init"` and validates the output. **Primary test.** | After any `cave_api/` change |
| `examples.py` | Runs `init` on every example under `cave_api/examples/` and validates each. | After touching any file in `cave_api/examples/` |
| `database.py` | Checks DB state (a user exists and has a personal team). Server-layer only. | After Django model or auth changes |
| `cache_and_session.py` | Tests cache, session state, and WebSocket broadcasting. Server-layer only. | After cache, session, or WebSocket changes |
| `replay.py` | Replays a recorded mutation log (`tests/mutation_logs/`) through `execute_command` and validates the resulting session state. | After capturing a mutation log, or to regression-test a specific session |

```
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

### Standard pattern

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
