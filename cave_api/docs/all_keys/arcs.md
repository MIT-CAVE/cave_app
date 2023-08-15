# `arcs`
The `arcs` group contains data that is typically used to visualize flows between two points on the "**Map**" view. Depending on the nature of the flows and the purpose of the visualization, the flows between two locations can be represented by a single arc (source and destination) or a sequence of arc segments representing a [`path`](#path).

The structure of an `arcs` group looks as follows:
```py
"arcs": {
    "types": {
        "customType1": {
            "name": "Flow Type 1",
            "colorByOptions": {
                "customPropKey8": {
                    "a": "rgb(128,255,255)",
                    "b": "rgb(0,153,51)",
                    "c": "rgb(0,0,128)",
                    "d": "rgb(204,0,0)",
                    "e": "rgb(153,77,0)",
                    "f": "rgb(255,25,255)",
                },
                "customPropKey9": {
                    "min": 0,
                    "max": 50,
                    "startGradientColor": {
                        "dark": "rgb(233, 0, 0)",
                        "light": "rgb(52, 52, 236)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(96, 2, 2)",
                        "light": "rgb(23, 23, 126)",
                    },
                },
                "customPropKey10": {
                    "min": 0,
                    "max": 40,
                    "startGradientColor": {
                        "dark": "rgb(233, 0, 0)",
                        "light": "rgb(52, 52, 236)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(96, 2, 2)",
                        "light": "rgb(23, 23, 126)",
                    },
                },
            },
            "lineBy": "solid",
            "sizeByOptions": {
                "customPropKey9": {"min": 0, "max": 50},
                "customPropKey10": {"min": 0, "max": 40},
            },
            "startSize": "15px",
            "endSize": "30px",
            "props": {
                "customPropKey9": {
                    "name": "Numeric Prop Example A",
                    "type": "num",
                    "help": "Help for numeric prop example A",
                    "unit": "A units",
                },
                "customPropKey10": {
                    "name": "Numeric Prop Example B",
                    "type": "num",
                    "help": "Help for numeric prop example B",
                    "unit": "B units",
                },
                "customPropKey8": {
                    "name": "Example Categorical Prop",
                    "type": "selector",
                    "variant": "dropdown",
                    "value": ["a"],
                    "options": {
                        "a": {"name": "A"},
                        "b": {"name": "B"},
                        "c": {"name": "C"},
                        "d": {"name": "D"},
                        "e": {"name": "E"},
                        "f": {"name": "F"},
                    },
                },
            },
            "layout": {
                "type": "grid",
                "numColumns": "auto",
                "numRows": 1,
                "data": {
                    "col1": {"type": "item", "itemId": "customPropKey9", "col": 1},
                    "col2": {
                        "type": "item",
                        "itemId": "customPropKey10",
                        "col": 2,
                    },
                    "col3": {
                        "type": "item",
                        "itemId": "customPropKey8",
                        "col": 3,
                    },
                },
            },
        },
    },
    "data": {
        "arc1": {
            "startLatitude": 43.78,
            "startLongitude": -79.63,
            "endLatitude": 39.82,
            "endLongitude": -86.18,
            "startClick": 800,
            "endClick": 1600,
            "type": "T1",
            "category": {
                "customLocation": ["locCaOn", "locUsIn"],
                "customSku": ["SKU2", "SKU1"],
            },
            "props": {
                "customPropKey9": {
                    "timeValues": {
                        0: { "value": 0 },
                        1: { "value": 100 },
                        2: { "value": 300 },
                    }
                },
                "customPropKey10": {
                    "value": 40,
                },
                "customPropKey8": {
                    "value": "b",
                },
            },
        },
        # As many arcs as needed
    },
},
```

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`category`](../common_keys/common_keys.md#category)
- [`colorByOptions`](../common_keys/common_keys.md#colorByOptions)
- [`column`](../common_keys/common_keys.md#column)
- [`data`](../common_keys/common_keys.md#data)
- [`enabled`](../common_keys/common_keys.md#enabled)
- [`endGradientColor`](../common_keys/common_keys.md#end-gradient)
- [`endSize`](../common_keys/common_keys.md#endSize)
- [`help`](../common_keys/props.md#help)
- [`max`](../common_keys/common_keys.md#color-by-max)
- [`min`](../common_keys/common_keys.md#color-by-min)
- [`name`](../common_keys/common_keys.md#name)
- [`prop > type`](../common_keys/props.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`sizeByOptions`](../common_keys/common_keys.md#sizeByOptions)
- [`startSize`](../common_keys/common_keys.md#startSize)
- [`startGradientColor`](../common_keys/common_keys.md#start-gradient)
- [`timeValues`](../common_keys/time_value.md)
- [`unit`](../common_keys/common_keys.md#unit)
- [`value`](../common_keys/props.md#value)
- [`variant`](../common_keys/props.md#variant)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="arc-data-point">`data.customArcData*`</a> | Required | A custom key wrapper for the parameters required to visualize an arc flow and the data associated with it in the "**Map**" view.
`data.customArcData*.category`&swarhk;<br>`.customDataChunck*` | | See [`customDataChunck*`](../all_keys/categories.md#customDataChunck).
`data.customArcData*.category`&swarhk;<br>`.customDataChunck*.customDataKey*` | | See [`customDataKey*`](../all_keys/categories.md#customDataKey).
`data.customArcData*.endAltitude` | | The altitude (in meters) for the target location in the "**Map**" view. It takes a float value.
`data.customArcData*.endClick`<br>(*Under construction*) | | Related to the animation frame rate of an arc layer. It takes an integer value.
`data.customArcData*.endLatitude` | Required | The latitude for the target location in the "**Map**" view. It takes a float value.
`data.customArcData*.endLongitude` | Required | The longitude for the target location in the "**Map**" view. It takes a float value.
`data.customArcData*.geoJsonValue` | | To be used only in conjunction with `types.customArcType*.geoJson`. The identifier for this arc as identified in the specified geoJson object. This identifier is matched to the `types.customArcType*.geoJson.geoJsonProp` as it relates to each geoJson object in the file specified at `types.customArcType*.geoJson.geoJsonLayer`.
`data.customArcData*.height` | `1` | The height multiplier relative to the distance between two points for the apex of a `3d` (lineBy) arc. For example, a value of `0` would turn a `3d` (lineBy) arc into the equivalent to a `solid` (lineBy) arc.
`data.customArcData*.name` | | A name for the arc flow that will be displayed as a title in the map modal.
<a name="path">`data.customArcData*.path`</a> | | A list of coordinate points (`[<longitude>, <latitude>]`), such that every two consecutive coordinates represent an arc segment of a path to be rendered in the "**Map**" view. Additionally, a third position can be added to each coordinate (`[<longitude>, <latitude>, <altitude>]`), to visually represent altitude on the map.<br><br>Please note that `path` is not supported for `3d` arcs. If you need to create a "`3d` path", you can do so by joining multiple arcs which start and end coordinates match the segments of the intended path.<br><br>The use of `path` overrides any behavior resulting from the use of the following `data.customArcData*.` keys: `startLongitude`, `startLatitude`, `startAltitude`, `endLongitude`, `endLatitude`, and `endAltitude`.
`data.customArcData*.props`&swarhk;<br>`.customPropKey*` | | See [`customPropKey*`](../common_keys/props.md#customPropKey).
`data.customArcData*.startAltitude` | | The altitude (in meters) for the source location in the "**Map**" view. It takes a float value.
`data.customArcData*.startClick`<br>(*Under construction*) | | Related to the animation frame rate of an arc layer. It takes an integer value.
`data.customArcData*.startLatitude` | Required | The latitude for the source location in the "**Map**" view. It takes a float value.
`data.customArcData*.startLongitude` | Required | The longitude for the source location in the "**Map**" view. It takes a float value.
`data.customArcData*.tilt` | `0` | Expressed in degrees (-90&deg; to 90&deg;), this feature enables you to tilt the arc sideways when dealing with multiple arcs that share the same source and target locations in the "**Map**" view.
`data.customArcData*.type` | Required | The `type` key sets the arc type of `customArcData*` to a `customArcType*` key, to match specific visualization preferences for an arc flow.
`types` | Required | The `types` key allows you to define different arc types in terms of styling and data viz settings.
<a name="arc-type">`types.customArcType*`</a> | | A wrapper for key-value pairs that match a specific set of data viz preferences for an arc flow.
`types.customArcType*.lineBy` | `'solid'` | The pattern of dashes and gaps used to form the shape of an arc's stroke. It takes one of the following values: `'dashed'`, `'dotted'`, `'solid'`, `'3d'`, or `'geoJson'`. Arcs using a GeoJSON source must always be set to `'geoJson'`. This can be set in individual arcs to overwrite the default for the type.
<a name="geoJson">`types.customArcType*.geoJson`</a> | | A wrapper for the [`geoJsonLayer`](#geojson_layer) and [`geoJsonProp`](#geojson_prop) keys in an arc type. If this key is present, all custumArcData.* object of this type should include a `geoJsonValue` key, rather than a `path` or `startLongitude` and `startLatitude`/`endLongitude` and `endLatitude` pair.
<a name="geoJsonLayer">`types.customArcType*.geoJson`&swarhk;<br>`.geoJsonLayer`</a> | | Sets the GeoJSON data source of `customArcType*` to a URL of a GeoJSON data source. Note that this URL is fetched on app startup or, if passed later, when the layer is enabled by the app user.
<a name="geoJsonProp">`types.customArcType*.geoJson`&swarhk;<br>`.geoJsonProp`</a> | | Contains the name of a [GeoJSON property](#https://datatracker.ietf.org/doc/html/rfc7946#section-1.5) in the data source specified in `geoJsonLayer`.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"arcs": {
    "types": {
        "T1": {
            "name": "Flow Type 1",
            "colorByOptions": {
                "selectorPropForColor": {
                    "a": "rgb(128,255,255)",
                    "b": "rgb(0,153,51)",
                    "c": "rgb(0,0,128)",
                    "d": "rgb(204,0,0)",
                    "e": "rgb(153,77,0)",
                    "f": "rgb(255,25,255)",
                },
                "numericPropExampleA": {
                    "min": 0,
                    "max": 50,
                    "startGradientColor": {
                        "dark": "rgb(233, 0, 0)",
                        "light": "rgb(52, 52, 236)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(96, 2, 2)",
                        "light": "rgb(23, 23, 126)",
                    },
                },
                "numericPropExampleB": {
                    "min": 0,
                    "max": 40,
                    "startGradientColor": {
                        "dark": "rgb(233, 0, 0)",
                        "light": "rgb(52, 52, 236)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(96, 2, 2)",
                        "light": "rgb(23, 23, 126)",
                    },
                },
            },
            "lineBy": "solid",
            "sizeByOptions": {
                "numericPropExampleA": {"min": 0, "max": 50},
                "numericPropExampleB": {"min": 0, "max": 40},
            },
            "startSize": "15px",
            "endSize": "30px",
            "props": {
                "numericPropExampleA": {
                    "name": "Numeric Prop Example A",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example A",
                    "unit": "A units",
                },
                "numericPropExampleB": {
                    "name": "Numeric Prop Example B",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example B",
                    "unit": "B units",
                },
                "selectorPropForColor": {
                    "name": "Example Categorical Prop",
                    "type": "selector",
                    "variant": "dropdown",
                    "value": ["a"],
                    "options": {
                        "a": {"name": "A"},
                        "b": {"name": "B"},
                        "c": {"name": "C"},
                        "d": {"name": "D"},
                        "e": {"name": "E"},
                        "f": {"name": "F"},
                    },
                    "enabled": True,
                },
            },
            "layout": {
                "type": "grid",
                "numColumns": "auto",
                "numRows": 1,
                "data": {
                    "col1": {"type": "item", "itemId": "numericPropExampleA", "col": 1},
                    "col2": {
                        "type": "item",
                        "itemId": "numericPropExampleB",
                        "col": 2,
                    },
                    "col3": {
                        "type": "item",
                        "itemId": "selectorPropForColor",
                        "col": 3,
                    },
                },
            },
        },
        "T2": {
            "name": "Flow Type 2",
            "colorByOptions": {
                "selectorPropForColor": {
                    "a": "rgb(128,255,255)",
                    "b": "rgb(0,153,51)",
                    "c": "rgb(0,0,128)",
                    "d": "rgb(204,0,0)",
                    "e": "rgb(153,77,0)",
                    "f": "rgb(255,25,255)",
                },
                "numericPropExampleA": {
                    "min": 0,
                    "max": 50,
                    "startGradientColor": {
                        "dark": "rgb(233, 0, 0)",
                        "light": "rgb(52, 52, 236)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(96, 2, 2)",
                        "light": "rgb(23, 23, 126)",
                    },
                },
                "numericPropExampleB": {
                    "min": 0,
                    "max": 40,
                    "startGradientColor": {
                        "dark": "rgb(233, 0, 0)",
                        "light": "rgb(52, 52, 236)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(96, 2, 2)",
                        "light": "rgb(23, 23, 126)",
                    },
                },
            },
            "colorBy": "numericPropExampleA",
            "lineBy": "dotted",
            "sizeByOptions": {
                "numericPropExampleA": {"min": 0, "max": 50},
                "numericPropExampleB": {"min": 0, "max": 40},
            },
            "sizeBy": "numericPropExampleB",
            "startSize": "15px",
            "endSize": "30px",
            "props": {
                "numericPropExampleA": {
                    "name": "Numeric Prop Example A",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example A",
                    "unit": "A units",
                },
                "numericPropExampleB": {
                    "name": "Numeric Prop Example B",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example B",
                    "unit": "B units",
                },
                "selectorPropForColor": {
                    "name": "Example Categorical Prop",
                    "type": "selector",
                    "variant": "dropdown",
                    "value": ["a"],
                    "options": {
                        "a": {"name": "A"},
                        "b": {"name": "B"},
                        "c": {"name": "C"},
                        "d": {"name": "D"},
                        "e": {"name": "E"},
                        "f": {"name": "F"},
                    },
                    "enabled": True,
                },
            },
            "layout": {
                "type": "grid",
                "numColumns": 1,
                "numRows": "auto",
                "data": {
                    "row1": {
                        "type": "item",
                        "itemId": "numericPropExampleA",
                        "row": 1,
                    },
                    "row2": {
                        "type": "item",
                        "itemId": "numericPropExampleB",
                        "row": 2,
                    },
                    "row3": {
                        "type": "item",
                        "itemId": "selectorPropForColor",
                        "row": 3,
                    },
                },
            },
        },
    },
    "data": {
        "arc1": {
            "startLatitude": 43.78,
            "startLongitude": -79.63,
            "endLatitude": 39.82,
            "endLongitude": -86.18,
            "startClick": 800,
            "endClick": 1600,
            "type": "T1",
            "category": {
                "location": ["locCaOn", "locUsIn"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 50,
                },
                "numericPropExampleB": {
                    "value": 40,
                },
                "selectorPropForColor": {
                    "value": "b",
                },
            },
        },
        "arc2": {
            "startLatitude": 39.82,
            "startLongitude": -86.18,
            "endLatitude": 42.89,
            "endLongitude": -85.68,
            "startClick": 1600,
            "endClick": 2000,
            "type": "T2",
            "category": {
                "location": ["locUsMi", "locUsIn"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 30,
                },
                "numericPropExampleB": {
                    "value": 20,
                },
                "selectorPropForColor": {
                    "value": "e",
                },
            },
        },
        "arc3": {
            "startLatitude": 39.82,
            "startLongitude": -86.18,
            "endLatitude": 28.49,
            "endLongitude": -81.56,
            "startClick": 1600,
            "endClick": 2000,
            "type": "T2",
            "category": {
                "location": ["locUsFl", "locUsIn"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 30,
                },
                "numericPropExampleB": {
                    "value": 14,
                },
                "selectorPropForColor": {
                    "value": "d",
                },
            },
        },
        "arc4": {
            "startLatitude": 39.82,
            "startLongitude": -86.18,
            "endLatitude": 42.361176,
            "endLongitude": -71.084707,
            "startClick": 1600,
            "endClick": 2000,
            "type": "T2",
            "category": {
                "location": ["locUsMa", "locUsIn"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 30,
                },
                "numericPropExampleB": {
                    "value": 6,
                },
                "selectorPropForColor": {
                    "value": "f",
                },
            },
        },
    },
},
```
</details>
