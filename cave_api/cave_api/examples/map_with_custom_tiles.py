def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/4.10.1/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/4.10.1",
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {
                "data": ["refreshButton", "mapPage"],
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
                "additionalMapStyles": ["mapboxDark", "cartoVoyager", "osmRasterTiles"],
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
                },
                "cartoVoyager": {
                    "name": "Carto Voyager",
                    "icon": "md/MdExplore",
                    # For CartoDB based Mapbox GL styles:
                    # See: https://github.com/CartoDB/basemap-styles/blob/master/docs/basemap_styles.json
                    "spec": "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
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
                    "currentStyle": "osmRasterTiles",
                    # Specify the default viewport for the map
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
        # Add a map page to the app using the example map specified above
        "pages": {
            "currentPage": "mapPage",
            "data": {
                "mapPage": {
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
