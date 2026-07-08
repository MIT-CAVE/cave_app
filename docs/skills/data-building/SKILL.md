---
name: data-building
description: Build grouped charts and tabular hierarchies using GroupsBuilder and DateGroupsBuilder for groupedOutputs.
---

# Building Data Hierarchies for Charts

The CAVE API uses a nested dictionary structure for `groupedOutputs` to populate charts and pivot tables. `cave_utils` simplifies constructing this schema from flat tabular data.

## Using `GroupsBuilder`

For hierarchical, non-temporal group relationships, use `GroupsBuilder` to build groupings and map data indices to group hierarchies:

```python
from cave_utils.builders.groups import GroupsBuilder

# 1. Prepare flat relational data
location_group_data = [
    {"country": "USA", "state": "Michigan"},
    {"country": "USA", "state": "Massachusetts"},
    {"country": "Canada", "state": "Ontario"},
]

# 2. Instantiate GroupsBuilder
location_group_builder = GroupsBuilder(
    group_name="Locations",
    group_data=location_group_data,
    group_parents={"state": "country"}, # Defines hierarchy: state under country
    group_names={
        "country": "Countries",
        "state": "States",
    },
)

# 3. Serialize grouping schema for session_data['groupedOutputs']['groupings']
location_groupings_dict = location_group_builder.serialize()

# 4. Generate the corresponding mapping ID list for session_data['groupedOutputs']['data'][...]['groupLists']
location_id_list = location_group_builder.get_id_list()
```

## Using `DateGroupsBuilder`

For timeline or date-based groupings, use `DateGroupsBuilder` to automatically bucket and serialize date timelines:

```python
from cave_utils.builders.groups import DateGroupsBuilder

# 1. Prepare date string ids
date_ids = ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"]

# 2. Instantiate DateGroupsBuilder
date_builder = DateGroupsBuilder("Date", date_ids)

# 3. Serialize date grouping schema for session_data['groupedOutputs']['groupings']
date_groupings_dict = date_builder.serialize()
```

## Wiring into `session_data`

The outputs of these builders are mapped to the `groupedOutputs` top-level key:

```python
"groupedOutputs": {
    "order": {
        "groupings": ["location", "date"],
    },
    "groupings": {
        "location": location_group_builder.serialize(),
        "date": date_builder.serialize(),
    },
    "data": {
        "salesData": {
            "order": {
                "stats": ["sales"],
            },
            "stats": {
                "sales": {
                    "name": "Sales",
                    "unit": "units",
                },
            },
            # Map statistical values (usually pivoted into list format via pamda)
            "valueLists": {
                "sales": [95, 100, 100, 98],
            },
            # Map groupings to matching rows in valueLists
            "groupLists": {
                "location": location_group_builder.get_id_list(),
                "date": date_ids, # Original date list
            },
        },
    },
}
```

