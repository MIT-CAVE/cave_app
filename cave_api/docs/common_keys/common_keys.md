# Common keys
## At the Top level
Key | Default | Description
--- | ------- | -----------
<a name="allowModification">`allowModification`</a> | `True` | If `True`, end users can request changes to the data within the key group during user interaction with the CAVE app and the server will process the request. Note, this only blocks a user from being able to modify a server side structure for security reasons. To block client side interactions, see the [`enabled`](props.md#enabled) key.
<a name="data">`data`</a> | Required | Dictionary object that contains data related to this key group.
<a name="sendToApi">`sendToApi`</a> | `True` | If `True`, the data will be serialized and sent as `session_data` when calling `execute_command`.
<a name="sendToClient">`sendToClient`</a> | `True` | If `True`, the data will be sent to the requesting CAVE app client. While most of the time this should be `True`, there are use cases where the API designer might want to store some type of state that is not consumed directly (see [Top Level Custom Keys](../custom_keys.md)).

## Nested inside the `data` group
Key | Default | Description
--- | ------- | -----------
<a name="category">`category`</a> | | A dictionary of category custom keys appropriated to a string or list of strings (custom keys inside each custom category). This is used in an object to associate categories for aggregation and filtering purposes.
<a name="color">`color`</a> | | The color to be appropriated to the current object.[^1]
<a name="colorBy">`colorBy`</a> | | Specifies a [`customPropKey*`](props.md#customPropKey), which variation of its values is visualized through a color gradient. The color gradient is bounded by [`startGradientColor`](#start-gradient) and [`endGradientColor`](#end-gradient), and is specified in [`colorByOptions`](#colorByOptions).<br><br>Used in [`arcs`](../all_keys/arcs.md), [`nodes`](../all_keys/nodes.md) and [`geos`](../all_keys/geos.md).
<a name="colorByOptions">`colorByOptions`</a> | | An object with [parameters](../all_keys/categories.md#custom_data_key_) keys that are provided for the user to choose from a drop-down menu in the "**Map Legend**" and view their variation in terms of a color gradient.<br><br>The associated value should be either an object with shape `{"min": 0, "max": 0, "startGradientColor": "rgb(0,0,0)", "endGradientColor": "rbg(0,0,0)"}` that contains the expected [`min`](#color-by-min) and [`max`](#color-by-max) values and color gradient for the parameter or a dictionary with shape `{"custom_color_key_1": "rgb(233, 0, 0)"}` for parameters with discrete values. Note that `min` and `max` are reserved keys and should not be provided as `custom_color_key_*`s.<br><br>Used in [`arcs`](../all_keys/arcs.md), [`nodes`](../all_keys/nodes.md) and [`geos`](../all_keys/geos.md).
<a name="end-gradient">`colorByOptions.endGradientColor`</a> | | The final color in a color gradient that matches the maximum value specified in [`colorByOptions.max`](#color-by-max). This should be an RGB string. EG: `'rgb(0,0,0)'`.
<a name="color-by-max">`colorByOptions.max`</a> | | The maximum value that a parameter can take in.
<a name="color-by-min">`colorByOptions.min`</a> | | The minimum value that a parameter can take in.
<a name="color-by-null">colorByOptions.nullColor</a> | `'rgb(0,0,0)'` | The color to set any objects with a null value for the given prop. This should be an RGB string. EG: `'rgb(0,0,0)'`. This can also by set to the `None` keyword to hide these objects. Not supported for groupable nodes.
<a name="start-gradient">`colorByOptions.startGradientColor`</a> | | The starting color in a color gradient that matches the minimum value specified in [`colorByOptions.min`](#color-by-min). This should be an RGB string. EG: `'rgb(0,0,0)'`.
<a name="column">`column`</a>  | | A column position number (left to right) at which a UI element will be displayed when in a `grid` layout. This includes layouts for([`'options'` panes](../all_keys/app_bar.md#options-pane) or [KPIs](../all_keys/kpis.md)) or a map modal ([`arcs`](../all_keys/arcs.md), [`nodes`](../all_keys/nodes.md), and [`geos`](../all_keys/geos.md)). If omitted in a full-width view layout, the element will not be displayed in the UI.
<a name="data">`data`</a> | | Dictionary object that contains data related to the use case.
<a name="endSize">`endSize`</a> | | The end dimension in pixels for a stroke width of an arc or the size of an icon on a node, which matches the maximum value of a given parameter in a set of data points. This should be a pixel string. EG: `'45px'`.<br><br>Used in [`arcs`](../all_keys/arcs.md) and [`nodes`](../all_keys/nodes.md).
<a name="icon">`icon`</a> | Required | The name of a [React Icon](https://react-icons.github.io/react-icons) that will be displayed in the UI. Currently icons are downloaded after the app has loaded (not in the build) and stored in a local cache. This reduces build size while allowing for large icon sets to be supported. Current icon support depends on which statically built icon svgs you are using. See [settings.data.iconUrl](../all_keys/settings.md#iconUrl) for more info.
<a name="layout">`layout`</a> | | A dictionary object that describes how [props](props.md) or [KPIs](../all_keys/kpis.md) are organized within their UI container components. See the [layout](layout.md) section for a more detailed explanation of this group and some common use cases.
<a name="name">`name`</a> | | The name of the element to be displayed as a label in the user interface. If omitted, the parent key of the **un`name`d** group is displayed.
<a name="number-format">`numberFormat`</a> | | A dictionary object that contains properties to enable language-sensitive number formatting. See the [number formatting](number_format.md) section for a more detailed explanation of this group and different use cases.
<a name="order">`order`</a> | | When specified in a key group, the `order` parameter sets the position in which the element is rendered in the UI, relative to its siblings. The `order` key takes integer values and the sibling elements will be sorted in ascending order. Since this parameter is optional, all **un`order`ed** items will be sorted alphabetically against each other and placed after the **`order`ed** items. Therefore, if you do not specify any `order` for a group of sibling keys, all of them will be sorted alphabetically according to their `name` values (or parent key when `name` is not specified).
<a name="props-short">`props`</a> | Required | A dictionary object that contains the specification of the input controls in the UI. See the [props](props.md) section for a more detailed explanation of this group and its different `prop` items.
<a name="sizeBy">`sizeBy`</a> | | The parameter selected to show its variation in terms of stroke width ([`arcs`](../all_keys/arcs.md)) or icon size ([`nodes`](../all_keys/nodes.md)). The size range is bounded by [`startSize`](#startSize) and [`endSize`](#endSize).
<a name="sizeByOptions">`sizeByOptions`</a> | | An object with [parameters](../all_keys/categories.md#custom_data_key_) keys that are provided for the user to choose from a drop-down menu in the "**Map Legend**" and view their variation in terms of stroke width ([`arcs`](../all_keys/arcs.md)) or icon size ([`nodes`](../all_keys/nodes.md)). The associated value should be an object with shape `{"min": 0, "max": 0}` that contains the expected minimum and maximum values for the parameter.
<a name="size-by-null">sizeByOptions.nullSize</a> | `None` | The size to set any objects with a null value for the given prop. This should be a pixel string. EG: `'45px'`. This can also by set to the `None` keyword to hide these objects. Not supported for groupable nodes.
<a name="startSize">`startSize`</a> | | The starting dimension in pixels for a stroke width of an arc or the size of a node icon, which matches the minimum value of a given parameter in a set of data points. This should be a pixel string. EG: `'45px'`.<br><br>Used in [`arcs`](../all_keys/arcs.md) and [`nodes`](../all_keys/nodes.md).

[^1]: This key matches a string that contains a [color value](https://developer.mozilla.org/en-US/docs/Web/CSS/color_value) or a dictionary object with color values per theme keys. The allowed theme keys in the current version are `'dark'` and `'light'`.

## Important Common Keys
- ## [`props`](props.md)

- ## [`layout`](layout.md)

- ## [`numberFormat`](numberFormat.md)

- ## [`timeObject`](timeObject.md)