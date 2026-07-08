---
name: layout-design
description: Design and structure app layouts (grids, rows, columns, and containers) for custom panes and draggables using layout specifications.
---

# Designing Layouts in CAVE

CAVE custom panes and draggable elements rely on a structured layout configuration to position interactive components (props).

## Layout Structure

Layout definitions reside inside a pane or draggable definition under the `layout` key:

```python
"layout": {
    "type": "grid",
    "numColumns": 2,      # Renders a 2-column grid
    "numRows": "auto",    # Dynamically sizes rows
    "data": {
        "item_1": {"type": "item", "itemId": "prop_a", "column": 1, "row": 1},
        "item_2": {"type": "item", "itemId": "prop_b", "column": 2, "row": 1},
        "item_3": {"type": "item", "itemId": "prop_c", "column": 1, "row": 2, "columnSpan": 2}
    }
}
```

### Key Parameters:

| Attribute | Type | Description |
|---|---|---|
| `type` | `str` | Must be either `"grid"` (container) or `"item"` (leaf containing a prop). |
| `numColumns` | `str` \| `int` | Number of columns in a grid. Defaults to `"auto"`. |
| `numRows` | `str` \| `int` | Number of rows in a grid. Defaults to `"auto"`. |
| `itemId` | `str` | Used for `type="item"` to map layout to a prop key in the `props` dictionary. |
| `column` / `row` | `int` | 1-based index positioning the item inside its parent grid. |
| `style` | `dict` | CSS escape hatch (e.g. `{"padding": "10px"}`). |

## Common Layout Variants

1. **Simple Stack (Single Column):** Set `numColumns: 1` and `numRows: "auto"`. Items will stack vertically.
2. **Grid Matrix:** Explicitly coordinate items by assigning distinct `column` and `row` indices.
3. **Escaping Borders with Containers:** Customize `container` in the prop definitions:
   - `"vertical"`: Title on top, wrapped in an embossed box (default).
   - `"horizontal"`: Title on left, component on right.
   - `"none"`: Renders component directly without title/borders.

## Nested Grids (Subgrids)

Since a grid layout element can contain other layout elements, you can nest layout definitions to create complex dashboard structures. 

To define a nested grid, set the child element's `"type"` to `"grid"` and include a nested `"data"` block.

### Example: Nested Grid Definition

```python
"layout": {
    "type": "grid",
    "numColumns": 2,
    "numRows": 1,
    "data": {
        "left_item": {
            "type": "item",
            "itemId": "primary_toggle",
            "column": 1,
            "row": 1
        },
        "right_grid_column": {
            "type": "grid",
            "column": 2,
            "row": 1,
            "numColumns": 1,
            "numRows": 2,
            "data": {
                "top_subitem": {
                    "type": "item",
                    "itemId": "numeric_input_1",
                    "column": 1,
                    "row": 1
                },
                "bottom_subitem": {
                    "type": "item",
                    "itemId": "numeric_input_2",
                    "column": 1,
                    "row": 2
                }
            }
        }
    }
}
```

In this example, the main layout is split into two columns. The left column contains a single item (`primary_toggle`), while the right column contains a nested grid structure that arranges two sub-items (`numeric_input_1` and `numeric_input_2`) in a vertical stack.

