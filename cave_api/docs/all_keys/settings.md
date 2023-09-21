# `settings`
This key group allows designers to specify settings they want the site to use overriding setting defaults. For example, designers can specify the URL where icons are fetched from. If this is not supplied, it defaults to the one specified in [`cave_static` constants](https://github.com/MIT-CAVE/cave_static/blob/main/src/utils/constants.js) for each version.

Below is the `settings` group with its sub-keys matched by typical values:
```py
"settings": {
    "allowModification": False,
    "sendToApi": False,
    "sendToClient": True,
    "data": {
        "demo": {
            "customViewKey*": {
                "show": False,
            },
            "customMapKey*": {
                "scrollSpeed": 2,
            },
            "customViewKey*": {
                "displayTime": 1,
            },
        },
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
            "fallbackValue": "Not available",
            "unitPlacement": "afterWithSpace",
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
- [`order`](../common_keys//common_keys.md#order)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="iconUrl">`iconUrl`</a> | | The URL of SVG icon sources to be fetched into the CAVE app. EG: `https://react-icons.mitcave.com/4.8.0`. This URL should allow for paths that follow the folder pattern of react-icons with each icon getting its own file. Using the example url, and calling the icon `FaWarehouse` the following path should exist `https://react-icons.mitcave.com/4.8.0/fa/FaWarehouse.js` (where each js file is an svg object). The cave team periodically releases this specially formatted version of the react-icons following react-icons's versioning structure. To see the icons supported for any given version released by the CAVE team, go to the coresponding react-icons documentation. For `https://react-icons.mitcave.com/4.8.0` You would go to the docs for react icons `4.8.0`. Please note: All icons specified in the CAVE API are fetched by end users from this URL when an instance of the CAVE app starts running in their browsers.
<a name="debug">`debug`</a> | `False` | A boolean flag to include additional features or resources for CAVE App developers and designers to test a CAVE application. For example, `undefined` values can occur when data coming from two categories used for grouping and subgrouping have missing values. This can happen for one of two reasons: the two categories used for grouping and subgrouping don't make sense when put together, or the API data is incomplete for some data points. If the `debug` flag is set to `True`, inconsistent or missing values are tagged as `undefined` and displayed on the dashboard charts.<br><br>Please note that the `debug` flag must be set to `False` when deploying to a production environment.
<a name="number-format">`numberFormat`</a> | | A dictionary object that contains the properties [`fallbackValue`](../common_keys/common_keys.md#fallback-value), [`legendMaxLabel`](../common_keys/props.md#legend-max-label), [`legendMinLabel`](../common_keys/props.md#legend-min-label), [`legendNotation`](../common_keys/props.md#legend-notation), [`legendNotationDisplay`](../common_keys/props.md#legend-notation-display), [`legendPrecision`](../common_keys/props.md#legend-precision), [`locale`](../common_keys/common_keys.md#locale), [`precision`](../common_keys/common_keys.md#precision), [`notation`](../common_keys/common_keys.md#notation), [`notationDisplay`](../common_keys/common_keys.md#notation-display), [`trailingZeros`](../common_keys/common_keys.md#trailing-zeros), [`unit`](../common_keys/common_keys.md#unit), and [`unitPlacement`](../common_keys/common_keys.md#unit-placement) in order to enable language-sensitive formatting for numerical values. The `numberFormat` specification affects the display format of all numeric data in the CAVE app. However, these attributes can be customized by defining them within a [prop](props.md), [stat](../all_keys/stats.md), or [KPI](../all_keys/kpis.md) element.
<a name="sync">`sync`</a> | `{}` | A dictionary with key value pairs that allow API designers to specify paths within API state to be set to use local state on CAVE app startup, and to be toggled between local and session synchronized by users.
`sync.customSyncKey*.data` | `{}` | A dictionary with key value pairs, where values are unqiue paths in the API that can be synced or desynced.
`sync.customSyncKey*.value` | `True` | A boolean value that determines whether the given paths are synced on app startup
`sync.customSyncKey*.showToggle` | `False` | A boolean value that determines whether a toggle for the given paths is shown in the appSettings pane.
<a name="timeLength">`timeLength`</a> | | An integer representing the length of all `value` lists found in any supplied [`timeValues`](../common_keys/time_value.md)s. If no `timeValues` are used, this key can be omitted to hide the time selector in the app.
<a name="timeUnits">`timeUnits`</a> | `'units'` | A string used to describe each unit of time between steps in [`timeValues`](../common_keys/time_value.md)s (e.g. 'day', 'week', 'month', etc.). This is only used for display purposes.
`customMapStyle*` | `{}` | A dictionary containing custom style options for the map views.
`customMapStyle*.fog` | `{}` | A dictionary complying with the [Mapbox-GL fog spec](https://docs.mapbox.com/mapbox-gl-js/style-spec/fog/). If left empty default fog is used based on whether the user is in light or dark mode.
`customMapStyle*.style` | Required | Either a URL string pointing to a [Mapbox-GL style spec](https://docs.mapbox.com/mapbox-gl-js/style-spec/), or a dictionary complying with the spec.
<a name="demo">`demo`</a> | `{}` | A dictionary with appBar views as keys, and and objects with values that modify the default demo mode.
`demo.customViewKey*.show` | `True` | A boolean value that determines whether demo mode will automatically display this view.
`demo.customViewKey*.displayTime` | `100` for maps, `10` for pages | An integer or a float value representing the number of seconds to display the view during demo mode.
`demo.customMapKey*.scrollSpeed` | `0.05` | A float value representing degrees of rotation per frame (degrees per 13 milliseconds). This key only applies to map views

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"settings": {
    "allowModification": False,
    "sendToApi": False,
    "sendToClient": True,
    "data": {
        "demo": {
            "map2": {
                "show": False,
            },
            "map1": {
                "scrollSpeed": 2,
            },
            "dash1": {
                "displayTime": 1,
            },
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
            "fallbackValue": "N/A",
            "unitPlacement": "afterWithSpace",
        },
        "debug": True,
    },
},
```
</details>
