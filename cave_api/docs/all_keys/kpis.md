# `kpis`
The `kpis` group contains all the KPI data that will be displayed on the "**KPI**" view. These are typically highly aggregated statistics calculated by the api. In general, KPIs are used to compare values across sessions and give a high level overview of output. Filters and aggregations will not affect `kpis`.

Let's look inside the structure of `kpis`:
```py
"kpis": {
    "data": {
        "customKpi1": {
            "name": "A name to be displayed in the UI",
            "unit": "units",
            "type": "num",
            "icon": "fa/FaBox",
            "value": 100,
            "mapKpi": True,
        },
        # As many custom KPIs as needed
    },
    "layout": {...},
}
```

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`column`](../common_keys/common_keys.md#column)
- [`data`](../common_keys/common_keys.md#data)
- [`fallbackValue`](../common_keys/common_keys.md#fallback-value)
- [`icon`](../common_keys/common_keys.md#icon)
- [`layout`](../common_keys/layout.md)
- [`locale`](../common_keys/common_keys.md#locale)
- [`name`](../common_keys/common_keys.md#name)
- [`precision`](../common_keys/common_keys.md#precision)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`trailingZeros`](../common_keys/common_keys.md#trailing-zeros)
- [`unit`](../common_keys/common_keys.md#unit)
- [`unitPlacement`](../common_keys/common_keys.md#unit-placement)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`customKpi*` | Required | A custom key wrapper for the KPI data.
`customKpi*.mapKpi` | `False` | The `mapKpi` flag allows designers to specify up to six parameters that are displayed on a permanent grid in the "**Map**" view. The grid layout (rows *x* columns) changes with the number of parameters present in the data, scaling up to 2 rows and 3 columns.
`customKpi*.type` | `'num'` | As a direct child of `customKpi*`, the `type` key defines the UI construct used to render the KPI and restricts the set of key-value pairs that can be used with this type.
`customKpi*.value` | | The actual value of the KPI.
<a name="variant">`customKpi*.variant`</a> | | Used to modify the UI for a given KPI `type`. The presentation to the end user changes, but the `value`s should remain with the same structure. For example, you can modify the appearance of a `'head'` KPI in terms of the orientation of its related items (`'column'` or `'row'`).

## KPI `type`s and their `variant`s:

### `'head'`
Allows users to place a header for an individual section, containing a title (via [`name`](common_keys.md#name)) and a [`help`](#help) message. The `mapKpi` and `value` keys are ignored when used along this type.
#### Variants:
>`'column'` (**default**): Acts as a header for a column of related KPI items.<br>
`'row'`: Acts as a header for a row of related KPI items.<br>

### `'num'`
Displays a numeric value. All keys are valid to use with this type.

### `'text'`
Displays a text string.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"kpis": {
    "data": {
        "kpiHeader1": {
            "type": "head",
            "name": "Example KPI Header 1",
            "icon": "bs/BsInboxes",
        },
        "kpiHeader2": {
            "type": "head",
            "name": "Example KPI Header 2",
            "icon": "bs/BsTruck",
        },
        "key1": {
            "name": "KPI Example 1",
            "value": 18,
            "icon": "bs/BsFillEmojiFrownFill",
            "mapKpi": True,
            "precision": 0,
            "unit": "frowns",
        },
        "key2": {
            "name": "KPI Example 2",
            "icon": "bs/BsFillEmojiSmileFill",
            "value": 32,
            "mapKpi": True,
            "precision": 0,
            "unit": "smiles",
        },
        "key3": {
            "name": "KPI Example 3",
            "icon": "bs/BsInboxes",
            "value": 100,
            "precision": 4,
            "trailingZeros": True,
            "unit": "units",
        },
        "key4": {
            "name": "A Big Number",
            "icon": "bs/BsTruck",
            "value": 10000000000000,
            "precision": 0,
            "unit": "units",
        },
        "key5": {
            "name": "A Really Big Number",
            "icon": "md/MdExpand",
            "value": 9007199254740991,
            "precision": 2,
            "trailingZeros": False,
            "unit": "$",
            "unitPlacement": "before",
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
