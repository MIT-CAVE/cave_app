def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            "data": {
                # Icon Url is used to load icons from a custom icon library
                # See the available versions provided by the cave team here:
                # https://react-icons.mitcave.com/versions.txt
                # Once you select a version, you can see the available icons in the version
                # EG: https://react-icons.mitcave.com/4.10.1/icon_list.txt
                "iconUrl": "https://react-icons.mitcave.com/4.10.1",
            },
        },
        "appBar": {
            "appBarId": "mapDashboard",
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": ["refreshButton", "mapDashboard"],
            },
            "data": {
                # Add a simple button to the app bar to trigger the `init` command
                # This is useful for resetting the app to its initial state
                "refreshButton": {
                    "icon": "md/MdRefresh",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                },
                # Add a pane button to launch a map focused dashboard
                "mapDashboard": {
                    "icon": "md/MdMap",
                    "type": "page",
                    "bar": "upperLeft",
                },
            },
        },
        "maps": {
            # Specify the order of map style items as they will appear in the style selector
            "order": {
                "additionalMapStyles": ["mapboxDark", "cartoVoyager"],
            },
            # Add custom map styles
            "additionalMapStyles": {
                # For general mapbox GL based styles, a simple api interface can be used with
                # the `spec` key referencing the url to a mapbox GL style
                "mapboxDark": {
                    "name": "Mapbox Dark",
                    "icon": "md/MdBrightness2",
                    # For mapbox styles:
                    # See: https://docs.mapbox.com/api/maps/styles/
                    "spec": "mapbox://styles/mapbox/dark-v11",
                    # You can add a custom fog spec for any globe projection
                    # This adds a custom atmosphere effect to the edge of a map
                    # See: https://docs.mapbox.com/mapbox-gl-js/api/map/#map#setfog
                    "fog": {
                        "range": [0.8, 8],
                        "color": "#dc9f9f",
                        "horizon-blend": 0.5,
                        "high-color": "#245bde",
                        "space-color": "#000000",
                        "star-intensity": 0.15,
                    },
                },
                "cartoVoyager": {
                    "name": "Carto Voyager",
                    "icon": "md/MdExplore",
                    # For CartoDB based Mapbox GL styles:
                    # See: https://github.com/CartoDB/basemap-styles/blob/master/docs/basemap_styles.json
                    "spec": "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
                    # Complex fog specs allow for even more customization
                    # See: https://docs.mapbox.com/mapbox-gl-js/api/map/#map#setfog
                    "fog": {
                        "range": [0.5, 10],
                        "color": "#ffffff",
                        "high-color": "#245cdf",
                        "space-color": [
                            "interpolate",
                            ["linear"],
                            ["zoom"],
                            2,
                            "orange",
                            4,
                            "blue",
                        ],
                        "horizon-blend": [
                            "interpolate",
                            ["exponential", 1.2],
                            ["zoom"],
                            5,
                            0.02,
                            7,
                            0.08,
                        ],
                        "star-intensity": [
                            "interpolate",
                            ["linear"],
                            ["zoom"],
                            5,
                            0.35,
                            6,
                            0,
                        ],
                    },
                },
            },
            "data": {
                "exampleMap": {
                    "name": "Example Map",
                    "currentProjection": "globe",
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 4.66,
                        "pitch": 0,
                        "bearing": 0,
                        "height": 1287,
                        "altitude": 1.5,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                },
            },
        },
        "pages": {
            "data": {
                "mapDashboard": {
                    "pageLayout": [
                        {
                            "type": "map",
                            "mapId": "exampleMap",
                            "showToolbar": False,
                            "maximized": True},
                    ],
                },
            },
        },
    }
