---
name: add-test
description: Add a test for a custom execute_command command, or extend replay/mutation-log regression testing. Use when asked to write a test or add test coverage for cave_api changes.
---

# Adding a Test

`tests/init.py` covers the `init` command. If your app defines additional commands, add a dedicated test file.

**Pattern** (`tests/test_<command_name>.py`):

```python
from cave_api.api import execute_command
from cave_utils import Socket, Validator

def test_<command_name>():
    init_session_data = execute_command(session_data={}, socket=Socket(), command="init")
    session_data = execute_command(session_data=init_session_data, socket=Socket(), command="<command_name>")

    validator = Validator(session_data, ignore_keys=["meta"])
    validator.log.print_logs()
    assert len(validator.log.log) == 0

if __name__ == "__main__":
    test_<command_name>()
```

Chain calls in order if a command depends on state set by a prior command (e.g. `init` populating the pane your command mutates).

> [!TIP]
> For advanced schema checks or ignoring specific keys during validation, see the [data-validation](../data-validation/SKILL.md) skill.

Run it with `cave test test_<command_name>.py` — see [test](../test/SKILL.md).

### Replay-based regression tests

To reproduce a bug or regression-test a real user session, capture a mutation log (CSV/JSON) into `tests/mutation_logs/`, then add a path assertion to `tests/replay.py`'s `test_replay` function using `Replay.get_path([...])`. The bundled example is `MutationLogExample.csv`. 

> [!NOTE]
> By default, running `cave test replay.py` only executes `test_replay` on `MutationLogExample.csv`. To run validation against every log file in the `mutation_logs/` folder at once, modify `tests/replay.py` to comment out the `test_replay(...)` call and uncomment `test_all_logs()`.

```python
from utils.replay import Replay

replay = Replay(mutation_log_file=log_file, print_on_invalid=True, raise_on_invalid=True)
replay.advance(num_steps="all", validate_each_step=False, validate_on_completion=False)
replay.validate()
value = replay.get_path(["settings", "iconUrl"])
```

`advance()` options:

| Option | Default | What it does |
|---|---|---|
| `num_steps` | `1` | Steps to advance, or `"all"` for every remaining event |
| `validate_each_step` | `False` | Validate after every event — slower, but pinpoints the exact failing event |
| `validate_on_completion` | `True` | Validate once after all steps complete |

Run it with `cave test replay.py` — see [test](../test/SKILL.md).
