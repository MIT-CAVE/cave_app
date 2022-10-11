#### The `layout` key

The `layout` key allows for use cases where you want to arrange components that are related or simply group them under a well-structured layout. The supported components for use with a layout structure are [props](#the-props-key) and [KPIs](#kpis). In addition to properly aligning a group of props or KPIs, a `style` prop is provided to act as a escape hatch for specifying CSS rules. Through these CSS rules, it is possible to modify the appearance of your prop components or KPIs and allows a way to make them more distinctive or visually appealing.

The `layout` structure is the same for `props` and `kpis` and looks as follows:
```py
'layout': {
    'type': 'grid',
    'num_columns': 2,
    'num_rows': 'auto',
    'data': {
        'col1_row1': {
            'type': 'item',
            'column': 1,
            'row': 1,
            'itemId': 'custom_prop_or_kpi_key_1'
        },
        'col2_row1': {
            'type': 'grid',
            'num_columns': 'auto',
            'num_rows': 1,
            'column': 2,
            'row': 1,
            'data': {
                'col1': {
                    'type': 'item',
                    'column': 1,
                    'itemId': 'custom_prop_or_kpi_key_2',
                },
                'col2': {
                    'type': 'item',
                    'column': 2,
                    'itemId': 'custom_prop_or_kpi_key_3',
                },
                'col3': {...},
                # As many columns as needed
            },
        },
        'col1_row2': {
            'type': 'item',
            'column': 1,
            'row': 2,
            'itemId': 'custom_prop_or_kpi_key_4'
        },
        'col2_row2': {
            'type': 'item',
            'column': 2,
            'row': 2,
            'itemId': 'custom_prop_or_kpi_key_5'
        },
        'col1_row3': {...},
        'col2_row3': {...},
        # As many two-column rows as needed
    },
}
```

##### Nested inside the `layout` group
Key | Default | Description
--- | ------- | -----------
<a name="layout-data">`*.data`</a> | `{}` | A wrapper for layout elements that are contained in a `'grid'` layout type.
<a name="layout-height">`*.height`</a> | `'auto'` | Sets the height of a layout element: `'grid'` or `'item'`. This property is an exact equivalent of the [CSS `height` property](https://developer.mozilla.org/en-US/docs/Web/CSS/height) and is a shortcut for the definition `style: { height: ... }`. Typical values are in [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) or [percentage](https://developer.mozilla.org/en-US/docs/Web/CSS/percentage) units, e.g. `'300px'`, `'80%'`, or `'20em'`. Other [valid formats](https://developer.mozilla.org/en-US/docs/Web/CSS/height#values) can be used, although they are rather uncommon for most use cases in CAVE App design.
<a name="layout-columns">`*.num_columns`</a> | `'auto'` | An integer for the number of columns or the keyword `'auto'`.
<a name="layout-rows">`*.num_rows`</a> | `'auto'` | An integer for the number of rows or the keyword `'auto'`.
<a name="layout-type">`*.type`</a> | Required | The type of layout. It can be `'grid'` or `'item'`.
<a name="layout-width">`*.width`</a> | `'auto'` | Sets the width of a layout element: `'grid'` or `'item'`. This property is an exact equivalent of the [CSS `width` property](https://developer.mozilla.org/en-US/docs/Web/CSS/width) and is a shortcut for the definition `style: { width: ... }`. Typical values are in [length](https://developer.mozilla.org/en-US/docs/Web/CSS/length) or [percentage](https://developer.mozilla.org/en-US/docs/Web/CSS/percentage) units, e.g. `'300px'`, `'80%'`, or `'20em'`. Other [valid formats](https://developer.mozilla.org/en-US/docs/Web/CSS/width#values) can be used, although they are rather uncommon for most use cases in CAVE App design.
<a name="layout-column">`layout.data.*.column`</a> | | An integer for the grid column position starting from left to right. If omitted, the layout element will fill the first empty grid element found within the specified [`row`](#layout-row), starting from left to right. If the [`row`](#layout-row) property is also omitted, the search sequence for empty slots can continue from top to bottom.<br><br>Note that if multiple sibling layout elements (i.e. sharing the same `data` parent) are missing `column` and/or `row` properties, the insert sequence between them will be determined by their wrapper key names in alphabetical order. <!-- TODO (0.3.0): See [example for layout elements with unspecified position](#). -->
<a name="layout-container">`layout.data.*.container`</a> | `'vertical'`<br><br>or<br><br> `'none'`<br>(only for the [`head`](#head) prop) | A UI wrapper that modifies the appearance of an item by adding a title based on its [`name`](#name), a [`help`](#help) tooltip, and adjusting the position and size of its input controls. Available options are `'vertical'`, `'horizontal'`, `'titled'` and `'none'`. By default, the [`'head'`](#head) prop is set to have a `'none'` container.<br><br>This feature is currently only supported for [`props`](#the-props-key).
<a name="elevation">`layout.data.*.elevation`</a> | `1` | Used in conjunction with a [`container`](#layout-container) definition, `elevation` controls the size of the shadow applied to the surface to visually differentiate or highlight the item from others of the same container type. Possible values are `0` to `24`.
<a name="layout-item-id">`layout.data.*.itemId`</a> | | The ID of a prop or KPI item to be placed in a specific position within the layout. This property is required by a layout element of type `'item'`.
<a name="marquee">`layout.data.*.marquee`</a> | `False`<br><br>or<br><br> `True`<br>(only for [`'horizontal'` `container`](#layout-container)s) | Used in conjunction with a [`container`](#layout-container) definition, `marquee` sets the behavior of the container title so that, if `True`, the title is displayed as a marquee when the length of the title exceeds its reserved width in the container; otherwise, the title wraps vertically. Unless set to `False`, a `'horizontal'` `container` has `marquee` enabled by default.
<a name="layout-row">`layout.data.*.row`</a> | | An integer for the grid row position starting from top to bottom. If omitted, the layout element will fill the first empty grid element found within the specified [`column`](#layout-column), starting from top to bottom. If the [`column`](#layout-column) property is also omitted, the search sequence for empty slots will start from left to right and continue from top to bottom.<br><br>Note that if multiple sibling layout elements (i.e. sharing the same `data` parent) are missing `column` and/or `row` properties, the insert sequence between them will be determined by their wrapper key names in alphabetical order. <!-- TODO (0.3.0): See [example for layout elements with unspecified position](#). -->
<a name="layout-style">`layout.data.*.style`</a> | `{}` | A dictionary object containing [CSS styles](https://developer.mozilla.org/en-US/docs/Web/CSS) to apply to a layout element of type `'item'`.

#### Examples
To better illustrate various use cases for a `'grid'` layout, we will rely on the same `props` structure, shown below:

```py
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
}
```

##### By number of rows and columns
The following are different layout configurations based on the outer number of rows and columns, as well as different interior layout arrangements, contained in an [`options` pane](#panes):

###### Fixed number of columns and rows
In this example, all elements are explicitly positioned within the layout. This is the recommended approach for most cases.

<details>
  <summary>Click here to show / hide example</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 3,
    'num_rows': 4,
    'data': {
        'col1_row1': {
            'type': 'item',
            'itemId': 'solver_section',
            'column': 1,
            'row': 1,
        },
        'col1_row2': {
            'type': 'item',
            'itemId': 'Solver',
            'column': 1,
            'row': 2,
        },
        'col2_row1': {
            'type': 'item',
            'itemId': 'optimality_section',
            'column': 2,
            'row': 1,
        },
        'col2_row2': {
            'type': 'item',
            'itemId': 'Pct_Optimal',
            'column': 2,
            'row': 2,
        },
        'col3_row1': {
            'type': 'item',
            'itemId': 'distance_section',
            'column': 3,
            'row': 1,
        },
        'col3_row2': {
            'type': 'item',
            'itemId': '50_miles',
            'column': 3,
            'row': 2,
        },
        'col3_row3': {
            'type': 'item',
            'itemId': '100_miles',
            'column': 3,
            'row': 3,
        },
        'col3_row4': {
            'type': 'item',
            'itemId': '150_miles',
            'column': 3,
            'row': 4,
        },
    },
}
```

The visual result in the CAVE App is as follows:

![fixed-number-of-columns-and-rows](https://utils.mitcave.com/docs/cave_app-0.1.0/fixed-number-of-columns-and-rows.png)

</details>

###### Single-column
In this example, all items are arranged in a single column. Although the number of  rows are known, the `'auto'` feature helps you save time and effort when the number of items changes. Also, note that [`num_rows`](#layout_rows) is set to `'auto'` by default; However, it is recommended that you specify it explicitly in the layout to improve your code readability.

<details>
  <summary>Click here to show / hide example</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 1,
    'num_rows': 'auto',
    'data': {
        'solver_section': {
            'row': 1,
            'type': 'item',
            'itemId': 'solver_section',
        },
        'solver': {
            'row': 2,
            'type': 'item',
            'itemId': 'Solver',
        },
        'optimality_section': {
            'row': 3,
            'type': 'item',
            'itemId': 'optimality_section',
        },
        'pct_optimal': {
            'row': 4,
            'type': 'item',
            'itemId': 'Pct_Optimal',
        },
        'distance_section': {
            'row': 5,
            'type': 'item',
            'itemId': 'distance_section',
        },
        '50_miles': {
            'row': 6,
            'type': 'item',
            'itemId': '50_miles',
        },
        '100_miles': {
            'row': 7,
            'type': 'item',
            'itemId': '100_miles',
        },
        '150_miles': {
            'row': 8,
            'type': 'item',
            'itemId': '150_miles',
        },
    },
}
```

The visual result in the CAVE App is as follows:

![single-column](https://utils.mitcave.com/docs/cave_app-0.1.0/single-column.png)
</details>

###### Single-row
In this example, all items are arranged in a single row. Like in the previous example, the `'auto'` feature helps you save time and effort when the number of items changes. The [`num_columns`](#layout-columns) is set to `'auto'` by default, but it is recommended that you specify it explicitly in the layout to improve your code readability.

<details>
  <summary>Click here to show / hide example</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 'auto',
    'num_rows': 1,
    'data': {
        'column1': {
            'column': 1,
            'type': 'item',
            'itemId': 'solver_section',
        },
        'column2': {
            'column': 2,
            'type': 'item',
            'itemId': 'Solver',
        },
        'column3': {
            'column': 3,
            'type': 'item',
            'itemId': 'optimality_section',
        },
        'column4': {
            'column': 4,
            'type': 'item',
            'itemId': 'Pct_Optimal',
        },
        'column5': {
            'column': 5,
            'type': 'item',
            'itemId': 'distance_section',
        },
        'column6': {
            'column': 6,
            'type': 'item',
            'itemId': '50_miles',
        },
        'column7': {
            'column': 7,
            'type': 'item',
            'itemId': '100_miles',
        },
        'column8': {
            'column': 8,
            'type': 'item',
            'itemId': '150_miles',
        },
    },
}
```
The visual result in the CAVE App is as follows:

![single-row](https://utils.mitcave.com/docs/cave_app-0.1.0/single-row.png)
</details>

###### Fixed number of columns
In this example, a fixed number of columns has been set, letting the CAVE App estimate the number of rows needed to contain the items specified in the layout. One possible use case is when two or more sections are clearly defined and should be kept as [`'head'`](#head)ers in the first row of the layout. Here, the rest of the items will be arranged to fill in the layout with their positions determined by their explicitly set [`column`](#layout-column)s or [`row`](#layout-row)s, or based on the `layout_key_*` names assigned to them.

As in the previous examples, the `'auto'` feature helps you save time and effort when the number of items changes but the number of columns is known to be fixed. Keeping [`num_rows`](#layout-rows) explicitly set to `'auto'` is a good practice to improve your code readability.

<details>
  <summary>Click here to show / hide example</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 2,
    'num_rows': 'auto',
    'data': {
        'layout_key_1': {
            'type': 'item',
            'itemId': 'solver_section',
            'column': 1,
        },
        'layout_key_2': {
            'type': 'item',
            'itemId': 'Solver',
            'column': 1,
        },
        'layout_key_3': {
            'type': 'item',
            'itemId': 'optimality_section',
            'column': 1,
        },
        'layout_key_4': {
            'type': 'item',
            'itemId': 'Pct_Optimal',
            'column': 1,
        },
        'layout_key_5': {
            'type': 'item',
            'itemId': 'distance_section',
            'column': 2,
        },
        'layout_key_6': {
            'type': 'item',
            'itemId': '50_miles',
            'column': 2,
        },
        'layout_key_7': {
            'type': 'item',
            'itemId': '100_miles',
            'column': 2,
        },
        'layout_key_8': {
            'type': 'item',
            'itemId': '150_miles',
            'column': 2,
        },
    },
}
```
The visual result in the CAVE App is as follows:

![fixed-number-of-columns](https://utils.mitcave.com/docs/cave_app-0.1.0/fixed-number-of-columns.png)
</details>

###### Fixed number of rows
In this example, a fixed number of rows has been set, letting the CAVE App estimate the number of columns needed to contain the items specified in the layout. As in the previous examples, the `'auto'` feature helps you save time and effort when the number of items changes but the number of rows is known to be fixed. Keeping [`num_columns`](#layout-columns) explicitly set to `'auto'` is a good practice to improve your code readability.

<details>
  <summary>Click here to show / hide example</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 'auto',
    'num_rows': 2,
    'data': {
        'layout_key_1': {
            'type': 'item',
            'itemId': 'solver_section',
            'row': 1,
        },
        'layout_key_2': {
            'type': 'item',
            'itemId': 'Solver',
        },
        'layout_key_3': {
            'type': 'item',
            'itemId': 'optimality_section',
            'row': 1,
        },
        'layout_key_4': {
            'type': 'item',
            'itemId': 'Pct_Optimal',
        },
        'layout_key_5': {
            'type': 'item',
            'itemId': 'distance_section',
            'row': 1,
        },
        'layout_key_6': {
            'type': 'item',
            'itemId': '50_miles',
        },
        'layout_key_7': {
            'type': 'item',
            'itemId': '100_miles',
        },
        'layout_key_8': {
            'type': 'item',
            'itemId': '150_miles',
        },
    },
}
```
The visual result in the CAVE App is as follows:

![fixed-number-of-rows](https://utils.mitcave.com/docs/cave_app-0.1.0/fixed-number-of-rows.png)
</details>

###### Auto-grid (or unspecified number of rows and columns)
In this example, the number of rows and columns is unknown. Here, the CAVE App will estimate the number of rows and columns closest to a square-shaped grid needed to contain the elements specified in the layout. While this may be fairly uncommon, one possible use case is when two or more items that don't follow any logical order, need to be held together.

As in the previous examples, the `'auto'` feature helps you save time and effort if the number of these grouped items changes. Setting both [`num_columns`](#layout-columns) and [`num_rows`](#layout-rows) to `'auto'` is still a good practice to improve your code readability.

The _auto-grid_ rendering is also triggered when the `layout` property is empty or has not been specified along a [`props`](#the-props-key) or [`kpis`](#kpis) structure.

<details>
  <summary>Click here to show / hide example</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 'auto',
    'num_rows': 'auto',
    'data': {
        'layout_key_1': {
            'type': 'item',
            'itemId': 'solver_section',
            'row': 1,
            'column': 1,
        },
        'layout_key_2': {
            'type': 'item',
            'itemId': 'Solver',
        },
        'layout_key_3': {
            'type': 'item',
            'itemId': 'optimality_section',
            'row': 1,
            'column': 2,
        },
        'layout_key_4': {
            'type': 'item',
            'itemId': 'Pct_Optimal',
        },
        'layout_key_5': {
            'type': 'item',
            'itemId': 'distance_section',
            'row': 1,
            'column': 3,
        },
        'layout_key_6': {
            'type': 'item',
            'itemId': '50_miles',
        },
        'layout_key_7': {
            'type': 'item',
            'itemId': '100_miles',
        },
        'layout_key_8': {
            'type': 'item',
            'itemId': '150_miles',
        },
    },
}
```
</details>

<!-- TODO (0.3.0):
##### By different values of [`column`](#layout-column) and [`row`](#layout-row)

<details>
  <summary>Unspecified `row`</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 1,
    'num_rows': 'auto',
    'data': {
        'row1': {
            'type': 'item',
            'itemId': 'solver_section',
        },
        'row2': {
            'type': 'item',
            'itemId': 'Solver',
        },
        'row3': {
            'type': 'item',
            'itemId': 'optimality_section',
        },
        'row4': {
            'type': 'item',
            'itemId': 'Pct_Optimal',
        },
        'row5': {
            'type': 'item',
            'itemId': 'distance_section',
        },
        'foo': {
            'type': 'item',
            'itemId': '50_miles',
        },
        'bar': {
            'type': 'item',
            'itemId': '100_miles',
        },
        'baz': {
            'type': 'item',
            'itemId': '150_miles',
        },
    },
}
```
</details>

<details>
  <summary>Unspecified `column`</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 1,
    'num_rows': 'auto',
    'data': {
        'row1': {
            'type': 'item',
            'itemId': 'solver_section',
        },
        'row2': {
            'type': 'item',
            'itemId': 'Solver',
        },
        'row3': {
            'type': 'item',
            'itemId': 'optimality_section',
            'row': 3,
        },
        'row4': {
            'type': 'item',
            'itemId': 'Pct_Optimal',
            'row': 4,
        },
        'row5': {
            'type': 'item',
            'itemId': 'distance_section',
            'row': 5,
        },
        'foo': {
            'type': 'item',
            'itemId': '50_miles',
        },
        'bar': {
            'type': 'item',
            'itemId': '100_miles',
        },
        'baz': {
            'type': 'item',
            'itemId': '150_miles',
        },
    },
}
```
</details>

<details>
  <summary>Unspecified `row`s and `column`s</summary>

```py
'layout': {
    'type': 'grid',
    'num_columns': 3,
    'num_rows': 3,
    'data': {
        'layout_key_1': {
            'type': 'item',
            'itemId': 'solver_section',
        },
        'layout_key_2': {
            'type': 'item',
            'itemId': 'Solver',
        },
        'layout_key_3': {
            'type': 'item',
            'itemId': 'optimality_section',
        },
        'layout_key_4': {
            'type': 'item',
            'itemId': 'Pct_Optimal',
        },
        'layout_key_5': {
            'type': 'item',
            'itemId': 'distance_section',
        },
        'layout_key_6': {
            'type': 'item',
            'itemId': '50_miles',
        },
        'layout_key_7': {
            'type': 'item',
            'itemId': '100_miles',
        },
        'layout_key_8': {
            'type': 'item',
            'itemId': '150_miles',
        },
    },
}
```
</details>

##### UI / UX tips
-->
