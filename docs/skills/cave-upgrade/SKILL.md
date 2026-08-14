---
name: cave-upgrade
description: Upgrade the CAVE app version and assist the user with code migration, API schema updates, and testing. Use when asked to upgrade CAVE app versions, list CAVE versions, or migrate/update code for a new CAVE version.
---

# Upgrading CAVE App Versions and Migrating Code

Upgrading a CAVE application (cave_app) is a two-step process: upgrading the CAVE template framework files using the CLI, and migrating custom API code to fit the new version's schema. This skill outlines the exact workflow for managing version upgrades, handling code migrations (especially for major version changes), and verifying correctness through tests and validation.

> [!IMPORTANT]
> Template upgrades can overwrite local files and alter configuration settings. Always seek explicit user confirmation before running any upgrade commands.

---

## 1. Check Current Version

Before upgrading or checking for available updates, determine your project's currently running versions (CLI, App, Static, and Utils) using:

```bash
cave version
```

This command prints:
- **CLI Version**: The installed version of the management CLI itself.
- **CAVE App**: The template repository version for Django infrastructure.
- **CAVE Static**: The frontend static build version (loaded by browsers from CDN, or `Local`).
- **CAVE Utils**: The validation/builder Python library version.

---

## 2. List Available Versions

Use the CAVE CLI to retrieve a list of available app and static package versions. This is useful for identifying target versions to upgrade to.

```bash
cave list-versions
```
*(Shorthand: `cave lv`)*

### Common Flags:
- `--all`: Show the full history of older versions (by default, only the 5 most recent per major version are listed).
- `--pattern <glob>`: Filter the output (e.g., `cave lv --pattern v3.*` to see only v3 releases).

---

If a user specifies to update to 3.6, then simply use the most recent 3.6.x version (e.g., `v3.6.0`) for the upgrade command.

## 3. Upgrade the Framework Version

Once a version is selected or specified by the user, run the upgrade command if it is necessary.

> [!CAUTION]
> The `cave upgrade` command modifies local repository files. Make sure to ask the user to ensure that all local changes are committed or stashed before running.

```bash
cave upgrade --version <version>
```
*(e.g., `cave upgrade --version v3.6.0`)*

### Options:
- `--skip-env-upgrade`: Skip updating the project [.env](file:///home/conmak/development/app/cave_app/.env) file (useful if you want to preserve customized settings - you will need to manually update the .env file to match the updated .env_example file).
- `-y` / `--yes`: Automatically answer confirmation prompts with yes.

---

## 4. Assess Code Migration Needs

Once the template upgrade is complete (or if the user states they have already upgraded to a specific version), ask if they want help migrating their code to the new version.

Assess whether the version bump is **Minor** or **Major**:

- **Minor Version Updates** (e.g., `v3.5.0` to `v3.6.0`): These updates are backward-compatible. No API changes are typically required. Re-running the test suite if it exists is usually sufficient.
- **Major Version Updates** (e.g., `v2.4.0` to `v3.6.0`): These updates involve breaking API schema changes. You must perform a code migration to adapt [cave_api](file:///home/conmak/development/app/cave_app/cave_api/) code to the new schemas.

### Version Compatibility and Mixed Environments

An upgraded project can run mixed component versions under certain conditions:
- **Serving Older Static Versions**: A CAVE project running on `cave_app==3.6.0` can serve a prior `cave_static` major version (e.g. `2.4.0`), validated using its corresponding `cave_utils` package (e.g. `2.3.0`).
- **Validation Consistency**: In mixed environments, the reference schemas in [docs/cave_api_docs](file:///home/conmak/development/app/cave_app/docs/cave_api_docs/) are generated from the running `cave_utils` version. If the API payload passes validation against that `cave_utils` version, it is should work with that `cave_static` consumer and can be safely served by `cave_app==3.6.0`.
- **Backward Compatibility Constraints**: `cave_app` (v3.0+) only maintains backward support for the **most recent** `cave_static` version of each prior major distribution (e.g., the last release of the `2.x.x` line, which is `2.4.0`). Intermediate/older static versions within a prior major distribution (e.g., `2.3.0`) are not supported under `cave_app 3.0+`.
- **Utils to Static Alignment**: The `cave_utils` package version should closely approximate the `cave_static` version (specifically targeting the most recent equivalent minor version available) to prevent discrepancies between backend validation rules and frontend capabilities.

### Upgrading Static and Utils Independently

If you need a new feature from a newer static bundle or updated validation utilities (e.g., a new chart component or validator bug fix available in `cave_static 3.7.0` or `cave_utils 3.7.0`), you can upgrade them **without** performing a full `cave_app` Django server upgrade.

#### 1. Upgrading `cave_static` version:
To route the app to a newer static build hosted on the CDN:
  Open [.env](file:///home/conmak/development/app/cave_app/.env) and update the `STATIC_APP_URL` and `STATIC_APP_URL_PATH` variables:
  ```env
  STATIC_APP_URL='https://builds.mitcave.com'
  STATIC_APP_URL_PATH='3.7.0/index.html'
  ```
  Then, run `cave reset` to rebuild the database and apply the environment variable changes. Make sure the user is aware that this is a destructive operation that will reset the database and any local state.

#### 2. Upgrading `cave_utils` version:
To update the validation library and generation utilities:
* Open [pyproject.toml](file:///home/conmak/development/app/cave_app/pyproject.toml) and update the version string pinned in the `dependencies` list:
  ```toml
  dependencies = [
      ...
      "cave_utils==3.7.0",
      ...
  ]
  ```
* Run `cave run` to trigger a package reinstall inside the Docker container.

> [!NOTE]
> If the user has already upgraded and wants help with the migration directly, skip steps 1, 2, & 3 and immediately proceed with the migration workflow.
> It is possible that you can not determine if the version was a major or minor update.

---

## 5. Execute the Code Migration Workflow

If a migration is needed, follow this checklist to adapt custom code:

1. **Locate custom API entry points**:
   - Inspect [api.py](file:///home/conmak/development/app/cave_app/cave_api/api.py) to check which app mode is running (e.g., Option 2 template in `cave_api/src/app.py` or Option 3 custom example).
   - Review how `execute_command` is implemented and routed.

2. **Cross-reference schemas**:
   - Open [API_README.md](file:///home/conmak/development/app/cave_app/docs/API_README.md) to understand overall API changes.
   - Inspect the target schema definitions in the [docs/cave_api_docs](file:///home/conmak/development/app/cave_app/docs/cave_api_docs/) directory.
   - Check files like `cave_utils_api_utils_general.txt` for changes to prop definitions, variants, and component shapes (like sliders, selectors, etc.).

3. **Refactor custom app code**:
   - Update dictionaries returned by `execute_command` to match new schema expectations (e.g., adapting `panes`, `mapFeatures`, `maps`, or `groupedOutputs`).
   - Replace deprecated prop types or keys.
   - Update imports of `cave_utils` tools or builders if their paths changed.

4. **Regenerate API documentation files**:
   - If you have updated `cave_utils`, make sure the reference schema files under [docs/cave_api_docs](file:///home/conmak/development/app/cave_app/docs/cave_api_docs/) match the new package definitions.
   - You can regenerate these files locally by running [generate_docs.sh](file:///home/conmak/development/app/cave_app/utils/generate_docs.sh) inside the Docker container:
     ```bash
     cave run --entrypoint ./utils/generate_docs.sh
     ```
   - This executes the documentation builder in the container context and outputs the updated text files directly into your workspace.

---

## 6. Verify the Upgrade with Testing Options

Always verify the code behaves correctly after any version change or refactoring. Recommend the following testing paths to the user:

### Option A: Schema Validation with `cave test`
The fastest way to test is headlessly running the validator against your `init` output:
```bash
cave test init.py
```
This runs the test defined in [init.py](file:///home/conmak/development/app/cave_app/tests/init.py). You can also run other tests in the [tests](file:///home/conmak/development/app/cave_app/tests/) folder, such as:
- `cave test examples.py`: Validates all bundled examples.
- `cave test replay.py`: Runs replay logs to check session state regression.

See [test](file:///home/conmak/development/app/cave_app/docs/skills/test/SKILL.md) and [add-test](file:///home/conmak/development/app/cave_app/docs/skills/add-test/SKILL.md) for more detail.

### Option B: Enabling Live Validation
Enable real-time schema validation of all API outputs by setting `LIVE_API_VALIDATION_PRINT=true` in [.env](file:///home/conmak/development/app/cave_app/.env):
```env
LIVE_API_VALIDATION_PRINT=true
```
Then, boot the app via `cave run`. The server console will print detailed JSON validation reports on every API call. See [data-validation](file:///home/conmak/development/app/cave_app/docs/skills/data-validation/SKILL.md).

### Option C: Manual Validator Checks
Run a quick Python verification check using `cave_utils.Validator` on custom test payloads to debug a specific component's layout or structure:
```python
from cave_utils import Validator
validator = Validator(session_data, ignore_keys=["meta"])
validator.log.print_logs()
assert len(validator.log.log) == 0
```

### Option D: Browser DevTools Inspection
If the schema validates but the frontend goes grey or fails to render, check the browser console for runtime JavaScript errors:
- Open DevTools: `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (Mac).
- Navigate to the **Console** tab to identify component rendering issues.

