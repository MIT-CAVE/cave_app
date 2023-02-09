# `nodes`
The `nodes` group contains data that is typically used to visualize single geographic locations in the "**Map**" view.

The structure of a `nodes` group looks as follows:
```py
"nodes": {
    "types": {
        "customNodeType1": {
            "name": "Node Type A",
            "colorByOptions": {
                "customPropKey1": {
                    "min": 0,
                    "max": 80,
                    "startGradientColor": {
                        "dark": "rgb(233, 0, 0)",
                        "light": "rgb(52, 52, 236)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(96, 2, 2)",
                        "light": "rgb(23, 23, 126)",
                    },
                },
                "customPropKey2": {
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
                "customPropKey3": {
                    "false": "rgb(255,0,0)",
                    "true": "rgb(0,255,0)"
                },
            },
            "minSizeRange": 0,
            "sizeByOptions": {
                "customPropKey1": {"min": 0, "max": 80},
                "customPropKey2": {"min": 0, "max": 50},
            },
            "startSize": "30px",
            "endSize": "45px",
            "icon": "MdStore",
            "props": {
                "customPropKey1": {
                    "name": "Numeric Prop Example A",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example A",
                    "numberFormat": {
                        "unit": "A units",
                    },
                },
                "customPropKey2": {
                    "name": "Numeric Prop Example B",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example B",
                    "numberFormat": {
                        "unit": "B units",
                    },
                },
                "customPropKey3": {
                    "name": "Boolean Prop Example",
                    "type": "toggle",
                    "value": True,
                    "enabled": True,
                    "help": "Help for boolean prop",
                },
            },
        },
    },
    "data": {
        "customNodeData1": {
            "latitude": 43.78,
            "longitude": -79.63,
            "type": "customNodeType1",
            "category": {
                "customDataChunck1": ["customDataKey1"],
                "customDataChunck2": ["customDataKey2"],
            },
            "props": {
                "customPropKey1": {
                    "value": 100,
                },
                "customPropKey2": {
                    "value": 50,
                },
                "customPropKey3": {
                    "value": True,
                },
            },
        },
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
- [`endGradientColor`](../common_keys/common_keys.md#endGradientColor)
- [`endSize`](../common_keys/common_keys.md#endSize)
- [`help`](../common_keys/props.md#help)
- [`icon`](../common_keys/common_keys.md#icon)
- [`name`](../common_keys/common_keys.md#name)
- [`numberFormat`](../common_keys/common_keys.md#number-format)
- [`prop > type`](../common_keys/props.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`sizeByOptions`](../common_keys/common_keys.md#sizeByOptions)
- [`startSize`](../common_keys/common_keys.md#startSize)
- [`startGradientColor`](../common_keys/common_keys.md#startGradientColor)
- [`value`](../common_keys/props.md#value)
- [`variant`](../common_keys/props.md#variant)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="node-data-point">`data.customNodeData*`</a> | Required | A custom key wrapper for the parameters required to visualize a node and the data associated with it in the "**Map**" view.
`data.customNodeData*.altitude` | `1` | The altitude of the node (in meters) above sea level. Defaults to 1 to appear on top of `geo` layers.
`data.customNodeData*.category`&swarhk;<br>`.customDataChunck*` | | See [`customDataChunck*`](categories.md#customDataChunck).
`data.customNodeData*.category`&swarhk;<br>`.customDataChunck*.customDataKey*` | | See [`customDataKey*`](categories.md#customDataKey).
`data.customNodeData*.latitude` | Required | The latitude of the node location in the "**Map**" view. It takes a float value.
`data.customNodeData*.longitude` | Required | The longitude of the node location in the "**Map**" view. It takes a float value.
`data.customNodeData*.name` | | A name for the node location that will be displayed as a title in the map modal.
`data.customNodeData*.props`&swarhk;<br>`.customPropKey*` | | See [`customPropKey*`](../common_keys/props.md#customPropKey).
`data.customNodeData*.type` | Required | The `type` key sets the node type of `customNodeData*` to a `customNodeType*` key, to match specific visualization preferences for a node.
`types` | Required | The `types` key allows you to define different types of nodes in terms of styling and data viz settings.
<a name="node-type">`types.customNodeType*`</a> | | A wrapper for key-value pairs that match a specific set of data viz preferences for a node.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"nodes": {
    "types": {
        "nodeTypeA": {
            "name": "Node Type A",
            "colorByOptions": {
                "numericPropExampleA": {
                    "min": 0,
                    "max": 80,
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
                "booleanPropExample": {
                    "false": "rgb(255,0,0)",
                    "true": "rgb(0,255,0)"
                },
            },
            "minSizeRange": 0,
            "sizeByOptions": {
                "numericPropExampleA": {"min": 0, "max": 80},
                "numericPropExampleB": {"min": 0, "max": 50},
            },
            "startSize": "30px",
            "endSize": "45px",
            "icon": "MdStore",
            "props": {
                "numericPropExampleA": {
                    "name": "Numeric Prop Example A",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example A",
                    "numberFormat": {
                        "unit": "A units",
                    },
                },
                "numericPropExampleB": {
                    "name": "Numeric Prop Example B",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example B",
                    "numberFormat": {
                        "unit": "B units",
                    },
                },
                "booleanPropExample": {
                    "name": "Boolean Prop Example",
                    "type": "toggle",
                    "value": True,
                    "enabled": True,
                    "help": "Help for boolean prop",
                },
            },
        },
        "nodeTypeB": {
            "name": "Node Type B",
            "colorByOptions": {
                "numericPropExampleA": {
                    "min": 0,
                    "max": 1000,
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
                "booleanPropExample": {
                    "false": "rgb(233, 0, 0)",
                    "true": "rgb(0, 233, 0)"
                },
            },
            "sizeByOptions": {
                "numericPropExampleA": {"min": 0, "max": 100},
                "numericPropExampleB": {"min": 0, "max": 250},
            },
            "startSize": "30px",
            "endSize": "45px",
            "icon": "BsBuilding",
            "props": {
                "numericPropExampleA": {
                    "name": "Numeric Prop Example A",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example A",
                    "numberFormat": {
                        "unit": "A units",
                    },
                },
                "numericPropExampleB": {
                    "name": "Numeric Prop Example B",
                    "type": "num",
                    "enabled": True,
                    "help": "Help for numeric prop example B",
                    "numberFormat": {
                        "unit": "B units",
                    },
                },
                "booleanPropExample": {
                    "name": "Boolean Prop Example",
                    "type": "toggle",
                    "value": True,
                    "enabled": True,
                    "help": "Help for boolean prop",
                },
            },
        },
    },
    "data": {
        "node1": {
            "latitude": 43.78,
            "longitude": -79.63,
            "type": "nodeTypeA",
            "category": {
                "location": ["locCaOn"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 100,
                },
                "numericPropExampleB": {
                    "value": 50,
                },
                "booleanPropExample": {
                    "value": True,
                },
            },
        },
        "node2": {
            "latitude": 39.82,
            "longitude": -86.18,
            "type": "nodeTypeA",
            "category": {
                "location": ["locUsIn"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 80,
                },
                "numericPropExampleB": {
                    "value": 40,
                },
                "booleanPropExample": {
                    "value": True,
                },
            },
        },
        "node3": {
            "latitude": 42.89,
            "longitude": -85.68,
            "type": "nodeTypeB",
            "category": {
                "location": ["locUsMi"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 500,
                },
                "numericPropExampleB": {
                    "value": 150,
                },
                "booleanPropExample": {
                    "value": True,
                },
            },
        },
        "node4": {
            "latitude": 28.49,
            "longitude": -81.56,
            "type": "nodeTypeB",
            "category": {
                "location": ["locUsFl"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 1000,
                },
                "numericPropExampleB": {
                    "value": 250,
                },
                "booleanPropExample": {
                    "value": True,
                },
            },
        },
        "node5": {
            "latitude": 42.361176,
            "longitude": -71.084707,
            "type": "nodeTypeB",
            "category": {
                "location": ["locUsMa"],
                "sku": ["SKU2", "SKU1"],
            },
            "props": {
                "numericPropExampleA": {
                    "value": 1000,
                },
                "numericPropExampleB": {
                    "value": 250,
                },
                "booleanPropExample": {
                    "value": True,
                },
            },
        },
    },
}
```
</details>
