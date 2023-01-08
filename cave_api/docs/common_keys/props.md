# `props`

We dedicate a section to the `props` group, as it handles all of the user input controls, as well as most of the textual or numeric output in the CAVE App. Let's start with an in-depth look at its internal structure and how it translates to the UI.

```py
"props": {
    "customPropKey1": {
        "name": "Section header",
        "type": "head",
        "help": "A help text for the section header",
    },
    "customPropKey2": {
        "enabled": True,
        "name": "A name to be displayed in the UI",
        "type": "num",
        "value": 1,
        "numberFormat": {
            "precision": 0,
            "unit": "units",
        },
        "help": "A help text for the numeric input",
    },
    "customPropKey3": {
        "name": "A name to be displayed in the UI",
        "type": "num",
        "variant": "slider",
        "value": 30,
        "minValue": 0,
        "maxValue": 100,
        "label": "%",
        "help": "A help text for the slider",
    },
    "customPropKey4": {
        "enabled": True,
        "name": "A name to be displayed in the UI",
        "type": "selector",
        "variant": "dropdown",
        "value": "custom_option_2",
        "options": {
            "custom_option_1": {"name": "Custom Option 1"},
            "custom_option_2": {"name": "Custom Option 2"},
            "custom_option_3": {"name": "Custom Option 3"},
        },
        "help": "A help text for the dropdown selector",
    },
    # As many props as needed
}
```

## Nested inside the `props` group
Aside from [`name`](common_keys.md#name) and [`order`](common_keys.md#order) all the keys and values in the above structure are specific to the `props` group and therefore explained below:

Key | Default | Description
--- | ------- | -----------
<a name="customPropKey">`customPropKey*`</a> | | A custom key wrapper for a `props` item.
<a name="apiCommand">`customPropKey*.apiCommand`</a> | | If specified, passes an api command argument along with a mutation request. This command will be passed to `execute_command` for each session to be synced.
<a name="apiCommandKeys">`customPropKey*.apiCommandKeys`</a> | | If specified, only passes specific session keys over to `execute_command` for each session to be synced.
<a name="enabled">`customPropKey*.enabled`</a> | `False` | Enable a `props` element in the UI. If `False`, users cannot interact with the element in the UI.
<a name="help">`customPropKey*.help`</a> | | A help message that is displayed in the UI, as a result of a mouseover or touch event on a `customPropKey*` element.
<a name="label">`customPropKey*.label`</a> | | A label that is displayed in the UI next to the `customPropKey*` element.
<a name="max-value">`customPropKey*.maxValue`</a> | | Used along a `'num'` prop, it takes the maximum allowed value of the numeric input. Should not be equal to `minValue`.
<a name="min-value">`customPropKey*.minValue`</a> | | Used along a `'num'` prop, it takes the minimum allowed value of the numeric input. Should not be equal to `maxValue`.
<a name="options">`customPropKey*.options`</a> | Required | Used along a `'selector'` prop, it takes an object containing the [`custom_option_*`](#custom_option_)s to be displayed on the UI element mapped to their display properties.
<a name="custom_option_">`customPropKey*.options.custom_option_*`</a> | | Used along a `'selector'` prop, it takes an object containing the name of the option to be displayed on the UI element.
<a name="prop-type">`customPropKey*.type`</a> | Required | As a direct child of `customPropKey*`, the `type` key sets the UI element type, implicitly constraining the set of key-value pairs that can be used along this type. The `type` key takes one of the following values: `'head'`, `'text'`, `'num'`, `'toggle'`, `'button'`, or `'selector'`.
<a name="value">`customPropKey*.value`</a> | Required | The actual value of a `props` element. Depending on the prop [`type`](#prop-type), it can be a boolean (`'toggle'` \| `'button'`), a number (`'num'` \| `'button'`), a string in the case of `'text'`, `'button'` or the variants `'dropdown'` and `'radio'` of a `'selector'` type, or a [`custom_option_*`](#custom_option_) key array for the `'checkbox'` variant of `'selector'`.
<a name="variant">`customPropKey*.variant`</a> | | Used to modify the UI for a given prop `type`. For example, it can convert a numeric input to a slider input or a selector to a drop-down menu. The `value`s should remain the same structure, but the presentation to the end user changes.

## Prop `type`s and their `variant`s:

### `'head'`
Allows users to place a header for an individual section, containing a title (via [`name`](common_keys.md#name)) and a [`help`](#help) message. The [`value`](#value) key is not used with this type.

### `'text'`
Allows users to enter text in a UI field. Here, `value` takes a string.

### `'num'`
Allows users to enter a numeric value in a UI field. The `value` receives a numeric input that is formatted according to [`numberFormat`](number_format.md).
#### Variants:
>`'slider'`: Places a range of values along a bar, from which users may select a single value.<br>

### `'toggle'`
Allows to enable or disable the status of a single setting. Here, `value` receives a boolean value.

### `'button'`
Does not actually allow users to directly change a value. Instead,this allows users to trigger the `customPropKey*.apiCommand` on the server.

### `'selector'`
Allows end users to select options from a set. This `type` requires an array of dictionary objects for its [`value`](#value) key and a `variant` must be specified.
#### Variants:
>`'checkbox'`: Allows the user to select one or more items from a set of checkboxes.<br>
`'dropdown'`: Allows a compact way to display multiple options. The options appear upon interaction with an element (such as an icon or button) or when the user performs a specific action.<br>
`'radio'`: Allows the user to select one option from a set of mutually exclusive options.<br><br>
Since multiple selection is possible in the `'checkbox'` variant, one or more options in [`value`](#value) can be specified as a [`custom_option_*`](#custom_option_) key or [`custom_option_*`](#custom_option_) key array, respectively, while in the `dropdown` and `radio` variants, only one option is allowed to be present.

## Default `props` values and overriding
Very often, the `props` elements specified in [`arcs`](../all_keys/arcs.md), [`nodes`](../all_keys/nodes.md), and [`geos`](../all_keys/geos.md) are the same for a large number of items at the _data-point level_ ([customArcData*](../all_keys/arcs.md#arc-data-point), [customNodeData*](../all_keys/nodes.md#node-data-point) or [customGeoData*](../all_keys/geos.md#geo-data-point)). To reduce the overhead caused by duplicate `props` items and achieve a more lightweight data structure, it is possible to define a `props` dictionary at the _type level_ ([customArcType*](../all_keys/arcs.md#arc-type), [customNodeType*](../all_keys/nodes.md#node-type), or [customGeoType*](../all_keys/geos.md#geo-type)) so that a prop can be reused and overridden at the data-point level. In this case, two `props` items match by sharing the same [custom prop key](#customPropKey). The resulting prop from this match is a union of key-value pairs, where if a key exists in both `props` items, the value at the data-point level will be used.

## UI / UX tips
- When it comes to select multiple options from a set, you can save space by using `checkbox`es instead of on/off `toggle`s. However, if there is only one option, an on/off `toggle` is recommended instead.
- When a user is allowed to select only one option from a set, unless you need to expose all the available options with `radio`, you may consider using a `dropdown` instead, as it uses less space.
