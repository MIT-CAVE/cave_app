---
name: data-validation
description: Run validation checks on session data dictionary objects using cave_utils Validator. Detect and fix schema errors before running the server.
---

# Data Validation with `cave_utils`

CAVE can enforce strict schema validation for `session_data` outputs. Any validation failures appear as errors/warnings on the frontend or CLI.

> [!TIP]
> To run these validations as part of automated CI/CD checks or command regression testing, see [add-test](../add-test/SKILL.md).

## Manual Validation in Tests

To check a dictionary locally, use `cave_utils.Validator`:

```python
from cave_utils import Validator

session_data = {
    "settings": {"iconUrl": "https://example.com/icon.png"},
    "panes": {...}
}

# Run the validator
validator = Validator(session_data, ignore_keys=["meta"])

# Print issues
validator.log.print_logs()

# Assert correctness
assert len(validator.log.log) == 0, "Validation failed!"
```

## Running Live Validation on the Server

To debug validation issues in real-time while using the app:

1. Open `.env` in the root of your project directory.
2. Set the environment variable:
   ```env
   LIVE_API_VALIDATION_PRINT=true
   ```
3. Run or restart the app: `cave run`
4. The terminal will print detailed, structured JSON validation reports for every command interaction.

For more details on monitoring these logs and debugging exceptions in real-time, see [debug](../debug/SKILL.md).


