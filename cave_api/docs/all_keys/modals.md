## Modals
Similar to custom panes, modals can be used to place UI controls and buttons to allow interaction with actionable data. A modal appears as a dialogue box in the center of the screen. 

<details>
  <summary>Example modal</summary>

```py
"customModal": {
    "name": "Custom Modal",
    "props": {
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
        "dropdownItemExample": {
            "name": "Dropdown Item Example",
            "type": "selector",
            "variant": "dropdown",
            "value": ["option_c"],
            "options": {
                "option_a": {"name": "Option A"},
                "option_b": {"name": "Option B"},
                "option_c": {"name": "Option C"},
            },
            "enabled": True,
            "help": "Select an option from the dropdown",
        },
    },
    "layout": {
        "type": "grid",
        "numColumns": 2,
        "numRows": 2,
        "data": {
            "col1Row1": {
                "type": "item",
                "column": 1,
                "row": 1,
                "itemId": "toggleInputExample",
            },
            "col1Row2": {
                "type": "item",
                "column": 1,
                "row": 2,
                "itemId": "buttonInputExample",
            },
            "col2Row1": {
                "type": "item",
                "column": 2,
                "row": 1,
                "itemId": "numericSliderExample",
            },
            "col2Row2": {
                "type": "item",
                "column": 2,
                "row": 2,
                "itemId": "dropdownItemExample",
            },
        },
    },
},
```
</details>

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`layout`](../common_keys/common_keys.md#layout)
- [`name`](../common_keys/common_keys.md#name)
- [`order`](../common_keys/common_keys.md#order)
- [`prop > type`](../common_keys/common_keys.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`customModalKey*.props.customPropKey*` | | See [`customPropKey*`](../common_keys/props.md#customPropKey).
`customModalKey*.props.customPropKey*`&swarhk;<br>`.value.customOption*` | | See [`customOption*`](../common_keys/props.md#customOption).

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"modals": { 
    "data": {
        "exampleModal": {
            "name": "Example Modal",
            "props": {
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
                "dropdownItemExample": {
                    "name": "Dropdown Item Example",
                    "type": "selector",
                    "variant": "dropdown",
                    "value": ["option_c"],
                    "options": {
                        "option_a": {"name": "Option A"},
                        "option_b": {"name": "Option B"},
                        "option_c": {"name": "Option C"},
                    },
                    "enabled": True,
                    "help": "Select an option from the dropdown",
                },
            },
            "layout": {
                "type": "grid",
                "numColumns": 2,
                "numRows": 2,
                "data": {
                    "col1Row1": {
                        "type": "item",
                        "column": 1,
                        "row": 1,
                        "itemId": "toggleInputExample",
                    },
                    "col1Row2": {
                        "type": "item",
                        "column": 1,
                        "row": 2,
                        "itemId": "buttonInputExample",
                    },
                    "col2Row1": {
                        "type": "item",
                        "column": 2,
                        "row": 1,
                        "itemId": "numericSliderExample",
                    },
                    "col2Row2": {
                        "type": "item",
                        "column": 2,
                        "row": 2,
                        "itemId": "dropdownItemExample",
                    },
                },
            },
        },
    },
},
```
</details>
