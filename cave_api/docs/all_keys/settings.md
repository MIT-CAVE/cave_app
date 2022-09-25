#### `settings`
This key group allows designers to specify settings they want the site to use (overriding setting defaults. For example, designers can specify the URL where icons are fetched from. If this is not supplied, it defaults to the one specified in [cave_static constants](https://github.com/MIT-CAVE/cave_static/blob/0.1.0/src/utils/constants.js) for each version.

Below is the `settings` group with its sub-keys matched by typical values:
```py
"settings": {
    "allow_modification": False,
    "send_to_api": False,
    "send_to_client": True,
    "data": {
        "syncToggles": {
            "Map Layers": {
                "ml1": ["map", "data", "enabledTypes"],
                "ml2": ["nodes", "types"],
                "ml3": ["arcs", "types"],
                "ml4": ["geos", "types"],
            },
        },
        "defaultDesync": {
            "Map Layers": {
                "ml1": ["map", "data", "enabledTypes"],
                "ml2": ["nodes", "types"],
                "ml3": ["arcs", "types"],
                "ml4": ["geos", "types"],
            },
            "App Bar": {
                "ab1": ["appBar", "data", "dashboardId"],
                "ab2": ["appBar", "paneState"],
            },
        },
        "IconUrl": "https://react-icons.mitcave.com/0.0.1",
        "numberFormat": {
            "precision": 4,
            "trailingZeros": True,
            "whenTyping": False,
            "unitSpace": True,
        },
        "debug": True,
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`data`](#data)
- [`numberFormat`](#number-format)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="IconUrl">`IconUrl`</a> | | The URL of SVG icon sources to be fetched into the CAVE app. Please note all icons specified in the CAVE API are fetched by end users from this URL when an instance of the CAVE app start running in their browsers.
<a name="timeLength">`timeLength`</a> | | An integer representing the length of all `value` lists found in any supplied [`timeObjects`](#timeobjects). If no timeObjects are used `timeLength` can be omitted to hide the time selector in the app.
<a name="timeUnits">`timeUnits`</a> | `'units'` | A string used to describe each unit of time between steps in [`timeObjects`](#timeobjects) (e.g. 'day', 'week', 'month', etc.). This is only used for display purposes.
<a name="debug">`debug`</a> | `False` | A boolean flag to include additional features or resources for CAVE App developers and designers to test a CAVE application. For example, `undefined` values can occur when data coming from two categories used for grouping and subgrouping have missing values. This can happen for one of two reasons: the two categories used for grouping and subgrouping don't make sense when put together, or the API data is incomplete for some data points. If the `debug` flag is set to `True`, inconsistent or missing values are tagged as `undefined` and displayed on the dashboard charts.<br><br>Please note that the `debug` flag must be set to `False` when deploying to a production environment.
<a name="syncToggles">`syncToggles`</a> | `{}` | A dictionary with key value pairs that allow app users to switch API state into a local state. Keys are the toggle labels displayed to users, and values are dictionaries containing key value pairs. The keys in these dictionaries must be unique, and the values are arrays representing the paths to be controlled by that toggle. When toggled back into an API synced state the local data is removed, so this option isn't fully supported for some data inputs (e.g. props).
<a name="defaultDesync">`defaultDesync`</a> | `{}` | A dictionary with key value pairs that allow API designers to specify paths within API state to be set to use local state on CAVE app startup. The dictionary has the same shape as `syncToggles`, and any paths that should default to local and support toggling must use the same keys in both `defaultDesync` and `syncToggles`.