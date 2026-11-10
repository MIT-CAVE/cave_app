---
name: add-feature
description: Implement or update a CAVE API feature (button, chart, map, slider, pane, etc.). Use when asked to add, change, or build out app functionality.
---

# Adding or Modifying a Feature

Default assumption: this is an API change in `cave_api/`, not a server change — see the layer table and escalation criteria at the top of `docs/DEVELOPMENT.md`.

---

## Locating Target Elements (Buttons, Controls, Actions)

When modifying an existing button, control, or user interaction based on a users frame of reference (e.g., "when I click that button I just clicked", "update the model button that was just used", "add a notification to the recent action"):

1. **Infer from Server Logs First**:
   - Check recent server logs using `cave logs -n 50 -a` (or `cave logs -f` if following live). 
   - Look for the `api_command` string routed through `WS RECEIVE`, custom console prints, or WebSocket events triggered by the user's interaction.
   - Trace the command back to where it is defined in `session_data` (e.g., `appBar.data.<id>.apiCommand`, `panes.data.<pane_id>.props.<prop_id>.apiCommand`, or map actions) and where it is handled in `execute_command`.

2. **Search the Codebase**:
   - Grep `cave_api/` for the inferred `api_command` name or button ID (e.g. `grep -rn '"myCommand"' cave_api/` or `grep -rn 'apiCommand' cave_api/`).
   - Identify which file owns the handler (e.g., in `cave_api/src/` or `cave_api/examples/` if running the example selector).

3. **Clarify With even a moderate level of uncertainty**:
   - If the server logs show no relevant entries, multiple commands were executed, or the request could refer to more than one UI element, ask the user to clarify which item they mean (e.g., specify its label, icon, or location in the app bar, pane, or modal).
   - Before proceeding, confirm that the inferred item / element / command matches the user's description by asking the user if they mean in plain english. EG: "Do you mean the lightbulb icon button on the app bar?" or "Are you referring to the distance slider prop in the warehouse node pane?". Just make sure you understand what they want before making more changes.

4. **Add Diagnostic Logging if Still Unclear**:
   - If the exact button or handler cannot be determined from the description or logs or from clarifications, add temporary diagnostic instrumentation to `execute_command` in `cave_api/` with print statements or inspect incoming mutation values / mutation logs (`tests/mutation_logs/`).
   - Ask the user to click the button once more.
   - Inspect the logs (`cave logs -n 20`) to capture the exact `command` string and payload.
   - Clean up any temporary diagnostic prints once the handler is identified.

---

## Workflow

1. **Locate or Define the Target**:
   - For changes to existing controls/buttons: Follow the *Locating Target Elements* guidance above to find the exact command handler.
   - For new features: Identify the relevant `session_data` top-level key(s) (`panes`, `mapFeatures`, `maps`, `groupedOutputs`, ...) — see [api-reference](../api-reference/SKILL.md) for the key table, props schema, and field docs.
2. **Find a Reference Example**:
   - Find the closest existing example in `cave_api/examples/` and use it as a reference — don't build a prop schema from memory. See the [examples](../examples/SKILL.md) skill for a categorized guide.
3. **Implement**:
   - Implement in `cave_api/src/` (or update existing command handlers) and wire into `cave_api/api.py`'s `execute_command` router.
4. **Test & Format**:
   - If the feature adds a new command, write a test first — see [add-test](../add-test/SKILL.md).
   - Run [lint](../lint/SKILL.md) (`cave prettify`) before testing to format code and strip unused imports upfront.
   - Run [test](../test/SKILL.md) — at minimum `cave test init.py`; also `cave test examples.py` if you touched `cave_api/examples/`.
5. **Diagnose & Debug**:
   - If tests fail, diagnose whether the issue is the new code, a new test, or an existing test/example — fix, run `cave prettify`, and rerun tests.
   - If something isn't rendering as expected or interactions don't trigger properly, see [debug](../debug/SKILL.md).

Report back with a summary of what changed and which tests were run.
