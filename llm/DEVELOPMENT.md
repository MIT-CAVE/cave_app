# CAVE App — LLM Developer Guide

## How to Approach Changes

**Default assumption: every feature request is an API change.**

The CAVE App is split into two layers:

| Layer | Location | Who touches it |
|---|---|---|
| **API** (your app logic) | `cave_api/cave_api/` | You, almost always |
| **Server** (Django/WebSocket infra) | `cave_core/`, `cave_app/` | Rarely, only for auth/admin/server-level needs |

When a user asks to "add a button", "show a chart", "display a map", "create a slider", "change what the app does" — that is an **API change**. It lives in `cave_api/cave_api/` and is implemented by modifying `execute_command`.

Only escalate to server-level changes if the request is clearly about:
- Django admin configuration
- Authentication or user management
- URL routing
- WebSocket session infrastructure
- Static files, templates, or deployment

If in doubt, it is an API change.

---

## The API: One Function

The entire CAVE API is a single Python function:

```python
def execute_command(session_data, socket, command="init", **kwargs):
    ...
    return session_data
```

| Parameter | Description |
|---|---|
| `session_data` | A plain dict representing the full app state. The frontend renders whatever is in here. |
| `socket` | Sends notifications (`socket.notify("msg")`) or file exports (`socket.export("data:...")`) to the user. |
| `command` | A string identifying what action to perform. Defaults to `"init"` on first load. |

`execute_command` receives the current state, modifies it, and returns it. The framework handles routing, WebSockets, and rendering automatically.

**Always handle `"init"`** — it runs on session start and must return the full initial state.

**Standard command routing pattern:**
```python
def execute_command(session_data, socket, command="init", **kwargs):
    if command == "init" or command == "reset":
        return build_initial_state()
    elif command == "run_model":
        return update_state(session_data)
    raise Exception(f"Command '{command}' not implemented")
```

---

## Session Data: 10 Top-Level Keys

`session_data` is a plain dict. The top-level keys control every part of what the user sees. All are optional except `settings`.

| Key | Purpose | Doc file |
|---|---|---|
| `settings` | App-wide settings (icon URL, sync, etc.). **Required.** | `cave_api_docs/cave_utils_api_settings.txt` |
| `appBar` | Buttons and pane-launchers in the app bar | `cave_api_docs/cave_utils_api_appBar.txt` |
| `pages` | Static info pages | `cave_api_docs/cave_utils_api_pages.txt` |
| `panes` | Slide-out panels with input props (sliders, dropdowns, etc.) | `cave_api_docs/cave_utils_api_panes.txt` |
| `maps` | Map views with viewport, projection, layers | `cave_api_docs/cave_utils_api_maps.txt` |
| `mapFeatures` | Interactive items on maps (nodes, arcs, geos) | `cave_api_docs/cave_utils_api_mapFeatures.txt` |
| `groupedOutputs` | Hierarchical chart/table data with grouping | `cave_api_docs/cave_utils_api_groupedOutputs.txt` |
| `globalOutputs` | App-wide KPI values | `cave_api_docs/cave_utils_api_globalOutputs.txt` |
| `draggables` | Draggable UI overlay elements | `cave_api_docs/cave_utils_api_draggables.txt` |
| `extraKwargs` | Special server-level flags (e.g. `wipeExisting`) | `cave_api_docs/cave_utils_api_extraKwargs.txt` |

**Minimum valid app:**
```python
return {
    "settings": {
        "iconUrl": "https://react-icons.mitcave.com/5.4.0"
    }
}
```

---

## Props: The Building Blocks for Panes and Map Features

**Props** are UI component definitions. They appear in two places:

- **Panes** — interactive controls (sliders, dropdowns, buttons, etc.) that users manipulate to drive your app
- **Map features** — visualization schemas that control how nodes, arcs, and geos are colored, sized, and labeled

Every prop is a dictionary with a `name` and a `type`. Everything else is optional.

```python
{
    "my_slider": {
        "name": "My Slider",
        "type": "num",
        "variant": "slider",
        "minValue": 0,
        "maxValue": 100,
        "unit": "%",
        "apiCommand": "run_model",   # fires execute_command with command="run_model"
        "apiCommandKeys": ["panes"],  # only pass these session_data keys
    }
}
```

### Prop Types

| Type | What it renders | Common variants |
|---|---|---|
| `"head"` | Section header / divider | `"column"`, `"row"`, `"icon"` |
| `"num"` | Numeric input | `"field"`, `"slider"`, `"icon"`, `"incslider"` |
| `"toggle"` | Boolean switch | — |
| `"text"` | Text input | `"single"`, `"textarea"` |
| `"selector"` | Selection control | `"dropdown"`, `"radio"`, `"checkbox"`, `"combobox"`, `"comboboxMulti"`, `"nested"` |
| `"button"` | Clickable button (can fire `apiCommand`) | — |
| `"date"` | Date/time picker | `"date"`, `"time"`, `"datetime"` |
| `"media"` | Image or video display | `"picture"`, `"video"` |

### Props in Panes

Panes pair a `props` schema with a `values` dict. The keys must match.

```python
"panes": {
    "data": {
        "my_pane": {
            "name": "Controls",
            "props": {
                "speed": {"name": "Speed", "type": "num", "variant": "slider", "minValue": 0, "maxValue": 10}
            },
            "values": {
                "speed": 5   # current value, keyed by prop name
            },
            "layout": {"type": "grid", "numColumns": 1, "numRows": "auto"}
        }
    }
}
```

### Props in Map Features (Nodes, Arcs, Geos)

Map features use the same `props` schema, but values live in `data.valueLists` alongside location data.

```python
"mapFeatures": {
    "data": {
        "my_nodes": {
            "type": "node",
            "name": "Facilities",
            "props": {
                "capacity": {"name": "Capacity", "type": "num", "variant": "icon"}
            },
            "data": {
                "location": {
                    "latitude": [[42.3], [41.8]],   # one list per feature
                    "longitude": [[-71.0], [-87.6]]
                },
                "valueLists": {
                    "capacity": [500, 1200]           # one value per feature
                }
            }
        }
    }
}
```

**Key distinction:**

| | Panes | Map Features |
|---|---|---|
| Values key | `values` (flat dict, one value per prop) | `data.valueLists` (list of values, one per feature) |
| Location | N/A | `data.location` (`latitude`/`longitude` for nodes/arcs; `geoJsonValue` for geos) |

> **Full reference:** `llm/cave_api_docs/cave_utils_api_utils_general.txt` — documents every prop type, variant, field, gradient system, and options structure. Read this before building any pane or map feature.

---

## API Documentation Reference

Full structured documentation for the CAVE API and all `cave_utils` modules lives in:

```
.claude/cave_api_docs/
```

**Start here:**
- `llm/cave_api_docs/README.txt` — index of all doc files
- `llm/cave_api_docs/PROJECT_README.md` — `cave_utils` library overview (Validator, GroupsBuilder, Socket, etc.)

**Consult the relevant `.txt` file when building any specific feature.** Each file documents the exact required and optional fields, types, and constraints for that part of the API. These files are the ground truth for what is valid — they take precedence over examples or README descriptions if there is a conflict.

**Other useful docs:**
- `llm/cave_api_docs/cave_utils_builders_groups.txt` — GroupsBuilder for chart data
- `llm/cave_api_docs/cave_utils_socket.txt` — Socket methods
- `llm/cave_api_docs/cave_utils_arguments.txt` — Arguments utility

---

## Entry Point: `cave_api/cave_api/api.py`

This file is the single entry point. It must define or import `execute_command`. Three options are pre-configured (comment/uncomment to switch):

- **Option 1 (default):** Example selector — browse all bundled examples from within the running app. Useful for exploration; not a coding template.
- **Option 2:** `cave_api/cave_api/src/app.py` — the minimal starting template for a real app. **Use this when building a custom app.**
- **Option 3:** Load a specific example directly for quick reference or testing.

**Recommended workflow:**
1. Use Option 1 to explore examples and understand features
2. Switch to Option 2 (`src/app.py`) to start building
3. Keep examples intact in `cave_api/cave_api/examples/` — they remain available for reference

---

## Where to Write Custom App Code

```
cave_api/cave_api/src/       ← your app lives here
cave_api/cave_api/data/      ← static data files (CSV, JSON, GeoJSON)
cave_api/requirements.txt    ← Python dependencies for your app
```

`src/app.py` is the starting template. Add modules alongside it freely (`src/model.py`, `src/charts.py`, etc.).

**Loading data files:**
```python
import json
from importlib import resources

data_folder = resources.files("cave_api.data")
with open(data_folder.joinpath("my_data.json").__str__()) as f:
    data = json.load(f)
```

**Adding dependencies:** edit `cave_api/requirements.txt` and restart with `cave run`.

---

## Examples

`cave_api/cave_api/examples/` contains 20+ working examples. They are the best reference for how to construct any specific feature. Key examples:

| Example | What it shows |
|---|---|
| `api_command.py` | Button → custom command → socket notification |
| `api_command_export.py` | Export data to browser via command |
| `map_nodes.py` / `map_arcs.py` / `map_geos.py` | Map feature types |
| `chart_grouped_outputs_builder.py` | GroupsBuilder for chart data |
| `general_props_all.py` | Every pane prop type (sliders, dropdowns, etc.) |
| `pane_wall.py` / `pane_modal.py` | Pane layout variants |
| `data_local_example.py` | Loading local CSV/JSON data |
| `kitchen_sink.py` | Comprehensive multi-feature example |

The `examples/selector/example_selector.py` file is infrastructure for the selector UI — it is not a coding example.

---

## Testing

Tests live in `cave_api/tests/`. Standard pattern:

```python
from cave_api.cave_api.src.app import execute_command
from cave_utils import Socket, Validator

session_data = execute_command(session_data={}, socket=Socket(), command="init")
validator = Validator(session_data, ignore_keys=["meta"])
validator.log.print_logs()
```

Run in Docker:
```
cave test test_init.py    # single file
cave test -all            # all tests
```

---

## Linting

Always use the Cave CLI formatter before committing:
```
cave prettify        # api code and tests only
cave prettify -all   # entire codebase
```

---

## Hot Reload

Python file changes in `cave_api/` reload automatically while `cave run` is active. Restart required for: CSV/JSON data files, `requirements.txt` changes, `Dockerfile` changes.

---

## Debugging

| Tool | How |
|---|---|
| Print statements | Output appears in the `cave run` terminal |
| Live validation | Set `LIVE_API_VALIDATION_PRINT=true` in `.env` |
| Manual validation | Run `cave test test_init.py` |
| Browser console | `Ctrl+Shift+i` → Console tab (grey screen = frontend error) |

---

## Project Structure (Full)

```
cave_api/               ← API layer (your app)
  cave_api/
    api.py              ← entry point (Option 1/2/3)
    src/                ← custom app code goes here
      app.py            ← minimal starting template
    examples/           ← 20+ reference examples (keep intact)
      selector/         ← example browser UI (infrastructure, not a template)
    data/               ← static data files
  tests/                ← test files
  requirements.txt      ← Python deps for the API

cave_core/              ← Django app: models, views, WebSockets, auth
cave_app/               ← Django project: settings, ASGI, URLs
templates/              ← Django HTML templates
static/                 ← static assets
media/                  ← user-uploaded media
utils/                  ← Cave CLI utilities (start, reset, etc.)
```

### Server-layer files (only modify for infrastructure needs)

- `cave_core/models.py` — database models and model-level logic
- `cave_core/auth.py` — authentication backends
- `cave_core/views/` — HTTP views and endpoints
- `cave_core/websockets/` — WebSocket session logic
- `cave_core/utils/` — cache, session, emailing, timing utilities
- `cave_app/` — Django project settings, ASGI, URL routing

---

## Ignore

Gitignored paths are not relevant: `__pycache__`, `venv`, `.claude`, `*.egg-info`, `build`, `dist`.
