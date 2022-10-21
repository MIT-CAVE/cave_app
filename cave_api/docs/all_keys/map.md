### `map`
This key group allows designers to specify information about the starting state of the map, what information is contained and how it is grouped in the legend, and what viewports can be easily jumped to by the user.

Below is the `map` group with its sub-keys matched by typical or placeholder values:
```py
'map': {
    'name': 'map',
    'data':{
        'enabledArcTypes': {'arc': {'T1': True}},
        'defaultViewport': {
            'longitude': -75.44766721108091,
            'latitude': 40.34530681636297,
            'zoom': 4.657916626867326,
            'pitch': 0,
            'bearing': 0,
            'height': 1287,
            'altitude': 1.5,
            'maxZoom': 12,
            'minZoom': 2
        },
        'optionalViewports': {
            'ov0': {
                'icon': 'FaGlobeAsia',
                'name': 'Asia',
                'zoom': 4,
                'order': 1,
                'pitch': 0,
                'bearing': 0,
                'maxZoom': 12,
                'minZoom': 2,
                'latitude': 30,
                'longitude': 121
            },
        },
        'legendGroups': [
            {
                'name': 'DC Delivery',
                'nodeTypes': ['DC'],
                'arcTypes': ['T1'],
                'geoTypes': ['state', 'country']
            }
        ],
    },
}
```

##### Common keys
- [`allow_modification`](../common_keys/common_keys.md#allow_modification)
- [`data`](../common_keys/common_keys.md#data)
- [`icon`](../common_keys/common_keys.md#icon)
- [`name`](../common_keys/common_keys.md#name)
- [`send_to_api`](../common_keys/common_keys.md#send_to_api)
- [`send_to_client`](../common_keys/common_keys.md#send_to_client)

##### Special and custom keys
Key | Default | Description
--- | ------- | -----------
<a name="defaultViewport">`defaultViewport`</a> | | A dictionary object containing geo properties that set the map's default field of view. Also used by the "home" button in the app.
`defaultViewport.bearing` | `0` | The initial bearing (rotation) of the map, measured in degrees counter-clockwise from north.
`defaultViewport.pitch` | `0` | The initial pitch (*tilt*) of the viewport in the "**Map**" view, measured in degrees away from the plane of the screen (0&deg; - 85&deg;). A pitch of 0&deg; results in a two-dimensional map, as if your line of sight forms a perpendicular angle with the earth's surface, while a greater value like 60&deg; looks ahead towards the horizon.
`defaultViewport.latitude` | `42.36157` | The center latitude of the viewport in the "**Map**" view. It takes a float value.
`defaultViewport.longitude` | `-71.08463` | The center longitude of the viewport in the "**Map**" view. It takes a float value.
`defaultViewport.maxZoom` | `22` | The maximum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`defaultViewport.minZoom` | `1.5` | The minimum zoom level of the viewport in the "**Map**" view. It takes an integer value.
`defaultViewport.zoom` | `13` | The initial zoom level of the viewport in the "**Map**" view. It takes an integer value. Learn more about the zoom levels [here](#https://docs.mapbox.com/help/glossary/zoom-level/).
<a name="enabledTypes">`enabledTypes`</a> | `{}` | A wrapper for the [`arc`](#arc), [`node`](#node), and [`geo`](#geo) keys, each of which matches the respective layer type ([arc type](arcs.md#arc-type), [node type](nodes.md#node-type), or [geo type](geos.md#geo-type)) with a boolean indicating whether the layer type should be visualized in the "**Map**" view or not. The initial states of the boolean values are displayed accordingly in the map legend and can be toggled by the user.
<a name="arc">`enabledTypes.arc`</a> | | A dictionary object containing [arc types](arcs.md#arc-type) as keys mapped to boolean values to enable or disable the visualization of arc types in the "**Map**" view.
<a name="node">`enabledTypes.node`</a> | | A dictionary object containing [node types](nodes.md#node-type) as keys mapped to boolean values to enable or disable the visualization of node types in the "**Map**" view.
<a name="geo">`enabledTypes.geo`</a> | | A dictionary object containing [geo types](geos.md#geo-type) as keys mapped to boolean values to enable or disable the visualization of geo types in the "**Map**" view.
<a name="optionalViewports">`optionalViewports`</a> | | A dictionary of optional viewports that can be jumped to by users. Each optional viewport should contain the same keys as `defaultViewport` as well as `name` and `icon` keys.
<a name="legendGroups">`legendGroups`</a> | `[]` | A list of all groupings to be shown in the map legend. Groups are displayed in list order with each group having an internal order of `nodes`, `arcs`, then `geos`. Types not included in any legend group cannot be toggled.
`legendGroups[i].nodeTypes` | | A list of all node types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`legendGroups[i].arcTypes` | | A list of all arc types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
`legendGroups[i].geoTypes` | | A list of all geo types to include in the legend group. Note that settings (`colorBy`, `sizeBy`) are syncronized across the same type in multiple groups.
