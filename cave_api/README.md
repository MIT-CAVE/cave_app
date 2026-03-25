# Cave API

The `cave_api` is the Python backend layer of every Cave app. It is where you write your model logic, run data pipelines, perform computations, and define exactly what the user sees via an API. This happens in vanilla Python. Everything else (routing, session management, WebSocket communication, and rendering) is handled automatically by the Cave framework.

## Design Philosophy

The entire API surface is a single function:

```python
def execute_command(session_data, socket, command="init", **kwargs):
    ...
    return session_data
```

You receive the current app state (`session_data`), do whatever your model needs to do, and return the updated state. The Cave App takes care of broadcasting the result to the frontend in real time. This keeps your backend logic completely decoupled from the UI. No knowledge of React, WebSockets, or HTTP is required.

## What You Can Build

The `session_data` dict you return controls everything the user sees. Depending on what keys you include, you can build:

- **Interactive maps**: plot nodes, arcs, and geographic areas with clickable props and legend controls
- **Charts and dashboards**: bar, line, scatter, and other chart types driven directly by your model outputs
- **KPI panels**: global output values displayed prominently across the app
- **Panes with input props**: sliders, dropdowns, text fields, toggles, and more that feed parameters back into your model
- **Multi-command workflows**: buttons that trigger specific actions (run model, export results, reset state, etc.)

As a developer, you only ever need to touch `cave_api`. The rest of the stack is managed for you.

---

# Related Projects

Each CAVE app depends on three supporting projects:

| Project | What it is |
|---|---|
| **cave_utils** | A Python package with validation, logging, and builder utilities. Auto-installed via `requirements.txt`. Available on [PyPI](https://pypi.org/project/cave-utils). |
| **cave_static** | A static React build that browsers load to render the app UI. The exact version your app uses is set in `.env`. Hosted on a CDN. |
| **cave_cli** | The command-line tool used to create, run, test, and manage CAVE apps. Run `cave help` to see all available commands. |

---

# Versioning

CAVE projects follow a `major.minor.patch` versioning scheme that is synchronized across `cave_app`, `cave_static`, and `cave_utils`.

- **Major** version bumps indicate breaking API changes.
- **Minor** version bumps add new features with no breaking changes.
- **Patch** version bumps are bug fixes.

This means a `cave_app 3.x.y` project is guaranteed to work with any `cave_static 3.a.b` where `a >= x` (or `a == x` and `b >= y`). You can upgrade to a newer minor version of `cave_static` (picking up new chart types, components, or UI features) without touching your API code.

To upgrade your app to a newer `cave_static` version:

1. Update `your_app/.env` with the new version.
2. In the admin page, edit the `globals.static_app_url_path` value, **or** run `cave reset` to apply the change from `.env`.

Stable `cave_static` builds are accessible via CDN at `https://builds.mitcave.com/major.minor.patch/index.html`. Stable releases do not include `-dev` in the branch name. You can see all available versions with `cave lv --repo cave_static`

> **Note:** Patch versions may not align across projects. For example, `cave_app 3.0.1` might ship alongside `cave_static 3.0.1` and `cave_utils 3.0.2` if only `cave_utils` needed a bug fix.

`cave_utils` is listed in `your_app/requirements.txt` as `cave-utils>=x.y.z`. Because Docker may cache package versions, you may occasionally need to bump this version to pull the latest patch. Use `cave lv --repo cave_utils` to see the latest version and update accordingly.

---

**Detailed API documentation:** [API Spec](https://mit-cave.github.io/cave_utils/cave_utils/api.html)

**Full set of working examples:** [cave_api/cave_api/examples](cave_api/cave_api/examples)

---

# How It Works

Everything in the Cave API flows through one function:

```python
def execute_command(session_data, socket, command="init", **kwargs):
    ...
    return session_data
```

| Parameter | What it is |
|---|---|
| `session_data` | A dict representing the full state of the app. The frontend renders whatever is in here. |
| `socket` | A communication channel to send messages or files back to the user. |
| `command` | A string indicating what action to perform. Defaults to `"init"` on first load. |

Your function receives the current app state, does whatever your model needs to do, updates the state dict, and returns it. The Cave App takes care of the rest.

The simplest possible API:

```python
def execute_command(session_data, socket, command="init", **kwargs):
    return {
        "settings": {
            "iconUrl": "https://react-icons.mitcave.com/5.4.0"
        }
    }
```

---

# Quick Start: Connecting Your Model

1. Open `my_app/cave_api/cave_api/api.py`.

2. By default it imports from the example selector. Replace that import with your own code:

    ```python
    # Before (default):
    from cave_api.cave_api.example_selector import execute_command

    # After (your model):
    from cave_api.cave_api.my_model import execute_command
    ```

    Or define `execute_command` directly in `api.py`.

3. Create `my_app/cave_api/cave_api/my_model.py` and write your function:

    ```python
    def execute_command(session_data, socket, command="init", **kwargs):
        if command == "init":
            # Run your model and build the initial app state
            results = my_model_function()
            session_data = build_app_state(results)
            return session_data
        raise Exception(f"Command '{command}' not implemented")
    ```

4. If the cave app is running, you do not need to restart it, It will reload automatically when you save any python file. If you update other files like CSVs, JSONs, package dependencies, or the Dockerfile, you will need to restart the app to see those changes. You can restart with:

    ```
    ctrl + c (to stop the app)
    cave reset (if you want to clear all session data and the database -> A fresh start)
    cave run
    ```

> **Tip:** Browse the examples in `cave_api/cave_api/examples/` to see complete working implementations for maps, charts, panes, and more.

## Walkthrough: Adding a Button to an Example

Here is a concrete end-to-end example of modifying an existing example. We will add a flag button to `api_command.py` that sends `Hello World!` to the browser.

> **Note:** Make sure `your_app/cave_api/cave_api/api.py` is importing from `cave_api.examples.example_selector`.

1. Start the app:
    ```
    cd path/to/your_app
    cave run
    ```
2. Open `http://localhost:8000/cave/` in Google Chrome and log in.
3. Click on the app page and select the `api_command.py` example from the 3-sliders menu in the top left.
4. Open `your_app/cave_api/cave_api/examples/api_command.py` and make two edits:

    **In the `if command == "init"` block**, add this key to `appBar.data`:
    ```python
    "sayHelloButton": {
        "icon": "md/MdFlag",
        "apiCommand": "sayHello",
        "type": "button",
        "bar": "lowerLeft",
    },
    ```

    **After the `elif command == "myCommand"` block** (before the final exception), add:
    ```python
    elif command == "sayHello":
        socket.notify("Hello World!")
        print("Hello World!")
        return session_data
    ```

5. Save the file. The app reloads automatically.
6. Go to the browser, jump to another example, and then back to `api_command.py` to reload the new session data.
7. You should see a new flag icon in the bottom left corner of the app. Click it to see `Hello World!` as a notification in the browser and printed in your terminal.

---

# Core Concepts

## Commands

Commands are how the frontend triggers actions in your Python code. The `command` parameter is a plain string: you define what strings you respond to.

- **`init`**: called automatically when a session starts. Always handle this. Return the full initial app state.
- **`reset`**: called when a user resets the session. Handle this the same as `init` if you want a clean slate.
- **Custom commands**: any string you define. You bind them to buttons or other UI elements in the app state dict.

```python
def execute_command(session_data, socket, command="init", **kwargs):
    if command == "init" or command == "reset":
        return build_initial_state()
    elif command == "run_model":
        results = my_model()
        return update_state(session_data, results)
    raise Exception(f"Command '{command}' not implemented")
```

To wire a button in the app bar to `"run_model"`, include this in the state you return from `init`:

```python
"appBar": {
    "order": {"data": ["runButton"]},
    "data": {
        "runButton": {
            "icon": "md/MdPlayArrow",
            "apiCommand": "run_model",
            "type": "button",
            "bar": "upperLeft",
        }
    }
}
```

## Session Data

`session_data` is a plain Python dict. It represents the complete state of the app: what pages exist, what data is shown, what the user sees. You build it in `init` and update it in response to commands.

The structure follows the [API Spec](https://mit-cave.github.io/cave_utils/cave_utils/api.html). Top-level keys include things like `settings`, `appBar`, `maps`, `panes`, `groupedOutputs`, and more. You only need to include the keys relevant to your app.

## Socket

The `socket` object lets you communicate with the user during command execution:

| Method | What it does |
|---|---|
| `socket.notify("message")` | Shows a notification in the app |
| `socket.export("data:...")` | Triggers a file download in the browser |

```python
elif command == "run_model":
    socket.notify("Running model, please wait...")
    results = my_long_running_model()
    socket.notify("Model complete!")
    return update_state(session_data, results)
```

---

# Building Chart Outputs (GroupsBuilder)

If your model produces tabular data that you want to visualize in charts, the `GroupsBuilder` is the fastest way to get there. It handles the grouping and aggregation structure that charts expect.

<details>
  <summary>Using the GroupsBuilder</summary>

  1. Import `GroupsBuilder`:
      ```python
      from cave_utils.builders.groups import GroupsBuilder
      ```

  2. Prepare your data as a list of dicts:
      ```python
      data = [
          {"continent": "North America", "country": "USA", "state": "Maine"},
          ...
      ]
      ```

  3. Create a `GroupsBuilder`:
      ```python
      group_builder = GroupsBuilder(
          group_name="Geography",
          group_data=data,
          group_parents={"continent": "country", "country": "state"},
          group_names={
              "continent": "Continents",
              "country": "Countries",
              "state": "States",
          },
      )
      ```

  4. Use it in your session data:
      ```python
      {
          "groupedOutputs": {
              "groupings": {
                  "geoGrouping": group_builder.serialize()
              },
              "data": {
                  "myMetric": {
                      ...,
                      "groupLists": {
                          "geoGrouping": group_builder.get_id_list(),
                      }
                  }
              }
          }
      }
      ```

</details>

A complete working example is at `cave_api/cave_api/examples/chart_grouped_outputs_builder.py`.

Full `GroupsBuilder` documentation: [API Spec — GroupsBuilder](https://mit-cave.github.io/cave_utils/cave_utils/builders/groups.html#GroupsBuilder)

---

# Adding Python Dependencies

Add any packages your model needs to `my_app/cave_api/requirements.txt`:

```
numpy~=1.26.0
scipy~=1.11.0
```

The next time you run `cave run`, Docker will install these automatically.

> **Note:** Do not add these to `my_app/requirements.txt` or `my_app/utils/extra_requirements.txt`: those are for the server, not the API.

<details>
  <summary>Troubleshooting package install failures</summary>

If a package fails to install (often due to a missing system-level dependency), run the app in interactive mode to diagnose:

```
cave run -it
```

Then in the container terminal:

```
pip install -r cave_api/requirements.txt
```

The error output will usually tell you what system package is missing. Once identified, add the necessary steps to your `Dockerfile` before the `pip install` line:

```dockerfile
RUN apt-get update
RUN apt-get install -y <your-dependency>
```

Then exit the container (`exit`) and run `cave run` again.

</details>

---

# Working with Data Files

If your model uses static data files (CSVs, JSON, GeoJSON, etc.), place them in `my_app/cave_api/cave_api/data/` and access them with `importlib.resources`:

```python
import json
from importlib import resources

data_folder = resources.files("cave_api.data")
data_path = data_folder.joinpath("my_data.json").__str__()

with open(data_path) as f:
    data = json.load(f)
```

Using `importlib.resources` ensures the path resolves correctly regardless of how or where the package is installed.

See `cave_api/cave_api/examples/data_local_example.py` for a full working example.

---

# Testing

Tests live in `my_app/cave_api/tests/`. The standard pattern is to call `execute_command` directly and validate the returned state using `cave_utils.Validator`:

```python
from cave_api.cave_api.my_model import execute_command
from cave_utils import Socket, Validator

session_data = execute_command(session_data={}, socket=Socket(), command="init")

validator = Validator(session_data, ignore_keys=["meta"])
validator.log.print_logs()
```

To run a test file (from your project root):

```
cave test test_init.py
```

The validator checks that your session data conforms to the API spec and prints any warnings or errors. It is the fastest way to catch structural mistakes before opening the browser.

---

# Debugging

**Print statements** are the simplest tool. Output from your API code appears in the terminal running `cave run` or `cave test`.

**Live API validation** catches structural errors in your session data automatically. Enable it in `my_app/.env`:

```
LIVE_API_VALIDATION_PRINT=true
```

This will print validation warnings to the terminal whenever `execute_command` returns.

**Running tests** is the most thorough approach:

```
cave test test_init.py
```

Add targeted test cases to `cave_api/tests/` as your app grows to cover key commands and edge cases.

**Browser console** is useful when validation passes but the app still crashes (the page goes grey and only the app bar remains). Open the browser DevTools console and look for errors:

- Mac: `Cmd + Option + i`
- Linux/Windows: `Ctrl + Shift + i`

Navigate to the **Console** tab and inspect any log output to pinpoint the issue.

---

# Further Reading

- [API Spec](https://mit-cave.github.io/cave_utils/cave_utils/api.html): full reference for all session data keys and values
- [Examples](cave_api/cave_api/examples/): 20+ working examples covering maps, charts, panes, and more
- [Custom Mapping](cave_api/custom_mapping.md): instructions for custom map tiles and coordinate systems
- [cave_utils on PyPI](https://pypi.org/project/cave-utils): the validation and builder utilities used in the API
