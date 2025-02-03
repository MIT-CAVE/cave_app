def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.4.0/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0"
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
            # Specify available map projections that can be selected in the dashboards by the user
            "data": {
                "exampleMap": {
                    "name": "Example Map",
                    # Specify the default projection for the map
                    # Note: globe can only be used if you have a mapbox token
                    "currentProjection": "globe",
                    # Specify the default viewport for the map
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 4.66,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                    "legendGroups": {
                        "facilities": {
                            "name": "Facilities",
                            "data": {
                                "warehouse": {
                                    "value": True,
                                    "colorBy": "includesAutomation",
                                    "colorByOptions": [
                                        "capacity",
                                        "includesAutomation",
                                    ],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    "icon": "fa6/FaWarehouse",
                                    # Add a filter to the map to only show capacity > 90
                                    "filters": [
                                        {
                                            "id": 0,
                                            "type": "group",
                                            "groupId": 0,
                                            "logic": "and",
                                            "edit": False,
                                        },
                                        {
                                            "id": 1,
                                            "type": "rule",
                                            "parentGroupId": 0,
                                            "prop": "capacity",
                                            "option": "gt",
                                            "value": "90"
                                        }
                                    ]
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "warehouse": {
                    "type": "node",
                    "name": "Warehouse",
                    "props": {
                        "scenario": {
                            "name": "Scenario",
                            "type": "text",
                            "enabled": False,
                            "display": False,
                            "help": "The scenario name",
                            "allowFiltering": False,  # This prop cannot be used for filtering
                        },
                        "capacity": {
                            "name": "Capacity",
                            "type": "num",
                            "unit": "Cubic Feet",
                            "help": "The warehouse capacity in cubic feet",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {
                                        "value": "min",
                                        "size": "30px",
                                        "color": "rgb(233 0 0)",
                                    },
                                    {
                                        "value": "max",
                                        "size": "45px",
                                        "color": "rgb(96 2 2)",
                                    },
                                ],
                            },
                        },
                        "includesAutomation": {
                            "name": "Includes Automation",
                            "type": "toggle",
                            "help": "Whether the warehouse includes automation",
                            "options": {
                                "false": {"color": "rgb(255 0 0)"},
                                "true": {"color": "rgb(0 255 0)"},
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "latitude": [[43.78], [39.82]],
                            "longitude": [[-79.63], [-86.18]],
                        },
                        "valueLists": {
                            "capacity": [100, 80],
                            "includesAutomation": [True, False],
                            "scenario": ["Scenario 1", "Scenario 2"],
                        },
                    },
                },
            }
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
