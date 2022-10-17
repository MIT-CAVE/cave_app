### `nodes`
The `nodes` group contains data that is typically used to visualize geographic locations in the "**Map**" view.

The structure of a `nodes` group looks as follows:
```py
'nodes': {
    'name': 'A name that will be displayed in the map legend.',
    'types': {
        'custom_node_type_1': {
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
            ,
            'colorBy': 'custom_prop_key_10',
            'sizeByOptions': {
              'custom_prop_key_10': {'min': 0, 'max': 25},
              'custom_prop_key_11': {'min': 0, 'max': 35}
            ,
            'sizeBy': 'custom_prop_key_11',
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
            'icon': 'FaWarehouse',
            'order': 1,
        },
        'custom_node_type_2': {...},
        # As many node types as needed
    },
    'data': {
        'custom_node_data_1': {
            'latitude': 42.361176,
            'longitude': -71.084707,
            'type': 'custom_node_type_2',
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
                },
                'custom_prop_key_11': {
                    'name': 'A name to be displayed in the UI',
                    'type': 'num',
                    'variant': 'slider',
                    'value': 40,
                    'enabled': False,
                    'help': 'A help text for the numeric input',
                    'numberFormat': {
                        'unit': 'units',
                    },
                },
                'custom_prop_key_12': {
                    'type': 'toggle',
                    'value': True,
                    'enabled': False,
                    'help': 'A help text for this toggle'
                },
            },
            'layout': {...},
        },
        'custom_node_data_2': {...},
        # As many node data chunks as needed
    },
}
```

##### Common keys
- [`allow_modification`](../common_keys/common_keys.md#allow_modification)
- [`category`](../common_keys/common_keys.md#category)
- [`colorBy`](../common_keys/common_keys.md#colorBy)
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
- [`order`](../common_keys/common_keys.md#order)
- [`prop > type`](../common_keys/props.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`send_to_api`](../common_keys/common_keys.md#send_to_api)
- [`send_to_client`](../common_keys/common_keys.md#send_to_client)
- [`sizeBy`](../common_keys/common_keys.md#sizeBy)
- [`sizeByOptions`](../common_keys/common_keys.md#sizeByOptions)
- [`startSize`](../common_keys/common_keys.md#startSize)
- [`startGradientColor`](../common_keys/common_keys.md#startGradientColor)
- [`value`](../common_keys/props.md#value)
- [`variant`](../common_keys/props.md#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="node-data-point">`data.custom_node_data_*`</a> | Required | A custom key wrapper for the parameters required to visualize a node and the data associated with it in the "**Map**" view.
`data.custom_node_data_*.altitude` | `1` | The altitude of the node (in meters) above sea level. Defaults to 1 to appear on top of `geo` layers.
`data.custom_node_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](categories.md#custom_data_chunk_).
`data.custom_node_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](categories.md#custom_data_key_).
`data.custom_node_data_*.latitude` | Required | The latitude of the node location in the "**Map**" view. It takes a float value.
`data.custom_node_data_*.longitude` | Required | The longitude of the node location in the "**Map**" view. It takes a float value.
`data.custom_node_data_*.name` | | A name for the node location that will be displayed as a title in the map modal.
`data.custom_node_data_*.props`&swarhk;<br>`.custom_prop_key_*` | | See [`custom_prop_key_*`](../common_keys/props.md#custom_prop_key_).
`data.custom_node_data_*.type` | Required | The `type` key sets the node type of `custom_node_data_*` to a `custom_node_type_*` key, to match specific visualization preferences for a node.
`types` | Required | The `types` key allows you to define different types of nodes in terms of styling and data viz settings.
<a name="node-type">`types.custom_node_type_*`</a> | | A wrapper for key-value pairs that match a specific set of data viz preferences for a node.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'nodes': {
    'data': {
        'Brazilian': {
            'type': 'Manufacturer',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate or deactivate the manufacturer.',
                    'type': 'toggle',
                    'value': True,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'value': 'Campinas, Brazil',
                    'output': False,
                    'enabled': False,
                },
                'Product family': {
                    'help': 'Product family produced by the manufacturer.',
                    'type': 'text',
                    'value': 'LowVal',
                    'output': False,
                    'enabled': False,
                },
                'Transportation Modes': {
                    'cost': False,
                    'help': 'Type of transportation modes that can be used for the manufacturer.',
                    'type': 'selector',
                    'radio': True,
                    'value': {'Air': True, 'Sea': False},
                    'enabled': True,
                },
                'Manufacturing Cost ($/pallet)': {
                    'help': 'Manufacturing cost per pallet.',
                    'type': 'num',
                    'value': 450,
                    'output': False,
                    'enabled': False,
                },
                'Production acquired (pallets)': {
                    'help': 'Quantity purchased from the manufacturer, larger than or equal to the minimum order.',
                    'type': 'num',
                    'value': 500,
                    'output': True,
                    'enabled': False,
                },
                'Min Order / Max Capacity (pallets)': {
                    'help': 'Minimum quantity to be purchased if active / Maximum production capacity.',
                    'type': 'num',
                    'value': '500 / 7000',
                    'output': False,
                    'enabled': False,
                },
            },
            'layout': {
                'type': 'grid',
                'num_columns': 1,
                'num_rows': 'auto',
                'data': {
                    'active': {
                        'type': 'item',
                        'itemId': 'Active',
                        'row': 3,
                    },
                    'location': {
                        'type': 'item',
                        'itemId': 'Location',
                        'row': 1,
                    },
                    'product_family': {
                        'type': 'item',
                        'itemId': 'Product family',
                        'row': 2,
                    },
                    'transportation_modes': {
                        'type': 'item',
                        'itemId': 'Transportation Modes',
                        'row': 7,
                    },
                    'manufacturing_cost_per_pallet': {
                        'type': 'item',
                        'itemId': 'Manufacturing Cost ($/pallet)',
                    },
                    'production_acquired': {
                        'type': 'item',
                        'itemId': 'Production acquired (pallets)',
                        'row': 6,
                    },
                    'min_order_max_capacity': {
                        'type': 'item',
                        'itemId': 'Min Order / Max Capacity (pallets)',
                    },
                },
            },
            'category': {'Manufacturer': ['Brazilian']},
            'latitude': -22.934,
            'longitude': -47.093,
        },
        'Atlanta DC': {
            'type': 'Distribution Center',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate/open or deactivate/close the distribution center.',
                    'type': 'toggle',
                    'value': True,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'value': 'Atlanta, US',
                    'output': False,
                    'enabled': False,
                },
                'Fixed Cost (k$)': {
                    'help': 'Fixed cost of the distribution center.',
                    'type': 'num',
                    'value': '360.0',
                    'output': False,
                    'enabled': False,
                },
                'Capacity (pallets)': {
                    'help': 'Maximum capacity of the distribution center.',
                    'type': 'num',
                    'value': 17000,
                    'output': False,
                    'enabled': False,
                },
                'Inventory Cost (k$)': {
                    'help': 'Cost of inventory accounting for cycle stock and safety stock.',
                    'type': 'num',
                    'value': '6.5',
                    'output': True,
                    'enabled': False,
                },
                'Demand Served (pallets)': {
                    'help': 'Total demand served from the distribution center.',
                    'type': 'num',
                    'value': 1998,
                    'output': True,
                    'enabled': False,
                },
                'Capacity Utilization (%)': {
                    'help': 'Percentage of available capacity occupied.',
                    'type': 'num',
                    'value': 11.75,
                    'output': True,
                    'enabled': False,
                },
                'Transportation cost (k$)': {
                    'help': 'Cost of delivery to warehouses for interfacility flows departing from the distribution center.',
                    'type': 'num',
                    'value': '56.5',
                    'output': True,
                    'enabled': False,
                },
            },
            'category': {'Distribution Center': ['Atlanta DC']},
            'latitude': 34.037,
            'longitude': -84.235,
        },
        'Korean Tiger': {
            'type': 'Manufacturer',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate or deactivate the manufacturer.',
                    'type': 'toggle',
                    'value': False,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'value': 'Daegu, Korea',
                    'output': False,
                    'enabled': False,
                },
                'Product family': {
                    'help': 'Product family produced by the manufacturer.',
                    'type': 'text',
                    'value': 'LowVal',
                    'output': False,
                    'enabled': False,
                },
                'Transportation Modes': {
                    'cost': False,
                    'help': 'Type of transportation modes that can be used for the manufacturer.',
                    'type': 'selector',
                    'radio': True,
                    'value': {'Air': True, 'Sea': False},
                    'enabled': True,
                },
                'Manufacturing Cost ($/pallet)': {
                    'help': 'Manufacturing cost per pallet.',
                    'type': 'num',
                    'value': 300,
                    'output': False,
                    'enabled': False,
                },
                'Production acquired (pallets)': {
                    'help': 'Quantity purchased from the manufacturer, larger than or equal to the minimum order.',
                    'type': 'num',
                    'value': 0,
                    'output': True,
                    'enabled': False,
                },
                'Min Order / Max Capacity (pallets)': {
                    'help': 'Minimum quantity to be purchased if active / Maximum production capacity.',
                    'type': 'num',
                    'value': '800 / 8000',
                    'output': False,
                    'enabled': False,
                },
            },
            'category': {'Manufacturer': ['Korean Tiger']},
            'latitude': 35.871,
            'longitude': 128.602,
        },
        'Reno Warehouse': {
            'type': 'Warehouse',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate/open or deactivate/close the warehouse.',
                    'type': 'toggle',
                    'value': False,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'value': 'Reno, Nevada, US',
                    'output': False,
                    'enabled': False,
                },
                'Fixed Cost (k$)': {
                    'help': 'Fixed cost of the warehouse, depending on its capacity and accounting for economies of scale.',
                    'type': 'num',
                    'value': '264.2',
                    'output': True,
                    'enabled': False,
                },
                'Capacity (pallets)': {
                    'type': 'num',
                    'value': 4000,
                    'slider': True,
                    'enabled': True,
                    'maxValue': 8000,
                    'minValue': 2000,
                },
                'Inventory Cost (k$)': {
                    'help': 'Cost of inventory accounting for cycle stock and safety stock.',
                    'type': 'num',
                    'value': '0.0',
                    'output': True,
                    'enabled': False,
                },
                'Demand Served (pallets)': {
                    'help': 'Total demand served from the warehouse.',
                    'type': 'num',
                    'value': 0,
                    'output': True,
                    'enabled': False,
                },
                'Capacity Utilization (%)': {
                    'help': 'Percentage of available capacity occupied.',
                    'type': 'num',
                    'value': 0,
                    'output': True,
                    'enabled': False,
                },
                'Last Mile Distribution Cost (k$)': {
                    'help': 'Cost of delivery to customer locations for routes departing from the warehouse.',
                    'type': 'num',
                    'value': '0.0',
                    'output': True,
                    'enabled': False,
                },
            },
            'category': {'Warehouse': ['Reno Warehouse']},
            'latitude': 39.526,
            'longitude': -119.813,
        },
    },
    'name': 'Nodes',
    'types': {
        'Warehouse': {
            'icon': 'FaSquareFull',
            'sizeBy': 'Capacity (pallets)',
            'colorBy': 'Capacity Utilization (%)',
            'endSize': '17px',
            'startSize': '12px',
            'sizeByOptions': {
                'Capacity (pallets)': {'min': 0, 'max': 2000},
                'Capacity Utilization (%)': {'min': 0, 'max': 99},
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
            'colorByOptions': {
                'Capacity (pallets)': {
                    'min': 0,
                    'max': 2000,
                    'endGradientColor': 'rgb(51, 153, 51)',
                    'startGradientColor': 'rgb(204, 255, 153)',
                },
                'Capacity Utilization (%)': {
                    'min': 0,
                    'max': 99,
                    'endGradientColor': 'rgb(51, 153, 51)',
                    'startGradientColor': 'rgb(204, 255, 153)',
                },
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
        },
        'Manufacturer': {
            'icon': 'BsOctagonFill',
            'sizeBy': 'Production Capacity (pallets)',
            'colorBy': 'Manufacturing Cost ($/pallet)',
            'endSize': '25px',
            'startSize': '15px',
            'sizeByOptions': {
                'Capacity (pallets)': {'min': 0, 'max': 2000},
                'Capacity Utilization (%)': {'min': 0, 'max': 99},
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
            'colorByOptions': {
                'Capacity (pallets)': {
                    'min': 0,
                    'max': 2000,
                    'endGradientColor': 'rgb(255, 0, 0)',
                    'startGradientColor': 'rgb(255, 204, 153)',
                },
                'Capacity Utilization (%)': {
                    'min': 0,
                    'max': 99,
                    'endGradientColor': 'rgb(255, 0, 0)',
                    'startGradientColor': 'rgb(255, 204, 153)',
                },
                'Fixed Cost (k$)': {
                    'min': 0,
                    'max': 200,
                    'endGradientColor': 'rgb(255, 0, 0)',
                    'startGradientColor': 'rgb(255, 204, 153)',
                },
            },
        },
        'Distribution Center': {
            'icon': 'BsTriangleFill',
            'sizeBy': 'Capacity (pallets)',
            'colorBy': 'Capacity Utilization (%)',
            'endSize': '25px',
            'startSize': '15px',
            'sizeByOptions': {
                'Capacity (pallets)': {'min': 0, 'max': 2000},
                'Capacity Utilization (%)': {'min': 0, 'max': 99},
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
            'colorByOptions': {
                'Capacity (pallets)': {
                    'min': 0,
                    'max': 2000,
                    'endGradientColor': 'rgb(0, 0, 255)',
                    'startGradientColor': 'rgb(102, 255, 255)',
                },
                'Capacity Utilization (%)': {
                    'min': 0,
                    'max': 99,
                    'endGradientColor': 'rgb(0, 0, 255)',
                    'startGradientColor': 'rgb(102, 255, 255)',
                },
                'Fixed Cost (k$)': {
                    'min': 0,
                    'max': 200,
                    'endGradientColor': 'rgb(0, 0, 255)',
                    'startGradientColor': 'rgb(102, 255, 255)',
                },
            },
        },
    },
}
```
</details>