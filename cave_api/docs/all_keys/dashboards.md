# `dashboards`
The `dashboards` key allows API designers to create custom dashboards for displaying charts and tables of statistics and kpi data. This key allows for default information and layout to be specified, as well as whether the dashboards can be edited by the user.

The structure of the `dashboards` group looks as follows:
```py
'dashboards': {
  'data': {
    "customDash1": {
      "dashboardLayout": [
          {
              "chart": "Bar",
              "grouping": "Average",
              "statistic": "numericStatExampleA",
          },
          {
              "chart": "Line",
              "grouping": "Sum",
              "statistic": "numericStatExampleB",
          },
          {
              "chart": "Bar",
              "level": "size",
              "category": "sku",
              "grouping": "Sum",
              "statistic": "numericExampleCalculationStat",
          },
          {
              "type": "kpis",
              "chart": "Bar",
              "grouping": "Sum",
              "sessions": [],
              "kpi": "key5",
          },
      ],
      "statOptions": [
        "numericExampleCalculationStat",
        "numericStatExampleB",
        "numericStatExampleA",
      ],
      "lockedLayout": False,
    },
  },
}
```
## Special and custom keys
Key | Default | Description
--- | ------- | -----------
`customDashKey.dashboardLayout` | `[]` | A list of chart items (max of 4 items currently supported) that belong to the current dashboard. Each chart item contains the following keys: `chart`, `grouping`, `statistic`, `category`, `level`, `type`, and `lockedLayout`.
`customDashKey.statOptions` | `[]` | A list of stat type keys that can be displayed in the charts on the dashboard. If the list is empty or no list is passed all stats are availible.
`customDashKey.dashboardLayout.*.*.category` | | The category selected from the "**Group By**" drop-down menu of a chart in a dashboard view. This key is different from the common key [`category`](../common_keys/common_keys.md#category).
`customDashKey.dashboardLayout.*.*.category2` | | The category selected from the "**Sub Group**" drop-down menu of a chart in a dashboard view. This uses the data resulting from "**Group By**" as input and allows you to further divide it based on the selected `category2` and [`level2`](#level2).
`customDashKey.dashboardLayout.*.*.chart` | | The chart type selected from the top-left drop-down menu of a chart in a dashboard view. The `chart` key sets the type of chart to one of these values: `'Bar'`,`'Stacked Bar'`,`'Line'`,`'Cumulative Line'`,`'Table'`,`'Box Plot'`,`'Waterfall'`,`'Stacked Waterfall'`,`'Sunburst'`
`customDashKey.dashboardLayout.*.*.grouping` | | A statistical or mathematical function selected by the user from a predefined set, to be applied over the data and rendered in a chart. It takes one of the following values: `'Sum'`, `'Average'`, `'Minimum'` or `'Maximum'`.
`customDashKey.dashboardLayout.*.*.kpi` | | The KPI key or the list of KPI keys selected from the "**KPIs**" drop-down of a chart in a dashboard view if chart `type='kpis'`.
`customDashKey.dashboardLayout.*.*.level` | | The second-level aggregation selected from the "**Group By**" drop-down menu of a chart in a dashboard view.
<a name="level2">`customDashKey.dashboardLayout.*.*.level2`</a> | | The second-level aggregation selected from the "**Sub Group**" drop-down menu of a chart in a dashboard view.
`customDashKey.dashboardLayout.*.*.lockedLayout` | `False` | A boolean to indicate if the layout on this chart can be changed by users.
`customDashKey.dashboardLayout.*.*.statistic` | | The statistic selected from the "**Statistic**" drop-down menu of a chart in a dashboard view if the chart `type='stats'`
`customDashKey.dashboardLayout.*.*.type` | `'stats'` | One of `'stats'`, `'maps'`, or `'kpis'`
`customDashKey.lockedLayout` | `False` | If `True`, prevents users from modifying the layout of a dashboard view by adding or removing charts.
`customDashKey.dashboardLayout.*.*.mapId` | | The map key to display in the chart item if `type='maps'`.

## Example

<details>
  <summary>Click here to show / hide example</summary>
  
```py
"dashboards": {
    "data": {
        "dash1": {
            "dashboardLayout": [
                {
                    "chart": "Bar",
                    "grouping": "Average",
                    "statistic": "numericStatExampleA",
                },
                {
                    "type": "kpis",
                    "chart": "Line",
                    "grouping": "Sum",
                    "sessions": [],
                    "kpi": ["key1", "key2"],
                },
                {
                    "chart": "Bar",
                    "level": "size",
                    "category": "sku",
                    "grouping": "Sum",
                    "statistic": "numericExampleCalculationStat",
                },
                {
                    "chart": "Stacked Waterfall",
                    "grouping": "Sum",
                    "statistic": "numericStatExampleA",
                    "category": "location",
                    "level": "state",
                    "category2": "sku",
                    "level2": "sku",
                },
            ],
            "lockedLayout": False,
        },
    }
},
```py
</details>

[`'Bar'`]: <https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-Y%20Axis=true&knob-vertical%20gridlines=true&knob-horizontal%20gridlines=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&selectedKind=Series%2FVerticalBarSeries%2FBase&selectedStory=multiple%20VerticalBarSeries%20-%20clustered&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs>
[`'Line'`]: https://uber.github.io/react-vis/website/dist/storybook/index.html?knob-X%20Axis=true&knob-BarSeries.1.cluster=stack%201&knob-BarSeries.2.cluster=stack%201&knob-BarSeries.3.cluster=stack%201&knob-vertical%20gridlines=true&knob-stroke=%2312939a&knob-horizontal%20gridlines=true&knob-opacity=1&knob-curve=curveBasis&knob-fill=%2312939a&knob-style=%7B%22stroke%22%3A%22%232c51be%22%2C%22strokeWidth%22%3A%223px%22%7D&knob-colorScale=category&knob-Y%20Axis=true&selectedKind=Series%2FLineSeries%2FBase&selectedStory=With%20negative%20numbers&full=0&addons=1&stories=1&panelRight=0&addonPanel=storybooks%2Fstorybook-addon-knobs
[`'Box Plot'`]: https://plotly.com/javascript/box-plots/