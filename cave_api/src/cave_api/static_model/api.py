def execute_command(session_data, command="init"):
    """
    Usage:
    - Execute a command to mutate the current session_data

    Requires:

    - `session_data`:
        - Type: dict
        - What: A dict of `session_data` objects to use when configuring this session
        - See: https://github.com/MIT-CAVE/cave_app/blob/0.2.0/cave_api/README_API_STRUCTURE.md

    Optional:

    - `command`:
        - Type: str
        - What: A string to indicate a command to be processed by the api
        - Default: 'init'

    Returns:
    - `output`:
        - Type: dict of dicts
        - What: A dict of dictionaries to mutate the current session given the current `session_data`
        - See: https://github.com/MIT-CAVE/cave_app/blob/0.2.0/cave_api/README_API_STRUCTURE.md
    """
    example = {
        "settings": {
            "allow_modification": False,
            "send_to_api": False,
            "send_to_client": True,
            "data": {
                "syncToggles": {
                    "Map Layers": {
                        "ml1": ["map", "data", "enabledTypes"],
                        "ml2": ["nodes", "types"],
                        "ml3": ["arcs", "types"],
                        "ml4": ["geos", "types"],
                    },
                },
                "defaultDesync": {
                    "Map Layers": {
                        "ml1": ["map", "data", "enabledTypes"],
                        "ml2": ["nodes", "types"],
                        "ml3": ["arcs", "types"],
                        "ml4": ["geos", "types"],
                    },
                    "App Bar": {
                        "ab1": ["appBar", "data", "dashboardId"],
                        "ab2": ["appBar", "paneState"],
                    },
                },
                "IconUrl": "https://react-icons.mitcave.com/0.0.1",
                "numberFormat": {
                    "precision": 4,
                    "trailingZeros": False,
                    "unitSpace": True,
                },
                "debug": True,
            },
        },
        "categories": {
            "allow_modification": False,
            "data": {
                "Location": {
                    "data": {
                        "loc_US_MI": {
                            "Region": "North America",
                            "Country": "USA",
                            "State": "Michigan",
                        },
                        "loc_US_MA": {
                            "Region": "North America",
                            "Country": "USA",
                            "State": "Massachusetts",
                        },
                        "loc_US_FL": {
                            "Region": "North America",
                            "Country": "USA",
                            "State": "Florida",
                        },
                        "loc_US_IN": {
                            "Region": "North America",
                            "Country": "USA",
                            "State": "Indiana",
                        },
                        "loc_CA_ON": {
                            "Region": "North America",
                            "Country": "Canada",
                            "State": "Ontario",
                        },
                    },
                    "name": "Locations",
                    "nestedStructure": {
                        "Region": {
                            "name": "Regions",
                            "order": 1,
                        },
                        "Country": {
                            "name": "Countries",
                            "ordering": ["USA", "Canada"],
                            "order": 2,
                        },
                        "State": {
                            "name": "States",
                            "order": 3,
                        },
                    },
                    "layoutDirection": "horizontal",
                    "order": 1,
                },
                "Product": {
                    "data": {
                        "prd_abc123": {
                            "Type": "Fruit",
                            "Size": "Big",
                            "Product": "Apple",
                        },
                        "prd_def456": {
                            "Type": "Fruit",
                            "Size": "Small",
                            "Product": "Grape",
                        },
                    },
                    "name": "Products",
                    "nestedStructure": {
                        "Type": {
                            "name": "Types",
                            "order": 1,
                        },
                        "Size": {
                            "name": "Sizing",
                            "ordering": ["Small", "Big"],
                            "order": 2,
                        },
                        "Product": {
                            "name": "Products",
                            "order": 3,
                        },
                    },
                    "layoutDirection": "horizontal",
                    "order": 2,
                },
            },
        },
        "appBar": {
            "data": {
                "appSettings": {
                    "icon": "MdOutlineSettings",
                    "type": "pane",
                    "variant": "appSettings",
                    "bar": "upper",
                    "order": 1,
                },
                "button_reset": {
                    "name": "Reset Button",
                    "icon": "MdSync",
                    "color": {
                        "dark": "rgb(255, 101, 101)",
                        "light": "rgb(212, 0, 0)",
                    },
                    "apiCommand": "reset",
                    "type": "button",
                    "bar": "upper",
                    "order": 2,
                },
                "button_1": {
                    "name": "Solve Button",
                    "icon": "BsLightningFill",
                    "color": {
                        "dark": "rgb(178, 179, 55)",
                        "light": "rgb(79, 79, 24)",
                    },
                    "apiCommand": "solve_session",
                    "type": "button",
                    "bar": "upper",
                    "order": 2,
                },
                "settings": {
                    "name": "Settings Pane",
                    "props": {
                        "Solver": {
                            "name": "Solver",
                            "type": "selector",
                            "variant": "dropdown",
                            "value": [
                                {"name": "Gurobi", "value": True},
                                {"name": "Cplex", "value": False},
                                {"name": "CoinOR", "value": False},
                            ],
                            "enabled": True,
                            "help": "Select a solver type to use",
                        },
                        "Pct_Optimal": {
                            "name": "Percent Optimal",
                            "type": "num",
                            "value": 97,
                            "enabled": True,
                            "help": "What percent of optimal would you like to solve to?",
                            "maxValue": 100,
                            "minValue": 0,
                            "numberFormat": {
                                "unit": "%",
                                "unitSpace": False,
                                "trailingZeros": True,
                            },
                        },
                        "min_profit": {
                            "name": "Minimum profit",
                            "type": "num",
                            "value": 10000,
                            "enabled": True,
                            "variant": "field",
                            "help": "The minimum intended profit",
                            "maxValue": 999999999999999,
                            "minValue": -999999999999999,
                            "numberFormat": {
                                "precision": 0,
                                "trailingZeros": False,
                                "currency": True,
                                "unit": "$",
                            },
                        },
                    },
                    "icon": "BsWrench",
                    "type": "pane",
                    "variant": "options",
                    "teamSync": True,
                    "bar": "upper",
                    "order": 3,
                },
                "settingsBig": {
                    "name": "A Big Settings Pane",
                    "width": "100%",
                    "props": {
                        "solver_section": {
                            "name": "Solver Section",
                            "type": "head",
                            "help": "Some help for the solver section",
                        },
                        "Solver": {
                            "name": "Solver",
                            "type": "selector",
                            "variant": "dropdown",
                            "value": [
                                {"name": "Gurobi", "value": True},
                                {"name": "Cplex", "value": False},
                                {"name": "CoinOR", "value": False},
                            ],
                            "enabled": True,
                            "help": "Select a solver type to use",
                        },
                        "optimality_section": {
                            "name": "Optimality Section",
                            "type": "head",
                            "help": "Some help for the optimality section",
                        },
                        "Pct_Optimal": {
                            "name": "Percent Optimal",
                            "type": "num",
                            "value": 97,
                            "enabled": True,
                            "variant": "slider",
                            "help": "What percent of optimal would you like to solve to?",
                            "maxValue": 100,
                            "minValue": 0,
                        },
                        "distance_section": {
                            "name": "Demand Served At Distances",
                            "type": "head",
                            "help": "How much demand do you expect to serve at the following distances?",
                        },
                        "50_miles": {
                            "name": "50 Miles",
                            "type": "num",
                            "value": 45,
                            "enabled": True,
                            "variant": "slider",
                            "help": "Expected demand filled at 50 miles",
                            "maxValue": 100,
                            "minValue": 0,
                        },
                        "100_miles": {
                            "name": "100 Miles",
                            "type": "num",
                            "value": 35,
                            "enabled": True,
                            "variant": "slider",
                            "help": "Expected demand filled at 100 miles",
                            "maxValue": 100,
                            "minValue": 0,
                        },
                        "150_miles": {
                            "name": "150 Miles",
                            "type": "num",
                            "value": 25,
                            "enabled": True,
                            "variant": "slider",
                            "help": "Expected demand filled at 150 miles",
                            "maxValue": 100,
                            "minValue": 0,
                        },
                        "200_miles": {
                            "name": "200 Miles",
                            "type": "num",
                            "value": 45,
                            "enabled": True,
                            "variant": "slider",
                            "help": "Expected demand filled at 200 miles",
                            "maxValue": 120,
                            "minValue": 0,
                        },
                        "250_miles": {
                            "name": "250 Miles",
                            "type": "num",
                            "value": 75,
                            "enabled": True,
                            "variant": "slider",
                            "help": "Expected demand filled at 250 miles",
                            "maxValue": 120,
                            "minValue": 0,
                        },
                    },
                    "layout": {
                        "type": "grid",
                        "num_columns": 3,
                        "num_rows": "auto",
                        "data": {
                            "col1_row1": {
                                "type": "item",
                                "column": 1,
                                "row": 1,
                                "itemId": "solver_section",
                            },
                            "col1_row2": {
                                "type": "item",
                                "column": 1,
                                "row": 2,
                                "itemId": "Solver",
                            },
                            "col3_row2": {
                                "type": "item",
                                "column": 3,
                                "row": 2,
                                "itemId": "Pct_Optimal",
                                "container": "horizontal",
                            },
                            "col3_row1": {
                                "type": "item",
                                "column": 3,
                                "row": 1,
                                "itemId": "optimality_section",
                            },
                            "col3_row3": {
                                "type": "grid",
                                "num_columns": 7,
                                "num_rows": 1,
                                "column": 3,
                                "row": 3,
                                "data": {
                                    "col1": {
                                        "type": "item",
                                        "column": 1,
                                        "itemId": "50_miles",
                                    },
                                    "col2": {
                                        "type": "item",
                                        "column": 2,
                                        "container": "titled",
                                        "itemId": "150_miles",
                                    },
                                    "col3": {
                                        "type": "item",
                                        "column": 3,
                                        "itemId": "50_miles",
                                    },
                                    "col4": {
                                        "type": "item",
                                        "column": 4,
                                        "itemId": "200_miles",
                                    },
                                    "id_11": {
                                        "type": "item",
                                        "container": "titled",
                                        "itemId": "Pct_Optimal",
                                    },
                                    "id_12": {
                                        "type": "item",
                                        "container": "titled",
                                        "itemId": "150_miles",
                                    },
                                    "id_13": {
                                        "type": "item",
                                        "itemId": "50_miles",
                                    },
                                },
                            },
                            "col3_row4": {
                                "type": "grid",
                                "num_columns": 7,
                                "num_rows": 1,
                                "column": 3,
                                "row": 4,
                                "data": {
                                    "col1": {
                                        "type": "item",
                                        "column": 1,
                                        "itemId": "100_miles",
                                    },
                                    "col2": {
                                        "type": "item",
                                        "column": 2,
                                        "itemId": "50_miles",
                                    },
                                    "col3": {
                                        "type": "item",
                                        "column": 3,
                                        "itemId": "150_miles",
                                    },
                                    "col4": {
                                        "type": "item",
                                        "column": 4,
                                        "itemId": "200_miles",
                                    },
                                    "id_21": {
                                        "type": "item",
                                        "container": "titled",
                                        "itemId": "100_miles",
                                    },
                                    "id_22": {
                                        "type": "item",
                                        "container": "titled",
                                        "itemId": "250_miles",
                                    },
                                    "id_23": {
                                        "type": "item",
                                        "itemId": "Pct_Optimal",
                                    },
                                },
                            },
                            "col2_row1": {
                                "type": "item",
                                "column": 2,
                                "row": 1,
                                "itemId": "distance_section",
                            },
                            "col2_row3": {
                                "type": "item",
                                "row": 3,
                                "column": 2,
                                "itemId": "200_miles",
                            },
                            "col2_row2": {
                                "type": "item",
                                "row": 2,
                                "column": 2,
                                "itemId": "250_miles",
                            },
                        },
                    },
                    "icon": "FaCogs",
                    "type": "pane",
                    "variant": "options",
                    "bar": "upper",
                    "order": 4,
                },
                "context": {
                    "name": "Context Pane",
                    "props": {
                        "Demand_Multiplier": {
                            "type": "num",
                            "value": 100,
                            "enabled": True,
                            "help": "Percentage multiplier times the base demand (100%=Given Demand)",
                            "label": "%",
                            "variant": "slider",
                            "maxValue": 500,
                            "minValue": 0,
                            "selectableCategories": ["Location", "Product"],
                        },
                        "Supply_Multiplier": {
                            "type": "num",
                            "value": 100,
                            "enabled": True,
                            "help": "Percentage multiplier times the base supply (100%=Given Supply)",
                            "label": "%",
                            "minValue": 0,
                            "numberFormat": {
                                "precision": 0,
                            },
                            "selectableCategories": ["Location", "Product"],
                        },
                    },
                    "data": {
                        "context_1": {
                            "prop": "Demand_Multiplier",
                            "value": 110,
                            "applyCategories": {"Location": ["loc_US_MI"]},
                        }
                    },
                    "icon": "BsInboxes",
                    "type": "pane",
                    "variant": "context",
                    "order": 5,
                    "bar": "upper",
                },
                "filter": {
                    "icon": "FaFilter",
                    "type": "pane",
                    "variant": "filter",
                    "order": 6,
                    "bar": "upper",
                },
                "map_1": {
                    "type": "map",
                    "icon": "FaMapMarkedAlt",
                    "bar": "lower",
                    "order": 1,
                },
                "dash_1": {
                    "type": "stats",
                    "icon": "MdInsertChart",
                    "name": "Dashboard 1",
                    "order": 2,
                    "bar": "lower",
                    "dashboardLayout": [
                        {
                            "chart": "Bar",
                            "grouping": "Average",
                            "statistic": "demand_met",
                        },
                        {
                            "chart": "Line",
                            "grouping": "Sum",
                            "statistic": "demand_pct",
                        },
                        {
                            "chart": "Bar",
                            "level": "Size",
                            "category": "Product",
                            "grouping": "Sum",
                            "statistic": "demand_met",
                        },
                        {
                            "chart": "Bar",
                            "grouping": "Minimum",
                            "type": "kpis",
                            "sessions": [],
                            "kpi": "Really Big Number",
                        },
                    ],
                    "lockedLayout": False,
                },
                "kpi_1": {
                    "type": "kpi",
                    "icon": "MdSpeed",
                    "bar": "lower",
                    "order": 3,
                },
            }
        },
        "map": {
            "data": {
                "enabledTypes": {"arc": {"T1": True}},
                "defaultViewport": {
                    "longitude": -75.44766721108091,
                    "latitude": 40.34530681636297,
                    "zoom": 4.657916626867326,
                    "pitch": 0,
                    "bearing": 0,
                    "height": 1287,
                    "altitude": 1.5,
                    "maxZoom": 12,
                    "minZoom": 2,
                },
                "optionalViewports": {
                    "ov0": {
                        "icon": "FaGlobeAsia",
                        "name": "Asia",
                        "zoom": 4,
                        "order": 1,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                        "latitude": 30,
                        "longitude": 121,
                    },
                    "ov1": {
                        "icon": "FaGlobeEurope",
                        "name": "EMEA",
                        "zoom": 4,
                        "order": 1,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                        "latitude": 47,
                        "longitude": 14,
                    },
                },
                "legendGroups": [
                    {
                        "name": "DC Delivery",
                        "nodeTypes": ["DC"],
                        "arcTypes": ["T1"],
                    },
                    {
                        "name": "Store Delivery",
                        "nodeTypes": ["Store"],
                        "arcTypes": ["T2"],
                    },
                    {"name": "Demand Geography", "geoTypes": ["state", "country"]},
                ],
            },
        },
        "arcs": {
            "types": {
                "T1": {
                    "name": "Flow Type 1",
                    "colorByOptions": {
                        "Primary Type": {
                            "Air": "rgb(128,255,255)",
                            "Mixed": "rgb(0,153,51)",
                            "Water": "rgb(0,0,128)",
                            "Train": "rgb(204,0,0)",
                            "Truck": "rgb(153,77,0)",
                            "3rd Party": "rgb(255,25,255)",
                        },
                        "Flow Capacity": {
                            "min": 0,
                            "max": 50,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                        "Flow": {
                            "min": 0,
                            "max": 40,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                    },
                    "colorBy": "Flow",
                    "lineBy": "solid",
                    "sizeByOptions": {
                        "Flow Capacity": {"min": 0, "max": 50},
                        "Flow": {"min": 0, "max": 40},
                    },
                    "sizeBy": "Flow Capacity",
                    "startSize": "15px",
                    "endSize": "30px",
                    "order": 1,
                    "props": {
                        "Flow Capacity": {
                            "name": "Flow Capacity (test)",
                            "type": "num",
                            "enabled": False,
                            "help": "Flow Capacity",
                            "numberFormat": {
                                "unit": "units (test)",
                            },
                        },
                    },
                },
                "T2": {
                    "name": "Flow Type 2",
                    "colorByOptions": {
                        "Flow Capacity": {
                            "min": 0,
                            "max": 50,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                        "Flow": {
                            "min": 0,
                            "max": 40,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                    },
                    "colorBy": "Flow",
                    "lineBy": "dotted",
                    "sizeByOptions": {
                        "Flow Capacity": {"min": 0, "max": 50},
                        "Flow": {"min": 0, "max": 40},
                    },
                    "sizeBy": "Flow Capacity",
                    "startSize": "15px",
                    "endSize": "30px",
                    "order": 2,
                    "props": {
                        "Flow Capacity": {
                            "name": "Flow Capacity (test)",
                            "type": "num",
                            "enabled": False,
                            "help": "Flow Capacity",
                            "numberFormat": {
                                "unit": "units (test)",
                            },
                            "value": 80,
                        },
                    },
                },
            },
            "data": {
                "arc_1": {
                    "startLatitude": 43.78,
                    "startLongitude": -79.63,
                    "endLatitude": 39.82,
                    "endLongitude": -86.18,
                    "startClick": 800,
                    "endClick": 1600,
                    "type": "T1",
                    "category": {
                        "Location": ["loc_CA_ON", "loc_US_IN"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Flow Capacity": {
                            "value": 50,
                        },
                        "Flow": {
                            "name": "Flow (test)",
                            "type": "num",
                            "value": 40,
                            "enabled": False,
                            "help": "Flow",
                            "numberFormat": {
                                "unit": "units (test)",
                            },
                        },
                        "Primary Type": {
                            "name": "Primary Type",
                            "type": "selector",
                            "variant": "dropdown",
                            "value": [
                                {"name": "Air", "value": False},
                                {"name": "Train", "value": True},
                                {"name": "Truck", "value": False},
                                {"name": "3rd Party", "value": False},
                                {"name": "Mixed", "value": False},
                                {"name": "Water", "value": False},
                            ],
                            "enabled": True,
                        },
                    },
                    "layout": {
                        "type": "grid",
                        "num_columns": 1,
                        "num_rows": "auto",
                        "data": {
                            "flow_capacity": {
                                "type": "item",
                                "itemId": "Flow Capacity",
                                "row": 1,
                            },
                            "flow": {
                                "type": "item",
                                "itemId": "Flow",
                                "row": 2,
                            },
                            "primary_type": {
                                "type": "item",
                                "itemId": "Primary Type",
                            },
                        },
                    },
                },
                "arc_2": {
                    "startLatitude": 39.82,
                    "startLongitude": -86.18,
                    "endLatitude": 42.89,
                    "endLongitude": -85.68,
                    "startClick": 1600,
                    "endClick": 2000,
                    "type": "T2",
                    "category": {
                        "Location": ["loc_US_MI", "loc_US_IN"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Flow Capacity": {
                            "value": 30,
                        },
                        "Flow": {
                            "type": "num",
                            "value": 20,
                            "enabled": False,
                            "help": "Flow",
                        },
                    },
                    "layout": {
                        "type": "grid",
                        "num_columns": 1,
                        "num_rows": "auto",
                        "data": {
                            "flow_capacity": {
                                "type": "item",
                                "itemId": "Flow Capacity",
                                "row": 1,
                            },
                            "flow": {
                                "type": "item",
                                "itemId": "Flow",
                            },
                        },
                    },
                },
                "arc_3": {
                    "startLatitude": 39.82,
                    "startLongitude": -86.18,
                    "endLatitude": 28.49,
                    "endLongitude": -81.56,
                    "startClick": 1600,
                    "endClick": 2000,
                    "type": "T2",
                    "category": {
                        "Location": ["loc_US_FL", "loc_US_IN"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Flow Capacity": {
                            "value": 30,
                        },
                        "Flow": {
                            "type": "num",
                            "value": 14,
                            "enabled": False,
                            "help": "Flow",
                        },
                    },
                    "layout": {
                        "type": "grid",
                        "num_columns": 1,
                        "num_rows": "auto",
                        "data": {
                            "flow_capacity": {
                                "type": "item",
                                "itemId": "Flow Capacity",
                                "row": 1,
                            },
                            "flow": {
                                "type": "item",
                                "itemId": "Flow",
                            },
                        },
                    },
                },
                "arc_4": {
                    "startLatitude": 39.82,
                    "startLongitude": -86.18,
                    "endLatitude": 42.361176,
                    "endLongitude": -71.084707,
                    "startClick": 1600,
                    "endClick": 2000,
                    "type": "T2",
                    "category": {
                        "Location": ["loc_US_MA", "loc_US_IN"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Flow Capacity": {
                            "type": "num",
                            "value": 30,
                            "enabled": False,
                            "help": "Flow Capacity",
                        },
                        "Flow": {
                            "type": "num",
                            "value": 6,
                            "enabled": False,
                            "help": "Flow",
                        },
                    },
                },
            },
        },
        "nodes": {
            "types": {
                "DC": {
                    "name": "DCs",
                    "colorByOptions": {
                        "Size": {
                            "min": 0,
                            "max": 80,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                        "Capacity": {
                            "min": 0,
                            "max": 50,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                        "Active": {"false": "rgb(255,0,0)", "true": "rgb(0,255,0)"},
                    },
                    "colorBy": "Size",
                    "minSizeRange": 0,
                    "sizeByOptions": {
                        "Size": {"min": 0, "max": 80},
                        "Capacity": {"min": 0, "max": 50},
                    },
                    "sizeBy": "Capacity",
                    "startSize": "30px",
                    "endSize": "45px",
                    "icon": "MdStore",
                    "order": 2,
                    "props": {
                        "Size": {
                            "type": "num",
                            "enabled": True,
                            "help": "The Size in SQ Meters",
                            "numberFormat": {
                                "unit": "Sq Meters",
                            },
                        },
                    },
                },
                "Store": {
                    "name": "Stores",
                    "colorByOptions": {
                        "Size": {
                            "min": 0,
                            "max": 1000,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                        "Capacity": {
                            "min": 0,
                            "max": 50,
                            "startGradientColor": {
                                "dark": "rgb(233, 0, 0)",
                                "light": "rgb(52, 52, 236)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(96, 2, 2)",
                                "light": "rgb(23, 23, 126)",
                            },
                        },
                        "Active": {"false": "rgb(233, 0, 0)", "true": "rgb(0, 233, 0)"},
                    },
                    "colorBy": "Size",
                    "sizeByOptions": {
                        "Size": {"min": 0, "max": 100},
                        "Capacity": {"min": 0, "max": 250},
                    },
                    "sizeBy": "Capacity",
                    "startSize": "30px",
                    "endSize": "45px",
                    "icon": "BsBuilding",
                    "order": 1,
                    "props": {
                        "Size": {
                            "type": "num",
                            "enabled": True,
                            "help": "The Size in SQ Meters",
                            "numberFormat": {
                                "unit": "Sq Meters",
                            },
                        },
                    },
                },
            },
            "data": {
                "node_1": {
                    "latitude": 43.78,
                    "longitude": -79.63,
                    "type": "DC",
                    "category": {
                        "Location": ["loc_CA_ON"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Size": {
                            "value": 100,
                        },
                        "Capacity": {
                            "type": "num",
                            "value": 50,
                            "enabled": False,
                            "help": "The capacity in units",
                        },
                        "Active": {
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "The active status of this location",
                        },
                    },
                },
                "node_2": {
                    "latitude": 39.82,
                    "longitude": -86.18,
                    "type": "DC",
                    "category": {
                        "Location": ["loc_US_IN"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Size": {
                            "value": 80,
                        },
                        "Capacity": {
                            "type": "num",
                            "value": 40,
                            "enabled": False,
                            "help": "The capacity in units",
                        },
                        "Active": {
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "The active status of this location",
                        },
                    },
                },
                "node_3": {
                    "latitude": 42.89,
                    "longitude": -85.68,
                    "type": "Store",
                    "category": {
                        "Location": ["loc_US_MI"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Size": {
                            "value": 500,
                        },
                        "Capacity": {
                            "type": "num",
                            "value": 150,
                            "enabled": False,
                            "help": "The capacity in units",
                        },
                        "Active": {
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "The active status of this location",
                        },
                    },
                },
                "node_4": {
                    "latitude": 28.49,
                    "longitude": -81.56,
                    "type": "Store",
                    "category": {
                        "Location": ["loc_US_FL"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Size": {
                            "value": 1000,
                        },
                        "Capacity": {
                            "type": "num",
                            "value": 250,
                            "enabled": False,
                            "help": "The capacity in units",
                        },
                        "Active": {
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "The active status of this location",
                        },
                    },
                },
                "node_5": {
                    "latitude": 42.361176,
                    "longitude": -71.084707,
                    "type": "Store",
                    "category": {
                        "Location": ["loc_US_MA"],
                        "Product": ["prd_def456", "prd_abc123"],
                    },
                    "props": {
                        "Size": {
                            "value": 1000,
                        },
                        "Capacity": {
                            "type": "num",
                            "value": 250,
                            "enabled": False,
                            "help": "The capacity in units",
                        },
                        "Active": {
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "The active status of this location",
                        },
                    },
                },
            },
        },
        "geos": {
            "types": {
                "state": {
                    "name": "State",
                    "colorByOptions": {
                        "Demand": {
                            "min": 0,
                            "max": 300,
                            "startGradientColor": {
                                "dark": "rgb(100, 100, 100)",
                                "light": "rgb(200, 200, 200)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(20, 205, 20)",
                                "light": "rgb(10, 100, 10)",
                            },
                        }
                    },
                    "colorBy": "Demand",
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/world-states-provinces-md.json",
                        "geoJsonProp": "code_hasc",
                    },
                    "icon": "BsHexagon",
                    "props": {
                        "Demand": {
                            "type": "num",
                            "enabled": True,
                            "help": "The Demand of this Geography",
                            "numberFormat": {
                                "unit": "units",
                            },
                        },
                    },
                },
                "country": {
                    "name": "Country",
                    "colorByOptions": {
                        "Demand": {
                            "min": 0,
                            "max": 800,
                            "startGradientColor": {
                                "dark": "rgb(100, 100, 100)",
                                "light": "rgb(200, 200, 200)",
                            },
                            "endGradientColor": {
                                "dark": "rgb(20, 205, 20)",
                                "light": "rgb(10, 100, 10)",
                            },
                        }
                    },
                    "colorBy": "Demand",
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/countries-sm.json",
                        "geoJsonProp": "FIPS_10",
                    },
                    "icon": "BsHexagon",
                    "props": {
                        "Demand": {
                            "type": "num",
                            "enabled": True,
                            "help": "The Demand of this Geography",
                            "numberFormat": {
                                "unit": "units",
                            },
                        },
                    },
                },
            },
            "data": {
                "geo_1": {
                    "name": "Ontario, Canada",
                    "geoJsonValue": "CA.ON",
                    "type": "state",
                    "category": {"Location": ["loc_CA_ON"]},
                    "props": {
                        "Demand": {
                            "value": 50,
                        }
                    },
                },
                "geo_2": {
                    "name": "Michigan, USA",
                    "geoJsonValue": "US.MI",
                    "type": "state",
                    "category": {"Location": ["loc_US_MI"]},
                    "props": {
                        "Demand": {
                            "value": 300,
                        }
                    },
                },
                "geo_3": {
                    "name": "Massachusetts, USA",
                    "geoJsonValue": "US.MA",
                    "type": "state",
                    "category": {"Location": ["loc_US_MI"]},
                    "props": {
                        "Demand": {
                            "value": 250,
                        }
                    },
                },
                "geo_4": {
                    "name": "Florida, USA",
                    "geoJsonValue": "US.FL",
                    "type": "state",
                    "category": {"Location": ["loc_US_MI"]},
                    "props": {
                        "Demand": {
                            "value": 100,
                        }
                    },
                },
                "geo_5": {
                    "name": "Indiana, USA",
                    "geoJsonValue": "US.FL",
                    "type": "state",
                    "category": {"Location": ["loc_US_MI"]},
                    "props": {
                        "Demand": {
                            "value": 200,
                        }
                    },
                },
                "geo_c_1": {
                    "name": "Canada",
                    "geoJsonValue": "CA",
                    "type": "country",
                    "category": {"Location": ["loc_CA_ON"]},
                    "props": {
                        "Demand": {
                            "value": 50,
                        }
                    },
                },
                "geo_c_2": {
                    "name": "USA",
                    "geoJsonValue": "US",
                    "type": "country",
                    "category": {
                        "Location": [
                            "loc_US_FL",
                            "loc_US_MA",
                            "loc_US_IN",
                            "loc_US_MI",
                        ]
                    },
                    "props": {
                        "Demand": {
                            "value": 800,
                        }
                    },
                },
            },
        },
        "stats": {
            "types": {
                "demand_met": {
                    "name": "Demand Met",
                    "calculation": "demand_met",
                    "numberFormat": {
                        "unit": "units",
                    },
                    "order": 1,
                },
                "demand_tot": {
                    "name": "Demand Total",
                    "calculation": "demand_tot",
                    "numberFormat": {
                        "unit": "units",
                    },
                    "order": 2,
                },
                "demand_pct": {
                    "name": "Demand Percentage",
                    "calculation": 'demand_met / groupSum("demand_tot")',
                    "numberFormat": {
                        "precision": 2,
                        "trailingZeros": True,
                        "unitSpace": False,
                        "unit": "%",
                    },
                    "order": 3,
                },
            },
            "data": {
                "d1": {
                    "category": {
                        "Location": ["loc_CA_ON"],
                        "Product": ["prd_abc123"],
                    },
                    "values": {"demand_met": 5, "demand_tot": 10},
                },
                "d2": {
                    "category": {
                        "Location": ["loc_CA_ON"],
                        "Product": ["prd_def456"],
                    },
                    "values": {"demand_met": 4, "demand_tot": 5},
                },
                "d3": {
                    "category": {
                        "Location": ["loc_US_MI"],
                        "Product": ["prd_abc123"],
                    },
                    "values": {"demand_met": 6, "demand_tot": 7},
                },
                "d4": {
                    "category": {
                        "Location": ["loc_US_MI"],
                        "Product": ["prd_def456"],
                    },
                    "values": {"demand_met": 3, "demand_tot": 5},
                },
            },
        },
        "kpis": {
            "data": {
                "key_1": {
                    "name": "Global Demand Met",
                    "value": 18,
                    "icon": "BsInboxes",
                    "map_kpi": True,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "units",
                    },
                },
                "key_2": {
                    "name": "Customer Happiness",
                    "value": 16,
                    "icon": "BsFillEmojiSmileFill",
                    "map_kpi": True,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "smiles",
                    },
                },
                "demand_header": {
                    "type": "head",
                    "name": "Demand Section",
                    "icon": "BsInboxes",
                },
                "demand": {
                    "name": "Global Demand",
                    "icon": "BsInboxes",
                    "numberFormat": {
                        "precision": 4,
                        "trailingZeros": True,
                        "unit": "units",
                    },
                    "value": 100,
                },
                "supply_header": {
                    "type": "head",
                    "name": "Supply Section",
                    "icon": "BsTruck",
                },
                "big_number": {
                    "name": "Big Number",
                    "icon": "BsTruck",
                    "value": 10000000000000,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "units",
                    },
                },
                "supply": {
                    "name": "Really Big Number",
                    "icon": "BsTruck",
                    "value": 9007199254740991,
                    "numberFormat": {
                        "precision": 2,
                        "unit": "$",
                        "currency": True,
                        "trailingZeros": False,
                    },
                },
            },
            "layout": {
                "type": "grid",
                "num_columns": "auto",
                "num_rows": "auto",
                "data": {
                    "col1_row1": {
                        "type": "item",
                        "itemId": "demand_header",
                        "column": 1,
                        "row": 1,
                    },
                    "col1_row2": {
                        "type": "item",
                        "itemId": "demand",
                        "column": 1,
                        "row": 2,
                    },
                    "col2_row1": {
                        "type": "item",
                        "itemId": "supply_header",
                        "column": 2,
                        "row": 1,
                    },
                    "col2_row2": {
                        "type": "item",
                        "itemId": "big_number",
                        "column": 2,
                        "row": 2,
                    },
                    "col2_row3": {
                        "type": "item",
                        "itemId": "supply",
                        "column": 2,
                        "row": 3,
                    },
                    "key_1": {
                        "type": "item",
                        "itemId": "key_1",
                    },
                    "key_2": {
                        "type": "item",
                        "itemId": "key_2",
                    },
                },
            },
        },
        "kwargs": {
            "wipe_existing": True,
        },
    }
    if command == "reset":
        return example
    if session_data:
        for key, value in session_data.items():
            example[key] = value
    return example
