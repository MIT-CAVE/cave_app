# `categories`
Both designers and users often need to work with different levels of data aggregation. the `categories` top level key allows for easy and arbitrary aggregation/filtering of data in the UI. They are a core aspect for how chart groupings, chart subgroupgings and general filtering works.

Below is an example of the `categories` top level key:
```py
'categories': {
    'allowModification': False,
    'sendToApi': False,
    'sendToClient': True,
    'data': {
        'customCategory1': {  # Inside a category group
            'name': 'A name to be displayed in the UI',
            'data': {
                'customDataChunk1': {
                    'customDataKey1': 'customDataValue1',
                    'customDataKey2': 'customDataValue2',
                    'customDataKey3': 'customDataValue3',
                },
                'customDatachunk2': {
                    'customDataKey1': 'customDataValue4',
                    'customDataKey2': 'customDataValue5',
                    'customDataKey3': 'customDataValue6',
                },
                # As many data chunks as needed
            },
            'nestedStructure': {
                'customDataKey1': {
                    'name': 'A name to be displayed in the UI'
                    # Optional ordering (the default is alphabetical)
                    'ordering': [
                        'customDataValue1',
                        'customDataValue4',
                    ],
                    'order': 1,
                },
                'customDataKey2': {...},
                'customDataKey3': {...},
                'customDataKey4': {...},
                # As many data keys as defined within the data chunks
            },
            'layoutDirection': 'horizontal',
            'order': 2,
        },
        'customCategory2': {...},
        # As many categories as needed
    },
}
```

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`data`](../common_keys/common_keys.md#data)
- [`name`](../common_keys/common_keys.md#name)
- [`order`](../common_keys/common_keys.md#order)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="customCategory">`customCategory*`</a> | Required | A custom key for categorical data. Each `customCategory*` key encloses a well-defined structure. This represents a higher level structure for filtering and aggregation purposes. A simple example is geography which can be represented by a nested structure (`township` &rarr; `state` &rarr; `country` &rarr; `continent`).
`customCategory*.data` | | Dictionary object that contains `customDataChunck*` items.
<a name="customDataChunck">`customCategory*.data.customDataChunck*`</a> | | A wrapper for key-value pairs that are grouped by any categorical context set by the designer. This represents the smallest level of aggregation. For example, an app that groups data geographically to the township level would need one data chunk per township they want to represent.
<a name="customDataKey">`customCategory*.data`&swarhk;<br>`.customDataChunck*.customDataKey*`<br><br>or<br><br>`customCategory*.nestedStructure`&swarhk;<br>`.customDataChunck*.customDataKey*`</a> | | A data property representing a specific group level of data. Following our geographic example, there should be four custom data keys (`township`, `state`, `country` and `continent`) per custom data chunk.
`customCategory*.data`&swarhk;<br>`.customDataKey*.customDataValue*` | | A match value for `customDataKey*`. Can either be string, numeric or boolean. Given our geographic example, a custom data key named `township` could have a data value of `'cambridge'` or any other township.
`customCategory*.layoutDirection` | `'vertical'` | The direction in which `customDataKey*`s appear in the "**Group By**" drop-down menu of a chart. It can be `'horizontal'` or `'vertical'`. If omitted, the items will be displayed vertically in the UI.
`customCategory*.nestedStructure` | Required | A container dictionary for specifying the rendering properties of the items that are displayed in the "**Group By**" drop-down menu of a chart in a dashboard view.
`customCategory*.nestedStructure`&swarhk;<br>`.customDataKey*.ordering` | | A special key of a [`customDataChunck*`](#customDataChunck) that sets the position in which the `customDataValue*`s contained in the data chunk are rendered in the "**Group By**" drop-down menu of a chart. Its value is a list of strings in which the order of `customDataValue*`s is determined by their indices in the list (ascending order). All values that are not included in the list will be sorted alphabetically and placed after the values that are actually present.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"categories": {
    "allowModification": False,
    "data": {
        "location": {
            "data": {
                "locUsMi": {
                    "region": "North America",
                    "country": "USA",
                    "state": "Michigan",
                },
                "locUsMa": {
                    "region": "North America",
                    "country": "USA",
                    "state": "Massachusetts",
                },
                "locUsFl": {
                    "region": "North America",
                    "country": "USA",
                    "state": "Florida",
                },
                "locUsIn": {
                    "region": "North America",
                    "country": "USA",
                    "state": "Indiana",
                },
                "locCaOn": {
                    "region": "North America",
                    "country": "Canada",
                    "state": "Ontario",
                },
            },
            "name": "Locations",
            "nestedStructure": {
                "region": {
                    "name": "Regions",
                    "order": 1,
                },
                "country": {
                    "name": "Countries",
                    "ordering": ["USA", "Canada"],
                    "order": 2,
                },
                "state": {
                    "name": "States",
                    "order": 3,
                },
            },
            "layoutDirection": "horizontal",
            "order": 1,
        },
        "sku": {
            "data": {
                "SKU1": {
                    "type": "Type A",
                    "size": "Size A",
                    "sku": "SKU1",
                },
                "SKU2": {
                    "type": "Type A",
                    "size": "Size B",
                    "sku": "SKU2",
                },
            },
            "name": "SKUs",
            "nestedStructure": {
                "type": {
                    "name": "Types",
                    "order": 1,
                },
                "size": {
                    "name": "Sizing",
                    "ordering": ["Type B", "Type A"],
                    "order": 2,
                },
                "sku": {
                    "name": "SKU",
                    "order": 3,
                },
            },
            "layoutDirection": "horizontal",
            "order": 2,
        },
    },
}
```
</details>