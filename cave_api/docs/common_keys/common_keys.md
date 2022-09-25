### Common keys
#### At the Top level
Key | Default | Description
--- | ------- | -----------
<a name="allow_modification">`allow_modification`</a> | `True` | If `True`, end users can request changes to the data within the key group during user interaction with the CAVE app and the server will process the request. Note, this only blocks a user from being able to modify a server side structure for security reasons. To block client side interactions, see the [`enabled`](#enabled) key.
<a name="data">`data`</a> | Required | Dictionary object that contains data related to this key group.
<a name="send_to_api">`send_to_api`</a> | `True` | If `True`, the data will be serialized and sent as `session_data` when calling `execute_command`.
<a name="send_to_client">`send_to_client`</a> | `True` | If `True`, the data will be sent to the requesting CAVE app client. While most of the time this should be `True`, there are use cases where the API designer might want to store some type of state that is not consumed directly (see [Top Level Custom Keys](#top-level-custom-keys)).

#### Nested inside the `data` group
Key | Default | Description
--- | ------- | -----------
<a name="category">`category`</a> | | A dictionary of category custom keys appropriated to a string or list of strings (custom keys inside each custom category). This is used in an object to associate categories for aggregation and filtering purposes.
<a name="color">`color`</a> | | The color to be appropriated to the current object.[^1]
<a name="colorBy">`colorBy`</a> | | The parameter selected to show its variation in terms of a color gradient. The color gradient is bounded by [`startGradientColor`](#startGradientColor) and [`endGradientColor`](#endGradientColor). Used in [`arcs`](#arcs), [`nodes`](#nodes) and [`geos`](#geos).
<a name="colorByOptions">`colorByOptions`</a> | | A object with [parameters](#custom_data_key_) keys that are provided for the user to choose from a drop-down menu in the "**Map Legend**" and view their variation in terms of a color gradient. The associated value should be either an object with shape `{"min": 0, "max": 0, "startGradientColor": "rgb(0,0,0)", "endGradientColor": "rbg(0,0,0)"}` that contains the expected minimum and maximum values and color for the parameter Used in [`arcs`](#arcs), [`nodes`](#nodes) and [`geos`](#geos) or a dictionary with shape `{"custom_color_key_here":"rgb(233, 0, 0)"}` for discrete variables. Note: `min` and `max` are reserved keys and should not be provided as a `custom_color_key`.
<a name="column">`column`</a>  | | A column position number (left to right) at which a UI element will be displayed when in a `grid` layout. This includes layouts for([`'options'` panes](#options-pane) or [KPIs](#kpis)) or a map modal ([`arcs`](#arcs), [`nodes`](#nodes), and [`geos`](#geos)). If omitted in a full-width view layout, the element will not be displayed in the UI.
<a name="deprecat-constraint">`constraint`</a> (_Deprecated in `0.2.0`_) | `'float'` | Used along a `'num'` type, its value can be `'int'` or `'float'` to enforce integer or floating point values respectively, for a prop element in the UI.
<a name="data">`data`</a> | | Dictionary object that contains data related to the use case.
<a name="endSize">`endSize`</a> | | The end dimension in pixels for a stroke width of an arc or the size of an icon on a node, which matches the maximum value of a given parameter in a set of data points. Used in [`arcs`](#arcs) and [`nodes`](#nodes).
<a name="icon">`icon`</a> | Required | The name of a [React Icon](https://react-icons.github.io/react-icons) that will be displayed in the UI. Currently icons are downloaded after the app has loaded (not in the build) and stored in a local cache. This reduces build size while allowing for all react-icons to be supported.
<a name="layout">`layout`</a> | | A dictionary object that describes how [props](#the-props-key) or [KPIs](#kpis) are organized within their UI container components. See the [layout](#the-layout-key) section for a more detailed explanation of this group and some common use cases.
<a name="name">`name`</a> | | The name of the element to be displayed as a label in the user interface. If omitted, the parent key of the **un`name`d** group is displayed.
<a name="number-format">`numberFormat`</a> | | A dictionary object that contains properties to enable language-sensitive number formatting. See the [number formatting](#the-numberformat-key) section for a more detailed explanation of this group and different use cases.
<a name="order">`order`</a> | | When specified in a key group, the `order` parameter sets the position in which the element is rendered in the UI, relative to its siblings. The `order` key takes integer values and the sibling elements will be sorted in ascending order. Since this parameter is optional, all **un`order`ed** items will be sorted alphabetically against each other and placed after the **`order`ed** items. Therefore, if you do not specify any `order` for a group of sibling keys, all of them will be sorted alphabetically according to their `name` values (or parent key when `name` is not specified).
<a name="props">`props`</a> | Required | A dictionary object that contains the specification of the input controls in the UI. See the [props](#the-props-key) section for a more detailed explanation of this group and its different `prop` items.
<a name="sizeBy">`sizeBy`</a> | | The parameter selected to show its variation in terms of stroke width ([`arcs`](#arcs)) or icon size ([`nodes`](#nodes)). The size range is bounded by [`startSize`](#startSize) and [`endSize`](#endSize).
<a name="sizeByOptions">`sizeByOptions`</a> | | An object with [parameters](#custom_data_key_) keys that are provided for the user to choose from a drop-down menu in the "**Map Legend**" and view their variation in terms of stroke width ([`arcs`](#arcs)) or icon size ([`nodes`](#nodes)). The associated value should be an object with shape `{"min": 0, "max": 0}` that contains the expected minimum and maximum values for the parameter.
<a name="startSize">`startSize`</a> | | The starting dimension in pixels for a stroke width of an arc or the size of an icon on a node, which matches the minimum value of a given parameter in a set of data points. Used in [`arcs`](#arcs) and [`nodes`](#nodes).
<a name="deprecat-unit">`unit`</a> (_Deprecated in `0.2.0`_) | | A unit of measurement that is displayed next to the numeric value in an item ([`'num'` prop](#num), [KPI](#kpis), or [stat](#stats)). The use of this property is deprecated as of version `0.2.0` in favor of [`numberFormat.unit`](#unit). <!-- REVIEW: Update this note when dropping support for `unit` in 1.0.0 -->

[^1]: This key matches a string that contains a [color value](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) or a dictionary object with color values per theme keys. The allowed theme keys in the current version are `'dark'` and `'light'`.

#### Important Common Keys
- #### [props](props.md)

- #### [layout](layout.md)

- #### [numberFormat](numberFormat.md)

- #### [timeObject](timeObject.md)