## Panes
Panes are constructs primarily used to place UI controls (toggles, text and number fields, sliders, etc.), as well as buttons to allow interaction with actionable data. Custom panes can be designed to enable users to tune up the parameters of a simulation, navigate through different case study scenarios, reset the state of a simulation, synchronize data or settings with other users, and so on.

Panes can be of different [`variant`](#pane-variant)s, so to keep the data structure examples simple and modular, you can examine each one at a time in the following switchables:

<details>
  <summary>App Settings pane</summary>

```py
"appSettings": {
    "variant": "appSettings",
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
            "precision": 0,
            "unit": "units",
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
            "value": ["option_c"],
            "options": {
                "option_a": {"name": "Option A"},
                "option_b": {"name": "Option B"},
                "option_c": {"name": "Option C"},
            },
            "enabled": True,
            "help": "Select an option from the dropdown",
        },
        "checkboxItemExample": {
            "name": "Checkbox Item Example",
            "type": "selector",
            "variant": "checkbox",
            "value": ["option_a", "option_c"],
            "options": {
                "option_a": {"name": "Option A"},
                "option_b": {"name": "Option B"},
                "option_c": {"name": "Option C"},
            },
            "enabled": True,
            "help": "Select all relevant items",
        },
        "radioItemExample": {
            "name": "Radio Item Example",
            "type": "selector",
            "variant": "radio",
            "value": ["option_a"],
            "options": {
                "option_a": {"name": "Option A"},
                "option_b": {"name": "Option B"},
                "option_c": {"name": "Option C"},
            },
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
    "variant": "options",
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
    "variant": "context",
},
```

Extra Information:

Context panes can be used to create a list of contexts which can be applied to a model.

A context represents a prop applied to a set of [`category`](../all_keys/categories.md)s.
    - `applyCategories`: Determines which category items this context should be applied to.
        - Note: Only category items from categories listed in `selectableCategories` (based on the selected prop) can be applied to this context.
    - `prop`: Used to determine which prop the current context is altering.
    - `value`: Used to determine the value of the prop for this context.

To create a UI for a context pane, a `prop` key must be specified in the `props` section of the pane. 
    - The following prop `type`s are supported:
        - `num` Numeric inputs 
        - `head`: Will createa prop with no inputs. This is great to simplify contexts where no value is required, but a context is still needed.
    - Within each prop, a special `selectableCategories` key must be specified. This key takes a list of category keys (**only**). These are the used to determine which categories this context can be applied to.

Notes:
    - Any data in the `context` pane is required to be handled fully by the API designer.
    - N contexts can be created by the user, so the API designer should be able to handle N contexts.
        - EG: Assume users want to apply a 10% price increase to all `sku`s at all `location`s, but also want to apply a 5% price decrease to all `sku`s at `location` `locUsMi`.
            - Option 1: (Recommended) The API designer should apply the 10% price increase to all `sku`s at all `location`s, and then apply a 5% price decrease to all `sku`s at `location` `locUsMi`.
            - Option 2: The API designer would choose to take precenence for the last context applied. In this case, the API designer would apply the 5% price decrease to all `sku`s at `location` `locUsMi`, and then apply a 10% price increase to all `sku`s at all `location`s not in `location` `locUsMi`.

Example Ideas:

Consider an app that handles information for products (skus) and locations at which they are sold.
The API designer wants to allow users to modify the price of each sku at each location.

Option 1:
    - Create a `geos` layer where each location gets its own geo, and each geo has the price of every sku.
    - End users could then click on each geo and modify the price of each sku at that location.
    - Asssuming that there are 300 locations and the user wants to bump up sku prices at each location by 10%, the user would have to click on each location and modify each sku's price by 10%.
    - This would take the user over 1200 clicks and a lot of frustration to complete (at a minimum)

Option 2:
    - Create a `context` pane with a prop for percent price modification that can apply to the `sku` and `location` categories.
    - End users could then add a context (selecting price modification), setting the value to 10%, select the all button for the `location` category and finally select the `sku` they want to modify.
    - This would take the user ~10 clicks and would be much less frustrating to complete (and far easier to understand)
- On the API side, the designer would need to apply the context (percent price modification) to all the selected `sku`s/`location`s on an API command.
    - In general, API designers should aim to keep this context in place and apply during API command execution.
        - Think of this as a "sticky" context that is applied to the selected `sku`s/`location`s until the user chooses to remove it.
    - There are also use cases where API designers might choose to apply the context to the selected `sku`s/`location`s, save their state and clear out the context pane after some command is executed.
        - Think of this as a "one time" context that is applied to the selected `sku`s/`location`s and can not be removed.


</details>

<details>
  <summary>Filter pane</summary>

```py
"filter": {
    "variant": "filter",
},
```
</details>

<details>
  <summary>Session pane</summary>

```py
"CustomSessionPane": {
    "name": "Sessions",
    "variant": "session",
},
```
</details>

## Common keys
- [`allowModification`](../common_keys/common_keys.md#allowModification)
- [`layout`](../common_keys/common_keys.md#layout)
- [`name`](../common_keys/common_keys.md#name)
- [`order`](../common_keys/common_keys.md#order)
- [`precision`](../common_keys/common_keys.md#precision)
- [`prop > type`](../common_keys/common_keys.md#prop-type)
- [`props`](../common_keys/common_keys.md#props-short)
- [`sendToApi`](../common_keys/common_keys.md#sendToApi)
- [`sendToClient`](../common_keys/common_keys.md#sendToClient)
- [`unit`](../common_keys/common_keys.md#unit)
- [`variant`](../common_keys/common_keys.md#variant)

## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`customContextPaneKey*.data.customContextData*` | | This represents the data structure created by the client to store each context in a list of contexts. Initial values can be provided by the API designer if needed.
`customContextPaneKey*.data.customContextData*`&swarhk;<br>`.applyCategories` | | Used **only** with a [`context`](#context-pane) pane, it takes a dictionary of [`category`](../all_keys/categories.md)s, each of which is paired with a partial list of its [`customDataChunck*`](../all_keys/categories.md#customDataChunck) keys. This data is normally generated by user interactions as they build out contexts and returned to the API when an `apiCommand` is triggered. Initial values can be provided by the API designer if needed.
`customContextPaneKey*.data.customContextData*`&swarhk;<br>`.applyCategories.category*.customDataChunck*` | | See [`customDataChunck*`](../all_keys/categories.md#customDataChunck).
`customContextPaneKey*.data.customContextData*`&swarhk;<br>`.prop` | | Used in the `data` portion of a [`context`](#context-pane) pane to note which prop the current context is altering. Takes a `customPropKey*`.
`customPaneKey*.props.customPropKey*` | | See [`customPropKey*`](../common_keys/props.md#customPropKey).
`customPaneKey*.props.customPropKey*`&swarhk;<br>`.value.customOption*` | | See [`customOption*`](../common_keys/props.md#customOption).
`customContextPaneKey*.props.customPropKey*`&swarhk;<br>`.selectableCategories` | Required | Used in a [`context`](#context-pane) pane, it takes a list of [`category_*`](#category_) keys (**only**). These are the used to determine which categories this context can be applied to.
`customPaneKey*.teamSync` | `False` | If `True`, creates a sync button on the top of the pane. When that sync button is clicked, everything in that pane is synced across all sessions for that team (or user if individual session) such that all other sessions for that team have the exact same pane as it exists in the current session.
`customPaneKey*.teamSyncCommand` | | If specified, passes an API command argument along with a mutation request. This command will be passed to `execute_command` for each session to be synced.
`customPaneKey*.teamSyncCommandKeys` | | If specified, only passes specific session keys over to `execute_command` for each session to be synced.
<a name="pane-variant">`customPaneKey*.variant`</a> | `'options'` | As a direct child of `customPaneKey*`, the `variant` key is used to determine the pane variant. Each variant comes along with additional keys that add specific functionality to the pane. Acceptable values inclue `session`, `appSettings`, `options`, `context`, `filter`
`customPaneKey*.width` | `'auto'` | Sets the width of the pane. This property is an exact equivalent of the [CSS `width` property](https://developer.mozilla.org/en-US/docs/Web/CSS/width). If set to `'auto'`, the pane will stretch to fit its content with a width no less than `'450px'`. If the specified width exceeds the width of the viewport, the pane will match the width of the viewport.
<!-- `paneState.open` | | Takes a `customPaneKey*` value to cause the referenced pane to open when the app loads. -->
<!-- `filtered` | `{}` | Takes key value pairs where the keys are category keys, and the values are lists of lowest level items in that category to be included (not filtered out). If a category is not included in this dictionary then all items in that category are displayed. -->

## Example

<details>
  <summary>Click here to show / hide example</summary>

```py
"panes": {
    "data": {
        "session": {
            "variant": "session",
            "name": "Session",
        },
        "appSettings": {
            "variant": "appSettings",
        },
        "examplePropsPane": {
            "name": "Example Props Pane",
            "variant": "options",
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
                    "precision": 0,
                    "unit": "units",
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
                    "value": ["option_c"],
                    "options": {
                        "option_a": {"name": "Option A"},
                        "option_b": {"name": "Option B"},
                        "option_c": {"name": "Option C"},
                    },
                    "enabled": True,
                    "help": "Select an option from the dropdown",
                },
                "checkboxItemExample": {
                    "name": "Checkbox Item Example",
                    "type": "selector",
                    "variant": "checkbox",
                    "value": ["option_a", "option_c"],
                    "options": {
                        "option_a": {"name": "Option A"},
                        "option_b": {"name": "Option B"},
                        "option_c": {"name": "Option C"},
                    },
                    "enabled": True,
                    "help": "Select all relevant items",
                },
                "radioItemExample": {
                    "name": "Radio Item Example",
                    "type": "selector",
                    "variant": "radio",
                    "value": ["option_a"],
                    "options": {
                        "option_a": {"name": "Option A"},
                        "option_b": {"name": "Option B"},
                        "option_c": {"name": "Option C"},
                    },
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
        },
        "filter": {
            "name": "Filter",
            "variant": "filter",
        },
        "context": {
            "name": "Context Pane",
            "variant": "context",
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
        },
    },
},
```
</details>
