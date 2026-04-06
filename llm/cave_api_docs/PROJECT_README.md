# Cave Utilities

[![PyPI version](https://badge.fury.io/py/cave_utils.svg)](https://badge.fury.io/py/cave_utils)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python utilities for the [CAVE App](https://github.com/MIT-CAVE/cave_app) framework: API validation, data builders, and shared helpers.

## Overview

`cave_utils` is a foundational library for building CAVE applications. It provides:

- **API validation**: validate `session_data` dicts against the full CAVE API spec, with structured error and warning reporting
- **Data builders**: helper classes for constructing hierarchical and date-based group structures
- **Shared utilities**: logging, geographic calculations, coordinate systems, and argument parsing

It is designed to be embedded in a CAVE API server, but can also be used standalone for testing and data development.

## Features

- Validates all 10 top-level CAVE API keys (`settings`, `appBar`, `pages`, `panes`, `maps`, `mapFeatures`, `globalOutputs`, `groupedOutputs`, `draggables`, `extraKwargs`)
- Cross-field validation with structured error paths (e.g. `maps.data.myMap.currentProjection`)
- Time-series (`timeValues`) and ordering (`order`) validation built in
- `GroupsBuilder` and `DateGroupsBuilder` for constructing hierarchical group structures from flat data
- `GeoUtils` for shortest-path calculations over geographic networks
- `CustomCoordinateSystem` for converting Cartesian 2D/3D coordinates to lat/long
- Runtime type enforcement via [`type_enforced`](https://github.com/connor-makowski/type_enforced)

## Requirements

- Python ≥ 3.11

## Installation

```sh
pip install cave_utils
```

## Quick Start

### Validating Session Data

```python
from cave_utils import Validator

session_data = {
    "settings": {
        "iconUrl": "https://example.com/icon.png",
    },
    "appBar": {
        "data": {
            "btn_home": {
                "icon": "md/MdHome",
                "type": "button",
            }
        }
    },
}

result = Validator(session_data=session_data)

# Inspect errors and warnings
for entry in result.log.log:
    print(entry)
# Empty list means fully valid
```

### Using GroupsBuilder

```python
from cave_utils.builders.groups import GroupsBuilder

builder = GroupsBuilder(
    data=[
        {"id": "region_east", "name": "East", "parent": None},
        {"id": "state_ny", "name": "New York", "parent": "region_east"},
        {"id": "state_ma", "name": "Massachusetts", "parent": "region_east"},
    ],
    id_field="id",
    name_field="name",
    parent_field="parent",
)

# Serialize to the CAVE API groupedOutputs format
groups_data = builder.serialize()
```

## Public API

| Class | Import | Description |
|---|---|---|
| `Validator` | `from cave_utils import Validator` | Validates a `session_data` dict against the full CAVE API spec |
| `LogObject` | `from cave_utils import LogObject` | Structured log container for errors and warnings |
| `Socket` | `from cave_utils import Socket` | No-op WebSocket stub for use in tests |
| `Arguments` | `from cave_utils import Arguments` | Parses kwargs, flags, and positional args from raw argument lists |
| `GeoUtils` | `from cave_utils import GeoUtils` | Geographic utilities including shortest-path via `scgraph` |
| `CustomCoordinateSystem` | `from cave_utils import CustomCoordinateSystem` | Converts 2D/3D Cartesian coordinates to lat/long |

Full API reference: [mit-cave.github.io/cave_utils](https://mit-cave.github.io/cave_utils/index.html)

## LLM Docs

`cave_utils` can generate plain text documentation for all its modules, suitable for use with AI assistants (Claude, Gemini, etc.).

**From Python:**
```python
from cave_utils import generate_docs
generate_docs("path/to/output_dir")
```

**From the command line:**
```sh
cave-utils-docs path/to/output_dir
```

If no directory is specified, docs are written to `./cave_utils_docs/`.

The output directory will contain one `.txt` file per module plus a `README.txt` index and a `PROJECT_README.md` with this project overview. You can point your AI assistant at this directory or reference individual files in a `CLAUDE.md` / system prompt.

## Development

All development tasks run inside Docker. Make sure Docker is installed and running.

| Command | Description |
|---|---|
| `./run.sh` | Drop into an interactive Docker shell |
| `./run.sh test` | Run all tests |
| `./run.sh prettify` | Format code with autoflake + black |
| `./run.sh docs` | Regenerate pdoc documentation |

> `./run.sh` requires a TTY. Run it directly in your terminal, not from a non-interactive CI environment.

### Running Tests

Tests live in `test/`. The main test file (`test_validator.py`) imports every example in `test/api_examples/`, runs it through `Validator`, and asserts no errors or warnings are produced. Unit tests exist for each module.

```sh
./run.sh test
```

### Hot-Reload with a Cave App

To develop `cave_utils` against a running Cave App, mount the local source as a Docker volume:

```sh
cave run --docker-args "--volume {local_path_to_cave_utils}/cave_utils:/cave_utils"
```

Then in the Cave App's `utils/run_server.sh`, add `pip install -e /cave_utils` before the server starts. Changes to `cave_utils` source will be reflected on the next API call without rebuilding the container.

Set `LIVE_API_VALIDATION_PRINT=True` in the Cave App's `.env` to see validation output on every API command.

## Release Process

1. Ensure all tests pass (`./run.sh test`) and code is formatted (`./run.sh prettify`)
2. Update `version` in both `pyproject.toml` and `setup.cfg`
3. Update the version in `utils/docs.sh` and regenerate docs (`./run.sh docs`)
4. Build and publish:
    ```sh
    python3 -m virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
