### `geos`
The `geos` group takes in data and renders it as geographic areas on the "**Map**" view, to visualize spatial distribution of parameters.

The internal structure of `geos` is very similar to that of the `arcs` and `nodes` groups. The most relevant discrepancy is the addition of the special key `geoJson`.

Let's look inside the structure of `geos`:
```py
'geos': {
    'name': 'A name that will be displayed in the map legend.',
    'types': {
        'custom_geo_type_1': {
            'name': 'A name to be displayed in the UI',
            'colorByOptions': {
                'custom_prop_key_1': {
                    'min': 0,
                    'max': 60,
                    'startGradientColor': {
                        'dark': 'rgb(233, 0, 0)',
                        'light': 'rgb(52, 52, 236)',
                    },
                    'endGradientColor': {
                        'dark': 'rgb(96, 2, 2)',
                        'light': 'rgb(23, 23, 126)',
                    },
                },
                'custom_prop_key_2': {
                    'min': 0,
                    'max': 40,
                    'startGradientColor': {
                        'dark': 'rgb(233, 0, 0)',
                        'light': 'rgb(52, 52, 236)',
                    },
                    'endGradientColor': {
                        'dark': 'rgb(96, 2, 2)',
                        'light': 'rgb(23, 23, 126)',
                    },
                },
                'custom_prop_key_3': {
                  'custom_color_key_1':'rgb(233,0,0)',
                  'custom_color_key_2':'rgb(0,233,0)'
                }
            },
            'colorBy': 'custom_prop_key_1',
            'geoJson': {
                'geoJsonLayer': 'https://cave-geojsons.s3.amazonaws.com/geojson_data_1.json',
                'geoJsonProp': 'geojson_prop_1',
            },
            'props': {
                'custom_prop_key_1': {
                    'type': 'num',
                    'help': 'A help text for this numeric input',
                    'numberFormat': {
                        'unit': 'units',
                    },
                    'enabled': True,
                },
                'custom_prop_key_2': {...},
                # As many default props as needed
            },
            'icon': 'FaHexagon',
        },
        'custom_geo_type_2': {...},
        # As many geo types as needed
    },
    'data': {
        'custom_geo_data_1': {
            'name': 'A name to be displayed in the UI',
            'geoJsonValue': 'geojson_value_1',
            'type': 'custom_geo_type_1',
            'category': {
                'custom_data_chunk_1': ['custom_data_key_1']
                # As many data chunks as needed
            },
            'props': {
                'custom_prop_key_1': {
                    'value': 60,
                },
                'custom_prop_key_2': {
                    'value': 9.5,
                },
                'custom_prop_key_3': {...},
                # As many custom props as needed
            },
        },
        'custom_geo_data_2': {...},
        # As many geo data chunks as needed
    },
}
```

##### Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`category`](../common_keys/common_keys.md#category)
- [`colorBy`](../common_keys/common_keys.md#colorBy)
- [`colorByOptions`](../common_keys/common_keys.md#colorByOptions)
- [`column`](../common_keys/common_keys.md#column)
- [`data`](../common_keys/common_keys.md#data)
- [`enabled`](../common_keys/common_keys.md#enabled)
- [`endGradientColor`](../common_keys/common_keys.md#end-gradient)
- [`help`](../common_keys/props.md#help)
- [`icon`](../common_keys/common_keys.md#icon)
- [`name`](../common_keys/common_keys.md#name)
- [`numberFormat`](../common_keys/common_keys.md#number-format)
- [`order`](../common_keys/common_keys.md#order)
- [`prop > type`](../common_keys/props.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`startGradientColor`](../common_keys/common_keys.md#start-gradient)
- [`value`](../common_keys/props.md#value)
- [`variant`](../common_keys/props.md#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="geo-data-point">`data.custom_geo_data_*`</a> | Required | A custom key wrapper for the parameters required to visualize a geo and the data associated with it on the "**Map**" view.
`data.custom_geo_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](categories.md#custom_data_chunk_).
`data.custom_geo_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](categories.md#custom_data_key_).
<a name="geojson-value">`data.custom_geo_data_*.geoJsonValue`</a> | | The value matched by [`geojson_prop_*`](#geojson_prop_) inside the GeoJSON data source. The CAVE App will aggregate all data matches found via the path: `features` &rarr; `<array-index>` &rarr; `properties` &rarr; `geojson_prop_*` &rarr; `geojson_value_*`.
<a name="geojson_value_">`data.custom_geo_data_*.geoJsonValue`&swarhk;<br>`.geojson_value_*`</a> | | The match value for the [geoJsonValue](#geojson-value) key.
`data.custom_geo_data_*.name` | | A name for the geo area that will be displayed as a title in the map modal.
`data.custom_geo_data_*.props`&swarhk;<br>`.custom_prop_key_*` | | See [`custom_prop_key_*`](../common_keys/props.md#custom_prop_key_).
`data.custom_geo_data_*.type` | Required | The `type` key sets the type of `custom_geo_data_*` to a `custom_geo_type_*` key, to match specific visualization preferences for a geo.
`types` | Required | The `types` key allows you to define different types of geos in terms of styling and data viz settings.
<a name="geo-type">`types.custom_geo_type_*`</a> | Required | A wrapper for key-value pairs that match a specific set of data viz preferences for a geo.
<a name="geojson">`types.custom_geo_type_*.geoJson`</a> | | A wrapper for the [`geoJsonLayer`](#geojson_layer) and [`geoJsonProp`](#geojson_prop) keys in a geo type.
<a name="geojson_layer">`types.custom_geo_type_*.geoJson`&swarhk;<br>`.geoJsonLayer`</a> | | Sets the GeoJSON data source of `custom_geo_type_*` to a URL of a GeoJSON data source. Note that this URL is fetched on app startup or, if passed later, when the layer is enabled by the app user.
<a name="geojson_prop">`types.custom_geo_type_*.geoJson`&swarhk;<br>`.geoJsonProp`</a> | | Contains the name of a [GeoJSON property](#https://datatracker.ietf.org/doc/html/rfc7946#section-1.5) in the data source specified in `geoJsonLayer`.
<a name="geojson_prop_">`types.custom_geo_type_*.geoJson`&swarhk;<br>`.geoJsonProp.geojson_prop_*`</a> | | The match value for the [geoJsonProp](#geojson_prop) key.

> Please note that in the CAVE App, the maximum total size of the combined GeoJSON data sources is 50 MiB. Feel free to use a tool like [mapshaper](https://mapshaper.org/) to meet the size requirements.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'geos': {
    'name': 'Geographies',
    'types': {
        'state': {
            'name': 'State',
            'colorByOptions': {
                'Demand': {
                    'min': 50,
                    'max': 250,
                    'startGradientColor': {
                        'dark': 'rgb(100, 100, 100)',
                        'light': 'rgb(200, 200, 200)',
                    },
                    'endGradientColor': {
                        'dark': 'rgb(20, 205, 20)',
                        'light': 'rgb(10, 100, 10)',
                    },
                }
            },
            'colorBy': 'Demand',
            'geoJson': {
                'geoJsonLayer': 'StateGeoJson',
                'geoJsonProp': 'code_hasc',
            },
            'props': {
                'Demand': {
                    'type': 'num',
                    'enabled': True,
                    'help': 'The Demand of this Geography',
                    'numberFormat': {
                        'unit': 'units',
                    },
                },
            },
            'icon': 'FaHexagon',
        },
        'country': {
            'name': 'Country',
            'colorByOptions': {
                'Demand': {
                    'min': 0,
                    'max': 800,
                    'startGradientColor': {
                        'dark': 'rgb(100, 100, 100)',
                        'light': 'rgb(200, 200, 200)',
                    },
                    'endGradientColor': {
                        'dark': 'rgb(20, 205, 20)',
                        'light': 'rgb(10, 100, 10)',
                    },
                }
            },
            'colorBy': 'Demand',
            'geoJson': {
                'geoJsonLayer': 'CountryGeoJson',
                'geoJsonProp': 'FIPS_10',
            },
            'startGradientColor': {
                'dark': 'rgb(100, 100, 100)',
                'light': 'rgb(200, 200, 200)',
            },
            'endGradientColor': {
                'dark': 'rgb(20, 205, 20)',
                'light': 'rgb(10, 100, 10)',
            },
            'props': {
                'Demand': {
                    'type': 'num',
                    'enabled': True,
                    'help': 'The Demand of this Geography',
                    'numberFormat': {
                        'unit': 'units',
                    },
                },
            },
            'icon': 'FaHexagon',
        },
    },
    'data': {
        'geo_1': {
            'name': 'Ontario, Canada',
            'geoJsonValue': 'CA.ON',
            'type': 'state',
            'category': {'Location': ['loc_CA_ON']},
            'props': {
                'Demand': {
                    'value': 50,
                }
            },
        },
        'geo_2': {
            'name': 'Michigan, USA',
            'geoJsonValue': 'US.MI',
            'type': 'state',
            'category': {'Location': ['loc_US_MI']},
            'props': {
                'Demand': {
                    'value': 300,
                }
            },
        },
        'geo_c_1': {
            'name': 'Canada',
            'geoJsonValue': 'CA',
            'type': 'country',
            'category': {'Location': ['loc_CA_ON']},
            'props': {
                'Demand': {
                    'value': 50,
                }
            },
        },
        'geo_c_2': {
            'name': 'USA',
            'geoJsonValue': 'US',
            'type': 'country',
            'category': {
                'Location': ['loc_US_FL', 'loc_US_MA', 'loc_US_IN', 'loc_US_MI']
            },
            'props': {
                'Demand': {
                    'value': 800,
                }
            },
        },
    },
}
```
</details>