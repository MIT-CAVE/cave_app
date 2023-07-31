### `maps`
This key group allows designers to specify information about the starting state of the map, what information is contained and how it is grouped in the legend, and what viewports can be easily jumped to by the user.

Below is the `maps` group with its sub-keys matched by typical or placeholder values:
```py
"maps": {
    "name": "map",
    "data": {
        "customMap": {
            "currentStyle": "customMapStyle1",
            "currentProjection": "globe"
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
                    "nodes": {
                        "customNodeType1": {
                            "colorBy": "customPropKey3",
                            "sizeBy": "customPropKey1",
                            "value": False,
                        }
                    },
                    "arcs": {
                        "customArcType1": {
                            "colorBy": "customPropKey9",
                            "sizeBy": "customPropKey10",
                            "value": True,
                        },
                    },
                    "geos": {
                        "customGeoType1": {
                            "value": False,
                            "order": 1
                        },
                        "customGeoType2": {
                            "value": False,
                            "order": 2,
                        },
                    },
                    "order": 1,
                },
                "customLegendGroupKey2": {
                    "name": "Warehouses",
                    "nodes": {
                        "customNodeType2": {
                            "value": True,
                        }
                    },
                    "arcs": {
                        "customArcType2": {
                            "value": False,
                        }
                    },
                    "order": 2,
                },
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
`customMapKey.currentProjection` | mercator | A string describing the current map projection. Can be either `'globe'` or `'mercator'`.
`customMapKey.currentStyle` | _default | A string describing the current map style. Can be `'_default'`, `'dark_matter'`, `'positron'`, `'OSM'`, or a custom style specified in the [`settings`](./settings.md) key.
<a name="defaultViewport">`customMapKey.defaultViewport`</a> | | A dictionary object containing geo properties that set the map's default field of view. Also used by the "home" viewport button in the app.
`customMapKey.defaultViewport.bearing` | `0` | The initial bearing (rotation) of the map, measured in degrees counter-clockwise from north.
`customMapKey.defaultViewport.pitch` | `0` | The initial pitch (*tilt*) of the viewport in the "**Map**" view, measured in degrees away from the plane of the screen (0&deg; - 85&deg;). A pitch of 0&deg; results in a two-dimensional map, as if your line of sight forms a perpendicular angle with the earth's surface, while a greater value like 60&deg; looks ahead towards the horizon.
`customMapKey.defaultViewport.latitude` | `42.36157` | The center latitude of the viewport in the "**Map**" view. It takes a float value.
`customMapKey.defaultViewport.longitude` | `-71.08463` | The center longitude of the viewport in the "**Map**" view. It takes a float value.
`customMapKey.defaultViewport.maxZoom` | `22` | The maximum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`customMapKey.defaultViewport.minZoom` | `1.5` | The minimum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`customMapKey.defaultViewport.zoom` | `13` | The initial zoom level of the viewport in the "**Map**" view. It takes an integer value. Learn more about the zoom levels [here](#https://docs.mapbox.com/help/glossary/zoom-level/).
<a name="optionalViewports">`customMapKey.optionalViewports`</a> | | A dictionary of optional viewports that can be jumped to by users. Each optional viewport should contain the same keys as `defaultViewport` as well as `name` and `icon` keys.
<a name="legendGroups">`customMapKey.legendGroups`</a> | `{}` | A dictionary object of all layer groupings to display in the map legend. The legend groups are displayed according to their `order` and each has an internal order of `nodes`, `arcs`, and `geos`. Types not included in any legend group cannot be toggled.
`customMapKey.legendGroups.customLegendGroupKey*` | `{}` | A custom key wrapper for a legend group that contains its `name`, its display `order` from top to bottom within the map legend, as well as the initial state of the toggles for [`arc type`](arcs.md#arc-type)s, [`node type`](nodes.md#node-type)s, and [`geo type`](geos.md#geo-type)s.
`customMapKey.legendGroups.customLegendGroupKey*.arcs` | `{}` | A list of all arc types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`customMapKey.legendGroups.customLegendGroupKey*.arcs`&swarhk;<br>`.customArcType*` | `{value: False}` | A [arc type](arcs.md#arc-type) that matches the initial state of the toggle within the legend group. The inner `value` key is paired with a boolean indicating whether the arc type should be displayed in the "Map" view or not, while the `order` key follows the standard [`order`](../common_keys/common_keys.md#order)ing convention, allowing to set the display order of the arc type within the legend group. The `colorBy` and `sizeBy` keys set the default coloring and sizing props of the arc type.
`customMapKey.legendGroups.customLegendGroupKey*.geos` | `{}` | A list of all geo types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`customMapKey.legendGroups.customLegendGroupKey*.geos`&swarhk;<br>`.customGeoType*` | `{value: False}` | A [geo type](geos.md#geo-type) that matches the initial state of the toggle within the legend group. The inner `value` key is paired with a boolean indicating whether the geo type should be displayed in the "Map" view or not, while the `order` key follows the standard [`order`](../common_keys/common_keys.md#order)ing convention, allowing to set the display order of the geo type within the legend group. The `colorBy` key set the default coloring prop of the geo type.
`customMapKey.legendGroups.customLegendGroupKey*.nodes` | `{}` | A dictionary of all node types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*` | `{}` | An object to hold the options related to each custom node type
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.value` | `False` | A boolean value to indicate if this layer should be shown
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.order` | | The [`order`](../common_keys/common_keys.md#order) value that this toggle should appear in the legend group
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.colorBy` | `False` | The prop to used to color this node layer
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.sizeBy` | `False` | The prop to used to size this node layer
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.allowGrouping` | `False` | A node specific key to determine if this node layer is able to be auto grouped.
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.group` | `False` | Group the nodes in this layer (to use this you must set `allowGrouping=true`)
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.groupCalcByColor` | `'mode'`<br><br>or<br><br> `'count'`<br>(only for [`'num'` prop](../common_keys/props.md#num)s) | The aggregation function to use on the prop specified in `colorBy`. See [Aggregation functions](#aggregation-functions).
`customMapKey.legendGroups.customLegendGroupKey*.nodes`&swarhk;<br>`.customNodeType*.groupCalcBySize` | `'count'` | The aggregation function to use on the prop specified in `sizeBy`. Only [`'num'` prop](../common_keys/props.md#num)s are supported for this setting. See [Numeric values](#numeric-values).

### Aggregation functions
In the "**Map**" view, nodes can be clustered together, and their values can be aggregated based on a chosen function. These aggregation functions efficiently summarize and visualize the data in the map, providing meaningful insights to users. The available functions depend on the value type associated with the props provided for each node.

#### Numeric values
Numeric values are associated with a [`'num'` prop](../common_keys/props.md#num) and offer various options for aggregation functions, including:
>`'count'`: Calculates the total number of nodes in the cluster.<br>
`'max'`: Finds the highest numeric value within the node cluster.<br>
`'min'`: Conversely, the `'min'` function finds the lowest numeric value within the node cluster and returns it as the result of the aggregation.<br>
`'mean'`: Calculates the average of all the numeric values within the node cluster.<br>
`'median'`: Finds the middle numeric value within the node cluster data when the values are sorted in ascending order. If there is an even number of elements, it calculates the average of the two middle values.<br>
`'mode'`: Returns the most frequently occurring value within the node cluster data.<br>
`'sum'`: Adds up all the numeric values within the node cluster and returns the total sum.

Example: Consider three nodes with values `[10, 15, 5]`. By choosing the `'sum'` function for aggregation, the resulting value for the cluster would be `30` (`10` + `15` + `5`).

#### Boolean values
For boolean values (obtained from a [`'toggle'` prop](../common_keys/props.md#toggle)), the following functions are available:
>`'mode'`: Returns the most frequently occurring value within the node cluster.<br>
`'or'`: Evaluates boolean values within the node cluster and returns `True` if at least one of the values is `True`. Otherwise, it returns `False`.<br>
`'and'`: Evaluates boolean values within the node cluster and returns `True` if all of the values are `True`. Otherwise, it returns `False`.

Example: Imagine four nodes with values `[False, True, False, True]`. If we choose the `'or'` function, the cluster value would be `True`, as it evaluates to `True` if at least one node value is `True`.

#### Categorical values
When dealing with categorical values (taken from a [`'selector'` prop](../common_keys/props.md#selector)), the only available function is `'mode'`.
>`'mode'`: Returns the most frequently occurring value within the node cluster.

Example: Suppose we have five nodes with values `["Monday", "Tuesday", "Monday", "Wednesday", "Monday", "Thursday", "Thursday"]`. If we choose the `'mode'` function, the cluster value would be `"Monday"` because it appears most frequently. In case, two elements have the same frequency, the `'mode'` function would return the first to appear in the list. Thus, `["Food", "Clothing", "Electronics", "Home", "Clothing", "Home"]` would yield `"Clothing"` since it appears first in the list with the same frequency as `"Home"`.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"maps": {
    "data": {
        "map1": {
            "currentProjection": "mercator",
            "currentStyle": "dark_matter"
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
                    "nodes": {
                        "nodeTypeA": {
                            "value": True,
                            "sizeBy": "numericPropExampleA",
                            "colorBy": "booleanPropExample",
                        }
                    },
                    "arcs": {
                        "T1": {
                            "colorBy": "numericPropExampleA",
                            "sizeBy": "numericPropExampleB",
                            "value": True,
                        }
                    },
                    "order": 1,
                },
                "lgb": {
                    "name": "Legend Group B",
                    "nodes": {
                        "nodeTypeB": {
                            "value": True,
                            "sizeBy": "numericPropExampleB",
                            "colorBy": "booleanPropExample",
                        }
                    },
                    "arcs": {
                        "T2": {
                            "colorBy": "numericPropExampleA",
                            "sizeBy": "numericPropExampleB",
                            "value": True,
                        }
                    },
                    "geos": {
                        "state": {
                            "value": True,
                            "order": 1,
                            "colorBy": "numericPropExampleC",
                        },
                        "country": {
                            "value": False,
                            "order": 2,
                            "colorBy": "numericPropExampleC",
                        },
                    },
                    "order": 2,
                },
            },
        },
        "map2": {
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
                    "nodes": {
                        "nodeTypeA": {
                            "value": True,
                            "sizeBy": "numericPropExampleA",
                            "colorBy": "booleanPropExample",
                        }
                    },
                    "arcs": {
                        "T1": {
                            "colorBy": "numericPropExampleA",
                            "sizeBy": "numericPropExampleB",
                            "value": True,
                        }
                    },
                    "order": 1,
                },
                "lgb": {
                    "name": "Legend Group B",
                    "nodes": {
                        "nodeTypeB": {
                            "value": True,
                            "sizeBy": "numericPropExampleB",
                            "colorBy": "booleanPropExample",
                        }
                    },
                    "arcs": {
                        "T2": {
                            "colorBy": "numericPropExampleA",
                            "sizeBy": "numericPropExampleB",
                            "value": True,
                        }
                    },
                    "geos": {
                        "state": {
                            "value": True,
                            "order": 1,
                            "colorBy": "numericPropExampleC",
                        },
                        "country": {
                            "value": False,
                            "order": 2,
                            "colorBy": "numericPropExampleC",
                        },
                    },
                    "order": 2,
                },
            },
        },
    },
},
```
</details>
