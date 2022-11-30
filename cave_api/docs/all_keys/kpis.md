# `kpis`
The `kpis` group contains all the KPI data that will be displayed on the "**KPI**" view. These are typically highly aggregated statistics calculated by the api. In general, KPIs are used to compare values across sessions and give a high level overview of output. Filters and aggregations will not affect `kpis`.

Let's look inside the structure of `kpis`:
```py
'kpis': {
    'data': {
        'customKpi1': {
            'name': 'A name to be displayed in the UI',
            'numberFormat': {
                'unit': 'units',
            },
            'type': 'num',
            'icon': 'FaBox',
            'value': 100,
            'mapKpi': True,
        },
        # As many custom KPIs as needed
    },
    'layout': {...},
}
```

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`column`](../common_keys/common_keys.md#column)
- [`data`](../common_keys/common_keys.md#data)
- [`icon`](../common_keys/common_keys.md#icon)
- [`layout`](../common_keys/layout.md)
- [`name`](../common_keys/common_keys.md#name)
- [`numberFormat`](../common_keys/common_keys.md#number-format)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`customKpi*` | Required | A custom key wrapper for the KPI data.
`customKpi*.mapKpi` | `False` | The `mapKpi` flag allows designers to specify up to six parameters that are displayed on a permanent grid in the "**Map**" view. The grid layout (rows *x* columns) changes with the number of parameters present in the data, scaling up to 2 rows and 3 columns.
`customKpi*.type` | `'num'` | As a direct child of `customKpi*`, the `type` key defines the UI construct used to render the KPI and restricts the set of key-value pairs that can be used with this type. The `type` key takes one of the following values:<br><br>`'head'`: the `mapKpi`, [`numberFormat`](../common_keys/common_keys.md#number-format), and `value` keys are ignored when used along this type.<br>`'num'`: all keys are valid to use with this type.<br>`'text'`: the [`numberFormat`](../common_keys/common_keys.md#number-format) key is ignored when used along this type.<br>
`customKpi*.value` | | The actual value of the KPI.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"kpis": {
    "data": {
        "kpiHeader1": {
            "type": "head",
            "name": "Example KPI Header 1",
            "icon": "BsInboxes",
        },
        "kpiHeader2": {
            "type": "head",
            "name": "Example KPI Header 2",
            "icon": "BsTruck",
        },
        "key1": {
            "name": "KPI Example 1",
            "value": 18,
            "icon": "BsFillEmojiFrownFill",
            "mapKpi": True,
            "numberFormat": {
                "precision": 0,
                "unit": "frowns",
            },
        },
        "key2": {
            "name": "KPI Example 2",
            "value": 32,
            "icon": "BsFillEmojiSmileFill",
            "mapKpi": True,
            "numberFormat": {
                "precision": 0,
                "unit": "smiles",
            },
        },
        "key3": {
            "name": "KPI Example 3",
            "icon": "BsInboxes",
            "numberFormat": {
                "precision": 4,
                "trailingZeros": True,
                "unit": "units",
            },
            "value": 100,
        },
        "key4": {
            "name": "A Big Number",
            "icon": "BsTruck",
            "value": 10000000000000,
            "numberFormat": {
                "precision": 0,
                "unit": "units",
            },
        },
        "key5": {
            "name": "A Really Big Number",
            "icon": "MdExpand",
            "value": 9007199254740991,
            "numberFormat": {
                "precision": 2,
                "unit": "$",
                "currency": True,
                "trailingZeros": False,
            },
        },
    },
    "layout": {
        "type": "grid",
        "numColumns": "auto",
        "numRows": "auto",
        "data": {
            "col1Row1": {
                "type": "item",
                "itemId": "kpiHeader1",
                "column": 1,
                "row": 1,
            },
            "col1Row2": {
                "type": "item",
                "itemId": "key1",
                "column": 1,
                "row": 2,
            },
            "col1Row3": {
                "type": "item",
                "itemId": "key4",
                "column": 1,
                "row": 3,
            },
            "col1Row4": {
                "type": "item",
                "itemId": "key5",
                "column": 1,
                "row": 4,
            },
            "col2Row1": {
                "type": "item",
                "itemId": "kpiHeader2",
                "column": 2,
                "row": 1,
            },
            "col2Row2": {
                "type": "item",
                "itemId": "key2",
                "column": 2,
                "row": 2,
            },
            "col2Row3": {
                "type": "item",
                "itemId": "key3",
                "column": 2,
                "row": 3,
            },
        },
    },
},
```
</details>