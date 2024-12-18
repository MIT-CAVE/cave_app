def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.4.0/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0",
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": [
                    "mapPage",
                ],
            },
            "data": {
                # Add an appBar button to launch a map focused dashboard
                "mapPage": {
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
                            # For custom tiling styles from other raster sources (eg: stamen or open street map),
                # you can use the more complex spec dictionary based interface
                "osmRasterTiles": {
                    "name": "OSM Raster Tiles",
                    "icon": "md/MdBrush",
                    # See the `style` key in the following mapbox gl reference spec:
                    # https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
                    "spec": {
                        "version": 8,
                        "sources": {
                            "raster-tiles": {
                                "type": "raster",
                                # EG: See a list of raster sources based on OSM here:
                                # https://wiki.openstreetmap.org/wiki/Raster_tile_providers
                                "tiles": [
                                    "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                                ],
                                "tileSize": 256,
                                "attribution": "Map tiles by <a target='_top' rel='noopener' href='https://osmfoundation.org/'>OpenStreetMap</a>, under <a target='_top' rel='noopener' href='https://osmfoundation.org/copyright'>Open Database License</a>.",
                            },
                        },
                        "layers": [
                            {
                                "id": "simple-tiles",
                                "type": "raster",
                                "source": "raster-tiles",
                                "minzoom": 0,
                                "maxzoom": 22,
                            },
                        ],
                    },
                },
            },
            # Specify available map projections that can be selected in the dashboards by the user
            "data": {
                "exampleMap": {
                    "name": "Example Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "globe",
                    # Specify the current style for the map
                    "currentStyle": "cartoVoyager",
                    # Specify the default viewport for the map
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 2.66,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                },
            },
        },
        # Add a map page to the app using the example map specified above
        "pages": {
            "currentPage": "mapPage",
            "data": {
                "mapPage": {
                    "charts": {
                        "map": {
                            "type": "map",
                            "mapId": "exampleMap",
                            "showToolbar": False,
                            "maximized": True,
                        },
                    },
                    "pageLayout": ["map", None, None, None],
                },
            },
        },
    }
