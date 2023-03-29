# `settings`
This key group allows designers to specify settings they want the site to use (overriding setting defaults. For example, designers can specify the URL where icons are fetched from. If this is not supplied, it defaults to the one specified in [`cave_static` constants](https://github.com/MIT-CAVE/cave_static/blob/1.0.1/src/utils/constants.js) for each version.

Below is the `settings` group with its sub-keys matched by typical values:
```py
"settings": {
    "allowModification": False,
    "sendToApi": False,
    "sendToClient": True,
    "data": {
        "sync":{
            "mapLayers":{
                "name": "Map Layers",
                "showToggle": true,
                "value": false,
                "data":{
                    "ml1": ["map", "data", "legendGroups"],
                    "ml2": ["nodes", "types"],
                    "ml3": ["arcs", "types"],
                    "ml4": ["geos", "types"]
                }
            },
            "appBar": {
                "name": "App Bar",
                "showToggle": true,
                "value": false,
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
- [`name`](../common_keys/common_keys.md#name)
- [`numberFormat`](../common_keys/common_keys.md#number-format)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="iconUrl">`iconUrl`</a> | | The URL of SVG icon sources to be fetched into the CAVE app. Please note all icons specified in the CAVE API are fetched by end users from this URL when an instance of the CAVE app start running in their browsers.
<a name="debug">`debug`</a> | `False` | A boolean flag to include additional features or resources for CAVE App developers and designers to test a CAVE application. For example, `undefined` values can occur when data coming from two categories used for grouping and subgrouping have missing values. This can happen for one of two reasons: the two categories used for grouping and subgrouping don't make sense when put together, or the API data is incomplete for some data points. If the `debug` flag is set to `True`, inconsistent or missing values are tagged as `undefined` and displayed on the dashboard charts.<br><br>Please note that the `debug` flag must be set to `False` when deploying to a production environment.
<a name="sync">`sync`</a> | `{}` | A dictionary with key value pairs that allow API designers to specify paths within API state to be set to use local state on CAVE app startup, and to be toggled between local and session synchronized by users.
`sync.customSyncKey*.data` | `{}` | A dictionary with key value pairs, where values are unqiue paths in the api that can be synced or desynced.
`sync.customSyncKey*.value | True | A boolean value that determines whether the given paths are synced on app startup
`sync.customSyncKey*.showToggle` | `False` | A boolean value that determines whether a toggle for the given paths is shown in the appSettings pane.
<a name="timeLength">`timeLength`</a> | | An integer representing the length of all `value` lists found in any supplied [`timeObject`](../common_keys/time_object.md)s. If no `timeObject`s are used, this key can be omitted to hide the time selector in the app.
<a name="timeUnits">`timeUnits`</a> | `'units'` | A string used to describe each unit of time between steps in [`timeObject`](../common_keys/time_object.md)s (e.g. 'day', 'week', 'month', etc.). This is only used for display purposes.


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