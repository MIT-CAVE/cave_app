---
name: api-reference
description: Reference for the CAVE API surface — the execute_command function, session_data's 10 top-level keys, the props schema for panes/map features, and how to navigate the full field-level docs in docs/cave_api_docs/. Use when building or modifying any panes, map features, charts, or session_data structure, or when you need the exact required/optional fields for a specific API construct.
---

# CAVE API Reference

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

> **Full reference:** `docs/cave_api_docs/cave_utils_api_utils_general.txt` — documents every prop type, variant, field, gradient system, and options structure. Read this before building any pane or map feature.

## Consulting `docs/cave_api_docs/` for field-level detail

The tables above tell you *which* doc file covers a given `session_data` key — this section is how to use that folder itself.

`docs/cave_api_docs/` is the full generated reference for `cave_utils`, the library that validates everything `execute_command` returns. It's plain text, one file per `cave_utils` module.

**Start here:**
1. `docs/cave_api_docs/README.txt` — index of every doc file in the folder, mapped to its `cave_utils` module path (e.g. `cave_utils.api.panes` → `./cave_utils_api_panes.txt`)
2. `docs/cave_api_docs/PROJECT_README.md` — `cave_utils` library overview (Validator, GroupsBuilder, Socket, etc.) and a quick-start for validating `session_data` directly

**Then go specific:** once you know which top-level `session_data` key you're building (from the table above), open its matching `.txt` file. Each one documents the exact required/optional fields, types, and constraints for that part of the API — **treat these as ground truth**, taking precedence over any example or README if they conflict.

**Other useful docs in the same folder:**
- `cave_utils_api_utils_general.txt` — every prop type, variant, field, gradient system, and options structure
- `cave_utils_builders_groups.txt` — `GroupsBuilder`, for constructing `groupedOutputs` chart data
- `cave_utils_socket.txt` — `Socket` methods (`notify`, `export`, ...)
- `cave_utils_arguments.txt` — `Arguments` utility

If a doc file doesn't answer the question, grep the folder — `README.txt`'s module names map directly to file names (dots become underscores, prefixed `cave_utils_`).

These `.txt` files describe the schema abstractly (fields, types, constraints) — they aren't runnable code. For a working example that already assembles a given key or prop correctly, see the [examples](../examples/SKILL.md) skill.
