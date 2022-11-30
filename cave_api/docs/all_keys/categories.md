### `categories`
Both designers and users often need to work with different levels of data aggregation and allow for filtering of that data in the UI. The `categories` group allows for easy aggregation and filtering for end users.

Below is an example of the `categories` group:
```py
'categories': {
    'allowModification': False,
    'sendToApi': False,
    'sendToClient': True,
    'data': {
        'custom_category_1': {  # Inside a category group
            'data': {
                'custom_data_chunk_1': {
                    'custom_data_key_1': 'data_value_1',
                    'custom_data_key_2': 'data_value_2',
                    'custom_data_key_3': 'data_value_3',
                },
                'custom_data_chunk_2': {
                    'custom_data_key_1': 'data_value_4',
                    'custom_data_key_4': 'data_value_5',
                },
                # As many data chunks as needed
            },
            'name': 'A name to be displayed in the UI',
            'nestedStructure': {
                'custom_data_key_1': {
                    'name': 'A name to be displayed in the UI'
                    'ordering': [
                        'data_value_3',
                        'data_value_1',
                        'data_value_2',
                    ],
                    'order': 1,
                },
                'custom_data_key_2': {...},
                'custom_data_key_3': {...},
                'custom_data_key_4': {...},
                # As many data keys as defined within the data chunks
            },
            'layoutDirection': 'horizontal',
            'order': 2,
        },
        'custom_category_2': {...},
        # As many categories as needed
    },
}
```

##### Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`data`](../common_keys/common_keys.md#data)
- [`name`](../common_keys/common_keys.md#name)
- [`order`](../common_keys/common_keys.md#order)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="custom_category_">`custom_category_*`</a> | Required | A custom key for categorical data. Each `custom_category_*` key encloses a well-defined structure. This represents a higher level structure for filtering and aggregation purposes. A simple example is geography which can be represented by a nested structure (`township` &rarr; `state` &rarr; `country` &rarr; `continent`).
`custom_category_*.data` | | Dictionary object that contains `custom_data_chunk_*` items.
<a name="custom_data_chunk_">`custom_category_*.data.custom_data_chunk_*`</a> | | A wrapper for key-value pairs that are grouped by any categorical context set by the designer. This represents the smallest level of aggregation. For example, an app that groups data geographically to the township level would need one data chunk per township they want to represent.
<a name="custom_data_key_">`custom_category_*.data`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*`<br><br>or<br><br>`custom_category_*.nestedStructure`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*`</a> | | A data property representing a specific group level of data. Following our geographic example, there should be four custom data keys (`township`, `state`, `country` and `continent`) per custom data chunk.
`custom_category_*.data`&swarhk;<br>`.custom_data_key_*.data_value_*` | | A match value for `custom_data_key_*`. Can either be string, numeric or boolean. Given our geographic example, a custom data key named `township` could have a data value of `'cambridge'` or any other township.
`custom_category_*.layoutDirection` | `'vertical'` | The direction in which `custom_data_key_*`s appear in the "**Group By**" drop-down menu of a chart. It can be `'horizontal'` or `'vertical'`. If omitted, the items will be displayed vertically in the UI.
`custom_category_*.nestedStructure` | Required | A container dictionary for specifying the rendering properties of the items that are displayed in the "**Group By**" drop-down menu of a chart in a dashboard view.
`custom_category_*.nestedStructure`&swarhk;<br>`.custom_data_key_*.ordering` | | A special key of a [`custom_data_chunk_*`](#custom_data_chunk_) that sets the position in which the `data_value_*`s contained in the data chunk are rendered in the "**Group By**" drop-down menu of a chart. Its value is a list of strings in which the order of `data_value_*`s is determined by their indices in the list (ascending order). All values that are not included in the list will be sorted alphabetically and placed after the values that are actually present.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'categories': {
    'allowModification': False,
    'sendToApi': False,
    'sendToClient': True,
    'data': {
        'Location': {
            'data': {
                'loc_US_MI': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Michigan',
                },
                'loc_US_MA': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Massachusetts',
                },
                'loc_US_FL': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Florida',
                },
                'loc_US_IN': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Indiana',
                },
                'loc_CA_ON': {
                    'Region': 'North America',
                    'Country': 'Canada',
                    'State': 'Ontario',
                },
            },
            'name': 'Locations',
            'nestedStructure': {
                'Region': {
                    'name': 'Regions',
                    'order': 1,
                },
                'Country': {
                    'name': 'Countries',
                    'ordering': ['USA', 'Canada'],
                    'order': 2,
                },
                'State': {
                    'name': 'States',
                    'order': 3,
                },
            },
            'layoutDirection': 'horizontal',
            'order': 1,
        },
        'Product': {
            'data': {
                'prd_abc123': {
                    'Type': 'Fruit',
                    'Size': 'Big',
                    'Product': 'Apple'
                },
                'prd_def456': {
                    'Type': 'Fruit',
                    'Size': 'Small',
                    'Product': 'Grape',
                },
            },
            'name': 'Products',
            'nestedStructure': {
                'Type': {
                    'name': 'Types',
                    'order': 1,
                },
                'Size': {
                    'name': 'Sizing',
                    'ordering': ['Small', 'Big'],
                    'order': 2,
                },
                'Product': {
                    'name': 'Products',
                    'order': 3,
                },
            },
            'layoutDirection': 'horizontal',
            'order': 2,
        },
    },
}
```
</details>