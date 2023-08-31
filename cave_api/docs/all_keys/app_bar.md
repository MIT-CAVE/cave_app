# `appBar`
The `appBar` key allows API designers to create a custom bar located on the left or right of the CAVE app. It is possible to include both a left bar and a right bar. A bar allows for navigation between the different views of the app (e.g. Map, Dashboards), as well as interaction with panes. Each bar is split into two sections: upper and lower. Using both sections is not required, but it is generally recommended that the lower section be used for navigation through the CAVE app views and the upper section be used for interactive panes and buttons.

The structure of the `appBar` group looks as follows:
```py
'appBar': {
    "appBarId":"customDash1",
    'data': {
        "customSessionPane": {
            "icon": "md/MdApi",
            "type": "pane",
            "bar": "upperLeft",
            "order": 0,
        },
        "customAppSettingsPane": {
            "icon": "md/MdOutlineSettings",
            "type": "pane",
            "bar": "upperLeft",
            "order": 1,
        },
        "customSolveButton": {
            "name": "Solve Button",
            "icon": "bs/BsLightningFill",
            "color": {
                "dark": "rgb(178, 179, 55)",
                "light": "rgb(79, 79, 24)",
            },
            "apiCommand": "solve",
            "type": "button",
            "bar": "upperLeft",
            "order": 2,
        },
        "customPropsPane": {
            "icon": "fa/FaCogs",
            "type": "pane",
            "bar": "upperLeft",
            "order": 3,
        },
        "customMap1": {
            "type": "map",
            "icon": "fa/FaMapMarkedAlt",
            "bar": "lowerLeft",
            "order": 1,
        },
        "customDash1": {
            "type": "stats",
            "icon": "md/MdInsertChart",
            "name": "Dashboard 1",
            "bar": "lowerLeft",
            "order": 1,
        },
        "customKpi": {
            "type": "kpi",
            "icon": "md/MdSpeed",
            "bar": "lowerLeft",
            "order": 3,
        },
        # As many custom pane objects as needed
    },
}
```

## Page Views
Page views are the `cave_app`'s primary way to view and interact with the api information outside of panes. There are three types of page views that are all launched from the `appBar`.

In general, the `cave_app` has zero to many `map` views, zero to many `stats` views and zero or one `kpi` view.

<details>
  <summary>Map page</summary>

```py
"customMap1": {
    "type": "map",
    "icon": "fa/FaMapMarkedAlt",
    "bar": "lowerLeft",
    "order": 1,
},
```
</details>

<details>
  <summary>Stats page</summary>

```py
"customStats1": {
    "type": "stats",
    "icon": "md/MdInsertChart",
    "name": "Dashboard 1",
    "order": 2,
    "bar": "lowerLeft",
},
```
</details>

<details>
  <summary>Kpi page</summary>

```py
"customKpi": {
    "type": "kpi",
    "icon": "md/MdSpeed",
    "bar": "lowerLeft",
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
    "icon": "md/MdApi",
    "type": "pane",
    "bar": "upperLeft",
    "order": 0,
},
```
</details>

## Modals
Similar to custom panes, modals can be used to place UI controls and buttons to allow interaction with actionable data. A modal appears as a dialogue box in the center of the screen. The `appBar` group only contains the icon, order, and bar information about a modal with all other info being found in the `modals` group.

<details>
  <summary>Example Modal</summary>

```py
"customModal": {
    "icon": "ImCogs",
    "type": "modal",
    "bar": "upperLeft",
    "order": 1,
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
`appBarId` | Your first map view | The id (as a string) of the selected view. This would be the key of a `dashboard` view.
`customObjKey*` | Required | A custom key wrapper for the custom pane.
`customObjKey*.type` | Required | The type of object shown - takes one of these values: `stats`, `pane`, `modal`, or `button`. The type given changes what other props can be given to the object.
`customObjKey*.bar` | Required | The section of the `appBar` to display the object in. Accepts either `upperLeft`, `lowerLeft`, `upperRight`, or `lowerRight`. If no object is specified as `upperRight` or `lowerRight`, a right bar will not be created. Similarly, if no object is specified as `upperLeft` or `lowerLeft`, a left bar will not be created. The use of both an upper and a lower bar section is not required, and any object can be shown in any section.
`customButtonKey.apiCommand`<br> | | A string to pass to the API when the button is pressed.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"appBar": {
    "appBarId":"dash1",
    "data": {
        "session": {
            "icon": "md/MdApi",
            "type": "pane",
            "bar": "upperLeft",
            "order": 0,
        },
        "appSettings": {
            "icon": "md/MdOutlineSettings",
            "type": "pane",
            "bar": "upperLeft",
            "order": 1,
        },
        "resetButton": {
            "name": "Reset Button",
            "icon": "md/MdSync",
            "color": {
                "dark": "rgb(255, 101, 101)",
                "light": "rgb(212, 0, 0)",
            },
            "apiCommand": "reset",
            "type": "button",
            "bar": "upperLeft",
            "order": 2,
        },
        "buttonSolve": {
            "name": "Solve Button",
            "icon": "bs/BsLightningFill",
            "color": {
                "dark": "rgb(178, 179, 55)",
                "light": "rgb(79, 79, 24)",
            },
            "apiCommand": "solve",
            "type": "button",
            "bar": "upperLeft",
            "order": 3,
        },
        "examplePropsPane": {
            "icon": "fa/FaCogs",
            "type": "pane",
            "bar": "upperLeft",
            "order": 4,
        },
        "context": {            
            "icon": "bs/BsInboxes",
            "type": "pane",
            "order": 5,
            "bar": "upperLeft",
        },
        "filter": {
            "icon": "fa/FaFilter",
            "type": "pane",
            "order": 6,
            "bar": "upperLeft",
        },
        "dash1": {
            "type": "stats",
            "icon": "md/MdInsertChart",
            "name": "Dashboard 1",
            "order": 1,
            "bar": "lowerLeft",
        },
        "kpi1": {
            "type": "kpi",
            "icon": "md/MdSpeed",
            "bar": "lowerLeft",
            "order": 2,
        },
        "customModal": {
            "icon": "im/ImCogs",
            "type": "modal",
            "bar": "upperRight",
            "order": 0,
        },
        "map2": {
            "type": "map",
            "icon": "fa/FaMapMarkedAlt",
            "bar": "lowerRight",
            "order": 0,
        },
        "dash2": {
            "type": "stats",
            "icon": "md/MdInsertChart",
            "name": "Dashboard 1",
            "order": 1,
            "bar": "lowerRight",
        },
    }
},
```
</details>


