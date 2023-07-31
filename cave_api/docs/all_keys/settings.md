# `settings`
This key group allows designers to specify settings they want the site to use (overriding setting defaults. For example, designers can specify the URL where icons are fetched from. If this is not supplied, it defaults to the one specified in [`cave_static` constants](https://github.com/MIT-CAVE/cave_static/blob/main/src/utils/constants.js) for each version.

Below is the `settings` group with its sub-keys matched by typical values:
```py
"settings": {
    "allowModification": False,
    "sendToApi": False,
    "sendToClient": True,
    "data": {
        "additionalMapStyles": {
            "customMapStyle1": {
                {
                    "name": 'Custom Style',
                    "icon": 'MdExplore',
                    "order": 1,
                    "spec": 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json',
                    "fog": {
                        "range": [0.8, 8],
                        "color": "#dc9f9f",
                        "horizon-blend": 0.5,
                        "high-color": "#245bde",
                        "space-color": "#000000",
                        "star-intensity": 0.15
                    },
                }
            }
        },
        "sync":{
            "mapLayers":{
                "name": "Map Layers",
                "showToggle": True,
                "value": False,
                "data":{
                    "ml1": ["map", "data", "legendGroups"],
                    "ml2": ["nodes", "types"],
                    "ml3": ["arcs", "types"],
                    "ml4": ["geos", "types"]
                }
            },
            "appBar": {
                "name": "App Bar",
                "showToggle": True,
                "value": False,
                "data": {
                    "ab1": ["appBar", "data", "dashboardId"],
                    "ab2": ["appBar", "paneState"]
                }
            }
        },
        "iconUrl": "https://react-icons.mitcave.com/4.8.0",
        "numberFormat": {
            "precision": 4,
            "trailingZeros": True,
            "unitSpace": True,
        },
        "debug": True,
    },
}
```

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`data`](../common_keys/common_keys.md#data)
- [`icon`](../common_keys//common_keys.md#icon)
- [`name`](../common_keys/common_keys.md#name)
- [`numberFormat`](../common_keys/common_keys.md#number-format)
- [`order`](../common_keys//common_keys.md#order)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="iconUrl">`iconUrl`</a> | | The URL of SVG icon sources to be fetched into the CAVE app. EG: `https://react-icons.mitcave.com/4.8.0`. This URL should allow for paths that follow the folder pattern of react-icons with each icon getting its own file. Using the example url, and calling the icon `FaWarehouse` the following path should exist `https://react-icons.mitcave.com/4.8.0/fa/FaWarehouse.js` (where each js file is an svg object). The cave team periodically releases this specially formatted version of the react-icons following react-icons's versioning structure. To see the icons supported for any given version released by the CAVE team, go to the coresponding react-icons documentation. For `https://react-icons.mitcave.com/4.8.0` You would go to the docs for react icons `4.8.0`. Please note: All icons specified in the CAVE API are fetched by end users from this URL when an instance of the CAVE app starts running in their browsers.
<a name="debug">`debug`</a> | `False` | A boolean flag to include additional features or resources for CAVE App developers and designers to test a CAVE application. For example, `undefined` values can occur when data coming from two categories used for grouping and subgrouping have missing values. This can happen for one of two reasons: the two categories used for grouping and subgrouping don't make sense when put together, or the API data is incomplete for some data points. If the `debug` flag is set to `True`, inconsistent or missing values are tagged as `undefined` and displayed on the dashboard charts.<br><br>Please note that the `debug` flag must be set to `False` when deploying to a production environment.
<a name="sync">`sync`</a> | `{}` | A dictionary with key value pairs that allow API designers to specify paths within API state to be set to use local state on CAVE app startup, and to be toggled between local and session synchronized by users.
`sync.customSyncKey*.data` | `{}` | A dictionary with key value pairs, where values are unqiue paths in the API that can be synced or desynced.
`sync.customSyncKey*.value` | `True` | A boolean value that determines whether the given paths are synced on app startup
`sync.customSyncKey*.showToggle` | `False` | A boolean value that determines whether a toggle for the given paths is shown in the appSettings pane.
<a name="timeLength">`timeLength`</a> | | An integer representing the length of all `value` lists found in any supplied [`timeValues`](../common_keys/time_value.md)s. If no `timeValues` are used, this key can be omitted to hide the time selector in the app.
<a name="timeUnits">`timeUnits`</a> | `'units'` | A string used to describe each unit of time between steps in [`timeValues`](../common_keys/time_value.md)s (e.g. 'day', 'week', 'month', etc.). This is only used for display purposes.
`customMapStyle*` | {} | A dictionary containing custom style options for the map views.
`customMapStyle*.fog` | {} | A dictionary complying with the (Mapbox-GL fog spec)[https://docs.mapbox.com/mapbox-gl-js/style-spec/fog/]. If left empty default fog is used based on whether the user is in light or dark mode.
`customMapStyle*.style` | required | Either a URL string pointing to a (Mapbox-GL style spec)[https://docs.mapbox.com/mapbox-gl-js/style-spec/], or a dictionary complying with the spec.



## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"settings": {
    "allowModification": False,
    "sendToApi": False,
    "sendToClient": True,
    "data": {
        "sync":{
            "mapLayers":{
                "name": "Map Layers",
                "showToggle": True,
                "value": False,
                "data":{
                    "ml1": ["map", "data", "legendGroups"],
                    "ml2": ["nodes", "types"],
                    "ml3": ["arcs", "types"],
                    "ml4": ["geos", "types"],
                }
            },
            "appBar": {
                "name": "App Bar",
                "showToggle": True,
                "value": False,
                "data": {
                    "ab1": ["appBar", "data", "dashboardId"],
                    "ab2": ["appBar", "paneState"],
                }
            },
        },
        "iconUrl": "https://react-icons.mitcave.com/4.8.0",
        "numberFormat": {
            "precision": 4,
            "trailingZeros": False,
            "unitSpace": True,
        },
        "debug": True,
    },
},
```
</details>
