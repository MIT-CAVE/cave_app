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
                # Specify the order of map style items as they will appear in the style selector
                "order": {
                    "additionalMapStyles": ["mapboxDark", "cartoVoyager", "stamenWatercolor"],
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
                        "name": 'Carto Voyager',
                        "icon": 'md/MdExplore',
                        # For CartoDB based Mapbox GL styles:
                        # See: https://github.com/CartoDB/basemap-styles/blob/master/docs/basemap_styles.json
                        "spec": 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json',
                    },
                    # For custom tiling styles from other sources like stamen,
                    # you can use the more complex spec dictionary based interface
                    "stamenWatercolor": {
                        "name": "Stamen Watercolor",
                        "icon": "md/MdBrush",
                        # See the `style` key in the following mapbox gl reference spec:
                        # https://docs.mapbox.com/mapbox-gl-js/example/map-tiles/
                        "spec": {
                            "version": 8,
                            "sources": {
                                "raster-tiles": {
                                    "type": "raster",
                                    "tiles": [
                                        "https://stamen-tiles.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.jpg"
                                    ],
                                    "tileSize": 256,
                                    "attribution": "Map tiles by <a target='_top' rel='noopener' href='http://stamen.com'>Stamen Design</a>, under <a target='_top' rel='noopener' href='http://creativecommons.org/licenses/by/3.0'>CC BY 3.0</a>. Data by <a target='_top' rel='noopener' href='http://openstreetmap.org'>OpenStreetMap</a>, under <a target='_top' rel='noopener' href='http://creativecommons.org/licenses/by-sa/3.0'>CC BY SA</a>",
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
            },
        },
        "appBar": {
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
                            "type": "maps",
                            "mapId": "exampleMap"
                        },
                    ],
                },
            },
        },
    }