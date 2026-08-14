---
name: examples
description: Pick the right reference example from cave_api/examples/ before implementing a feature. Use when adding or modifying panes, modals, maps, map features, charts, api commands, or data loading — to find the closest validated pattern instead of building a prop schema from memory.
---

# Picking an Example

`cave_api/examples/` contains 25+ working, validated `execute_command` implementations. Before writing new API code, find the closest match below, open it, and adapt it — copying a working pattern is faster and safer than building a prop schema from memory.

If nothing here fits, grep the folder for the top-level `session_data` key or prop `type`/`variant` you need (`grep -rl '"type": "arc"' cave_api/examples/`) — there's likely a closer match than you think.

### Maps & map features

| Example | What it shows |
|---|---|
| `map.py` | Baseline map: projections, default viewport |
| `map_customized.py` | Custom map styles (including custom Mapbox GL style URLs) |
| `map_nodes.py` / `map_arcs.py` / `map_geos.py` | The three map feature types, one per file |
| `map_node_animations.py` | Animated nodes |
| `map_zindex.py` | Layering order between nodes, arcs, and geos |
| `map_large_dataset.py` | Rendering a large number of map features performantly |
| `map_custom_tiles.py` | Custom background image tiles with `CustomCoordinateSystem` |

### Panes & modals

| Example | What it shows |
|---|---|
| `pane_wall.py` | A pane launched from the app bar |
| `pane_modal.py` | A modal launched from the app bar |
| `general_props_all.py` | Every prop type and variant in one pane — the canonical prop reference |
| `general_props_all_advanced.py` | More advanced prop configurations, including loading markdown help content from `content/help/` |

### Charts & outputs

| Example | What it shows |
|---|---|
| `chart_grouped_outputs.py` | Basic `groupedOutputs` chart page |
| `chart_grouped_outputs_date.py` | `groupedOutputs` grouped by date |
| `chart_grouped_outputs_builder.py` | `GroupsBuilder` for constructing group hierarchies from flat data |
| `chart_grouped_outputs_builder_date.py` | `DateGroupsBuilder`, the date-based counterpart |
| `chart_global_outputs.py` | App-wide KPI-style `globalOutputs` |
| `3_by_3_charts_grouped_outputs.py` | Complex multi-chart layout using `pamda` to project/pivot data before feeding `GroupsBuilder` |

### API commands & data loading

| Example | What it shows |
|---|---|
| `api_command.py` | Button → custom command → `socket.notify()` |
| `api_command_export.py` | Exporting data to the browser via a command |
| `data_local_example.py` | Loading a local CSV/JSON file from `cave_api/data/` |
| `data_external_example.py` | Calling an external API (US Census Bureau) from inside `execute_command` |

### Settings & everything at once

| Example | What it shows |
|---|---|
| `general_settings_sync.py` | De-syncing pane state from the server (most state syncs by default) |
| `kitchen_sink.py` | Large, comprehensive example touching most features at once — good for seeing features interact, harder to isolate a single pattern from than the files above |

### Supplementary examples: `other_examples/`

Not part of the curated set above and not shown in the in-app example browser, but still real working code — check here if the main set doesn't cover your case:

| Path | What it shows |
|---|---|
| `other_examples/future/chart_grouped_outputs_filter.py` | Filtering on `groupedOutputs` |
| `other_examples/future/map_nodes_filter.py` | Filtering a node map feature |
| `other_examples/future/map_feature_all_3D.py` | 3D map features |
| `other_examples/map_feature_local_geojson/` | Loading a local GeoJSON file for a map feature, including a geojson-generation helper script |
| `other_examples/map_many_nodes.py` | A map variant with a very large node count |

### Not examples — infrastructure

- `examples/selector/example_selector.py` — serves the in-app example browser UI. Not a pattern to copy.
- `examples/content/` — static markdown/help assets referenced by `general_props_all_advanced.py`.

### After copying a pattern

Cross-check the specific fields you changed against the [api-reference](../api-reference/SKILL.md) skill (or the matching file in `docs/cave_api_docs/`) — examples show *a* valid configuration, not every valid field. If you edit a file inside `cave_api/examples/` itself, run `cave test examples.py` — see the [test](../test/SKILL.md) skill.
