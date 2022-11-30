# `appBar`
The `appBar` key allows API designers to create a custom bar located on the left of the CAVE app. This bar allows for navigation between the different views of the app (e.g. Map, Dashboards), as well as interaction with panes. The `appBar` is split into two sections: `upper` and `lower`. Using both sections is not required, but it is generally recommended that `lower` be used for navigation through the CAVE app views and `upper` for interactive panes and buttons.

The structure of the `appBar` group looks as follows:
```py
'appBar': {
    'data': {
        "customSessionPane": {
            "icon": "MdApi",
            "type": "pane",
            "variant": "session",
            "bar": "upper",
            "order": 0,
        },
        "customAppSettingsPane": {
            "icon": "MdOutlineSettings",
            "type": "pane",
            "variant": "appSettings",
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
            "name": "Example Props Pane",
            "props": {
                "numericHeader": {
                    "name": "Numeric Props",
                    "type": "head",
                    "help": "Some help for numeric props",
                },
                "numericInputExample": {
                    "name": "Numeric Input Example",
                    "type": "num",
                    "value": 50,
                    "enabled": True,
                    "help": "Help for the numeric input example",
                    "maxValue": 100,
                    "minValue": 0,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "units",
                    },
                },
                # As many props as needed
            },
            "layout": {
                "type": "grid",
                "numColumns": 1,
                "numRows": "auto",
                "data": {
                    "customCol1Row1": {
                        "type": "item",
                        "column": 1,
                        "row": 1,
                        "itemId": "numericHeader",
                    },
                    "customCol1Row2": {
                        "type": "item",
                        "column": 1,
                        "row": 2,
                        "itemId": "numericInputExample",
                    },
                },
            },
            "icon": "FaCogs",
            "type": "pane",
            "variant": "options",
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
            "dashboardLayout": [
                {
                    "chart": "Bar",
                    "grouping": "Average",
                    "statistic": "numericStatExampleA",
                },
                {
                    "chart": "Line",
                    "grouping": "Sum",
                    "statistic": "numericStatExampleB",
                },
                {
                    "chart": "Bar",
                    "level": "size",
                    "category": "sku",
                    "grouping": "Sum",
                    "statistic": "numericExampleCalculationStat",
                },
                {
                    "type": "kpis",
                    "chart": "Bar",
                    "grouping": "Sum",
                    "sessions": [],
                    "kpi": "kpi5",
                },
            ],
            "lockedLayout": False,
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

In general, the `cave_app` has zero or one `map` view, zero to many `stats` views and zero or one `kpi` view. 

<details>
  <summary>Map page</summary>

```py
"customMap": {
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
    "dashboardLayout": [
        {
            "chart": "Bar",
            "grouping": "Average",
            "statistic": "numericStatExampleA",
        },
        {
            "chart": "Line",
            "grouping": "Sum",
            "statistic": "numericStatExampleB",
        },
        {
            "chart": "Bar",
            "level": "size",
            "category": "sku",
            "grouping": "Sum",
            "statistic": "numericExampleCalculationStat",
        },
        {
            "type": "kpis",
            "chart": "Bar",
            "grouping": "Sum",
            "sessions": [],
            "kpi": "kpi5",
        },
    ],
    "lockedLayout": False,
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
Panes are subitems of the `appBar` group and are constructs primarily used to place UI controls (toggles, text and number fields, sliders, etc.), as well as buttons to allow interaction with actionable data. Custom panes can be designed to enable users to tune up the parameters of a simulation, navigate through different case study scenarios, reset the state of a simulation, synchronize data or settings with other users, and so on.

Panes can be of different [`variant`](#pane-variant)s, so to keep the data structure examples simple and modular, you can examine each one at a time in the following switchables:

<details>
  <summary>Session pane</summary>

```py
"CustomSessionPane": {
    "name": "Sessions",
    "icon": "MdApi",
    "type": "pane",
    "variant": "session",
    "bar": "upper",
    "order": 0,
},
```
</details>

<details>
  <summary>App Settings pane</summary>

```py
"appSettings": {
    "icon": "MdOutlineSettings",
    "type": "pane",
    "variant": "appSettings",
    "bar": "upper",
    "order": 1,
},
```
</details>

<details>
  <summary>Options pane</summary>

```py
"customPropsPane": {
    "name": "Example Props Pane",
    "props": {
        "numericHeader": {
            "name": "Numeric Props",
            "type": "head",
            "help": "Some help for numeric props",
        },
        "numericInputExample": {
            "name": "Numeric Input Example",
            "type": "num",
            "value": 50,
            "enabled": True,
            "help": "Help for the numeric input example",
            "maxValue": 100,
            "minValue": 0,
            "numberFormat": {
                "precision": 0,
                "unit": "units",
            },
        },
        "numericSliderExample": {
            "name": "Numeric Slider Example",
            "type": "num",
            "value": 50,
            "enabled": True,
            "variant": "slider",
            "help": "Help for the numeric slider example",
            "maxValue": 100,
            "minValue": 0,
        },
        "miscHeader": {
            "name": "Misc Props",
            "type": "head",
            "help": "Some help for miscelanous props",
        },
        "toggleInputExample": {
            "name": "Toggle Input Example",
            "type": "toggle",
            "value": True,
            "enabled": True,
            "help": "Help for the toggle input example",
        },
        "buttonInputExample": {
            "name": "Button Input Example (Creates an Error)",
            "value": "Press Me!",
            "type": "button",
            "apiCommand": "test",
            "enabled": True,
            "help": "Press this button to create an error",
        },
        "textInputExample": {
            "name": "Text Input Example",
            "type": "text",
            "value": "Example Text Here",
            "enabled": True,
            "help": "Help for the text input example",
        },
        "selectorHeader": {
            "name": "Selection Props",
            "type": "head",
            "help": "Some help for Selection Props",
        },
        "dropdownItemExample": {
            "name": "Dropdown Item Example",
            "type": "selector",
            "variant": "dropdown",
            "value": [
                {"name": "Option A", "value": False},
                {"name": "Option B", "value": False},
                {"name": "Option C", "value": True},
            ],
            "enabled": True,
            "help": "Select an option from the dropdown",
        },
        "checkboxItemExample": {
            "name": "Checkbox Item Example",
            "type": "selector",
            "variant": "checkbox",
            "value": [
                {"name": "Option A", "value": True},
                {"name": "Option B", "value": False},
                {"name": "Option C", "value": True},
            ],
            "enabled": True,
            "help": "Select all relevant items",
        },
        "radioItemExample": {
            "name": "Radio Item Example",
            "type": "selector",
            "variant": "radio",
            "value": [
                {"name": "Option A", "value": True},
                {"name": "Option B", "value": False},
                {"name": "Option C", "value": False},
            ],
            "enabled": True,
            "help": "Select one item from the list",
        },
    },
    "layout": {
        "type": "grid",
        "numColumns": 3,
        "numRows": "auto",
        "data": {
            "col1Row1": {
                "type": "item",
                "column": 1,
                "row": 1,
                "itemId": "numericHeader",
            },
            "col1Row2": {
                "type": "item",
                "column": 1,
                "row": 2,
                "itemId": "numericInputExample",
            },
            "col1Row3": {
                "type": "item",
                "column": 1,
                "row": 3,
                "itemId": "numericSliderExample",
            },
            "col2Row1": {
                "type": "item",
                "column": 2,
                "row": 1,
                "itemId": "miscHeader",
            },
            "col2Row2": {
                "type": "item",
                "column": 2,
                "row": 2,
                "itemId": "toggleInputExample",
            },
            "col2Row3": {
                "type": "item",
                "column": 2,
                "row": 3,
                "itemId": "buttonInputExample",
            },
            "col2Row4": {
                "type": "item",
                "column": 2,
                "row": 4,
                "itemId": "textInputExample",
            },
            "col3Row1": {
                "type": "item",
                "column": 3,
                "row": 1,
                "itemId": "selectorHeader",
            },
            "col3Row2": {
                "type": "item",
                "column": 3,
                "row": 2,
                "itemId": "dropdownItemExample",
            },
            "col3Row3": {
                "type": "item",
                "column": 3,
                "row": 3,
                "itemId": "checkboxItemExample",
            },
            "col3Row4": {
                "type": "item",
                "column": 3,
                "row": 4,
                "itemId": "radioItemExample",
            },
        },
    },
    "icon": "FaCogs",
    "type": "pane",
    "variant": "options",
    "bar": "upper",
    "order": 3,
},
```
</details>

<details>
  <summary>Context pane</summary>

```py
"customContextPane": {
    "name": "Example Context Pane",
    "props": {
        "numericContextProp": {
            "type": "num",
            "value": 100,
            "enabled": True,
            "help": "Numeric Context Prop Help",
            "label": "%",
            "variant": "slider",
            "maxValue": 500,
            "minValue": 0,
            "selectableCategories": ["location", "sku"],
        },
    },
    "data": {
        "context1": {
            "prop": "numericContextProp",
            "value": 110,
            "applyCategories": {"location": ["locUsMi"]},
        }
    },
    "icon": "BsInboxes",
    "type": "pane",
    "variant": "context",
    "order": 4,
    "bar": "upper",
},
```
</details>

<details>
  <summary>Filter pane</summary>

```py
"filter": {
    "icon": "FaFilter",
    "type": "pane",
    "variant": "filter",
    "order": 5,
    "bar": "upper",
},
```
</details>

<details>
  <summary>Session pane</summary>

```py
"CustomSessionPane": {
    "name": "Sessions",
    "icon": "MdApi",
    "type": "pane",
    "variant": "session",
    "bar": "upper",
    "order": 0,
},
```
</details>

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`color`](../common_keys/common_keys.md#color)
- [`data`](../common_keys/common_keys.md#data)
- [`enabled`](../common_keys/common_keys.md#enabled)
- [`help`](../common_keys/common_keys.md#help)
- [`icon`](../common_keys/common_keys.md#icon)
- [`label`](../common_keys/common_keys.md#label)
- [`layout`](../common_keys/common_keys.md#layout)
- [`maxValue`](../common_keys/common_keys.md#max-value)
- [`minValue`](../common_keys/common_keys.md#min-value)
- [`name`](../common_keys/common_keys.md#name)
- [`order`](../common_keys/common_keys.md#order)
- [`prop > type`](../common_keys/common_keys.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`value`](../common_keys/common_keys.md#value)
- [`variant`](../common_keys/common_keys.md#variant)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`customObjKey*` | Required | A custom key wrapper for the custom pane.
`customObjKey*.type` | Required | The type of object shown - takes one of these values: `map`, `stat`, `kpi`, `pane`, or `button`. The type given changes what other props can be given to the object.
`customObjKey*.bar` | Required | The section of the `appBar` to display the object in. Accepts either `upper` or `lower`. The use of both bar sections is not required, and any object can be shown in either bar.
`customMapKey*.static` | `False` | If `True`, the viewport of this map cannot be changed manually, but can only be switched between the default and optional viewports given in the `map` top-level key.
`customButtonKey.apiCommand`<br> | | A string to pass to the API when the button is pressed.
`customButtonKey.dashboardLayout` | `[]` | A list of chart items (max of 4 items currently supported) that belong to the current dashboard. Each chart item contains the following keys: `chart`, `grouping`, `statistic`, `category`, `level`, `type`, and `lockedLayout`.
`customButtonKey.dashboardLayout.*.*.category` | | The category selected from the "**Group By**" drop-down menu of a chart in a dashboard view. This key is different from the common key [`category`](../common_keys/common_keys.md#category).
`customButtonKey.dashboardLayout.*.*.category2` | | The category selected from the "**Sub Group**" drop-down menu of a chart in a dashboard view. This uses the data resulting from "**Group By**" as input and allows you to further divide it based on the selected `category2` and [`level2`](#level2).
`customButtonKey.dashboardLayout.*.*.chart` | | The chart type selected from the top-left drop-down menu of a chart in a dashboard view. The `chart` key sets the type of chart to one of these values: [`'Bar'`], [`'Line'`], [`'Box Plot'`].
`customButtonKey.dashboardLayout.*.*.grouping` | | A statistical or mathematical function selected by the user from a predefined set, to be applied over the data and rendered in a chart. It takes one of the following values: `'Sum'`, `'Average'`, `'Minimum'` or `'Maximum'`.
`customButtonKey.dashboardLayout.*.*.kpi` | | The KPI selected from the "**KPIs**" drop-down menu of a chart in a dashboard view if the chart `type='kpis'`
`customButtonKey.dashboardLayout.*.*.level` | | The second-level aggregation selected from the "**Group By**" drop-down menu of a chart in a dashboard view.
<a name="level2">`customButtonKey.dashboardLayout.*.*.level2`</a> | | The second-level aggregation selected from the "**Sub Group**" drop-down menu of a chart in a dashboard view.
`customButtonKey.dashboardLayout.*.*.lockedLayout` | `False` | A boolean to indicate if the layout on this chart can be changed by users.
`customButtonKey.dashboardLayout.*.*.statistic` | | The statistic selected from the "**Statistic**" drop-down menu of a chart in a dashboard view if the chart `type='stats'`
`customButtonKey.dashboardLayout.*.*.type` | `'stats'` | This has two options: `'stats'` or `'kpis'`
`customButtonKey.lockedLayout` | `False` | If `True`, prevents users from modifying the layout of a dashboard view by adding or removing charts.
`customContextPaneKey*.data.customContextData*` | | This represents the data structure created by the client to store each context in a list of contexts. Initial values can be provided by the API designer if needed.
`customContextPaneKey*.data.customContextData*`&swarhk;<br>`.applyCategories` | | Used **only** with a [`context`](#context-pane) pane, it takes a dictionary of [`category_*`](#category_)s, each of which is paired with a partial list of its [`customDataChunck*`](../all_keys/categories.md#customDataChunck) keys. This data is normally generated by user interactions as they build out contexts and returned to the API on a `configure` or `solve` request. Initial values can be provided by the API designer if needed.
`customContextPaneKey*.data.customContextData*`&swarhk;<br>`.applyCategories.category*.customDataChunck*` | | See [`customDataChunck*`](../all_keys/categories.md#customDataChunck).
`customContextPaneKey*.data.customContextData*`&swarhk;<br>`.prop` | | Used in the `data` portion of a [`context`](#context-pane) pane to note which prop the current context is altering. Takes a `customPropKey*`.
`customPaneKey*.props.customPropKey*` | | See [`customPropKey*`](../common_keys/props.md#customPropKey).
`customPaneKey*.props.customPropKey*`&swarhk;<br>`.value.customOption*` | | See [`customOption*`](../common_keys/props.md#customOption).
`customContextPaneKey*.props.customPropKey*`&swarhk;<br>`.selectableCategories` | Required | Used in a [`context`](#context-pane) pane, it takes a list of [`category_*`](#category_) keys (**only**). These are the used to determine which categories this context can be applied to.
`customPaneKey*.teamSync` | `False` | If `True`, creates a sync button on the top of the pane. When that sync button is clicked, everything in that pane is synced across all sessions for that team (or user if individual session) such that all other sessions for that team have the exact same pane as it exists in the current session.
`customPaneKey*.teamSyncCommand` | | If specified, passes an API command argument along with a mutation request. This command will be passed to `execute_command` for each session to be synced.
`customPaneKey*.teamSyncCommandKeys` | | If specified, only passes specific session keys over to `execute_command` for each session to be synced.
<a name="pane-variant">`customPaneKey*.variant`</a> | `'options'` | As a direct child of `customPaneKey*`, the `variant` key configures a pane to be an `'options'` or `'context'` pane. Each variant comes along with additional keys that add specific functionality to the pane.
`customPaneKey*.width` | `'auto'` | Sets the width of the pane. This property is an exact equivalent of the [CSS `width` property](https://developer.mozilla.org/en-US/docs/Web/CSS/width). If set to `'auto'`, the pane will stretch to fit its content with a width no less than `'450px'`. If the specified width exceeds the width of the viewport, the pane will match the width of the viewport.
`paneState.open` | | Takes a `customPaneKey*` value to cause the referenced pane to open when the app loads.
`filtered` | `{}` | Takes key value pairs where the keys are category keys, and the values are lists of lowest level items in that category to be included (not filtered out). If a category is not included in this dictionary then all items in that category are displayed.

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"appBar": {
    "data": {
        "session": {
            "icon": "MdApi",
            "type": "pane",
            "variant": "session",
            "bar": "upper",
            "order": 0,
        },
        "appSettings": {
            "icon": "MdOutlineSettings",
            "type": "pane",
            "variant": "appSettings",
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
            "name": "Example Props Pane",
            "props": {
                "numericHeader": {
                    "name": "Numeric Props",
                    "type": "head",
                    "help": "Some help for numeric props",
                },
                "numericInputExample": {
                    "name": "Numeric Input Example",
                    "type": "num",
                    "value": 50,
                    "enabled": True,
                    "help": "Help for the numeric input example",
                    "maxValue": 100,
                    "minValue": 0,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "units",
                    },
                },
                "numericSliderExample": {
                    "name": "Numeric Slider Example",
                    "type": "num",
                    "value": 50,
                    "enabled": True,
                    "variant": "slider",
                    "help": "Help for the numeric slider example",
                    "maxValue": 100,
                    "minValue": 0,
                },
                "miscHeader": {
                    "name": "Misc Props",
                    "type": "head",
                    "help": "Some help for miscelanous props",
                },
                "toggleInputExample": {
                    "name": "Toggle Input Example",
                    "type": "toggle",
                    "value": True,
                    "enabled": True,
                    "help": "Help for the toggle input example",
                },
                "buttonInputExample": {
                    "name": "Button Input Example (Creates an Error)",
                    "value": "Press Me!",
                    "type": "button",
                    "apiCommand": "test",
                    "enabled": True,
                    "help": "Press this button to create an error",
                },
                "textInputExample": {
                    "name": "Text Input Example",
                    "type": "text",
                    "value": "Example Text Here",
                    "enabled": True,
                    "help": "Help for the text input example",
                },
                "selectorHeader": {
                    "name": "Selection Props",
                    "type": "head",
                    "help": "Some help for Selection Props",
                },
                "dropdownItemExample": {
                    "name": "Dropdown Item Example",
                    "type": "selector",
                    "variant": "dropdown",
                    "value": [
                        {"name": "Option A", "value": False},
                        {"name": "Option B", "value": False},
                        {"name": "Option C", "value": True},
                    ],
                    "enabled": True,
                    "help": "Select an option from the dropdown",
                },
                "checkboxItemExample": {
                    "name": "Checkbox Item Example",
                    "type": "selector",
                    "variant": "checkbox",
                    "value": [
                        {"name": "Option A", "value": True},
                        {"name": "Option B", "value": False},
                        {"name": "Option C", "value": True},
                    ],
                    "enabled": True,
                    "help": "Select all relevant items",
                },
                "radioItemExample": {
                    "name": "Radio Item Example",
                    "type": "selector",
                    "variant": "radio",
                    "value": [
                        {"name": "Option A", "value": True},
                        {"name": "Option B", "value": False},
                        {"name": "Option C", "value": False},
                    ],
                    "enabled": True,
                    "help": "Select one item from the list",
                },
            },
            "layout": {
                "type": "grid",
                "numColumns": 3,
                "numRows": "auto",
                "data": {
                    "col1Row1": {
                        "type": "item",
                        "column": 1,
                        "row": 1,
                        "itemId": "numericHeader",
                    },
                    "col1Row2": {
                        "type": "item",
                        "column": 1,
                        "row": 2,
                        "itemId": "numericInputExample",
                    },
                    "col1Row3": {
                        "type": "item",
                        "column": 1,
                        "row": 3,
                        "itemId": "numericSliderExample",
                    },
                    "col2Row1": {
                        "type": "item",
                        "column": 2,
                        "row": 1,
                        "itemId": "miscHeader",
                    },
                    "col2Row2": {
                        "type": "item",
                        "column": 2,
                        "row": 2,
                        "itemId": "toggleInputExample",
                    },
                    "col2Row3": {
                        "type": "item",
                        "column": 2,
                        "row": 3,
                        "itemId": "buttonInputExample",
                    },
                    "col2Row4": {
                        "type": "item",
                        "column": 2,
                        "row": 4,
                        "itemId": "textInputExample",
                    },
                    "col3Row1": {
                        "type": "item",
                        "column": 3,
                        "row": 1,
                        "itemId": "selectorHeader",
                    },
                    "col3Row2": {
                        "type": "item",
                        "column": 3,
                        "row": 2,
                        "itemId": "dropdownItemExample",
                    },
                    "col3Row3": {
                        "type": "item",
                        "column": 3,
                        "row": 3,
                        "itemId": "checkboxItemExample",
                    },
                    "col3Row4": {
                        "type": "item",
                        "column": 3,
                        "row": 4,
                        "itemId": "radioItemExample",
                    },
                },
            },
            "icon": "FaCogs",
            "type": "pane",
            "variant": "options",
            "bar": "upper",
            "order": 3,
        },
        "context": {
            "name": "Context Pane",
            "props": {
                "numericContextProp": {
                    "type": "num",
                    "value": 100,
                    "enabled": True,
                    "help": "Numeric Context Prop Help",
                    "label": "%",
                    "variant": "slider",
                    "maxValue": 500,
                    "minValue": 0,
                    "selectableCategories": ["location", "sku"],
                },
            },
            "data": {
                "context1": {
                    "prop": "numericContextProp",
                    "value": 110,
                    "applyCategories": {"location": ["locUsMi"]},
                }
            },
            "icon": "BsInboxes",
            "type": "pane",
            "variant": "context",
            "order": 4,
            "bar": "upper",
        },
        "filter": {
            "icon": "FaFilter",
            "type": "pane",
            "variant": "filter",
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
            "dashboardLayout": [
                {
                    "chart": "Bar",
                    "grouping": "Average",
                    "statistic": "numericStatExampleA",
                },
                {
                    "chart": "Line",
                    "grouping": "Sum",
                    "statistic": "numericStatExampleB",
                },
                {
                    "chart": "Bar",
                    "level": "size",
                    "category": "sku",
                    "grouping": "Sum",
                    "statistic": "numericExampleCalculationStat",
                },
                {
                    "type": "kpis",
                    "chart": "Bar",
                    "grouping": "Sum",
                    "sessions": [],
                    "kpi": "kpi5",
                },
            ],
            "lockedLayout": False,
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

[`'Bar'`]: <https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-Y%20Axis=true&knob-vertical%20gridlines=true&knob-horizontal%20gridlines=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&selectedKind=Series%2FVerticalBarSeries%2FBase&selectedStory=multiple%20VerticalBarSeries%20-%20clustered&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs>
[`'Line'`]: https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&knob-vertical%20gridlines=true&knob-stroke=%2312939a&knob-horizontal%20gridlines=true&knob-opacity=1&knob-curve=curveBasis&knob-fill=%2312939a&knob-style=%7B%22stroke%22%3A%22%232c51be%22%2C%22strokeWidth%22%3A%223px%22%7D&knob-colorScale=category&knob-Y%20Axis=true&selectedKind=Series%2FLineSeries%2FBase&selectedStory=With%20negative%20numbers&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs
[`'Box Plot'`]: https://plotly.com/javascript/box-plots/
