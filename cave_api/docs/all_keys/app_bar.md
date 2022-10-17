### `appBar`
The `appBar` key allows API designers to create a custom bar located on the left of the CAVE app. This bar allows for navigation between the different views of the app (e.g. Map, Dashboards), as well as interaction with panes. The `appBar` is split into two sections: `upper` and `lower`. Using both sections is not required, but it is generally recommended that `lower` be used for navigation through the CAVE app views and `upper` for interactive panes and buttons.

The structure of the `appBar` group looks as follows:
```py
'appBar': {
    'data': {
        'custom_button_1': {
            'name': 'Solve Button',
            'bar': 'upper',
            'icon': 'BsLightningFill',
            'color': {
                'dark': 'rgb(64, 179, 54)',
                'light': 'rgb(24, 73, 20)',
            },
            'apiCommand': 'solve_session',
            'type': 'button',
            'order': 1,
        },
        'custom_pane_key_1': {
            'name': 'Settings Big Pane',
            'width': '100%',
            'bar': 'upper',
            'props': {
                'custom_prop_key_1': {
                    'name': 'Solver Section',
                    'type': 'head',
                    'help': 'Some help for the solver section',
                },
                'custom_prop_key_2': {...},
                # As many custom props as needed for this pane
            },
            'layout': {

            },
            'icon': 'BsWrench',
            'color': {
                'dark': 'rgb(46, 244, 208)',
                'light': 'rgb(17, 79, 68)',
            },
            'type': 'pane',
            'variant': 'options',
            'order': 2,
        },
        'custom_map_1': {
            'type': 'map',
            'bar': 'lower',
            'icon': 'FaMapMarkedAlt',
            'static': True,
            'color': {
                'dark': 'rgb(178, 179, 55)',
                'light': 'rgb(79, 79, 24)',
            },
        },
        'custom_filter_pane': {
            'icon': 'FaFilter',
            'bar': 'upper',
            'type': 'pane',
            'variant': 'filter',
            'order': 3,
        },
        'custom_appBar_obj': {...},
        # As many custom objects as needed
    },
    'paneState':{
        'open': 'custom_pane_key_1',
    },
    'filtered':{
        'category_1': 'custom_data_chunk_1',
    },
}
```

#### Panes
Panes are subitems of the `appBar` group and are constructs primarily used to place UI controls (toggles, text and number fields, sliders, etc.), as well as buttons to allow interaction with actionable data. Therefore, custom panes can be designed to enable users to tune up the parameters of a simulation, navigate through different case study scenarios, reset the state of a simulation, synchronize data or settings with other users, and so on.

Panes can be of different [`variant`](#pane-variant)s, so to keep the data structure examples simple and modular, you can examine each one at a time in the following switchables:

<details>
  <summary>Options pane</summary>

```py
'custom_pane_key_1': {
    'name': 'A name to be displayed in the UI',
    'width': '50%',
    'bar': 'upper',
    'props': {
        'custom_prop_key_1': {
            'name': 'Section header',
            'type': 'head',
            'help': 'A help text for the section header',
        },
        'custom_prop_key_2': {
            'enabled': True,
            'name': 'A name to be displayed in the UI',
            'type': 'num',
            'value': 1,
            'numberFormat': {
                'precision': 0,
                'unit': 'units',
            },
            'help': 'A help text for the numeric input',
        },
        'custom_prop_key_3': {
            'name': 'A name to be displayed in the UI',
            'type': 'num',
            'variant': 'slider',
            'value': 30,
            'minValue': 0,
            'maxValue': 100,
            'label': '%',
            'help': 'A help text for the slider',
        },
        'custom_prop_key_4': {
            'enabled': True,
            'name': 'A name to be displayed in the UI',
            'type': 'selector',
            'variant': 'dropdown',
            'value': {
                'custom_option_1': False,
                'custom_option_2': True,
                'custom_option_3': False,
            },
            'help': 'A help text for the dropdown selector',
        },
        # As many props as needed
    },
    'layout': {...},
    'icon': 'IoOptions',
    'color': {
        'dark': 'rgb(64, 179, 54)',
        'light': '#184914',
    },
    'type': 'pane',
    'variant': 'options'
    'teamSync': True,
    'order': 1,
}
```
</details>

<details>
  <summary>Context pane</summary>

```py
'custom_pane_key_3': {
    'bar': 'upper',
    'props': {
        'custom_prop_key_8': {
            'enabled': True,
            'type': 'num',
            'value': 100,
            'help': 'A help text for the numeric input',
            'label': '%',
            'variant': 'slider',
            'maxValue': 500,
            'minValue': 0,
            'selectableCategories': ['category_2'],
        },
        'custom_prop_key_9': {
            'enabled': True,
            'type': 'num',
            'value': 100,
            'help': 'A help text for the numeric input',
            'label': 'x',
            'minValue': 0,
            'numberFormat': {
                'precision': 0,
            },
            'selectableCategories': ['category_1', 'category_2'],
        },
        # As many props as needed
    },
    'data': {
        'custom_context_data_1': {
            'prop': 'custom_prop_key_8',
            'value': 110,
            'applyCategories': {
                'category_1': [
                    'custom_data_chunk_1',
                    'custom_data_chunk_2',
                ],
            },
        },
        'custom_context_data_2': {...},
        # As many context data as needed
    },
    'icon': 'FaBox',
    'type': 'pane',
    'variant': 'context',
    'order': 4,
}
```
</details>

The CAVE app also includes two built in pane variants: `filter`, which provides tools to filter data from different categories and at different levels of granularity, and `appSettings`, which gives users the ability to control the appearance and overall behavior of the CAVE app.

##### Common keys
- [`allow_modification`](../common_keys/common_keys.md#allow_modification)
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
- [`send_to_api`](../common_keys/common_keys.md#send_to_api)
- [`send_to_client`](../common_keys/common_keys.md#send_to_client)
- [`value`](../common_keys/common_keys.md#value)
- [`variant`](../common_keys/common_keys.md#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`custom_obj_key_*` | Required | A custom key wrapper for the custom pane.
`custom_obj_key_*.type` | Required | The type of object shown - takes one of these values: `map`, `stat`, `kpi`, `pane`, or `button`. The type given changes what other props can be given to the object.
`custom_obj_key_*.bar` | Required | The section of the `appBar` to display the object in. Accepts either `upper` or `lower`. The use of both bar sections is not required, and any object can be shown in either bar.
`custom_map_key_*.static` | `False` | If `True`, the viewport of this map cannot be changed manually, but can only be switched between the default and optional viewports given in the `map` top-level key.
`custom_button_key_*.apiCommand`<br> | | A string to pass to the API when the button is pressed.
`custom_button_key_*.dashboardLayout` | `[]` | A list of chart items (max of 4 items currently supported) that belong to the current dashboard. Each chart item contains the following keys: `chart`, `grouping`, `statistic`, `category`, `level`, `type`, and `lockedLayout`.
`custom_button_key_*.dashboardLayout.*.*.category` | | The category selected from the "**Group By**" drop-down menu of a chart in a dashboard view. This key is different from the common key [`category`](../common_keys/common_keys.md#category).
`custom_button_key_*.dashboardLayout.*.*.chart` | | The chart type selected from the top-left drop-down menu of a chart in a dashboard view. The `chart` key sets the type of chart to one of these values: [`'Bar'`], [`'Line'`], [`'Box Plot'`].
`custom_button_key_*.dashboardLayout.*.*.grouping` | | A statistical or mathematical function selected by the user from a predefined set, to be applied over the data and rendered in a chart. It takes one of the following values: `'Sum'`, `'Average'`, `'Minimum'` or `'Maximum'`.
`custom_button_key_*.dashboardLayout.*.*.kpi` | | The KPI selected from the "**KPIs**" drop-down menu of a chart in a dashboard view if the chart `type='kpis'`
`custom_button_key_*.dashboardLayout.*.*.level` | | The second-level aggregation selected from the "**Group By**" drop-down menu of a chart in a dashboard view.
`custom_button_key_*.dashboardLayout.*.*.lockedLayout` | `False` | A boolean to indicate if the layout on this chart can be changed by users.
`custom_button_key_*.dashboardLayout.*.*.statistic` | | The statistic selected from the "**Statistic**" drop-down menu of a chart in a dashboard view if the chart `type='stats'`
`custom_button_key_*.dashboardLayout.*.*.type` | `'stats'` | This has two options: `'stats'` or `'kpis'`
`custom_button_key_*.lockedLayout` | `False` | If `True`, prevents users from modifying the layout of a dashboard view by adding or removing charts.
`custom_context_pane_key_*.data.custom_context_data_*` | | This represents the data structure created by the client to store each context in a list of contexts. Initial values can be provided by the API designer if needed.
`custom_context_pane_key_*.data.custom_context_data_*`&swarhk;<br>`.applyCategories` | | Used **only** with a [`context`](#context-pane) pane, it takes a dictionary of [`category_*`](#category_)s, each of which is paired with a partial list of its [`custom_data_chunk_*`](../all_keys/categories.md#custom_data_chunk_) keys. This data is normally generated by user interactions as they build out contexts and returned to the API on a `configure` or `solve` request. Initial values can be provided by the API designer if needed.
`custom_context_pane_key_*.data.custom_context_data_*`&swarhk;<br>`.applyCategories.category_*.custom_data_chunk_*` | | See [`custom_data_chunk_*`](../all_keys/categories.md#custom_data_chunk_).
`custom_context_pane_key_*.data.custom_context_data_*`&swarhk;<br>`.prop` | | Used in the `data` portion of a [`context`](#context-pane) pane to note which prop the current context is altering. Takes a `custom_prop_key_*`.
`custom_pane_key_*.props.custom_prop_key_*` | | See [`custom_prop_key_*`](../common_keys/props.md#custom_prop_key_).
`custom_pane_key_*.props.custom_prop_key_*`&swarhk;<br>`.value.custom_option_*` | | See [`custom_option_*`](../common_keys/props.md#custom_option_).
`custom_context_pane_key_*.props.custom_prop_key_*`&swarhk;<br>`.selectableCategories` | Required | Used in a [`context`](#context-pane) pane, it takes a list of [`category_*`](#category_) keys (**only**). These are the used to determine which categories this context can be applied to.
`custom_pane_key_*.teamSync` | `False` | If `True`, creates a sync button on the top of the pane. When that sync button is clicked, everything in that pane is synced across all sessions for that team (or user if individual session) such that all other sessions for that team have the exact same pane as it exists in the current session.
`custom_pane_key_*.teamSyncCommand` | | If specified, passes an API command argument along with a mutation request. This command will be passed to `execute_command` for each session to be synced.
`custom_pane_key_*.teamSyncCommandKeys` | | If specified, only passes specific session keys over to `execute_command` for each session to be synced.
<a name="pane-variant">`custom_pane_key_*.variant`</a> | `'options'` | As a direct child of `custom_pane_key_*`, the `variant` key configures a pane to be an `'options'` or `'context'` pane. Each variant comes along with additional keys that add specific functionality to the pane.
`custom_pane_key_*.width` | `'450px'` | Sets the width of the pane. This property is an exact equivalent of the [CSS `width` property](https://developer.mozilla.org/en-US/docs/Web/CSS/width). If set to `'auto'`, the width of the pane will adjust to fit its content. If the specified width exceeds the width of the viewport, the pane will match the width of the viewport.
`paneState.open` | | Takes a `custom_pane_key_*` value to cause the referenced pane to open when the app loads.
`filtered` | `{}` | Takes key value pairs where the keys are category keys, and the values are lists of lowest level items in that category to be included (not filtered out). If a category is not included in this dictionary then all items in that category are displayed.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'appBar': {
    'data': {
        'button_1': {
            'name': 'Solve Button',
            'icon': 'BsLightningFill',
            'color': {
                'dark': 'rgb(64, 179, 54)',
                'light': 'rgb(24, 73, 20)',
            },
            'apiCommand': 'solve_session',
            'type': 'button',
            'bar': 'upper',
        },
        'settingsBig': {
            'name': 'Settings Big Pane',
            'width': '100%',
            'props': {
                'solver_section': {
                    'name': 'Solver Section',
                    'type': 'head',
                    'help': 'Some help for the solver section',
                },
                'Solver': {
                    'name': 'Solver',
                    'type': 'selector',
                    'variant': 'dropdown',
                    'value': [
                        {'name': 'Gurobi', 'value': True},
                        {'name': 'Cplex', 'value': False},
                        {'name': 'CoinOR', 'value': False},
                    ],
                    'enabled': True,
                    'help': 'Select a solver type to use',
                },
                'optimality_section': {
                    'name': 'Optimality Section',
                    'type': 'head',
                    'help': 'Some help for the optimality section',
                },
                'Pct_Optimal': {
                    'name': 'Percent Optimal',
                    'type': 'num',
                    'value': 97,
                    'enabled': True,
                    'variant': 'slider',
                    'help': 'What percent of optimal would you like to solve to?',
                    'maxValue': 100,
                    'minValue': 0,
                },
                'distance_section': {
                    'name': 'Demand Served At Distances',
                    'type': 'head',
                    'help': 'How much demand do you expect to serve at the following distances?',
                },
                '50_miles': {
                    'name': '50 Miles',
                    'type': 'num',
                    'value': 45,
                    'enabled': True,
                    'variant': 'slider',
                    'help': 'Expected demand filled at 50 miles',
                    'maxValue': 100,
                    'minValue': 0,
                },
                '100_miles': {
                    'name': '100 Miles',
                    'type': 'num',
                    'value': 35,
                    'enabled': True,
                    'variant': 'slider',
                    'help': 'Expected demand filled at 100 miles',
                    'maxValue': 100,
                    'minValue': 0,
                },
                '150_miles': {
                    'name': '150 Miles',
                    'type': 'num',
                    'value': 25,
                    'enabled': True,
                    'variant': 'slider',
                    'help': 'Expected demand filled at 150 miles',
                    'maxValue': 100,
                    'minValue': 0,
                },
            },
            'layout': {
                'type': 'grid',
                'num_columns': 3,
                'num_rows': 'auto',
                'data': {
                    'col1_row1': {
                        'type': 'item',
                        'itemId': 'solver_section',
                        'column': 1,
                        'row': 1,
                    },
                    'Solver': {
                        'type': 'item',
                        'itemId': 'Solver',
                        'column': 1,
                    },
                    'col2_row1': {
                        'type': 'item',
                        'itemId': 'optimality_section',
                        'column': 2,
                        'row': 1,
                    },
                    'Pct_Optimal': {
                        'type': 'item',
                        'itemId': 'Pct_Optimal',
                        'column': 2,
                    },
                    'col3_row1': {
                        'type': 'item',
                        'itemId': 'distance_section',
                        'column': 3,
                        'row': 1,
                    },
                    '50_miles': {
                        'type': 'item',
                        'itemId': '50_miles',
                        'column': 3,
                    },
                    '100_miles': {
                        'type': 'item',
                        'itemId': '100_miles',
                        'column': 3,
                    },
                    '150_miles': {
                        'type': 'item',
                        'itemId': '150_miles',
                        'column': 3,
                    },
                },
            'icon': 'BsWrench',
            'color': {
                'dark': 'rgb(46, 244, 208)',
                'light': 'rgb(17, 79, 68)',
            },
            'type': 'pane',
            'variant': 'options',
            'bar': 'upper',
            'order': 2,
        },
        'options': {
            'name': 'Options Pane',
            'props': {
                'Combine_Materials': {
                    'type': 'selector',
                    'value': [
                        {'name': 'True', 'value': True},
                        {'name': 'False', 'value': False},
                    ],
                    'enabled': True,
                    'help': 'Do you want to combine materials and treat them equally when solving?',
                    'variant': 'radio',
                },
                'Meet_Monthly_Demand': {
                    'type': 'selector',
                    'value': [
                        {'name': 'True', 'value': True},
                        {'name': 'False', 'value': False},
                    ],
                    'enabled': True,
                    'help': 'Do you want to force the solver to meet the monthly demand thresholds?',
                    'variant': 'radio',
                },
                'Combined Options': {
                    'name': 'Combined Options',
                    'type': 'selector',
                    'variant': 'checkbox',
                    'value': [
                        {'name': 'Meet Monthly Demand', 'value': True},
                        {'name': 'Combine Materials', 'value': False},
                    ],
                    'enabled': True,
                    'help': 'Help for both options',
                },
            },
            'icon': 'MdSettings',
            'type': 'pane',
            'variant': 'options',
            'bar': 'upper',
            'order': 1,
        },
        'map_1': {
            'type': 'map',
            'icon': 'FaMapMarkedAlt',
            'bar': 'upper',
            'color': {
                'dark': 'rgb(178, 179, 55)',
                'light': 'rgb(79, 79, 24)',
            },
        },
        'filter': {
            'icon': 'FaFilter',
            'type': 'pane',
            'variant': 'filter',
            'order': 6,
            'bar': 'upper',
        },
        'appSettings': {
            'icon': 'MdOutlineSettings',
            'type': 'pane',
            'variant': 'appSettings',
            'bar': 'upper',
        },
        'context': {
            'props': {
                'Demand_Multiplier': {
                    'type': 'num',
                    'value': 100,
                    'enabled': True,
                    'help': 'Percentage multiplier times the base demand (100%=Given Demand)',
                    'label': '%',
                    'variant': 'slider',
                    'maxValue': 500,
                    'minValue': 0,
                    'selectableCategories': ['Location', 'Product'],
                },
                'Supply_Multiplier': {
                    'type': 'num',
                    'value': 100,
                    'enabled': True,
                    'help': 'Percentage multiplier times the base supply (100%=Given Supply)',
                    'label': '%',
                    'minValue': 0,
                    'numberFormat': {
                        'precision': 0,
                    },
                    'selectableCategories': ['Location', 'Product'],
                },
            },
            'data': {
                'context_1': {
                    'prop': 'Demand_Multiplier',
                    'value': 110,
                    'applyCategories': {'Location': ['loc_US_MI']},
                }
            },
            'icon': 'BsInboxes',
            'type': 'pane',
            'variant': 'context',
            'order': 4,
            'bar': 'upper',
        },
        'settings': {
            'name': 'Settings Pane',
            'props': {
                'Solver': {
                    'name': 'Solver',
                    'type': 'selector',
                    'variant': 'dropdown',
                    'value': [
                        {'name': 'Gurobi', 'value': True},
                        {'name': 'Cplex', 'value': False},
                        {'name': 'CoinOR', 'value': False},
                    ],
                    'enabled': True,
                    'help': 'Select a solver type to use'
                },
                'optimality_section': {
                    'name': 'Optimality Section',
                    'type': 'head',
                    'help': 'Some help for the optimality section',
                },
                'Pct_Optimal': {
                    'name': 'Percent Optimal',
                    'type': 'num',
                    'value': 97,
                    'enabled': True,
                    'help': 'What percent of optimal would you like to solve to?',
                    'maxValue': 100,
                    'minValue': 0,
                },
            },
            'icon': 'BsWrench',
            'color': {
                'dark': 'rgb(64, 179, 54)',
                'light': 'rgb(24, 73, 20)',
            },
            'type': 'pane',
            'variant': 'options',
            'teamSync': True,
            'bar': 'lower',
            'order': 1,
        },
        'dash_1': {
            'icon': 'BsCircleFill',
            'name': 'Dashboard 1',
            'type': 'stats',
            'color': {
                'dark': 'rgb(178, 179, 55)',
                'light': 'rgb(79, 79, 24)',
            },
            'order': 2,
            'bar': 'lower',
            'dashboardLayout': [
                {
                    'chart': 'Bar',
                    'grouping': 'Average',
                    'statistic': 'demand_met',
                },
                {
                    'chart': 'Line',
                    'grouping': 'Sum',
                    'statistic': 'demand_pct',
                },
                {
                    'chart': 'Bar',
                    'level': 'Size',
                    'category': 'Product',
                    'grouping': 'Sum',
                    'statistic': 'demand_met',
                },
                {
                    'chart': 'Bar',
                    'grouping': 'Minimum',
                    'type': 'kpis',
                    'sessions': [],
                    'kpi': 'Really Big Number',
                },
            ],
            'lockedLayout': False,
        },
        'kpi_1': {
            'type': 'kpi',
            'icon': 'MdSpeed',
            'bar': 'lower',
            'color': {
                'dark': 'rgb(224, 224, 224)',
                'light': 'rgb(32, 32, 32)',
            },
            'order': 3,
        },
    }
}
```
</details>

[`'Bar'`]: <https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-Y%20Axis=true&knob-vertical%20gridlines=true&knob-horizontal%20gridlines=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&selectedKind=Series%2FVerticalBarSeries%2FBase&selectedStory=multiple%20VerticalBarSeries%20-%20clustered&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs>
[`'Line'`]: https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&knob-vertical%20gridlines=true&knob-stroke=%2312939a&knob-horizontal%20gridlines=true&knob-opacity=1&knob-curve=curveBasis&knob-fill=%2312939a&knob-style=%7B%22stroke%22%3A%22%232c51be%22%2C%22strokeWidth%22%3A%223px%22%7D&knob-colorScale=category&knob-Y%20Axis=true&selectedKind=Series%2FLineSeries%2FBase&selectedStory=With%20negative%20numbers&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs
[`'Box Plot'`]: https://plotly.com/javascript/box-plots/
