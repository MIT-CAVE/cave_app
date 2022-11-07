#### The `props` key
We dedicate a section to the `props` group, as it handles all of the user input controls, as well as most of the textual or numeric output in the CAVE App. Let's start with an in-depth look at its internal structure and how it translates to the UI.

```py
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
        'value': [
            {'name':'custom_option_1', 'value': False},
            {'name':'custom_option_2', 'value': True},
            {'name':'custom_option_3', 'value': False},
        ],
        'help': 'A help text for the dropdown selector',
    },
    # As many props as needed
}
```

##### Nested inside the `props` group
Aside from [`name`](common_keys.md#name) and [`order`](common_keys.md#order) all the keys and values in the above structure are specific to the `props` group and therefore explained below:

Key | Default | Description
--- | ------- | -----------
<a name="custom_prop_key_">`custom_prop_key_*`</a> | | A custom key wrapper for a `props` item.
<a name="apiCommand">`custom_prop_key_*.apiCommand`</a> | | If specified, passes an api command argument along with a mutation request. This command will be passed to `execute_command` for each session to be synced.
<a name="apiCommandKeys">`custom_prop_key_*.apiCommandKeys`</a> | | If specified, only passes specific session keys over to `execute_command` for each session to be synced.
<a name="enabled">`custom_prop_key_*.enabled`</a> | `False` | Enable a `props` element in the UI. If `False`, users cannot interact with the element in the UI.
<a name="help">`custom_prop_key_*.help`</a> | | A help message that is displayed in the UI, as a result of a mouseover or touch event on a `custom_prop_key_*` element.
<a name="label">`custom_prop_key_*.label`</a> | | A label that is displayed in the UI next to the `custom_prop_key_*` element.
<a name="max-value">`custom_prop_key_*.maxValue`</a> | | Used along a `'num'` prop, it takes the maximum allowed value of the numeric input. Should not be equal to `minValue`.
<a name="min-value">`custom_prop_key_*.minValue`</a> | | Used along a `'num'` prop, it takes the minimum allowed value of the numeric input. Should not be equal to `maxValue`.
<a name="prop-type">`custom_prop_key_*.type`</a> | Required | As a direct child of `custom_prop_key_*`, the `type` key sets the UI element type, implicitly constraining the set of key-value pairs that can be used along this type. The `type` key takes one of the following values: `'head'`, `'text'`, `'num'`, `'toggle'`, or `'selector'`.
<a name="value">`custom_prop_key_*.value`</a> | Required | The actual value for a `props` element. Depending on the prop [`type`](#prop-type), it can be a boolean (`'toggle'`), number (`'num'`), string (`'text'`), or an array of objects (`'selector'`).
<a name="custom_option_">`custom_prop_key_*.value.custom_option_*`</a> | | Used along a `'selector'` prop, it takes a string value to be displayed as an option on the UI element.
<a name="variant">`custom_prop_key_*.variant`</a> | | Used to modify the UI for a given prop `type`. For example, it can convert a numeric input to a slider input or a selector to a drop-down menu. The `value`s should remain the same structure, but the presentation to the end user changes.

##### Prop `type`s and their `variant`s:

##### `'head'`
Allows users to place a header for an individual section, containing a title (via [`name`](common_keys.md#name)) and a [`help`](#help) message. The [`value`](#value) key is not used with this type.

##### `'text'`
Allows users to enter text in a UI field. Here, `value` takes a string.

##### `'num'`
Allows users to enter a numeric value in a UI field. The `value` receives a numeric input that is formatted according to [`numberFormat`](number_format.md).
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

##### Default `props` values and overriding
Very often, the `props` elements specified in [`arcs`](../all_keys/arcs.md), [`nodes`](../all_keys/nodes.md), and [`geos`](../all_keys/geos.md) are the same for a large number of items at the _data-point level_ ([custom_arc_data_*](../all_keys/arcs.md#arc-data-point), [custom_node_data_*](../all_keys/nodes.md#node-data-point) or [custom_geo_data_*](../all_keys/geos.md#geo-data-point)). To reduce the overhead caused by duplicate `props` items and achieve a more lightweight data structure, it is possible to define a `props` dictionary at the _type level_ ([custom_arc_type_*](../all_keys/arcs.md#arc-type), [custom_node_type_*](../all_keys/nodes.md#node-type), or [custom_geo_type_*](../all_keys/geos.md#geo-type)) so that a prop can be reused and overridden at the data-point level. In this case, two `props` items match by sharing the same [custom prop key](#custom_prop_key_). The resulting prop from this match is a union of key-value pairs, where if a key exists in both `props` items, the value at the data-point level will be used.

##### UI / UX tips
- When it comes to select multiple options from a set, you can save space by using `checkbox`es instead of on/off `toggle`s. However, if there is only one option, an on/off `toggle` is recommended instead.
- When a user is allowed to select only one option from a set, unless you need to expose all the available options with `radio`, you may consider using a `dropdown` instead, as it uses less space.
