# CAVE App design
This document describes the data structure scheme used by a CAVE application to render custom user interfaces that accommodate to the use cases and preferences of a designer.

## CAVE API Structure
The CAVE API Structure is the core data structure required for user interface design of the CAVE App. Its primary purpose is to place, rearrange, style, and specify the behavior of most of the UI elements in a CAVE application.

At first glance, the top-level keys in the data structure look like this:
```py
{
    'settings': {...},
    'categories': {...},
    'appBar': {...},
    'arcs': {...},
    'nodes': {...},
    'geos': {...},
    'map': {...},
    'stats': {...},
    'kpis': {...},
    'kwargs':{...}
}
```
Throughout this documentation, we refer to the keys in the data structure above as _top-level keys_ (or _top-level groups_ to point out that these keys contain other key-value pairs).

Each top-level group might include unique elements or sub-keys that are specific to that group ([special keys](#special-keys)). However, other keys like `send_to_api` are meant to attach functionality that is more generic and therefore can be used in different top-level groups. To save time and [not repeat ourselves](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) throughout this documentation, we provide a "[Common keys](#common-keys)" section in advance, and any such keys found throughout this document are referred back to their definition.

There is a third type of keys ([custom keys](#custom-keys)), which depend on the data and, therefore, their names vary according to the use case. The designer can name these keys in the data structure at their convenience. Let's take a look at the following example where custom keys are used:
```py
{
    'categories': {
        'data':{
            'custom_location': {
                'data': {
                    'custom_loc_us_mi': {
                        'custom_region': 'North America',
                        'custom_country': 'USA',
                        'custom_state': 'Michigan'
                    },
                    'custom_loc_us_ma': {
                        'custom_region': 'North America',
                        'custom_country': 'USA',
                        'custom_state': 'Massachusetts'
                    },
                ...
                },
            }
        }
    }
}
```

Here, `custom_location`, `custom_loc_us_mi`, `custom_loc_us_ma`, `custom_region`, `custom_country`, and `custom_state` are all custom keys. These key names are not restricted and can be tied to the problem or use case data. These also do not need to be preceded by `custom_`, but this tag is used to indicate that they are custom keys for example purposes. (Throughout this document, if not explicitly mentioned, all custom keys are preceded by the `custom_` tag whenever they are found in an example.)

Custom keys are always included as a direct child of common keys such as `data`, `props`, `types`, and `category`, but they also appear as a direct child of less frequent keys such as `nestedStructure`, `propDefaults`, or even within another custom key, as shown in the structure above.

### Common keys
#### At the Top level
Key | Default | Description
--- | ------- | -----------
<a name="allow_modification">`allow_modification`</a> | `True` | If `True`, end users can request changes to the data within the key group during user interaction with the CAVE app and the server will process the request. Note, this only blocks a user from being able to modify a server side structure for security reasons. To block client side interactions, see the [`enabled`](#enabled) key.
<a name="data">`data`</a> | Required | Dictionary object that contains data related to this key group.
<a name="send_to_api">`send_to_api`</a> | `True` | If `True`, the data will be serialized and sent when calling `solve` and `configure` in the API.
<a name="send_to_client">`send_to_client`</a> | `True` | If `True`, the data will be sent to the requesting CAVE app client. (This is used for API state management.)

#### Nested inside the `data` group
Key | Default | Description
--- | ------- | -----------
<a name="category">`category`</a> | | A dictionary of category custom keys appropriated to a string or list of strings (custom keys inside each custom category). This is used in an object to associate categories for aggregation and filtering purposes.
<a name="color">`color`</a> | | The color to be appropriated to the current object.[^1]
<a name="colorBy">`colorBy`</a> | | The parameter selected to show its variation in terms of a color gradient. The color gradient is bounded by [`startGradientColor`](#startGradientColor) and [`endGradientColor`](#endGradientColor). Used in [`arcs`](#arcs), [`nodes`](#nodes) and [`geos`](#geos).
<a name="colorByOptions">`colorByOptions`</a> | | A object with [parameters](#custom_data_key_) keys that are provided for the user to choose from a drop-down menu in the "**Map Legend**" and view their variation in terms of a color gradient. The associated value should be either an object with shape `{"min": 0, "max": 0, "startGradientColor": "rgb(0,0,0)", "endGradientColor": "rbg(0,0,0)"}` that contains the expected minimum and maximum values and color for the parameter Used in [`arcs`](#arcs), [`nodes`](#nodes) and [`geos`](#geos) or a dictionary with shape `{"custom_color_key_here":"rgb(233, 0, 0)"}` for discrete variables. Note: `min` and `max` are reserved keys and should not be provided as a `custom_color_key`.
<a name="column">`column`</a>  | | A column position number (left to right) at which a UI element will be displayed when in a `grid` layout. This includes layouts for([`'options'` panes](#options-pane) or [KPIs](#kpis)) or a map modal ([`arcs`](#arcs), [`nodes`](#nodes), and [`geos`](#geos)). If omitted in a full-width view layout, the element will not be displayed in the UI.
<a name="constraint">`constraint`</a> | `'float'` | Used along a `'num'` type, its value can be `'int'` or `'float'` to enforce integer or floating point values respectively, for a prop element in the UI.
<a name="data">`data`</a> | | Dictionary object that contains data related to the use case.
<a name="endSize">`endSize`</a> | | The end dimension in pixels for a stroke width of an arc or the size of an icon on a node, which matches the maximum value of a given parameter in a set of data points. Used in [`arcs`](#arcs) and [`nodes`](#nodes).
<a name="icon">`icon`</a> | Required | The name of a [React Icon](https://react-icons.github.io/react-icons) that will be displayed in the UI. Currently icons are downloaded after the app has loaded (not in the build) and stored in a local cache. This reduces build size while allowing for all react-icons to be supported.
<a name="layout">`layout`</a> | | A dictionary object that describes how [props](#the-props-key) or [KPIs](#kpis) are organized within their UI container components. See the [layout](#the-layout-key) section for a more detailed explanation of this group and some common use cases.
<a name="name">`name`</a> | | The name of the element to be displayed as a label in the user interface. If omitted, the parent key of the **un`name`d** group is displayed.
<a name="order">`order`</a> | | When specified in a key group, the `order` parameter sets the position in which the element is rendered in the UI, relative to its siblings. The `order` key takes integer values and the sibling elements will be sorted in ascending order. Since this parameter is optional, all **un`order`ed** items will be sorted alphabetically against each other and placed after the **`order`ed** items. Therefore, if you do not specify any `order` for a group of sibling keys, all of them will be sorted alphabetically according to their `name` values (or parent key when `name` is not specified).
<a name="propDefaults">`propDefaults`</a> | | A dictionary object that contains one or more input control definitions (`props` items), to reduce the overhead caused by duplicate items. The `propDefaults` definitions can be overriden by `props` items.
<a name="props">`props`</a> | Required | A dictionary object that contains the specification of the input controls in the UI. The `props` and `propDefaults` items are matched by their parent custom keys. The resulting prop from a match is a union of key-value pairs, with common keys between `props` and `propDefaults` overridden by `props`. See the [props](#the-props-key) section for a more detailed explanation of this group and its different `prop` items.
<a name="sizeBy">`sizeBy`</a> | | The parameter selected to show its variation in terms of stroke width ([`arcs`](#arcs)) or icon size ([`nodes`](#nodes)). The size range is bounded by [`startSize`](#startSize) and [`endSize`](#endSize).
<a name="sizeByOptions">`sizeByOptions`</a> | | An object with [parameters](#custom_data_key_) keys that are provided for the user to choose from a drop-down menu in the "**Map Legend**" and view their variation in terms of stroke width ([`arcs`](#arcs)) or icon size ([`nodes`](#nodes)). The associated value should be an object with shape `{"min": 0, "max": 0}` that contains the expected minimum and maximum values for the parameter.
<a name="startSize">`startSize`</a> | | The starting dimension in pixels for a stroke width of an arc or the size of an icon on a node, which matches the minimum value of a given parameter in a set of data points. Used in [`arcs`](#arcs) and [`nodes`](#nodes).

[^1]: This key matches a string that contains a [color value](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) or a dictionary object with color values per theme keys. The allowed theme keys in the current version are `'dark'` and `'light'`.

#### The `props` key
We dedicate a section to the `props` group, as it handles all of the user input controls, as well as most of the textual or numeric output in the CAVE App. Let's start with an in-depth look at its internal structure and how it translates to the UI.

```py
'props': {
    'custom_prop_key_1': {
        'name': 'Section header',
        'type': 'head',
        'help': 'A help text for the section header',
        'order': 0,
    },
    'custom_prop_key_2': {
        'enabled': True,
        'name': 'A name to be displayed in the UI',
        'type': 'num',
        'value': 1,
        'constraint': 'int',
        'unit': 'units',
        'help': 'A help text for the numeric input',
        'order': 1,
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
        'order': 2,
    },
    'custom_prop_key_4': {
        'enabled': True,
        'name': 'A name to be displayed in the UI',
        'type': 'selector',
        'variant': 'dropdown',
        'value': [
            {'name':'custom_option_1', 'value': False},
            {'name':'custom_option_2', 'value': True},
            {'name':'custom_option_3', 'value': False},
        ],
        'help': 'A help text for the dropdown selector',
        'order': 3,
    },
    # As many props as needed
}
```

##### Nested inside the `props` group
Aside from [`name`](#name) and [`order`](#order) all the keys and values in the above structure are specific to the `props` group and therefore explained below:

Key | Default | Description
--- | ------- | -----------
<a name="custom_prop_key_">`custom_prop_key_*`</a> | | A custom key wrapper for a `props` item.
<a name="enabled">`custom_prop_key_*.enabled`</a> | `False` | Enable a `props` element in the UI. If `False`, users cannot interact with the element in the UI.
<a name="help">`custom_prop_key_*.help`</a> | | A help message that is displayed in the UI, as a result of a mouseover or touch event on a `custom_prop_key_*` element.
<a name="label">`custom_prop_key_*.label`</a> | | A label that is displayed in the UI next to the `custom_prop_key_*` element.
<a name="maxValue">`custom_prop_key_*.maxValue`</a> | | Used along a `'num'` prop, it takes the maximum allowed value of the numeric input. Should not be equal to `minValue`.
<a name="minValue">`custom_prop_key_*.minValue`</a> | | Used along a `'num'` prop, it takes the minimum allowed value of the numeric input. Should not be equal to `maxValue`.
<a name="reinit">`custom_prop_key_*.reinit`</a> | `False` | If `True`, any change of the prop will trigger the server to send all session data to the `configure_session` method of the API. This is useful for settings that should change which panes or options are available to the end user in the app.
<a name="prop-type">`custom_prop_key_*.type`</a> | Required | As a direct child of `custom_prop_key_*`, the `type` key sets the UI element type, implicitly constraining the set of key-value pairs that can be used along this type. The `type` key takes one of the following values: `'head'`, `'text'`, `'num'`, `'toggle'`, or `'selector'`.
<a name="prop-unit">`custom_prop_key_*.unit`</a> | | A unit that is displayed next to the numeric value in a `props` element.
<a name="value">`custom_prop_key_*.value`</a> | Required | The actual value for a `props` element. Depending on the prop [`type`](#prop-type), it can be a boolean (`toggle`), number (`'num'`), string (`'text'`), or an array of objects (`'selector'`).
<a name="custom_option_">`custom_prop_key_*.value.custom_option_*`</a> | | Used along a `'selector'` prop, it takes a string value to be displayed as an option on the UI element.
<a name="variant">`custom_prop_key_*.variant`</a> | | Used to modify the UI for a given prop `type`. For example, it can convert a numeric input to a slider input or a selector to a drop-down menu. The `value`s should remain the same structure, but the presentation to the end user changes. Add `-condensed` at the end of any variant or `condensed` for any standard variant to get a smaller UI footprint. For example: a `num` prop type could have the following `variant`s: `condensed`, `slider` and `slider-condensed`.

##### Prop `type`s and their `variant`s:

##### `'head'`
Allows users to place a header for an individual section, containing a title (via [`name`](#name)) and a [`help`](#help) message. The [`value`](#value) key is not used with this type.

##### `'text'`
Allows users to enter text in a UI field. Here, `value` takes a string.

##### `'num'`
Allows users to enter a numeric value in a UI field. The `value` receives a numeric input that is validated against [`constraint`](#constraint).
###### Variants:
>`'slider'`: Places a range of values along a bar, from which users may select a single value.<br>

##### `'toggle'`
Allows to enable or disable the status of a single setting. Here, `value` receives a boolean value.

##### `'selector'`
Allows end users to select options from a set. This `type` requires an array of dictionary objects for its [`value`](#value) key and a `variant` must be specified.
###### Variants:
<!-- It might be convenient for design/development purposes to separate multi-select and single-select items. For example, by moving checkbox out of these variants and make it a variant of another abstract group. -->
>`'checkbox'`: Allows the user to select one or more items from a set of checkboxes.<br>
`'dropdown'`: Allows a compact way to display multiple options. The options appear upon interaction with an element (such as an icon or button) or when the user performs a specific action.<br>
`'radio'`: Allows the user to select one option from a set of mutually exclusive options.<br><br>
Since multiple selection is possible in the `checkbox` variant, one or more options in [`value`](#value) can be set to `True`, while in the `dropdown` and `radio` variants, only one option is allowed to be `True`.

##### UI / UX tips
- When it comes to select multiple options from a set, you can save space by using `checkbox`es instead of on/off `toggle`s. However, if there is only one option, an on/off `toggle` is recommended instead.
- When a user is allowed to select only one option from a set, unless you need to expose all the available options with `radio`, you may consider using a `dropdown` instead, as it uses less space.

#### The `layout` key
> (*Under construction*)
The `layout` key allows for use cases where you want to arrange components that are related or simply group them under a well-structured layout. The supported components for use with a layout structure are [props](#the-props-key) and [KPIs](#kpis). In addition to properly aligning a group of props or KPIs, an `style` prop is provided to act as a escape hatch for specifying CSS rules. Through these CSS rules, it is possible to modify the appereance of your prop components or KPIs and allows a way to make them more distinctive or visually appealing.

The structure for both prop and KPI `layout`s is the same. Let's dive into it:

```py
'layout': {
    'type': 'grid',
    'num_columns': 'auto',
    'num_rows': 'auto',
    'data': {
        'col1_row1': {
            'type': 'item',
            'column': 1,
            'row': 1,
            'itemId': 'custom_prop_or_kpi_key_1'
        },
        'col1_row2': {
            'type': 'item',
            'column': 1,
            'row': 1,
            'itemId': 'custom_prop_or_kpi_key_2',
        },
        # As many rows and columns as needed
    },
}
```

##### Nested inside the `layout` group
>(*Under construction*)

Key | Default | Description
--- | ------- | -----------
<a name="layout-column">`column`</a> | | An integer for the grid column from left to right.
<a name="layout-data">`data`</a> | `{}` | (*Under construction*)
<a name="layout-column">`itemId`</a> | | (*Under construction*)
<a name="layout-columns">`num_columns`</a> | `'auto'` | An integer for the number of columns or the keyword `'auto'`.
<a name="layout-rows">`num_rows`</a> | `'auto'` | An integer for the number of rows or the keyword `'auto'`.
<a name="layout-row">`row`</a> | | An integer for the grid row from top to bottom.
<a name="layout-column">`style`</a> | | (*Under construction*)
<a name="layout-type">`type`</a> | Required | The type of layout. It can be `'grid'` or `'item'`.

#### timeObjects
`timeObjects` can be used to replace numerical values displayed on the map or used as prop [`values`](#value) in [`geos`](#geos), [`arcs`](#arcs), or [`nodes`](#nodes). These objects contain a list of values that correspond to a specfic timestep. The user can step through these in order or select a specific timestep from a list. In order to use `timeObjects` a [`timeLength`](#timeLength) must be specified equal to the length of all `value` lists given. Optionally [`timeUnits`](#timeUnits) can be given to display the real world representation of each timestep.

Below is an example of a `timeObject` with a `timeLength` of 5
```py
{
    'timeObject': True,
    'value': [1, 1, 2, 3, 5],
}
```
- The `timeObject` key being set to `True` is required for all `timeObjects`.
- All `value` lists must have lengths equal to the set [`timeLength`](#timeLength). If the length is updated it must happen to all `value` lists and the `timeLength` at the same time.
### Top-level keys
Now, it is time to take take a look at each of the key groups in detail, including the meaning of all their nested sub-keys and their innermost values.

#### `settings`
This key group allows designers to specify settings they want the site to use (overriding setting defaults. For example, designers can specify the URL where icons are fetched from. If this is not supplied, it defaults to the one specified in the static build (`./src/app/constants`)

Below is the `settings` group with its sub-keys matched by typical values:
```py
"settings": {
    "allow_modification": False,
    "send_to_api": False,
    "send_to_client": True,
    "data": {
        "syncToggles": {
            "Layers": {"custom_path_name_1": ["map", "data", "enabledTypes"]},
            "Open pane": {"pane_path": ['appBar', 'paneState']},
        },
        "defaultDesync": {
            "Open pane": {"pane_path": ['appBar', 'paneState']},
        },
        "IconUrl": "https://react-icons.mitcave.com/0.0.1",
        "debug": True,
    },
        },
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`data`](#data)
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

### `categories`
Both designers and users often need to work with different levels of data aggregation and allow for filtering of that data in the UI. The `categories` group allows for easy aggregation and filtering for end users.

Below is an example of the `categories` group:
```py
'categories': {
    'allow_modification': False,
    'send_to_api': False,
    'send_to_client': True,
    'data': {
        'custom_category_1': {  # Inside a category group
            'data': {
                'custom_data_chunk_1': {
                    'custom_data_key_1': 'data_value_1',
                    'custom_data_key_2': 'data_value_2',
                    'custom_data_key_3': 'data_value_3',
                },
                'custom_data_chunk_2': {
                    'custom_data_key_1': 'data_value_4',
                    'custom_data_key_4': 'data_value_5',
                },
                # As many data chunks as needed
            },
            'name': 'A name to be displayed in the UI',
            'nestedStructure': {
                'custom_data_key_1': {
                    'name': 'A name to be displayed in the UI'
                    'ordering': [
                        'data_value_3',
                        'data_value_1',
                        'data_value_2',
                    ],
                    'order': 0,
                },
                'custom_data_key_2': {...},
                'custom_data_key_3': {...},
                'custom_data_key_4': {...},
                # As many data keys as defined within the data chunks
            },
            'layoutDirection': 'horizontal',
            'order': 2,
        },
        'custom_category_2': {...},
        # As many categories as needed
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`data`](#data)
- [`name`](#name)
- [`order`](#order)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="custom_category_">`custom_category_*`</a> | Required | A custom key for categorical data. Each `custom_category_*` key encloses a well-defined structure. This represents a higher level structure for filtering and aggregation purposes. A simple example is geography which can be represented by a nested structure (`township` &rarr; `state` &rarr; `country` &rarr; `continent`).
`custom_category_*.data` | | Dictionary object that contains `custom_data_chunk_*` items.
<a name="custom_data_chunk_">`custom_category_*.data.custom_data_chunk_*`</a> | | A wrapper for key-value pairs that are grouped by any categorical context set by the designer. This represents the smallest level of aggregation. For example, an app that groups data geographically to the township level would need one data chunk per township they want to represent.
<a name="custom_data_key_">`custom_category_*.data`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*`<br><br>or<br><br>`custom_category_*.nestedStructure`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*`</a> | | A data property representing a specific group level of data. Following our geographic example, there should be four custom data keys (`township`, `state`, `country` and `continent`) per custom data chunk.
`custom_category_*.data`&swarhk;<br>`.custom_data_key_*.data_value_*` | | A match value for `custom_data_key_*`. Can either be string, numeric or boolean. Given our geographic example, a custom data key named `township` could have a data value of `'cambridge'` or any other township.
`custom_category_*.layoutDirection` | `'vertical'` | The direction in which `custom_data_key_*`s appear in the "**Group By**" drop-down menu of a chart. It can be `'horizontal'` or `'vertical'`. If omitted, the items will be displayed vertically in the UI.
`custom_category_*.nestedStructure` | Required | A container dictionary for specifying the rendering properties of the items that are displayed in the "**Group By**" drop-down menu of a chart in a dashboard view.
`custom_category_*.nestedStructure`&swarhk;<br>`.custom_data_key_*.ordering` | | A special key of a [`custom_data_chunk_*`](#custom_data_chunk_) that sets the position in which the `data_value_*`s contained in the data chunk are rendered in the "**Group By**" drop-down menu of a chart. Its value is a list of strings in which the order of `data_value_*`s is determined by their indices in the list (ascending order). All values that are not included in the list will be sorted alphabetically and placed after the values that are actually present.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'categories': {
    'allow_modification': False,
    'send_to_api': False,
    'send_to_client': True,
    'data': {
        'Location': {
            'data': {
                'loc_US_MI': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Michigan',
                },
                'loc_US_MA': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Massachusetts',
                },
                'loc_US_FL': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Florida',
                },
                'loc_US_IN': {
                    'Region': 'North America',
                    'Country': 'USA',
                    'State': 'Indiana',
                },
                'loc_CA_ON': {
                    'Region': 'North America',
                    'Country': 'Canada',
                    'State': 'Ontario',
                },
            },
            'name': 'Locations',
            'nestedStructure': {
                'Region': {
                    'name': 'Regions',
                    'order': 1,
                },
                'Country': {
                    'name': 'Countries',
                    'ordering': ['USA', 'Canada'],
                    'order': 2,
                },
                'State': {
                    'name': 'States',
                    'order': 3,
                },
            },
            'layoutDirection': 'horizontal',
            'order': 0,
        },
        'Product': {
            'data': {
                'prd_abc123': {
                    'Type': 'Fruit',
                    'Size': 'Big',
                    'Product': 'Apple'
                },
                'prd_def456': {
                    'Type': 'Fruit',
                    'Size': 'Small',
                    'Product': 'Grape',
                },
            },
            'name': 'Products',
            'nestedStructure': {
                'Type': {
                    'name': 'Types',
                    'order': 1,
                },
                'Size': {
                    'name': 'Sizing',
                    'ordering': ['Small', 'Big'],
                    'order': 2,
                },
                'Product': {
                    'name': 'Products',
                    'order': 3,
                },
            },
            'layoutDirection': 'horizontal',
            'order': 1,
        },
    },
}
```
</details>

### `appBar`
The `appBar` key allows api designers to create a custom bar located on the left of the CAVE app. This bar allows for navigation between the different views of the app (e.g. Map, Dashboards), as well as interaction with panes. The appBar is split into 2 sections, `upper` and `lower`. Using both sections is not required, but it is generally recommeneded that `lower` be used for navigation and `upper` for interactive panes and buttons.

Panes are primarily used to place UI controls (toggles, text and number fields, sliders, etc.), as well as buttons to allow interaction with actionable data. Therefore, custom panes can be designed to enable users to tune up the parameters of a simulation, navigate through different case study scenarios, reset the state of a simulation, synchronize data or settings with other users, and so on. The CAVE app also includes 2 built in pane variants `filter`, which provides tools to filter data from different categories and at different levels of granularity, and `appSettings`, which gives users the ability to control the appearance and overall behavior of the CAVE app.

The structure of a `appBar` group looks as follows:
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
        'custom_pane_1': {
            'name': 'Settings Big Pane',
            'width': '100%',
            'bar': 'upper',
            'props': {
                'custom_prop_key_1': {
                    'name': 'Solver Section',
                    'type': 'head',
                    'help': 'Some help for the solver section',
                    'order': 1,
                    'column': 1,
                },
                'custom_prop_key_2': {...},
                    # As many custom props as needed for this pane
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
        'open': 'custom_pane_key',
    },
    'filtered':{
        'category_1': 'custom_data_chunk_1',
    },
}
```
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
            'constraint': 'int',
            'unit': 'units',
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
            'reinit': True,
            'help': 'A help text for the dropdown selector',
        },
        # As many props as needed
    },
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
            'constraint': 'int',
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

##### Common keys
- [`allow_modification`](#allow_modification)
- [`color`](#color)
- [`column`](#column)
- [`constraint`](#constraint)
- [`data`](#data)
- [`enabled`](#enabled)
- [`help`](#help)
- [`icon`](#icon)
- [`label`](#label)
- [`maxValue`](#maxValue)
- [`minValue`](#minValue)
- [`name`](#name)
- [`order`](#order)
- [`prop > type`](#prop-type)
- [`propDefaults`](#propDefaults)
- [`props`](#props)
- [`reinit`](#reinit)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)
- [`prop > unit`](#prop-unit)
- [`value`](#value)
- [`variant`](#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`custom_obj_key_*` | Required | A custom key wrapper for the custom pane.
`custom_obj_key_*.type` | Required | The type of object shown - takes one of these values: `map`, `stat`, `kpi`, `pane`, or `button`. The type given changes what other props can be given to the object.
`custom_obj_key_*.bar` | Required | The section of the appbar to display the object in. Accepts either `upper` or `lower`. The use of both bar sections is not required, and any object can be shown in either bar.
`custom_button_key_*.apiCommand`<br> | | A string to pass to the api when the button is pressed.
`custom_button_key_*.dashboardLayout` | `[]` | A list of chart items (max of 4 items currently supported) that belong to the current dashboard. Each chart item contains the following keys: `chart`, `grouping`, `statistic`, `category`, `level`, `type`, and `lockedLayout`.
`custom_button_key_*.dashboardLayout.*.*.category` | | The category selected from the "**Group By**" drop-down menu of a chart in a dashboard view. This key is different from the common key [`category`](#category).
`custom_button_key_*.dashboardLayout.*.*.chart` | | The chart type selected from the top-left drop-down menu of a chart in a dashboard view. The `chart` key sets the type of chart to one of these values: [`'Bar'`], [`'Line'`], [`'Box Plot'`].
`custom_button_key_*.dashboardLayout.*.*.grouping` | | A statistical or mathematical function selected by the user from a predefined set, to be applied over the data and rendered in a chart. It takes one of the following values: `'Sum'`, `'Average'`, `'Minimum'` or `'Maximum'`.
`custom_button_key_*.dashboardLayout.*.*.kpi` | | The kpi selected from the "**KPIs**" drop-down menu of a chart in a dashboard view if the chart `type='kpis'`
`custom_button_key_*.dashboardLayout.*.*.level` | | The second-level aggregation selected from the "**Group By**" drop-down menu of a chart in a dashboard view.
`custom_button_key_*.dashboardLayout.*.*.lockedLayout` | `false` | A boolean to indicate if the layout on this chart can be changed by users.
`custom_button_key_*.dashboardLayout.*.*.statistic` | | The statistic selected from the "**Statistic**" drop-down menu of a chart in a dashboard view if the chart `type='stats'`
`custom_button_key_*.dashboardLayout.*.*.type` | `'stats'` | This has two options: `'stats'` or `'kpis'`
`custom_button_key_*.lockedLayout` | `false` | If `true`, prevents users from modifying the layout of a dashboard view by adding or removing charts.
`custom_context_pane_key_*.data.custom_context_data_*` | | This represents the data structure created by the client to store each context in a list of contexts. Initial values can be provided by the API designer if needed.
`custom_context_pane_key_*.data.custom_context_data_*`&swarhk;<br>`.applyCategories` | | Used **only** with a [`context`](#context-pane) pane, it takes a dictionary of [`category_*`](#category_)s, each of which is paired with a partial list of its [`custom_data_chunk_*`](#custom_data_chunk_) keys. This data is normally generated by user interactions as they build out contexts and returned to the API on a `configure` or `solve` request. Initial values can be provided by the API designer if needed.
`custom_context_pane_key_*.data.custom_context_data_*`&swarhk;<br>`.applyCategories.category_*.custom_data_chunk_*` | | See [`custom_data_chunk_*`](#custom_data_chunk_).
`custom_context_pane_key_*.data.custom_context_data_*`&swarhk;<br>`.prop` | | Used in the `data` portion of a [`context`](#context-pane) pane to note which prop the current context is altering. Takes a `custom_prop_key_*`.
`custom_pane_key_*.props.custom_prop_key_*` | | See [`custom_prop_key_*`](#custom_prop_key_).
`custom_pane_key_*.props.custom_prop_key_*`&swarhk;<br>`.value.custom_option_*` | | See [`custom_option_*`](#custom_option_).
`custom_context_pane_key_*.props.custom_prop_key_*`&swarhk;<br>`.selectableCategories` | Required | Used in a [`context`](#context-pane) pane, it takes a list of [`category_*`](#category_) keys (**only**). These are the used to determine which categories this context can be applied to.
`custom_pane_key_*.teamSync` | `False` | If `True`, creates a sync button on the top of the pane. When that sync button is clicked, everything in that pane is synced across all sessions for that team (or user if individual session) such that all other sessions for that team have the exact same pane as it exists in the current session.
<a name="pane-variant">`custom_pane_key_*.variant`</a> | `'options'` | As a direct child of `custom_pane_key_*`, the `variant` key configures a pane to be an `'options'` or `'context'` pane. Each variant comes along with additional keys that add specific functionality to the pane.
`paneState.open` | null | Takes a `custom_pane_key` to cause that pane to be open upon loading the app.
`filtered` | {} | Takes key value pairs where the keys are category keys, and the values are lists of lowest level items in that category to be included (not filtered out). If a category is not included in this dictionary then all items in that category are displayed.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"appBar": {
    "data": {
        "button_1": {
            "name": "Solve Button",
            "icon": "BsLightningFill",
            "color": {
                "dark": "rgb(64, 179, 54)",
                "light": "rgb(24, 73, 20)",
            },
            "apiCommand": "solve_session",
            "type": "button",
            "bar": "upper",
        },
        "settingsBig": {
            "name": "Settings Big Pane",
            "width": "100%",
            "props": {
                "solver_section": {
                    "name": "Solver Section",
                    "type": "head",
                    "help": "Some help for the solver section",
                    "order": 1,
                    "column": 1,
                },
                "Solver": {
                    "name": "Solver",
                    "type": "selector",
                    "variant": "dropdown",
                    "value": [
                        {"name": "Gurobi", "value": True},
                        {"name": "Cplex", "value": False},
                        {"name": "CoinOR", "value": False},
                    ],
                    "enabled": True,
                    "help": "Select a solver type to use",
                    "reinit": True,
                    "order": 2,
                    "column": 1,
                },
                "optimality_section": {
                    "name": "Optimality Section",
                    "type": "head",
                    "help": "Some help for the optimality section",
                    "order": 1,
                    "column": 2,
                },
                "Pct_Optimal": {
                    "name": "Percent Optimal",
                    "type": "num",
                    "value": 97,
                    "enabled": True,
                    "variant": "slider",
                    "help": "What percent of optimal would you like to sove to?",
                    "maxValue": 100,
                    "minValue": 0,
                    "order": 2,
                    "column": 2,
                },
                "distance_section": {
                    "name": "Demand Served At Distances",
                    "type": "head",
                    "help": "How much demand do you expect to serve at the following distances?",
                    "order": 1,
                    "column": 3,
                },
                "50_miles": {
                    "name": "50 Miles",
                    "type": "num",
                    "value": 45,
                    "enabled": True,
                    "variant": "slider-condensed",
                    "help": "Expected demand filled at 50 miles",
                    "maxValue": 100,
                    "minValue": 0,
                    "order": 2,
                    "column": 3,
                },
                "100_miles": {
                    "name": "100 Miles",
                    "type": "num",
                    "value": 35,
                    "enabled": True,
                    "variant": "slider-condensed",
                    "help": "Expected demand filled at 100 miles",
                    "maxValue": 100,
                    "minValue": 0,
                    "order": 3,
                    "column": 3,
                },
                "150_miles": {
                    "name": "150 Miles",
                    "type": "num",
                    "value": 25,
                    "enabled": True,
                    "variant": "slider-condensed",
                    "help": "Expected demand filled at 150 miles",
                    "maxValue": 100,
                    "minValue": 0,
                    "order": 4,
                    "column": 3,
                },
            },
            "icon": "BsWrench",
            "color": {
                "dark": "rgb(46, 244, 208)",
                "light": "rgb(17, 79, 68)",
            },
            "type": "pane",
            "variant": "options",
            "bar": "upper",
            "order": 2,
        },
        "options": {
            "name": "Options Pane",
            "props": {
                "Combine_Materials": {
                    "type": "selector",
                    "value": [
                        {"name": "True", "value": True},
                        {"name": "False", "value": False},
                    ],
                    "enabled": True,
                    "help": "Do you want to combine materials and treat them equally when solving?",
                    "variant": "radio",
                    "order": 2,
                },
                "Meet_Monthly_Demand": {
                    "type": "selector",
                    "value": [
                        {"name": "True", "value": True},
                        {"name": "False", "value": False},
                    ],
                    "enabled": True,
                    "help": "Do you want to force the solver to meet the monthly demand thresholds?",
                    "variant": "radio",
                    "order": 3,
                },
                "Combined Options": {
                    "name": "Combined Options",
                    "type": "selector",
                    "variant": "checkbox",
                    "value": [
                        {"name": "Meet Monthly Demand", "value": True},
                        {"name": "Combine Materials", "value": False},
                    ],
                    "enabled": True,
                    "help": "Help for both options",
                    "reinit": True,
                    "order": 2,
                    "column": 1,
                },
            },
            "icon": "MdSettings",
            "type": "pane",
            "variant": "options",
            "bar": "upper",
            "order": 1,
        },
        "map_1": {
            "type": "map",
            "icon": "FaMapMarkedAlt",
            "bar": "upper",
            "color": {
                "dark": "rgb(178, 179, 55)",
                "light": "rgb(79, 79, 24)",
            },
        },
        "filter": {
            "icon": "FaFilter",
            "type": "pane",
            "variant": "filter",
            "order": 6,
            "bar": "upper",
        },
        "appSettings": {
            "icon": "MdOutlineSettings",
            "type": "pane",
            "variant": "appSettings",
            "bar": "upper",
        },
        "context": {
            "props": {
                "Demand_Multiplier": {
                    "type": "num",
                    "value": 100,
                    "enabled": True,
                    "help": "Percentage multiplier times the base demand (100%=Given Demand)",
                    "label": "%",
                    "variant": "slider",
                    "maxValue": 500,
                    "minValue": 0,
                    "selectableCategories": ["Location", "Product"],
                },
                "Supply_Multiplier": {
                    "type": "num",
                    "value": 100,
                    "enabled": True,
                    "help": "Percentage multiplier times the base supply (100%=Given Supply)",
                    "label": "%",
                    "minValue": 0,
                    "constraint": "int",
                    "selectableCategories": ["Location", "Product"],
                },
            },
            "data": {
                "context_1": {
                    "prop": "Demand_Multiplier",
                    "value": 110,
                    "applyCategories": {"Location": ["loc_US_MI"]},
                }
            },
            "icon": "BsInboxes",
            "type": "pane",
            "variant": "context",
            "order": 4,
            "bar": "upper",
        },
        "settings": {
            "name": "Settings Pane",
            "props": {
                "Solver": {
                    "name": "Solver",
                    "type": "selector",
                    "variant": "dropdown",
                    "value": [
                        {"name": "Gurobi", "value": True},
                        {"name": "Cplex", "value": False},
                        {"name": "CoinOR", "value": False},
                    ],
                    "enabled": True,
                    "help": "Select a solver type to use",
                    "reinit": True,
                    "order": 1,
                },
                "optimality_section": {
                    "name": "Optimality Section",
                    "type": "head",
                    "help": "Some help for the optimality section",
                    "order": 2,
                },
                "Pct_Optimal": {
                    "name": "Percent Optimal",
                    "type": "num",
                    "value": 97,
                    "enabled": True,
                    "help": "What percent of optimal would you like to sove to?",
                    "maxValue": 100,
                    "minValue": 0,
                    "order": 3,
                },
            },
            "icon": "BsWrench",
            "color": {
                "dark": "rgb(64, 179, 54)",
                "light": "rgb(24, 73, 20)",
            },
            "type": "pane",
            "variant": "options",
            "teamSync": True,
            "bar": "lower",
            "order": 1,
        },
        "dash_1": {
            "icon": "BsCircleFill",
            "name": "Dashboard 1",
            "type": "stats",
            "color": {
                "dark": "rgb(178, 179, 55)",
                "light": "rgb(79, 79, 24)",
            },
            "order": 2,
            "bar": "lower",
            "dashboardLayout": [
                {
                    "chart": "Bar",
                    "grouping": "Average",
                    "statistic": "demand_met",
                },
                {
                    "chart": "Line",
                    "grouping": "Sum",
                    "statistic": "demand_pct",
                },
                {
                    "chart": "Bar",
                    "level": "Size",
                    "category": "Product",
                    "grouping": "Sum",
                    "statistic": "demand_met",
                },
                {
                    "chart": "Bar",
                    "grouping": "Minimum",
                    "type": "kpis",
                    "sessions": [],
                    "kpi": "Really Big Number",
                },
            ],
            "lockedLayout": False,
        },
        "kpi_1": {
            "type": "kpi",
            "icon": "MdSpeed",
            "bar": "lower",
            "color": {
                "dark": "rgb(224, 224, 224)",
                "light": "rgb(32, 32, 32)",
            },
            "order": 3,
        },
    }
}
```
</details>

### `arcs`
The `arcs` group contains data that is typically used to visualize information flows between two locations in the "**Map**" view. Depending on the nature of the flows and the purpose of the visualization, the flows between two locations can be represented by a single arc (source and destination) or a sequence of arc segments representing a [`path`](#path).

The structure of an `arcs` group looks as follows:
```py
'arcs': {
    'name': 'A name that will be displayed in the map legend.',
    'types': {
        'custom_arc_type_1': {
            'name': 'A name to be displayed in the UI',
            'colorByOptions': {
              'custom_prop_key_10': {
                'min': 0,
                'max': 25,
                'startGradientColor': {
                    'dark': 'rgb(233, 0, 0)',
                    'light': 'rgb(52, 52, 236)',
                },
                'endGradientColor': {
                    'dark': 'rgb(96, 2, 2)',
                    'light': 'rgb(23, 23, 126)',
                },
              },
              'custom_prop_key_11': {
                'min': 0,
                'max': 35,
                'startGradientColor': {
                    'dark': 'rgb(233, 0, 0)',
                    'light': 'rgb(52, 52, 236)',
                },
                'endGradientColor': {
                    'dark': 'rgb(96, 2, 2)',
                    'light': 'rgb(23, 23, 126)',
                },
              },
              'custom_prop_key_12': {
                'custom_color_key_1':'rgb(233,0,0)',
                'custom_color_key_2':'rgb(0,233,0)'
              }
            },
            'colorBy': 'custom_prop_key_10',
            'lineBy': 'dotted',
            'sizeByOptions': {
              'custom_prop_key_10': {'min': 0, 'max': 25},
              'custom_prop_key_11': {'min': 0, 'max': 35}
            },
            'sizeBy': 'custom_prop_key_10',
            'startSize': '15px',
            'endSize': '30px',
            'order': 0,
        },
        'custom_arc_type_2': {...},
        # As many arc types as needed
    },
    'propDefaults': {
        'custom_prop_key_10': {
            'name': 'A name to be displayed in the UI',
            'type': 'num',
            'enabled': False,
            'help': 'A help text for the numeric input',
            'order': 1,
            'constraint': 'int',
            'unit': 'units',
            'column': 2,
        },
        # As many propDefaults as needed
    },
    'data': {
        'custom_arc_data_1': {
            'startLatitude': 43.78,
            'startLongitude': -79.63,
            'endLatitude': 39.82,
            'endLongitude': -86.18,
            'startClick': 800,
            'endClick': 1600,
            'type': 'custom_arc_type_1',
            'category': {
                'custom_data_chunk_1': [
                    'custom_data_key_2',
                    'custom_data_key_3'
                ],
                'custom_data_chunk_2': [
                    'custom_data_key_1',
                    'custom_data_key_4',
                ],
                # As many data chunks as needed
            },
            'props': {
                'custom_prop_key_10': {
                    'value': 50,
                    'variant': 'slider',
                },
                'custom_prop_key_11': {
                    'name': 'A name to be displayed in the UI',
                    'type': 'num',
                    'value': 40,
                    'enabled': False,
                    'help': 'A help text for the numeric input',
                    'order': 2,
                    'unit': 'units',
                },
            },
        },
        'custom_arc_data_2': {
            'path': [
                [-122.3535851, 37.9360513, 1],
                [-122.3179784, 37.9249513, 1.2],
                [-122.300284, 37.902646, 1.4],
                [-122.2843653, 37.8735039, 1.65],
                [-122.269058, 37.8694562, 2],
            ],
            'startClick': 200,
            'endClick': 1000,
            'type': 'custom_arc_type_2',
            'category': {
                'custom_data_chunk_1': [
                    'custom_data_key_1',
                    'custom_data_key_3'
                ],
                'custom_data_chunk_2': [
                    'custom_data_key_2',
                    'custom_data_key_4',
                ],
                # As many data chunks as needed
            },
            'props': {
                'custom_prop_key_10': {
                    'value': 20,
                    'variant': 'slider',
                },
                'custom_prop_key_12': {
                    'name': 'A name to be displayed in the UI',
                    'type': 'num',
                    'value': 30,
                    'enabled': False,
                    'help': 'A help text for the numeric input',
                    'order': 1,
                    'unit': 'units',
                },
            },
        },
        'custom_arc_data_3': {...},
        # As many arc data chunks as needed
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`category`](#category)
- [`colorBy`](#colorBy)
- [`colorByOptions`](#colorByOptions)
- [`column`](#column)
- [`constraint`](#constraint)
- [`data`](#data)
- [`enabled`](#enabled)
- [`endGradientColor`](#endGradientColor)
- [`endSize`](#endSize)
- [`help`](#help)
- [`name`](#name)
- [`order`](#order)
- [`prop > type`](#prop-type)
- [`propDefaults`](#propDefaults)
- [`props`](#props)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)
- [`sizeBy`](#sizeBy)
- [`sizeByOptions`](#sizeByOptions)
- [`startSize`](#startSize)
- [`startGradientColor`](#startGradientColor)
- [`prop > unit`](#prop-unit)
- [`value`](#value)
- [`variant`](#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`data.custom_arc_data_*` | Required | A custom key wrapper for the parameters required to visualize an arc flow and the data associated with it in the "**Map**" view.
`data.custom_arc_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](#custom_data_chunk_).
`data.custom_arc_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](#custom_data_key_).
`data.custom_arc_data_*.endAltitude` | | The altitude (in meters) for the target location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.endClick`<br>(*Under construction*) | | Related to the animation frame rate of an arc layer. It takes an integer value.
`data.custom_arc_data_*.endLatitude` | Required | The latitude for the target location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.endLongitude` | Required | The longitude for the target location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.height` | `1` | The height multiplier relative to the distance between two points for the apex of a `3d` (lineBy) arc. For example, a value of `0` would turn a `3d` (lineBy) arc into the equivalent to a `solid` (lineBy) arc.
`data.custom_arc_data_*.name` | | A name for the arc flow that will be displayed as a title in the map modal.
<a name="path">`data.custom_arc_data_*.path`</a> | | A list of coordinate points (`[<longitude>, <latitude>]`), such that every two consecutive coordinates represent an arc segment of a path to be rendered in the "**Map**" view. Additionally, a third position can be added to each coordinate (`[<longitude>, <latitude>, <altitude>]`), to visually represent altitude on the map.<br><br>Please note that `path` is not supported for `3d` arcs. If you need to create a "`3d` path", you can do so by joining multiple arcs which start and end coordinates match the segments of the intended path.<br><br>The use of `path` overrides any behavior resulting from the use of the following `data.custom_arc_data_*.` keys: `startLongitude`, `startLatitude`, `startAltitude`, `endLongitude`, `endLatitude`, and `endAltitude`.
`data.custom_arc_data_*.props`&swarhk;<br>`.custom_prop_key_*` | | See [`custom_prop_key_*`](#custom_prop_key_).
`data.custom_arc_data_*.startAltitude` | | The altitude (in meters) for the source location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.startClick`<br>(*Under construction*) | | Related to the animation frame rate of an arc layer. It takes an integer value.
`data.custom_arc_data_*.startLatitude` | Required | The latitude for the source location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.startLongitude` | Required | The longitude for the source location in the "**Map**" view. It takes a float value.
`data.custom_arc_data_*.type` | Required | The `type` key sets the arc type of `custom_arc_data_*` to a `custom_arc_type_*` key, to match specific visualization preferences for an arc flow.
`types` | Required | The `types` key allows you to define different arc types in terms of styling and data viz settings.
`types.custom_arc_type_*` | | A wrapper for key-value pairs that match a specific set of data viz preferences for an arc flow.
`types.custom_arc_type_*.lineBy` | `'solid'` | The pattern of dashes and gaps used to form the shape of an arc's stroke. It takes one of the following values: `'dashed'`, `'dotted'`, `'solid'`, or `'3d'`. This can be set in individual arcs to overwrite the default for the type.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'arcs': {
    'data': {
        'arc_1': {
            'type': 'Supply',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'order': 1,
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'order': 2,
                    'value': 500,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'order': 0,
                    'value': 'Campinas - Sao Paulo Airport',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 15,
                    'enabled': False,
                },
            },
            'category': {'Product': ['LowVal'], 'Location': ['loc_US_MI']},
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': -23.565,
            'endLongitude': -46.632,
            'startLatitude': -22.934,
            'startLongitude': -47.093,
        },
        'arc_2': {
            'type': 'Supply',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'order': 1,
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'order': 2,
                    'value': 1498.3,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'order': 0,
                    'value': 'Phoenix - Atlanta',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 292.2,
                    'enabled': False,
                },
            },
            'category': {'Product': ['HighVal'], 'Location': ['loc_US_MI']},
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': 34.037,
            'endLongitude': -84.235,
            'startLatitude': 33.448,
            'startLongitude': -112.074,
        },
        'arc_3': {
            'type': 'Interfacility',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'order': 1,
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'order': 2,
                    'value': 843.2,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'order': 0,
                    'value': 'Atlanta - Florence, South Carolina',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 27.6,
                    'enabled': False,
                },
            },
            'category': {
                'Product': ['LowVal', 'HighVal'],
                'Location': ['loc_US_MI'],
            },
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': 34.198,
            'endLongitude': -79.767,
            'startLatitude': 34.037,
            'startLongitude': -84.235,
        },
        'arc_4': {
            'type': 'Interfacility',
            'props': {
                'Transportation Mode': {
                    'help': 'Transportation mode used.',
                    'type': 'text',
                    'order': 1,
                    'value': 'Road',
                    'enabled': False,
                },
                'Throughput (pallets)': {
                    'help': 'Number of pallets shipped.',
                    'type': 'num',
                    'order': 2,
                    'value': 485.2,
                    'enabled': False,
                },
                'Origin and destination': {
                    'help': 'City of origin and city of destination of the flow.',
                    'type': 'text',
                    'order': 0,
                    'value': 'Atlanta - Jacksonville',
                    'enabled': False,
                },
                'Transportation Cost (k$)': {
                    'help': 'Cost of transportation.',
                    'type': 'num',
                    'value': 16.9,
                    'enabled': False,
                },
            },
            'category': {
                'Product': ['LowVal', 'HighVal'],
                'Location': ['loc_US_MI'],
            },
            'endClick': 2000,
            'startClick': 1600,
            'endLatitude': 30.332,
            'endLongitude': -81.656,
            'startLatitude': 34.037,
            'startLongitude': -84.235,
        },
    },
    'name': 'Transportation flows',
    'types': {
        'Supply': {
            'lineBy': 'solid',
            'sizeBy': 'Transportation Cost (k$)',
            'colorBy': 'Throughput (pallets)',
            'endSize': '10px',
            'startSize': '7px',
            'sizeByOptions': {
              'Throughput (pallets)': {'min': 0, 'max': 5000},
              'Transportation Cost (k$)': {'min': 5, 'max': 2000}
            },
            'colorByOptions': {
              'Throughput (pallets)': {
                'min': 0,
                'max': 5000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              },
              'Transportation Cost (k$)': {
                'min': 5,
                'max': 2000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              }
            },
        },
        'Interfacility': {
            'lineBy': 'solid',
            'sizeBy': 'Transportation Cost (k$)',
            'colorBy': 'Throughput (pallets)',
            'endSize': '7px',
            'startSize': '3px',
            'sizeByOptions': {
              'Throughput (pallets)': {'min': 0, 'max': 2000},
              'Transportation Cost (k$)': {'min': 5, 'max': 1000}
            },
            'colorByOptions': {
              'Throughput (pallets)': {
                'min': 0,
                'max': 2000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              },
              'Transportation Cost (k$)': {
                'min': 5,
                'max': 1000,
                'endGradientColor': 'rgb(255, 153, 51)',
                'startGradientColor': 'rgb(102, 255, 102)',
              }
            },
        },
    },
}
```
</details>

### `nodes`
The `nodes` group contains data that is typically used to visualize geographic locations in the "**Map**" view.

The structure of a `nodes` group looks as follows:
```py
'nodes': {
    'name': 'A name that will be displayed in the map legend.',
    'types': {
        'custom_node_type_1': {
            'name': 'A name to be displayed in the UI',
            'colorByOptions': {
              'custom_prop_key_10': {
                'min': 0,
                'max': 25,
                'startGradientColor': {
                    'dark': 'rgb(233, 0, 0)',
                    'light': 'rgb(52, 52, 236)',
                },
                'endGradientColor': {
                    'dark': 'rgb(96, 2, 2)',
                    'light': 'rgb(23, 23, 126)',
                },
              },
              'custom_prop_key_11': {
                    'min': 0,
                    'max': 35,
                    'startGradientColor': {
                        'dark': 'rgb(233, 0, 0)',
                        'light': 'rgb(52, 52, 236)',
                    },
                    'endGradientColor': {
                        'dark': 'rgb(96, 2, 2)',
                        'light': 'rgb(23, 23, 126)',
                    },
                },
              'custom_prop_key_12': {
                'custom_color_key_1':'rgb(233,0,0)',
                'custom_color_key_2':'rgb(0,233,0)'
              }
            ,
            'colorBy': 'custom_prop_key_10',
            'sizeByOptions': {
              'custom_prop_key_10': {'min': 0, 'max': 25},
              'custom_prop_key_11': {'min': 0, 'max': 35}
            ,
            'sizeBy': 'custom_prop_key_11',
            'startSize': '15px',
            'endSize': '30px',
            'icon': 'FaWarehouse',
            'order': 0,
        },
        'custom_node_type_2': {...},
        # As many node types as needed
    },
    'propDefaults': {
        'custom_prop_key_10': {
            'name': 'A name to be displayed in the UI',
            'type': 'num',
            'enabled': False,
            'help': 'A help text for the numeric input',
            'order': 1,
            'constraint': 'int',
            'unit': 'units',
        },
        # As many propDefaults as needed
    },
    'data': {
        'custom_node_data_1': {
            'latitude': 42.361176,
            'longitude': -71.084707,
            'type': 'custom_node_type_2',
            'category': {
                'custom_data_chunk_1': [
                    'custom_data_key_2',
                    'custom_data_key_3'
                ],
                'custom_data_chunk_2': [
                    'custom_data_key_1',
                    'custom_data_key_4',
                ],
                # As many data chunks as needed
            },
            'props': {
                'custom_prop_key_10': {
                    'value': 50,
                },
                'custom_prop_key_11': {
                    'name': 'A name to be displayed in the UI',
                    'type': 'num',
                    'variant': 'slider',
                    'value': 40,
                    'enabled': False,
                    'help': 'A help text for the numeric input',
                    'order': 2,
                    'unit': 'units',
                    'column': 2,
                },
                'custom_prop_key_12': {
                    'type': 'toggle',
                    'value': True,
                    'enabled': False,
                    'help': 'A help text for this toggle'
                },
            },
        },
        'custom_node_data_2': {...},
        # As many node data chunks as needed
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`category`](#category)
- [`colorBy`](#colorBy)
- [`colorByOptions`](#colorByOptions)
- [`column`](#column)
- [`constraint`](#constraint)
- [`data`](#data)
- [`enabled`](#enabled)
- [`endGradientColor`](#endGradientColor)
- [`endSize`](#endSize)
- [`help`](#help)
- [`icon`](#icon)
- [`name`](#name)
- [`order`](#order)
- [`prop > type`](#prop-type)
- [`propDefaults`](#propDefaults)
- [`props`](#props)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)
- [`sizeBy`](#sizeBy)
- [`sizeByOptions`](#sizeByOptions)
- [`startSize`](#startSize)
- [`startGradientColor`](#startGradientColor)
- [`prop > unit`](#prop-unit)
- [`value`](#value)
- [`variant`](#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`data.custom_node_data_*` | Required | A custom key wrapper for the parameters required to visualize a node and the data associated with it in the "**Map**" view.
`data.custom_node_data_*.altitude` | `1` | The altitude of the node (in meters) above sea level. Defaults to 1 to appear on top of `geo` layers.
`data.custom_node_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](#custom_data_chunk_).
`data.custom_node_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](#custom_data_key_).
`data.custom_node_data_*.latitude` | Required | The latitude of the node location in the "**Map**" view. It takes a float value.
`data.custom_node_data_*.longitude` | Required | The longitude of the node location in the "**Map**" view. It takes a float value.
`data.custom_node_data_*.name` | | A name for the node location that will be displayed as a title in the map modal.
`data.custom_node_data_*.props`&swarhk;<br>`.custom_prop_key_*` | | See [`custom_prop_key_*`](#custom_prop_key_).
`data.custom_node_data_*.type` | Required | The `type` key sets the node type of `custom_node_data_*` to a `custom_node_type_*` key, to match specific visualization preferences for a node.
`types` | Required | The `types` key allows you to define different types of nodes in terms of styling and data viz settings.
`types.custom_node_type_*` | | A wrapper for key-value pairs that match a specific set of data viz preferences for a node.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'nodes': {
    'data': {
        'Brazilian': {
            'type': 'Manufacturer',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate or deactivate the manufacturer.',
                    'type': 'toggle',
                    'order': 2,
                    'value': True,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'order': 0,
                    'value': 'Campinas, Brazil',
                    'output': False,
                    'enabled': False,
                },
                'Product family': {
                    'help': 'Product family produced by the manufacturer.',
                    'type': 'text',
                    'order': 1,
                    'value': 'LowVal',
                    'output': False,
                    'enabled': False,
                },
                'Transportation Modes': {
                    'cost': False,
                    'help': 'Type of transportation modes that can be used for the manufacturer.',
                    'type': 'selector',
                    'order': 8,
                    'radio': True,
                    'value': {'Air': True, 'Sea': False},
                    'enabled': True,
                },
                'Manufacturing Cost ($/pallet)': {
                    'help': 'Manufacturing cost per pallet.',
                    'type': 'num',
                    'order': 4,
                    'value': 450,
                    'output': False,
                    'enabled': False,
                },
                'Production acquired (pallets)': {
                    'help': 'Quantity purchased from the manufacturer, larger than or equal to the minimum order.',
                    'type': 'num',
                    'order': 6,
                    'value': 500,
                    'output': True,
                    'enabled': False,
                },
                'Min Order / Max Capacity (pallets)': {
                    'help': 'Minimum quantity to be purchased if active / Maximum production capacity.',
                    'type': 'num',
                    'order': 4,
                    'value': '500 / 7000',
                    'output': False,
                    'enabled': False,
                },
            },
            'category': {'Manufacturer': ['Brazilian']},
            'latitude': -22.934,
            'longitude': -47.093,
        },
        'Atlanta DC': {
            'type': 'Distribution Center',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate/open or deactivate/close the distribution center.',
                    'type': 'toggle',
                    'order': 1,
                    'value': True,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'order': 0,
                    'value': 'Atlanta, US',
                    'output': False,
                    'enabled': False,
                },
                'Fixed Cost (k$)': {
                    'help': 'Fixed cost of the distribution center.',
                    'type': 'num',
                    'order': 2,
                    'value': '360.0',
                    'output': False,
                    'enabled': False,
                },
                'Capacity (pallets)': {
                    'help': 'Maximum capacity of the distribution center.',
                    'type': 'num',
                    'order': 2,
                    'value': 17000,
                    'output': False,
                    'enabled': False,
                },
                'Inventory Cost (k$)': {
                    'help': 'Cost of inventory accounting for cycle stock and safety stock.',
                    'type': 'num',
                    'order': 3,
                    'value': '6.5',
                    'output': True,
                    'enabled': False,
                },
                'Demand Served (pallets)': {
                    'help': 'Total demand served from the distribution center.',
                    'type': 'num',
                    'order': 2,
                    'value': 1998,
                    'output': True,
                    'enabled': False,
                },
                'Capacity Utilization (%)': {
                    'help': 'Percentage of available capacity occupied.',
                    'type': 'num',
                    'order': 3,
                    'value': 11.75,
                    'output': True,
                    'enabled': False,
                },
                'Transportation cost (k$)': {
                    'help': 'Cost of delivery to warehouses for interfacility flows departing from the distribution center.',
                    'type': 'num',
                    'order': 4,
                    'value': '56.5',
                    'output': True,
                    'enabled': False,
                },
            },
            'category': {'Distribution Center': ['Atlanta DC']},
            'latitude': 34.037,
            'longitude': -84.235,
        },
        'Korean Tiger': {
            'type': 'Manufacturer',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate or deactivate the manufacturer.',
                    'type': 'toggle',
                    'order': 2,
                    'value': False,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'order': 0,
                    'value': 'Daegu, Korea',
                    'output': False,
                    'enabled': False,
                },
                'Product family': {
                    'help': 'Product family produced by the manufacturer.',
                    'type': 'text',
                    'order': 1,
                    'value': 'LowVal',
                    'output': False,
                    'enabled': False,
                },
                'Transportation Modes': {
                    'cost': False,
                    'help': 'Type of transportation modes that can be used for the manufacturer.',
                    'type': 'selector',
                    'order': 8,
                    'radio': True,
                    'value': {'Air': True, 'Sea': False},
                    'enabled': True,
                },
                'Manufacturing Cost ($/pallet)': {
                    'help': 'Manufacturing cost per pallet.',
                    'type': 'num',
                    'order': 4,
                    'value': 300,
                    'output': False,
                    'enabled': False,
                },
                'Production acquired (pallets)': {
                    'help': 'Quantity purchased from the manufacturer, larger than or equal to the minimum order.',
                    'type': 'num',
                    'order': 6,
                    'value': 0,
                    'output': True,
                    'enabled': False,
                },
                'Min Order / Max Capacity (pallets)': {
                    'help': 'Minimum quantity to be purchased if active / Maximum production capacity.',
                    'type': 'num',
                    'order': 4,
                    'value': '800 / 8000',
                    'output': False,
                    'enabled': False,
                },
            },
            'category': {'Manufacturer': ['Korean Tiger']},
            'latitude': 35.871,
            'longitude': 128.602,
        },
        'Reno Warehouse': {
            'type': 'Warehouse',
            'props': {
                'Active': {
                    'help': 'The toggle button serves to activate/open or deactivate/close the warehouse.',
                    'type': 'toggle',
                    'order': 1,
                    'value': False,
                    'output': False,
                    'enabled': True,
                },
                'Location': {
                    'help': 'City and country',
                    'type': 'text',
                    'order': 0,
                    'value': 'Reno, Nevada, US',
                    'output': False,
                    'enabled': False,
                },
                'Fixed Cost (k$)': {
                    'help': 'Fixed cost of the warehouse, depending on its capacity and accounting for economies of scale.',
                    'type': 'num',
                    'order': 1,
                    'value': '264.2',
                    'output': True,
                    'enabled': False,
                },
                'Capacity (pallets)': {
                    'type': 'num',
                    'order': 2,
                    'value': 4000,
                    'slider': True,
                    'enabled': True,
                    'maxValue': 8000,
                    'minValue': 2000,
                },
                'Inventory Cost (k$)': {
                    'help': 'Cost of inventory accounting for cycle stock and safety stock.',
                    'type': 'num',
                    'order': 3,
                    'value': '0.0',
                    'output': True,
                    'enabled': False,
                },
                'Demand Served (pallets)': {
                    'help': 'Total demand served from the warehouse.',
                    'type': 'num',
                    'order': 2,
                    'value': 0,
                    'output': True,
                    'enabled': False,
                },
                'Capacity Utilization (%)': {
                    'help': 'Percentage of available capacity occupied.',
                    'type': 'num',
                    'order': 2,
                    'value': 0,
                    'output': True,
                    'enabled': False,
                },
                'Last Mile Distribution Cost (k$)': {
                    'help': 'Cost of delivery to customer locations for routes departing from the warehouse.',
                    'type': 'num',
                    'order': 5,
                    'value': '0.0',
                    'output': True,
                    'enabled': False,
                },
            },
            'category': {'Warehouse': ['Reno Warehouse']},
            'latitude': 39.526,
            'longitude': -119.813,
        },
    },
    'name': 'Nodes',
    'types': {
        'Warehouse': {
            'icon': 'FaSquareFull',
            'sizeBy': 'Capacity (pallets)',
            'colorBy': 'Capacity Utilization (%)',
            'endSize': '17px',
            'startSize': '12px',
            'sizeByOptions': {
                'Capacity (pallets)': {'min': 0, 'max': 2000},
                'Capacity Utilization (%)': {'min': 0, 'max': 99},
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
            'colorByOptions': {
                'Capacity (pallets)': {
                    'min': 0,
                    'max': 2000,
                    'endGradientColor': 'rgb(51, 153, 51)',
                    'startGradientColor': 'rgb(204, 255, 153)',
                },
                'Capacity Utilization (%)': {
                    'min': 0,
                    'max': 99,
                    'endGradientColor': 'rgb(51, 153, 51)',
                    'startGradientColor': 'rgb(204, 255, 153)',
                },
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
        },
        'Manufacturer': {
            'icon': 'BsOctagonFill',
            'sizeBy': 'Production Capacity (pallets)',
            'colorBy': 'Manufacturing Cost ($/pallet)',
            'endSize': '25px',
            'startSize': '15px',
            'sizeByOptions': {
                'Capacity (pallets)': {'min': 0, 'max': 2000},
                'Capacity Utilization (%)': {'min': 0, 'max': 99},
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
            'colorByOptions': {
                'Capacity (pallets)': {
                    'min': 0,
                    'max': 2000,
                    'endGradientColor': 'rgb(255, 0, 0)',
                    'startGradientColor': 'rgb(255, 204, 153)',
                },
                'Capacity Utilization (%)': {
                    'min': 0,
                    'max': 99,
                    'endGradientColor': 'rgb(255, 0, 0)',
                    'startGradientColor': 'rgb(255, 204, 153)',
                },
                'Fixed Cost (k$)': {
                    'min': 0,
                    'max': 200,
                    'endGradientColor': 'rgb(255, 0, 0)',
                    'startGradientColor': 'rgb(255, 204, 153)',
                },
            },
        },
        'Distribution Center': {
            'icon': 'BsTriangleFill',
            'sizeBy': 'Capacity (pallets)',
            'colorBy': 'Capacity Utilization (%)',
            'endSize': '25px',
            'startSize': '15px',
            'sizeByOptions': {
                'Capacity (pallets)': {'min': 0, 'max': 2000},
                'Capacity Utilization (%)': {'min': 0, 'max': 99},
                'Fixed Cost (k$)': {'min': 0, 'max': 200},
            },
            'colorByOptions': {
                'Capacity (pallets)': {
                    'min': 0,
                    'max': 2000,
                    'endGradientColor': 'rgb(0, 0, 255)',
                    'startGradientColor': 'rgb(102, 255, 255)',
                },
                'Capacity Utilization (%)': {
                    'min': 0,
                    'max': 99,
                    'endGradientColor': 'rgb(0, 0, 255)',
                    'startGradientColor': 'rgb(102, 255, 255)',
                },
                'Fixed Cost (k$)': {
                    'min': 0,
                    'max': 200,
                    'endGradientColor': 'rgb(0, 0, 255)',
                    'startGradientColor': 'rgb(102, 255, 255)',
                },
            },
        },
    },
}
```
</details>

### `geos`
The `geos` group takes in data and renders it as geographic areas on the "**Map**" view, to visualize spatial distribution of parameters.

The internal structure of `geos` is very similar to that of the `arcs` and `nodes` groups. The most relevant discrepancy is the addition of a special key `geoJson` that is closely related to the GeoJSON data retrieved from the [`geoJsons`](#geoJsons) group.

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
            'icon': 'FaHexagon',
        },
        'custom_geo_type_2': {...},
        # As many geo types as needed
    },
    'propDefaults': {
        'custom_prop_key_1': {
            'type': 'num',
            'help': 'A help text for this numeric input',
            'unit': 'Units',
            'enabled': True,
        },
        'custom_prop_key_2': {...},
        # As many propDefaults as needed
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
- [`allow_modification`](#allow_modification)
- [`category`](#category)
- [`colorBy`](#colorBy)
- [`colorByOptions`](#colorByOptions)
- [`column`](#column)
- [`constraint`](#constraint)
- [`data`](#data)
- [`enabled`](#enabled)
- [`endGradientColor`](#endGradientColor)
- [`help`](#help)
- [`icon`](#icon)
- [`name`](#name)
- [`order`](#order)
- [`prop > type`](#prop-type)
- [`propDefaults`](#propDefaults)
- [`props`](#props)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)
- [`startGradientColor`](#startGradientColor)
- [`prop > unit`](#prop-unit)
- [`value`](#value)
- [`variant`](#variant)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`data.custom_geo_data_*` | Required | A custom key wrapper for the parameters required to visualize a geo and the data associated with it on the "**Map**" view.
`data.custom_geo_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](#custom_data_chunk_).
`data.custom_geo_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](#custom_data_key_).
<a name="geojson-value">`data.custom_geo_data_*.geoJsonValue`</a> | | The value matched by [`geojson_prop_*`](#geojson_prop_) inside the GeoJSON data source. The CAVE App will aggregate all data matches found via the path: `features` &rarr; `<array-index>` &rarr; `properties` &rarr; `geojson_prop_*` &rarr; `geojson_value_*`.
<a name="geojson_value_">`data.custom_geo_data_*.geoJsonValue`&swarhk;<br>`.geojson_value_*`</a> | | The match value for the [geoJsonValue](#geojson-value) key.
`data.custom_geo_data_*.name` | | A name for the geo area that will be displayed as a title in the map modal.
`data.custom_geo_data_*.props`&swarhk;<br>`.custom_prop_key_*` | | See [`custom_prop_key_*`](#custom_prop_key_).
`data.custom_geo_data_*.type` | Required | The `type` key sets the type of `custom_geo_data_*` to a `custom_geo_type_*` key, to match specific visualization preferences for a geo.
<a name="geojson">`types.custom_geo_type_*.geoJson`</a> | | A wrapper for the [`geoJsonLayer`](#geojson_layer) and [`geoJsonProp`](#geojson_prop) keys in a geo type.
<a name="geojson_layer">`types.custom_geo_type_*.geoJson`&swarhk;<br>`.geoJsonLayer`</a> | | Sets the GeoJSON data source of `custom_geo_type_*` to a URL of a GeoJSON data source. Note that this url is fetched on app startup or, if passed later, when the layer is enabled by the app user.
`types.custom_geo_type_*.geoJson`&swarhk;<br>`.geoJsonLayer.custom_geojson_data_*` | Required | See [`custom_geojson_data_*`](#custom_geojson_data_).
<a name="geojson_prop">`types.custom_geo_type_*.geoJson`&swarhk;<br>`.geoJsonProp`</a> | | Contains the name of a [GeoJSON property](#https://datatracker.ietf.org/doc/html/rfc7946#section-1.5) in the data source specified in `geoJsonLayer`.
<a name="geojson_prop_">`types.custom_geo_type_*.geoJson`&swarhk;<br>`.geoJsonProp.geojson_prop_*`</a> | | The match value for the [geoJsonProp](#geojson_prop) key.
`types` | Required | The `types` key allows you to define different types of geos in terms of styling and data viz settings.
`types.custom_geo_type_*` | Required | A wrapper for key-value pairs that match a specific set of data viz preferences for a geo.

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
            'icon': 'FaHexagon',
        },
    },
    'propDefaults': {
        'Demand': {
            'type': 'num',
            'enabled': True,
            'help': 'The Demand of this Geography',
            'unit': 'Units',
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

### `map`
This key group allows designers to specify information about the starting state of the map, what information is contained and how it is grouped in the legend, and what viewports can be easily jumped to by the user.

Below is the `map` group with its sub-keys matched by typical or placeholder values:
```py
"map": {
    "name": "map",
    "data":{
        "enabledArcTypes": {"arc": {"T1": True}},
        "defaultViewport": {
            "longitude": -75.44766721108091,
            "latitude": 40.34530681636297,
            "zoom": 4.657916626867326,
            "pitch": 0,
            "bearing": 0,
            "height": 1287,
            "altitude": 1.5,
            "maxZoom": 12,
            "minZoom": 2
        },
        "optionalViewports": {
            "ov0": {
                "icon": 'FaGlobeAsia',
                "name": 'Asia',
                "zoom": 4,
                "order": 1,
                "pitch": 0,
                "bearing": 0,
                "maxZoom": 12,
                "minZoom": 2,
                "latitude": 30,
                "longitude": 121
            },
        },
        "legendGroups": [
            {
                "name": "DC Delivery",
                "nodeTypes": ["DC"],
                "arcTypes": ["T1"],
                "geoTypes": ["state", "country"]
            }
        ],
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`data`](#data)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)
- [`name`](#name)
- [`icon`](#icon)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="enabledTypes">`enabledTypes`</a> | {} | An object with keys `arc`, `node`, and `geo`. Each value should be an object with each key in the object representing an type that should be enabled by default and all values set to true.
<a name="defaultViewport">`defaultViewport`</a> | | A dictionary object containing geo properties that set the map's default field of view. Also used by the "home" button in the app.
`defaultViewport.bearing` | `0` | The initial bearing (rotation) of the map, measured in degrees counter-clockwise from north.
`defaultViewport.pitch` | `0` | The initial pitch (*tilt*) of the viewport in the "**Map**" view, measured in degrees away from the plane of the screen (0&deg; - 85&deg;). A pitch of 0&deg; results in a two-dimensional map, as if your line of sight forms a perpendicular angle with the earth's surface, while a greater value like 60&deg; looks ahead towards the horizon.
`defaultViewport.latitude` | 42.36157 | The center latitude of the viewport in the "**Map**" view. It takes a float value.
`defaultViewport.longitude` | -71.08463 | The center longitude of the viewport in the "**Map**" view. It takes a float value.
`defaultViewport.maxZoom` | `22` | The maximum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`defaultViewport.minZoom` | `1.5` | The minimum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`defaultViewport.zoom` | `13` | The initial zoom level of the viewport in the "**Map**" view. It takes an integer value. Learn more about the zoom levels [here](#https://docs.mapbox.com/help/glossary/zoom-level/).
<a name="optionalViewports">`optionalViewports`</a> | | A dictionary of optional viewports that can be jumped to by users. Each optional viewport should contain the same keys as `defaultViewport` as well as `name` and `icon` keys.
<a name="legendGroups">`legendGroups`</a> | [] | A list of all groupings to be shown in the map legend. Groups are displayed in list order with each group having an internal order of nodes, arcs, then geos. Types not included in any legendGroup cannot be toggled.
`legendGroups[i].nodeTypes` | | A list of all node types to include in the legendGroup. Note that settings (colorBy, sizeBy) are syncronized across the same type in multiple groups.
`legendGroups[i].arcTypes` | | A list of all arc types to include in the legendGroup. Note that settings (colorBy, sizeBy) are syncronized across the same type in multiple groups.
`legendGroups[i].geoTypes` | | A list of all geo types to include in the legendGroup. Note that settings (colorBy, sizeBy) are syncronized across the same type in multiple groups.

### `stats`
The `stats` group takes parameter data that can be combined with geospatial data to represent it in the "**Map**" view or simply use its raw values to display in a dashboard view.

Let's look inside the structure of `stats`:
```py
'stats': {
    'name': 'Statistics',
    'types': {
        'custom_stat_key_1': {
            'name': 'A name to be displayed in the UI',
            'calculation': 'custom_stat_key_1 / custom_stat_key_2',
            'unit': 'Units',
            'order': 1,
        },
        'custom_stat_key_2': {...},
        # As many stats as needed
    },
    'data': {
        'custom_stat_data_1': {
            'category': {
                'custom_data_chunk_1': [
                    'custom_data_key_2',
                    'custom_data_key_4'
                ],
                'custom_data_chunk_2': [
                    'custom_data_key_1',
                    'custom_data_key_3',
                ],
                # As many data chunks as needed
            },
            'values': {
                'custom_stat_key_1': 3,
                'custom_stat_key_2': 8,
                # As many stat keys as needed
            },
        },
        'custom_stat_data_2': {...},
        # As many stat data chunks as needed
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`category`](#category)
- [`data`](#data)
- [`name`](#name)
- [`order`](#order)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`data.custom_stat_data_*` | Required | A custom key wrapper for the [`category`](#category) and [`values`](#values) keys.
`data.custom_stat_data_*.category`&swarhk;<br>`.custom_data_chunk_*` | | See [`custom_data_chunk_*`](#custom_data_chunk_).
`data.custom_stat_data_*.category`&swarhk;<br>`.custom_data_chunk_*.custom_data_key_*` | | See [`custom_data_key_*`](#custom_data_key_).
<a name="values">`data.custom_stat_data_*.values`</a> | Required | A wrapper for independent `custom_stat_key_*`s and their values.
<a name="custom_stat_key_">`types.custom_stat_key_*`</a> | Required | A key used to identify a parameter in a `calculation` expression and be referenced by the `values` group.
`types` | Required | The `types` key allows you to define the appearance and logic of the `custom_stat_key_*` parameters.
`types.custom_stat_key_*.calculation` | Required | Defines a math expression that allows the calculation of a `custom_stat_key_*` parameter that depends on the value of others. The expression is used to dynamically estimate the value of a parameter when the data containing its independent stats used in the calculation, has changed, e.g. after applying a filter. When a custom stat is independent, the math expression must match its own `custom_stat_key_*`. The CAVE App comes with a software package that provides built-in support for common math functions and operators. For a list of the available operators and examples of math expressions, see the [`expr-eval` documentation](https://github.com/silentmatt/expr-eval#documentation) and [`groupSum`](#groupsum) below.
`types.custom_stat_key_*.unit` | | A unit displayed next to the stat calculation result.

##### `groupSum`
`groupSum` is a special function provided by the CAVE app that takes an independent stat as input and outputs the sum of that stat across the level (or sub-level if present) specified by the user or api for that [dashboard](#dashboards) chart. Using `groupSum` is different than other `expr-eval` functions as the variable must be passed as a string rather than a literal (e.g. `groupSum("custom_stat")` not `groupSum(custom_stat)`). When using `groupSum` special consideration should be given to ensure the the dashboard grouping (sum, minimum, maximum, or average) makes it clear to users what the stat represents, as while `groupSum` sums across the level the stat calculation is still done to the individual stats which are then grouped.

#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'stats': {
    'name': 'Statistics',
    'types': {
        'demand_met': {
            'name': 'Demand Met',
            'calculation': 'demand_met',
            'unit': 'units',
            'order': 1,
        },
        'demand_tot': {
            'name': 'Demand Total',
            'calculation': 'demand_tot',
            'unit': 'units',
            'order': 2,
        },
        'demand_pct': {
            'name': 'Demand Percentage',
            'calculation': 'demand_met / groupSum("demand_tot")',
            'unit': '%',
            'order': 3,
        },
    },
    'data': {
        'd1': {
            'category': {
                'Location': ['loc_CA_ON'],
                'Product': ['prd_abc123'],
            },
            'values': {
                'demand_met': 5,
                'demand_tot': 10,
            },
        },
        'd2': {
            'category': {
                'Location': ['loc_CA_ON'],
                'Product': ['prd_def456'],
            },
            'values': {
                'demand_met': 4,
                'demand_tot': 5,
            },
        },
        'd3': {
            'category': {
                'Location': ['loc_US_MI'],
                'Product': ['prd_abc123'],
            },
            'values': {
                'demand_met': 6,
                'demand_tot': 7,
            },
        },
        'd4': {
            'category': {
                'Location': ['loc_US_MI'],
                'Product': ['prd_def456'],
            },
            'values': {
                'demand_met': 3,
                'demand_tot': 5,
            },
        },
    },
}
```
</details>

### `kpis`
The `kpis` group contains all the KPI data that will be displayed on the "**KPI**" view.

Let's look inside the structure of `kpis`:
```py
'kpis': {
    'data': {
        'custom_kpi_1': {
            'name': 'A name to be displayed in the UI',
            'unit': 'Units',
            'icon': 'FaBox',
            'order': 1,
            'column': 1,
            'value': 100,
        },
        # As many custom KPIs as needed
    },
}
```

##### Common keys
- [`allow_modification`](#allow_modification)
- [`column`](#column)
- [`data`](#data)
- [`icon`](#icon)
- [`name`](#name)
- [`order`](#order)
- [`send_to_api`](#send_to_api)
- [`send_to_client`](#send_to_client)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`custom_kpi_*` | Required | A custom key wrapper for the KPI data.
`custom_kpi_*.unit` | | A unit displayed next to the KPI value.
`custom_kpi_*.value` | | The actual value of the KPI. **If not specified, this item will be a KPI header**.
`custom_kpi_*.map_kpi` | False | The `map_kpi` flag allows designers to specify up to six parameters that are displayed on a permanent grid in the "**Map**" view. The grid layout (rows *x* columns) changes with the number of parameters present in the data, scaling up to 2 rows and 3 columns.


#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'kpis': {
    'data': {
        'demand': {
            'name': 'Global Demand',
            'unit': 'Units',
            'icon': 'FaBox',
            'order': 1,
            'column': 1,
            'value': 100,
        },
    },
}
```
</details>


### `kwargs`
The `kwargs` group contains special keys that are not actually stored in the data but instead used to instruct the server to do special tasks.

Let's look inside the structure of `kwargs`:
```py
'kwargs': {
  'wipe_existing':False
}
```

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
`wipe_existing` | True | Indicate if all current session data (the current session of the requesting user) should be wiped before overwriting all currently passed data. This can be used to reduce server load. For example given a specific command, if only a single top_level_key should be updated, you can simply pass that top_level_key dictionary and set `wipe_existing` to `False`. in this case, you would only overwrite that single top_level_key and leave the rest unchanged.



#### Example

<details>
  <summary>Click here to show / hide example</summary>

```py
'kwargs': {
  'wipe_existing':False
}
```
</details>


### Top-level custom keys
In addition to the standard CAVE top-level keys described in this document, designers can add custom top-level keys that allow them to persist data that is computed as a result of a user-side action. This emulates (on the back-end side) a pattern widely used in front-end development, called [state management](#https://en.wikipedia.org/wiki/State_management).

A fairly common use case for this approach is to persist data that may need to be invisible to users based on other user selections. For example, an app that has options that toggle other options might want to store any choices users have made when those options are not currently presented to the user. While designers could explore other solutions for data persistence, we believe that top-level custom keys provide an easy escape hatch for organizing and accessing a persistent data state in the CAVE API structure.

All top-level keys mentioned above are reserved for the use described above and should not be used as custom keys as this may break functionality. Additionally the following top-level keys are reserved and should not be used as custom keys:

- `ignore`
- `associated`

A CAVE API structure with top-level custom keys looks as follows:
```py
{
    'settings': {...},
    'categories': {...},
    'appBar': {...},
    'arcs': {...},
    'nodes': {...},
    'geos': {...},
    'map': {...},
    'stats': {...},
    'kpis': {...},
    'kwargs':{...},
    'custom_top_level_key_1': {
        'send_to_client': False,
        'custom_persisted_data_key_1': 10,
        'custom_persisted_data_key_2': [-1, 3],
        'custom_persisted_data_key_3': {...},
        # As many persisted data chunks as needed
    },
    'custom_top_level_key_2': {...},
    # As many custom top level keys as needed
}
```

It is worth noting that the client will ignore any keys not in the aforementioned sections. If you plan to use additional top-level keys, it is advised that `send_to_client=False` to prevent unnecessary data overhead. Also note: in order to access these for persistent state, you should set `send_to_api=True`.

[`'Bar'`]: <https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-Y%20Axis=true&knob-vertical%20gridlines=true&knob-horizontal%20gridlines=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&selectedKind=Series%2FVerticalBarSeries%2FBase&selectedStory=multiple%20VerticalBarSeries%20-%20clustered&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs>
[`'Line'`]: https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&knob-vertical%20gridlines=true&knob-stroke=%2312939a&knob-horizontal%20gridlines=true&knob-opacity=1&knob-curve=curveBasis&knob-fill=%2312939a&knob-style=%7B%22stroke%22%3A%22%232c51be%22%2C%22strokeWidth%22%3A%223px%22%7D&knob-colorScale=category&knob-Y%20Axis=true&selectedKind=Series%2FLineSeries%2FBase&selectedStory=With%20negative%20numbers&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs
[`'Box Plot'`]: https://plotly.com/javascript/box-plots/
