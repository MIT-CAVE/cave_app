### `map`
This key group allows designers to specify information about the starting state of the map, what information is contained and how it is grouped in the legend, and what viewports can be easily jumped to by the user.

Below is the `map` group with its sub-keys matched by typical or placeholder values:
```py
"map": {
    "name": "map",
    "data": {
        "defaultViewport": {
            "longitude": -75.44766721108091,
            "latitude": 40.34530681636297,
            "zoom": 4.657916626867326,
            "pitch": 0,
            "bearing": 0,
            "height": 1287,
            "altitude": 1.5,
            "maxZoom": 12,
            "minZoom": 2,
        },
        "optionalViewports": {
            "ov0": {
                "icon": "FaGlobeAsia",
                "name": "Asia",
                "zoom": 4,
                "order": 1,
                "pitch": 0,
                "bearing": 0,
                "maxZoom": 12,
                "minZoom": 2,
                "latitude": 30,
                "longitude": 121,
            },
        },
        "legendGroups": {
            "customLegendGroupKey1": {
                "name": "DC Delivery",
                "nodes": {"customNodeType1": {"value": False}},
                "arcs": {"customArcType1": {"value": True}},
                "geos": {
                    "customGeoType1": {"value": False, "order": 1},
                    "customGeoType2": {"value": False, "order": 2},
                },
                "order": 1,
            },
            "customLegendGroupKey2": {
                "name": "Warehouses",
                "nodes": {"customNodeType2": {"value": True}},
                "arcs": {"customArcType2": {"value": False}},
                "order": 2,
            },
        },
    },
}
```

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`data`](../common_keys/common_keys.md#data)
- [`icon`](../common_keys/common_keys.md#icon)
- [`name`](../common_keys/common_keys.md#name)
- [`order`](../common_keys/common_keys.md#order)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="defaultViewport">`defaultViewport`</a> | | A dictionary object containing geo properties that set the map's default field of view. Also used by the "home" viewport button in the app.
`defaultViewport.bearing` | `0` | The initial bearing (rotation) of the map, measured in degrees counter-clockwise from north.
`defaultViewport.pitch` | `0` | The initial pitch (*tilt*) of the viewport in the "**Map**" view, measured in degrees away from the plane of the screen (0&deg; - 85&deg;). A pitch of 0&deg; results in a two-dimensional map, as if your line of sight forms a perpendicular angle with the earth's surface, while a greater value like 60&deg; looks ahead towards the horizon.
`defaultViewport.latitude` | `42.36157` | The center latitude of the viewport in the "**Map**" view. It takes a float value.
`defaultViewport.longitude` | `-71.08463` | The center longitude of the viewport in the "**Map**" view. It takes a float value.
`defaultViewport.maxZoom` | `22` | The maximum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`defaultViewport.minZoom` | `1.5` | The minimum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`defaultViewport.zoom` | `13` | The initial zoom level of the viewport in the "**Map**" view. It takes an integer value. Learn more about the zoom levels [here](#https://docs.mapbox.com/help/glossary/zoom-level/).
<a name="optionalViewports">`optionalViewports`</a> | | A dictionary of optional viewports that can be jumped to by users. Each optional viewport should contain the same keys as `defaultViewport` as well as `name` and `icon` keys.
<a name="legendGroups">`legendGroups`</a> | `{}` | A dictionary object of all layer groupings to display in the map legend. The legend groups are displayed according to their `order` and each has an internal order of `nodes`, `arcs`, and `geos`. Types not included in any legend group cannot be toggled.
`legendGroups.customLegendGroupKey*` | `{}` | A custom key wrapper for a legend group that contains its `name`, its display `order` from top to bottom within the map legend, as well as the initial state of the toggles for [`arc type`](arcs.md#arc-type)s, [`node type`](nodes.md#node-type)s, and [`geo type`](geos.md#geo-type)s.
`legendGroups.customLegendGroupKey*.arcs` | `{}` | A list of all arc types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`legendGroups.customLegendGroupKey*.arcs.customArcType*` | `{value: False}` | A [arc type](arcs.md#arc-type) that matches the initial state of the toggle within the legend group. The inner `value` key is paired with a boolean indicating whether the arc type should be displayed in the "Map" view or not, while the `order` key follows the standard [`order`](../common_keys/common_keys.md#order)ing convention, allowing to set the display order of the arc type within the legend group.
`legendGroups.customLegendGroupKey*.geos` | `{}` | A list of all geo types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`legendGroups.customLegendGroupKey*.geos.customGeoType*` | `{value: False}` | A [geo type](geos.md#geo-type) that matches the initial state of the toggle within the legend group. The inner `value` key is paired with a boolean indicating whether the geo type should be displayed in the "Map" view or not, while the `order` key follows the standard [`order`](../common_keys/common_keys.md#order)ing convention, allowing to set the display order of the geo type within the legend group.
`legendGroups.customLegendGroupKey*.nodes` | `{}` | A dictionary of all node types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`legendGroups.customLegendGroupKey*.nodes.customNodeType*` | `{value: False}` | A [node type](nodes.md#node-type) that matches the initial state of the toggle within the legend group. The inner `value` key is paired with a boolean indicating whether the node type should be displayed in the "Map" view or not, while the `order` key follows the standard [`order`](../common_keys/common_keys.md#order)ing convention, allowing to set the display order of the node type within the legend group.


## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"map": {
    "data": {
        "defaultViewport": {
            "longitude": -75.44766721108091,
            "latitude": 40.34530681636297,
            "zoom": 4.657916626867326,
            "pitch": 0,
            "bearing": 0,
            "height": 1287,
            "altitude": 1.5,
            "maxZoom": 12,
            "minZoom": 2,
        },
        "optionalViewports": {
            "ov0": {
                "icon": "FaGlobeAsia",
                "name": "Asia",
                "zoom": 4,
                "order": 1,
                "pitch": 0,
                "bearing": 0,
                "maxZoom": 12,
                "minZoom": 2,
                "latitude": 30,
                "longitude": 121,
            },
            "ov1": {
                "icon": "FaGlobeEurope",
                "name": "EMEA",
                "zoom": 4,
                "order": 1,
                "pitch": 0,
                "bearing": 0,
                "maxZoom": 12,
                "minZoom": 2,
                "latitude": 47,
                "longitude": 14,
            },
        },
        "legendGroups": {
            "lga": {
                "name": "Legend Group A",
                "nodes": {"nodeTypeA": {"value": True}},
                "arcs": {"T1": {"value": True}},
                "order": 1,
            },
            "lgb": {
                "name": "Legend Group B",
                "nodes": {"nodeTypeB": {"value": True}},
                "arcs": {"T2": {"value": True}},
                "geos": {
                    "state": {"value": True, "order": 1},
                    "country": {"value": False, "order": 2},
                },
                "order": 2,
            },
        },
    },
}
```
</details>
