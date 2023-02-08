# `geos`
The `geos` group takes in data and renders it as geographic areas on the "**Map**" view, to visualize spatial distribution of parameters.

The internal structure of `geos` is very similar to that of the `arcs` and `nodes` groups. The most relevant discrepancy is the addition of the special key `geoJson`.

Let's look inside the structure of `geos`:
```py
"geos": {
    "name": "A name that will be displayed in the map legend.",
    "types": {
        "customGeoType1": {
            "name": "A name to be displayed in the UI",
            "colorByOptions": {
                "customPropKey1": {
                    "min": 0,
                    "max": 60,
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
                    "max": 40,
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
                  "customColorKey1": "rgb(233,0,0)",
                  "customColorKey2": "rgb(0,233,0)"
                }
            },
            "colorBy": "customPropKey1",
            "geoJson": {
                "geoJsonLayer": "https://cave-geojsons.s3.amazonaws.com/geojson_data_1.json",
                "geoJsonProp": "geojsonProp1",
            },
            "props": {
                "customPropKey1": {
                    "type": "num",
                    "help": "A help text for this numeric input",
                    "numberFormat": {
                        "unit": "units",
                    },
                    "enabled": True,
                },
                "customPropKey2": {...},
                "customPropKey3": {...},
            },
            "icon": "FaHexagon",
        },
        "customGeoType2": {...},
    },
    "data": {
        "customGeoData1": {
            "name": "A name to be displayed in the UI",
            "geoJsonValue": "geojson_value_1",
            "type": "customGeoType1",
            "category": {
                "customDataChunck1": ["customDataKey1"]
            },
            "props": {
                "customPropKey1": {
                    "value": 60,
                },
                "customPropKey2": {...},
                "customPropKey3": {...},
            },
        },
        "customGeoData2": {...},
        # As many geo data chunks as needed
    },
}
```

## Common keys
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
- [`prop > type`](../common_keys/props.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`startGradientColor`](../common_keys/common_keys.md#start-gradient)
- [`value`](../common_keys/props.md#value)
- [`variant`](../common_keys/props.md#variant)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`data.customGeoData*.category`&swarhk;<br>`.customDataChunck*` | | See [`customDataChunck*`](categories.md#customDataChunck).
`data.customGeoData*.category`&swarhk;<br>`.customDataChunck*.customDataKey*` | | See [`customDataKey*`](categories.md#customDataKey).
<a name="geojson-value">`data.customGeoData*.geoJsonValue`</a> | required | The identifier for this geo as identified in the specified geoJson object. This identifier is matched to the `types.customGeoType*.geoJson.geoJsonProp` as it relates to each geoJson object in the file specified at `types.customGeoType*.geoJson.geoJsonLayer`.
`data.customGeoData*.name` | | A name for the geo area that will be displayed as a title in the map modal.
`data.customGeoData*.props`&swarhk;<br>`.customPropKey*` | | See [`customPropKey*`](../common_keys/props.md#customPropKey).
`data.customGeoData*.type` | Required | The `type` key sets the type of `customGeoData*` to a `customGeoType*` key, to match specific visualization preferences for a geo.
`types` | Required | The `types` key allows you to define different types of geos in terms of styling and data viz settings.
<a name="geo-type">`types.customGeoType*`</a> | Required | A wrapper for key-value pairs that match a specific set of data viz preferences for a geo.
<a name="geoJson">`types.customGeoType*.geoJson`</a> | | A wrapper for the [`geoJsonLayer`](#geojson_layer) and [`geoJsonProp`](#geojson_prop) keys in a geo type.
<a name="geoJsonLayer">`types.customGeoType*.geoJson`&swarhk;<br>`.geoJsonLayer`</a> | | Sets the GeoJSON data source of `customGeoType*` to a URL of a GeoJSON data source. Note that this URL is fetched on app startup or, if passed later, when the layer is enabled by the app user.
<a name="geoJsonProp">`types.customGeoType*.geoJson`&swarhk;<br>`.geoJsonProp`</a> | | Contains the name of a [GeoJSON property](#https://datatracker.ietf.org/doc/html/rfc7946#section-1.5) in the data source specified in `geoJsonLayer`.

> Please note that in the CAVE App, the maximum total size of all combined GeoJSON data sources is 50 MiB. Feel free to use a tool like [mapshaper](https://mapshaper.org/) to meet the size requirements.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"geos": {
    "types": {
        "state": {
            "name": "State",
            "colorByOptions": {
                "numericPropExampleC": {
                    "min": 0,
                    "max": 300,
                    "startGradientColor": {
                        "dark": "rgb(100, 100, 100)",
                        "light": "rgb(200, 200, 200)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(20, 205, 20)",
                        "light": "rgb(10, 100, 10)",
                    },
                }
            },
            "colorBy": "numericPropExampleC",
            "geoJson": {
                "geoJsonLayer": "https://geojsons.mitcave.com/world/world-states-provinces-md.json",
                "geoJsonProp": "code_hasc",
            },
            "icon": "BsHexagon",
            "props": {
                "numericPropExampleC": {
                    "name": "Numeric Prop Example C",
                    "type": "num",
                    "enabled": True,
                    "help": "Help with the example numeric prop for this State",
                    "numberFormat": {
                        "unit": "C units",
                    },
                },
            },
        },
        "country": {
            "name": "Country",
            "colorByOptions": {
                "numericPropExampleC": {
                    "min": 0,
                    "max": 800,
                    "startGradientColor": {
                        "dark": "rgb(100, 100, 100)",
                        "light": "rgb(200, 200, 200)",
                    },
                    "endGradientColor": {
                        "dark": "rgb(20, 205, 20)",
                        "light": "rgb(10, 100, 10)",
                    },
                }
            },
            "colorBy": "numericPropExampleC",
            "geoJson": {
                "geoJsonLayer": "https://geojsons.mitcave.com/world/countries-sm.json",
                "geoJsonProp": "FIPS_10",
            },
            "icon": "BsHexagon",
            "props": {
                "numericPropExampleC": {
                    "name": "Numeric Prop Example C",
                    "type": "num",
                    "enabled": True,
                    "help": "Help with the example numeric prop for this Country",
                    "numberFormat": {
                        "unit": "units",
                    },
                },
            },
        },
    },
    "data": {
        "geo1": {
            "name": "Ontario, Canada",
            "geoJsonValue": "CA.ON",
            "type": "state",
            "category": {"location": ["locCaOn"]},
            "props": {
                "numericPropExampleC": {
                    "value": 50,
                }
            },
        },
        "geo2": {
            "name": "Michigan, USA",
            "geoJsonValue": "US.MI",
            "type": "state",
            "category": {"location": ["locUsMi"]},
            "props": {
                "numericPropExampleC": {
                    "value": 300,
                }
            },
        },
        "geo3": {
            "name": "Massachusetts, USA",
            "geoJsonValue": "US.MA",
            "type": "state",
            "category": {"location": ["locUsMi"]},
            "props": {
                "numericPropExampleC": {
                    "value": 250,
                }
            },
        },
        "geo4": {
            "name": "Florida, USA",
            "geoJsonValue": "US.FL",
            "type": "state",
            "category": {"location": ["locUsMi"]},
            "props": {
                "numericPropExampleC": {
                    "value": 100,
                }
            },
        },
        "geo5": {
            "name": "Indiana, USA",
            "geoJsonValue": "US.FL",
            "type": "state",
            "category": {"location": ["locUsMi"]},
            "props": {
                "numericPropExampleC": {
                    "value": 200,
                }
            },
        },
        "geoCountry1": {
            "name": "Canada",
            "geoJsonValue": "CA",
            "type": "country",
            "category": {"location": ["locCaOn"]},
            "props": {
                "numericPropExampleC": {
                    "value": 50,
                }
            },
        },
        "geoCountry2": {
            "name": "USA",
            "geoJsonValue": "US",
            "type": "country",
            "category": {
                "location": [
                    "locUsFl",
                    "locUsMa",
                    "locUsIn",
                    "locUsMi",
                ]
            },
            "props": {
                "numericPropExampleC": {
                    "value": 800,
                }
            },
        },
    },
},
```
</details>
