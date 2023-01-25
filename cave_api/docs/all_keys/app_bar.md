# `appBar`
The `appBar` key allows API designers to create a custom bar located on the left of the CAVE app. This bar allows for navigation between the different views of the app (e.g. Map, Dashboards), as well as interaction with panes. The `appBar` is split into two sections: `upper` and `lower`. Using both sections is not required, but it is generally recommended that `lower` be used for navigation through the CAVE app views and `upper` for interactive panes and buttons.

The structure of the `appBar` group looks as follows:
```py
'appBar': {
    'data': {
        "appBarId":"customDash1",
        "customSessionPane": {
            "icon": "MdApi",
            "type": "pane",
            "bar": "upper",
            "order": 0,
        },
        "customAppSettingsPane": {
            "icon": "MdOutlineSettings",
            "type": "pane",
            "bar": "upper",
            "order": 1,
        },
        "customSolveButton": {
            "name": "Solve Button",
            "icon": "BsLightningFill",
            "color": {
                "dark": "rgb(178, 179, 55)",
                "light": "rgb(79, 79, 24)",
            },
            "apiCommand": "solve",
            "type": "button",
            "bar": "upper",
            "order": 2,
        },
        "customPropsPane": {
            "icon": "FaCogs",
            "type": "pane",
            "bar": "upper",
            "order": 3,
        },
        "customMap": {
            "type": "map",
            "icon": "FaMapMarkedAlt",
            "bar": "lower",
            "order": 1,
        },
        "customDash1": {
            "type": "stats",
            "icon": "MdInsertChart",
            "name": "Dashboard 1",
            "order": 2,
            "bar": "lower",
        },
        "customKpi": {
            "type": "kpi",
            "icon": "MdSpeed",
            "bar": "lower",
            "order": 3,
        },
        # As many custom pane objects as needed
    },
}
```

## Page Views
Page views are the `cave_app`'s primary way to view and interact with the api information outside of panes. There are three types of page views that are all launced from the `appBar`.

In general, the `cave_app` has zero to many `map` views, zero to many `stats` views and zero or one `kpi` view.

<details>
  <summary>Map page</summary>

```py
"customMap1": {
    "type": "map",
    "icon": "FaMapMarkedAlt",
    "bar": "lower",
    "order": 1,
},
```
</details>

<details>
  <summary>Stats page</summary>

```py
"customStats1": {
    "type": "stats",
    "icon": "MdInsertChart",
    "name": "Dashboard 1",
    "order": 2,
    "bar": "lower",
},
```
</details>

<details>
  <summary>Kpi page</summary>

```py
"customKpi": {
    "type": "kpi",
    "icon": "MdSpeed",
    "bar": "lower",
    "order": 3,
},
```
</details>

## Panes
Panes are constructs primarily used to place UI controls (toggles, text and number fields, sliders, etc.), as well as buttons to allow interaction with actionable data. Custom panes can be designed to enable users to tune up the parameters of a simulation, navigate through different case study scenarios, reset the state of a simulation, synchronize data or settings with other users, and so on. The `appBar` group only contains the icon, order, and bar information about a pane with all other info being found in the `panes` group

<details>
  <summary>Example Pane</summary>

```py
"customSessionPane": {
    "icon": "MdApi",
    "type": "pane",
    "bar": "upper",
    "order": 0,
},
```
</details>

## Common keys
- [`color`](../common_keys/common_keys.md#color)
- [`data`](../common_keys/common_keys.md#data)
- [`enabled`](../common_keys/common_keys.md#enabled)
- [`help`](../common_keys/common_keys.md#help)
- [`icon`](../common_keys/common_keys.md#icon)
- [`label`](../common_keys/common_keys.md#label)
- [`maxValue`](../common_keys/common_keys.md#max-value)
- [`minValue`](../common_keys/common_keys.md#min-value)
- [`order`](../common_keys/common_keys.md#order)
- [`prop > type`](../common_keys/common_keys.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`value`](../common_keys/common_keys.md#value)


## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`appBarId` | Your first map view | The id (as a string) of the selected view. This would be the key of a `dashboard`, `map` or `kpi` view.
`customObjKey*` | Required | A custom key wrapper for the custom pane.
`customObjKey*.type` | Required | The type of object shown - takes one of these values: `map`, `stat`, `kpi`, `pane`, or `button`. The type given changes what other props can be given to the object.
`customObjKey*.bar` | Required | The section of the `appBar` to display the object in. Accepts either `upper` or `lower`. The use of both bar sections is not required, and any object can be shown in either bar.
`customMapKey*.static` | `False` | If `True`, the viewport of this map cannot be changed manually, but can only be switched between the default and optional viewports given in the `map` top-level key.
`customButtonKey.apiCommand`<br> | | A string to pass to the API when the button is pressed.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"appBar": {
    "data": {
        "appBarId":"dash1",
        "session": {
            "icon": "MdApi",
            "type": "pane",
            "bar": "upper",
            "order": 0,
        },
        "appSettings": {
            "icon": "MdOutlineSettings",
            "type": "pane",
            "bar": "upper",
            "order": 1,
        },
        "resetButton": {
            "name": "Reset Button",
            "icon": "MdSync",
            "color": {
                "dark": "rgb(255, 101, 101)",
                "light": "rgb(212, 0, 0)",
            },
            "apiCommand": "reset",
            "type": "button",
            "bar": "upper",
            "order": 2,
        },
        "buttonSolve": {
            "name": "Solve Button",
            "icon": "BsLightningFill",
            "color": {
                "dark": "rgb(178, 179, 55)",
                "light": "rgb(79, 79, 24)",
            },
            "apiCommand": "solve",
            "type": "button",
            "bar": "upper",
            "order": 2,
        },
        "examplePropsPane": {
            "icon": "FaCogs",
            "type": "pane",
            "bar": "upper",
            "order": 3,
        },
        "context": {            
            "icon": "BsInboxes",
            "type": "pane",
            "order": 4,
            "bar": "upper",
        },
        "filter": {
            "icon": "FaFilter",
            "type": "pane",
            "order": 5,
            "bar": "upper",
        },
        "map1": {
            "type": "map",
            "icon": "FaMapMarkedAlt",
            "bar": "lower",
            "order": 1,
        },
        "dash1": {
            "type": "stats",
            "icon": "MdInsertChart",
            "name": "Dashboard 1",
            "order": 2,
            "bar": "lower",
        },
        "kpi1": {
            "type": "kpi",
            "icon": "MdSpeed",
            "bar": "lower",
            "order": 3,
        },
    }
},
```
</details>


