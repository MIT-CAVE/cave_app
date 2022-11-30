### `stats`
The `stats` group takes parameter data that can be combined with geospatial data to represent it in the "**Map**" view or simply use its raw values to display in a dashboard view.

Let's look inside the structure of `stats`:
```py
'stats': {
    'name': 'Statistics',
    'types': {
        'custom_stat_key_1': {
            'name': 'A name to be displayed in the UI',
            'calculation': 'custom_stat_key_1 / custom_stat_key_2',
            'numberFormat': {
                'unit': 'units',
            },
            'order': 1,
        },
        'custom_stat_key_2': {...},
        # As many stats as needed
    },
    'data': {
        'custom_stat_data_1': {
            'category': {
                'custom_data_chunk_1': [
                    'custom_data_key_2',
                    'custom_data_key_4'
                ],
                'custom_data_chunk_2': [
                    'custom_data_key_1',
                    'custom_data_key_3',
                ],
                # As many data chunks as needed
            },
            'values': {
                'custom_stat_key_1': 3,
                'custom_stat_key_2': 8,
                # As many stat keys as needed
            },
        },
        'custom_stat_data_2': {...},
        # As many stat data chunks as needed
    },
}
```

##### Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`category`](../common_keys/common_keys.md#category)
- [`data`](../common_keys/common_keys.md#data)
- [`name`](../common_keys/common_keys.md#name)
- [`numberFormat`](../common_keys/common_keys.md#number-format)
- [`order`](../common_keys/common_keys.md#order)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`data.custom_stat_data_*` | Required | A custom key wrapper for the [`category`](../common_keys/common_keys.md#category) and [`values`](#values) keys.
`data.custom_stat_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](categories.md#custom_data_chunk_).
`data.custom_stat_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](categories.md#custom_data_key_).
<a name="values">`data.custom_stat_data_*.values`</a> | Required | A wrapper for independent `custom_stat_key_*`s and their values.
<a name="custom_stat_key_">`types.custom_stat_key_*`</a> | Required | A key used to identify a parameter in a `calculation` expression and be referenced by the `values` group.
`types` | Required | The `types` key allows you to define the appearance and logic of the `custom_stat_key_*` parameters.
`types.custom_stat_key_*.calculation` | Required | Defines a math expression that allows the calculation of a `custom_stat_key_*` parameter that depends on the value of others. The expression is used to dynamically estimate the value of a parameter when the data containing its independent stats used in the calculation, has changed, e.g. after applying a filter. When a custom stat is independent, the math expression must match its own `custom_stat_key_*`. The CAVE App comes with a software package that provides built-in support for common math functions and operators. For a list of the available operators and examples of math expressions, see the [`expr-eval` documentation](https://github.com/silentmatt/expr-eval#documentation) and [`groupSum`](#groupsum) below.

##### `groupSum`
`groupSum` is a special function provided by the CAVE app that takes an independent stat as input and outputs the sum of that stat across the level (or sub-level if present) specified by the user or API for that [dashboard](#dashboards) chart. Using `groupSum` is different than other [`expr-eval`](https://github.com/silentmatt/expr-eval) functions as the variable must be passed as a string rather than a literal, e.g. **`groupSum("custom_stat")`** (not `groupSum(custom_stat)`). When using `groupSum` special consideration should be given to ensure the the dashboard grouping (sum, minimum, maximum, or average) makes it clear to users what the stat represents, as while `groupSum` sums across the level the stat calculation is still done to the individual stats which are then grouped.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'stats': {
    'name': 'Statistics',
    'types': {
        'demand_met': {
            'name': 'Demand Met',
            'calculation': 'demand_met',
            'numberFormat': {
                'unit': 'units',
            },
            'order': 1,
        },
        'demand_tot': {
            'name': 'Demand Total',
            'calculation': 'demand_tot',
            'numberFormat': {
                'unit': 'units',
            },
            'order': 2,
        },
        'demand_pct': {
            'name': 'Demand Percentage',
            'calculation': 'demand_met / groupSum("demand_tot")',
            'numberFormat': {
                'unit': '%',
                'unitSpace': False,
            },
            'order': 3,
        },
    },
    'data': {
        'd1': {
            'category': {
                'Location': ['loc_CA_ON'],
                'Product': ['prd_abc123'],
            },
            'values': {
                'demand_met': 5,
                'demand_tot': 10,
            },
        },
        'd2': {
            'category': {
                'Location': ['loc_CA_ON'],
                'Product': ['prd_def456'],
            },
            'values': {
                'demand_met': 4,
                'demand_tot': 5,
            },
        },
        'd3': {
            'category': {
                'Location': ['loc_US_MI'],
                'Product': ['prd_abc123'],
            },
            'values': {
                'demand_met': 6,
                'demand_tot': 7,
            },
        },
        'd4': {
            'category': {
                'Location': ['loc_US_MI'],
                'Product': ['prd_def456'],
            },
            'values': {
                'demand_met': 3,
                'demand_tot': 5,
            },
        },
    },
}
```
</details>