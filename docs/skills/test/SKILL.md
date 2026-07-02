---
name: test
description: Run the cave_api test suite via the cave CLI (cave test <file>). Use when asked to run tests, verify an API change, or check that init/examples/replay logic is valid.
---

# Running Tests

Tests live in `tests/`. Do not run them directly with `python` — always go through the `cave` CLI, which runs them inside the app's Docker container:

```
cave test <test_file.py>
```

### Default available test files

| File | Purpose | When to run |
|---|---|---|
| `init.py` | Calls `execute_command` with `command="init"` and validates the output. **Primary test.** | After any `cave_api/` change |
| `examples.py` | Runs `init` on every example under `cave_api/examples/` and validates each. | After touching any file in `cave_api/examples/` |
| `database.py` | Checks DB state (a user exists and has a personal team). Server-layer only. | After Django model or auth changes |
| `replay.py` | Replays a recorded mutation log (`tests/mutation_logs/`) through `execute_command` and validates the resulting session state. | After capturing a mutation log, or to regression-test a specific session |

```
cave test init.py          # validate your app's init command (most common)
cave test examples.py      # validate all bundled examples
cave test database.py      # server-layer DB check
cave test replay.py        # replay a mutation log and validate session state
```

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
