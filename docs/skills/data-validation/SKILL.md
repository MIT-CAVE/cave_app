---
name: data-validation
description: Run validation checks on session data dictionary objects using cave_utils Validator. Detect and fix schema errors before running the server.
---

# Data Validation with `cave_utils`

CAVE can enforce strict schema validation for `session_data` outputs. Any validation failures appear as errors/warnings on the frontend or CLI.

> [!TIP]
> To run these validations as part of automated CI/CD checks or command regression testing, see [add-test](../add-test/SKILL.md).

---

## 1. Manual Validation in Tests

To check a dictionary locally, use `cave_utils.Validator` inside a test file (e.g. in `tests/`):

> [!IMPORTANT]
> `cave_utils` and other project dependencies are installed exclusively inside the Docker environment. Never run `python` directly on the host machine or attempt to run `docker exec` manually. Always run validation via `cave test <test_file.py>`.

```python
from cave_utils import Validator

session_data = {
    "settings": {"iconUrl": "https://example.com/icon.png"},
    "panes": {...},
}

# Run the validator
validator = Validator(session_data, ignore_keys=["meta"])

# Print issues
validator.log.print_logs()

# Assert correctness
assert len(validator.log.log) == 0, "Validation failed!"
```

Always format and run your tests with:
```sh
cave prettify && cave test init.py
```

---

## 2. Running Live Validation on the Server

To debug validation issues in real-time while using the app:

1. Open `.env` in the root of your project directory.
2. Set the environment variable:
   ```env
   LIVE_API_VALIDATION_PRINT=true
   ```
3. Run or restart the app: `cave run`
4. The server logs will print detailed, structured validation reports for every command interaction.
5. Monitor validation logs in real time using:
   ```sh
   # Scan errors and warnings:
   cave logs -e -w

   # Inspect recent validation reports:
   cave logs -n 50
   ```

For more details on monitoring these logs and debugging exceptions in real-time, see [debug](../debug/SKILL.md).
