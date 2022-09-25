### `arcs`
The `arcs` group contains data that is typically used to visualize information flows between two locations in the "**Map**" view. Depending on the nature of the flows and the purpose of the visualization, the flows between two locations can be represented by a single arc (source and destination) or a sequence of arc segments representing a [`path`](#path).

The structure of an `arcs` group looks as follows:
```py
'arcs': {
    'name': 'A name that will be displayed in the map legend.',
    'types': {
        'custom_arc_type_1': {
            'name': 'A name to be displayed in the UI',
            'colorByOptions': {
              'custom_prop_key_10': {
                'min': 0,
                'max': 25,
                'startGradientColor': {
                    'dark': 'rgb(233, 0, 0)',
                    'light': 'rgb(52, 52, 236)',
                },
                'endGradientColor': {
                    'dark': 'rgb(96, 2, 2)',
                    'light': 'rgb(23, 23, 126)',
                },
              },
              'custom_prop_key_11': {
                'min': 0,
                'max': 35,
                'startGradientColor': {
                    'dark': 'rgb(233, 0, 0)',
                    'light': 'rgb(52, 52, 236)',
                },
                'endGradientColor': {
                    'dark': 'rgb(96, 2, 2)',
                    'light': 'rgb(23, 23, 126)',
                },
              },
              'custom_prop_key_12': {
                'custom_color_key_1':'rgb(233,0,0)',
                'custom_color_key_2':'rgb(0,233,0)'
              }
            },
            'colorBy': 'custom_prop_key_10',
            'lineBy': 'dotted',
            'sizeByOptions': {
              'custom_prop_key_10': {'min': 0, 'max': 25},
              'custom_prop_key_11': {'min': 0, 'max': 35}
            },
            'sizeBy': 'custom_prop_key_10',
            'startSize': '15px',
            'endSize': '30px',
            'props': {
                'custom_prop_key_10': {
                    'name': 'A name to be displayed in the UI',
                    'type': 'num',
                    'enabled': False,
                    'help': 'A help text for the numeric input',
                    'numberFormat': {
                        'precision': 0,
                        'unit': 'units',
                    },
                },
                # As many default props as needed
            },
            'order': 1,
        },
        'custom_arc_type_2': {...},
        # As many arc types as needed
    },
    'data': {
        'custom_arc_data_1': {
            'startLatitude': 43.78,
            'startLongitude': -79.63,
            'endLatitude': 39.82,
            'endLongitude': -86.18,
            'startClick': 800,
            'endClick': 1600,
            'type': 'custom_arc_type_1',
            'category': {
                'custom_data_chunk_1': [
                    'custom_data_key_2',
                    'custom_data_key_3'
                ],
                'custom_data_chunk_2': [
                    'custom_data_key_1',
                    'custom_data_key_4',
                ],
                # As many data chunks as needed
            },
            'props': {
                'custom_prop_key_10': {
                    'value': 50,
                    'variant': 'slider',
                },
                'custom_prop_key_11': {
                    'name': 'A name to be displayed in the UI',
                    'type': 'num',
                    'value': 40,
                    'enabled': False,
                    'help': 'A help text for the numeric input',
                    'numberFormat': {
                        'unit': 'units',
                    },
                },
            },
        },
        'custom_arc_data_2': {
            'path': [
                [-122.3535851, 37.9360513, 1],
                [-122.3179784, 37.9249513, 1.2],
                [-122.300284, 37.902646, 1.4],
                [-122.2843653, 37.8735039, 1.65],
                [-122.269058, 37.8694562, 2],
            ],
            'startClick': 200,
            'endClick': 1000,
            'type': 'custom_arc_type_2',
            'category': {
                'custom_data_chunk_1': [
                    'custom_data_key_1',
                    'custom_data_key_3'
                ],
                'custom_data_chunk_2': [
                    'custom_data_key_2',
                    'custom_data_key_4',
                ],
                # As many data chunks as needed
            },
            'props': {
                'custom_prop_key_10': {
                    'value': 20,
                    'variant': 'slider',
                },
                'custom_prop_key_12': {
                    'name': 'A name to be displayed in the UI',
                    'type': 'num',
                    'value': 30,
                    'enabled': False,
                    'help': 'A help text for the numeric input',
                    'numberFormat': {
                        'unit': 'units',
                    },
                },
            },
        },
        'custom_arc_data_3': {...},
        # As many arc data chunks as needed
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`category`](#category)
- [`colorBy`](#colorBy)
- [`colorByOptions`](#colorByOptions)
- [`column`](#column)
- [`data`](#data)
- [`enabled`](#enabled)
- [`endGradientColor`](#endGradientColor)
- [`endSize`](#endSize)
- [`help`](#help)
- [`name`](#name)
- [`numberFormat`](#number-format)
- [`order`](#order)
- [`prop > type`](#prop-type)
- [`props`](#props)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)
- [`sizeBy`](#sizeBy)
- [`sizeByOptions`](#sizeByOptions)
- [`startSize`](#startSize)
- [`startGradientColor`](#startGradientColor)
- [`value`](#value)
- [`variant`](#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="arc-data-point">`data.custom_arc_data_*`</a> | Required | A custom key wrapper for the parameters required to visualize an arc flow and the data associated with it in the "**Map**" view.
`data.custom_arc_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](#custom_data_chunk_).
`data.custom_arc_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](#custom_data_key_).
`data.custom_arc_data_*.endAltitude` | | The altitude (in meters) for the target location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.endClick`<br>(*Under construction*) | | Related to the animation frame rate of an arc layer. It takes an integer value.
`data.custom_arc_data_*.endLatitude` | Required | The latitude for the target location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.endLongitude` | Required | The longitude for the target location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.height` | `1` | The height multiplier relative to the distance between two points for the apex of a `3d` (lineBy) arc. For example, a value of `0` would turn a `3d` (lineBy) arc into the equivalent to a `solid` (lineBy) arc.
`data.custom_arc_data_*.name` | | A name for the arc flow that will be displayed as a title in the map modal.
<a name="path">`data.custom_arc_data_*.path`</a> | | A list of coordinate points (`[<longitude>, <latitude>]`), such that every two consecutive coordinates represent an arc segment of a path to be rendered in the "**Map**" view. Additionally, a third position can be added to each coordinate (`[<longitude>, <latitude>, <altitude>]`), to visually represent altitude on the map.<br><br>Please note that `path` is not supported for `3d` arcs. If you need to create a "`3d` path", you can do so by joining multiple arcs which start and end coordinates match the segments of the intended path.<br><br>The use of `path` overrides any behavior resulting from the use of the following `data.custom_arc_data_*.` keys: `startLongitude`, `startLatitude`, `startAltitude`, `endLongitude`, `endLatitude`, and `endAltitude`.
`data.custom_arc_data_*.props`&swarhk;<br>`.custom_prop_key_*` | | See [`custom_prop_key_*`](#custom_prop_key_).
`data.custom_arc_data_*.startAltitude` | | The altitude (in meters) for the source location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.startClick`<br>(*Under construction*) | | Related to the animation frame rate of an arc layer. It takes an integer value.
`data.custom_arc_data_*.startLatitude` | Required | The latitude for the source location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.startLongitude` | Required | The longitude for the source location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.type` | Required | The `type` key sets the arc type of `custom_arc_data_*` to a `custom_arc_type_*` key, to match specific visualization preferences for an arc flow.
`types` | Required | The `types` key allows you to define different arc types in terms of styling and data viz settings.
<a name="arc-type">`types.custom_arc_type_*`</a> | | A wrapper for key-value pairs that match a specific set of data viz preferences for an arc flow.
`types.custom_arc_type_*.lineBy` | `'solid'` | The pattern of dashes and gaps used to form the shape of an arc's stroke. It takes one of the following values: `'dashed'`, `'dotted'`, `'solid'`, or `'3d'`. This can be set in individual arcs to overwrite the default for the type.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'arcs': {
    'data': {
        'arc_1': {
            'type': 'Supply',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'value': 500,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'value': 'Campinas - Sao Paulo Airport',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 15,
                    'enabled': False,
                },
            },
            'layout': {
                'type': 'grid',
                'num_columns': 1,
                'num_rows': 'auto',
                'data': {
                    'transportation_mode': {
                        'type': 'item',
                        'itemId': 'Transportation Mode',
                        'row': 2,
                    },
                    'throughput_pallets': {
                        'type': 'item',
                        'itemId': 'Throughput (pallets)',
                        'row': 3,
                    },
                    'origin_and_destination': {
                        'type': 'item',
                        'itemId': 'Origin and destination',
                        'row': 1,
                    },
                    'transportation_cost_k': {
                        'type': 'item',
                        'itemId': 'Transportation Cost (k$)',
                    },
                },
            },
            'category': {'Product': ['LowVal'], 'Location': ['loc_US_MI']},
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': -23.565,
            'endLongitude': -46.632,
            'startLatitude': -22.934,
            'startLongitude': -47.093,
        },
        'arc_2': {
            'type': 'Supply',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'value': 1498.3,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'value': 'Phoenix - Atlanta',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 292.2,
                    'enabled': False,
                },
            },
            'layout': {
                'type': 'grid',
                'num_columns': 1,
                'num_rows': 'auto',
                'data': {
                    'transportation_mode': {
                        'type': 'item',
                        'itemId': 'Transportation Mode',
                        'row': 2,
                    },
                    'throughput_pallets': {
                        'type': 'item',
                        'itemId': 'Throughput (pallets)',
                        'row': 3,
                    },
                    'origin_and_destination': {
                        'type': 'item',
                        'itemId': 'Origin and destination',
                        'row': 1,
                    },
                    'transportation_cost_k': {
                        'type': 'item',
                        'itemId': 'Transportation Cost (k$)',
                    },
                },
            },
            'category': {'Product': ['HighVal'], 'Location': ['loc_US_MI']},
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': 34.037,
            'endLongitude': -84.235,
            'startLatitude': 33.448,
            'startLongitude': -112.074,
        },
        'arc_3': {
            'type': 'Interfacility',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'value': 843.2,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'value': 'Atlanta - Florence, South Carolina',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 27.6,
                    'enabled': False,
                },
            },
            'layout': {
                'type': 'grid',
                'num_columns': 1,
                'num_rows': 'auto',
                'data': {
                    'transportation_mode': {
                        'type': 'item',
                        'itemId': 'Transportation Mode',
                        'row': 2,
                    },
                    'throughput_pallets': {
                        'type': 'item',
                        'itemId': 'Throughput (pallets)',
                        'row': 3,
                    },
                    'origin_and_destination': {
                        'type': 'item',
                        'itemId': 'Origin and destination',
                        'row': 1,
                    },
                    'transportation_cost_k': {
                        'type': 'item',
                        'itemId': 'Transportation Cost (k$)',
                    },
                },
            },
            'category': {
                'Product': ['LowVal', 'HighVal'],
                'Location': ['loc_US_MI'],
            },
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': 34.198,
            'endLongitude': -79.767,
            'startLatitude': 34.037,
            'startLongitude': -84.235,
        },
        'arc_4': {
            'type': 'Interfacility',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'value': 485.2,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'value': 'Atlanta - Jacksonville',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 16.9,
                    'enabled': False,
                },
            },
            'layout': {
                'type': 'grid',
                'num_columns': 1,
                'num_rows': 'auto',
                'data': {
                    'transportation_mode': {
                        'type': 'item',
                        'itemId': 'Transportation Mode',
                        'row': 2,
                    },
                    'throughput_pallets': {
                        'type': 'item',
                        'itemId': 'Throughput (pallets)',
                        'row': 3,
                    },
                    'origin_and_destination': {
                        'type': 'item',
                        'itemId': 'Origin and destination',
                        'row': 1,
                    },
                    'transportation_cost_k': {
                        'type': 'item',
                        'itemId': 'Transportation Cost (k$)',
                    },
                },
            },
            'category': {
                'Product': ['LowVal', 'HighVal'],
                'Location': ['loc_US_MI'],
            },
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': 30.332,
            'endLongitude': -81.656,
            'startLatitude': 34.037,
            'startLongitude': -84.235,
        },
    },
    'name': 'Transportation flows',
    'types': {
        'Supply': {
            'lineBy': 'solid',
            'sizeBy': 'Transportation Cost (k$)',
            'colorBy': 'Throughput (pallets)',
            'endSize': '10px',
            'startSize': '7px',
            'sizeByOptions': {
              'Throughput (pallets)': {'min': 0, 'max': 5000},
              'Transportation Cost (k$)': {'min': 5, 'max': 2000}
            },
            'colorByOptions': {
              'Throughput (pallets)': {
                'min': 0,
                'max': 5000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              },
              'Transportation Cost (k$)': {
                'min': 5,
                'max': 2000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              }
            },
        },
        'Interfacility': {
            'lineBy': 'solid',
            'sizeBy': 'Transportation Cost (k$)',
            'colorBy': 'Throughput (pallets)',
            'endSize': '7px',
            'startSize': '3px',
            'sizeByOptions': {
              'Throughput (pallets)': {'min': 0, 'max': 2000},
              'Transportation Cost (k$)': {'min': 5, 'max': 1000}
            },
            'colorByOptions': {
              'Throughput (pallets)': {
                'min': 0,
                'max': 2000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              },
              'Transportation Cost (k$)': {
                'min': 5,
                'max': 1000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              }
            },
        },
    },
}
```
</details>