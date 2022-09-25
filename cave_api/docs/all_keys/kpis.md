### `kpis`
The `kpis` group contains all the KPI data that will be displayed on the "**KPI**" view.

Let's look inside the structure of `kpis`:
```py
'kpis': {
    'data': {
        'custom_kpi_1': {
            'name': 'A name to be displayed in the UI',
            'numberFormat': {
                'unit': 'units',
            },
            'type': 'num',
            'icon': 'FaBox',
            'value': 100,
            'map_kpi': True,
        },
        # As many custom KPIs as needed
    },
    'layout': {...},
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`column`](#column)
- [`data`](#data)
- [`icon`](#icon)
- [`layout`](#layout)
- [`name`](#name)
- [`numberFormat`](#number-format)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`custom_kpi_*` | Required | A custom key wrapper for the KPI data.
`custom_kpi_*.map_kpi` | `False` | The `map_kpi` flag allows designers to specify up to six parameters that are displayed on a permanent grid in the "**Map**" view. The grid layout (rows *x* columns) changes with the number of parameters present in the data, scaling up to 2 rows and 3 columns.
`custom_kpi_*.type` | `'num'` | As a direct child of `custom_kpi_*`, the `type` key defines the UI construct used to render the KPI and restricts the set of key-value pairs that can be used with this type. The `type` key takes one of the following values:<br><br>`'head'`: the `map_kpi`, [`numberFormat`](#numberFormat), and `value` keys are ignored when used along this type.<br>`'num'`: all keys are valid to use with this type.<br>`'text'`: the [`numberFormat`](#numberFormat) key is ignored when used along this type.<br>
`custom_kpi_*.value` | | The actual value of the KPI.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'kpis': {
    'data': {
        'demand': {
            'name': 'Global Demand',
            'value': 100,
            'numberFormat': {
                'unit': 'units',
            },
            'icon': 'FaBox',
        },
        'demand_header': {
            'type': 'head',
            'name': 'Demand Section',
            'icon': 'BsInboxes',
        },
        'month_highest_demand': {
            'name': 'Month of highest demand',
            'value': 'December',
            'type': 'text',
            'map_kpi': True,
        },
        'customer_hapiness': {
            'name': 'Customer Happiness',
            'value': 16,
            'numberFormat': {
                'unit': 'smiles',
            },
            'icon': 'BsFillEmojiSmileFill',
            'map_kpi': True,
        },
    },
    'layout': {
        'type': 'grid',
        'num_columns': 1,
        'num_rows': 'auto',
        'data': {
            'row1': {
                'type': 'item',
                'itemId': 'demand_header',
                'row': 1,
            },
            'row2': {
                'type': 'item',
                'itemId': 'demand',
            },
            'row3': {
                'type': 'item',
                'itemId': 'month_highest_demand',
            },
            'row4': {
                'type': 'item',
                'itemId': 'customer_hapiness',
            },            
        },
    },
}
```
</details>