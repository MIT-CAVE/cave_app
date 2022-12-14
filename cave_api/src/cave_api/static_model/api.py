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
                "sync":{
                    "mapLayers":{
                        "name": "Map Layers",
                        "showToggle": True,
                        "value": False,
                        "data":{
                            "ml1": ["map", "data", "enabledTypes"],
                            "ml2": ["nodes", "types"],
                            "ml3": ["arcs", "types"],
                            "ml4": ["geos", "types"],
                        }
                    },
                    "appBar": {
                        "name": "App Bar",
                        "showToggle": True,
                        "value": False,
                        "data": {
                            "ab1": ["appBar", "data", "dashboardId"],
                            "ab2": ["appBar", "paneState"],
                        } 
                    },
                },
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
                "location": {
                    "data": {
                        "locUsMi": {
                            "region": "North America",
                            "country": "USA",
                            "state": "Michigan",
                        },
                        "locUsMa": {
                            "region": "North America",
                            "country": "USA",
                            "state": "Massachusetts",
                        },
                        "locUsFl": {
                            "region": "North America",
                            "country": "USA",
                            "state": "Florida",
                        },
                        "locUsIn": {
                            "region": "North America",
                            "country": "USA",
                            "state": "Indiana",
                        },
                        "locCaOn": {
                            "region": "North America",
                            "country": "Canada",
                            "state": "Ontario",
                        },
                    },
                    "name": "Locations",
                    "nestedStructure": {
                        "region": {
                            "name": "Regions",
                            "order": 1,
                        },
                        "country": {
                            "name": "Countries",
                            "ordering": ["USA", "Canada"],
                            "order": 2,
                        },
                        "state": {
                            "name": "States",
                            "order": 3,
                        },
                    },
                    "layoutDirection": "horizontal",
                    "order": 1,
                },
                "sku": {
                    "data": {
                        "SKU1": {
                            "type": "Type A",
                            "size": "Size A",
                            "sku": "SKU1",
                        },
                        "SKU2": {
                            "type": "Type A",
                            "size": "Size B",
                            "sku": "SKU2",
                        },
                    },
                    "name": "SKUs",
                    "nestedStructure": {
                        "type": {
                            "name": "Types",
                            "order": 1,
                        },
                        "size": {
                            "name": "Sizing",
                            "ordering": ["Type B", "Type A"],
                            "order": 2,
                        },
                        "sku": {
                            "name": "SKU",
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
                "resetButton": {
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
                "buttonSolve": {
                    "name": "Solve Button",
                    "icon": "BsLightningFill",
                    "color": {
                        "dark": "rgb(178, 179, 55)",
                        "light": "rgb(79, 79, 24)",
                    },
                    "apiCommand": "solve",
                    "type": "button",
                    "bar": "upper",
                    "order": 2,
                },
                "examplePropsPane": {
                    "name": "Example Props Pane",
                    "props": {
                        "numericHeader": {
                            "name": "Numeric Props",
                            "type": "head",
                            "help": "Some help for numeric props",
                        },
                        "numericInputExample": {
                            "name": "Numeric Input Example",
                            "type": "num",
                            "value": 50,
                            "enabled": True,
                            "help": "Help for the numeric input example",
                            "maxValue": 100,
                            "minValue": 0,
                            "numberFormat": {
                                "precision": 0,
                                "unit": "units",
                            },
                        },
                        "numericSliderExample": {
                            "name": "Numeric Slider Example",
                            "type": "num",
                            "value": 50,
                            "enabled": True,
                            "variant": "slider",
                            "help": "Help for the numeric slider example",
                            "maxValue": 100,
                            "minValue": 0,
                        },
                        "miscHeader": {
                            "name": "Misc Props",
                            "type": "head",
                            "help": "Some help for miscelanous props",
                        },
                        "toggleInputExample": {
                            "name": "Toggle Input Example",
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "Help for the toggle input example",
                        },
                        "buttonInputExample": {
                            "name": "Button Input Example (Creates an Error)",
                            "value": "Press Me!",
                            "type": "button",
                            "apiCommand": "test",
                            "enabled": True,
                            "help": "Press this button to create an error",
                        },
                        "textInputExample": {
                            "name": "Text Input Example",
                            "type": "text",
                            "value": "Example Text Here",
                            "enabled": True,
                            "help": "Help for the text input example",
                        },
                        "selectorHeader": {
                            "name": "Selection Props",
                            "type": "head",
                            "help": "Some help for Selection Props",
                        },
                        "dropdownItemExample": {
                            "name": "Dropdown Item Example",
                            "type": "selector",
                            "variant": "dropdown",
                            "value": [
                                {"name": "Option A", "value": False},
                                {"name": "Option B", "value": False},
                                {"name": "Option C", "value": True},
                            ],
                            "enabled": True,
                            "help": "Select an option from the dropdown",
                        },
                        "checkboxItemExample": {
                            "name": "Checkbox Item Example",
                            "type": "selector",
                            "variant": "checkbox",
                            "value": [
                                {"name": "Option A", "value": True},
                                {"name": "Option B", "value": False},
                                {"name": "Option C", "value": True},
                            ],
                            "enabled": True,
                            "help": "Select all relevant items",
                        },
                        "radioItemExample": {
                            "name": "Radio Item Example",
                            "type": "selector",
                            "variant": "radio",
                            "value": [
                                {"name": "Option A", "value": True},
                                {"name": "Option B", "value": False},
                                {"name": "Option C", "value": False},
                            ],
                            "enabled": True,
                            "help": "Select one item from the list",
                        },
                    },
                    "layout": {
                        "type": "grid",
                        "num_columns": 3,
                        "num_rows": "auto",
                        "data": {
                            "col1Row1": {
                                "type": "item",
                                "column": 1,
                                "row": 1,
                                "itemId": "numericHeader",
                            },
                            "col1Row2": {
                                "type": "item",
                                "column": 1,
                                "row": 2,
                                "itemId": "numericInputExample",
                            },
                            "col1Row3": {
                                "type": "item",
                                "column": 1,
                                "row": 3,
                                "itemId": "numericSliderExample",
                            },
                            "col2Row1": {
                                "type": "item",
                                "column": 2,
                                "row": 1,
                                "itemId": "miscHeader",
                            },
                            "col2Row2": {
                                "type": "item",
                                "column": 2,
                                "row": 2,
                                "itemId": "toggleInputExample",
                            },
                            "col2Row3": {
                                "type": "item",
                                "column": 2,
                                "row": 3,
                                "itemId": "buttonInputExample",
                            },
                            "col2Row4": {
                                "type": "item",
                                "column": 2,
                                "row": 4,
                                "itemId": "textInputExample",
                            },
                            "col3Row1": {
                                "type": "item",
                                "column": 3,
                                "row": 1,
                                "itemId": "selectorHeader",
                            },
                            "col3Row2": {
                                "type": "item",
                                "column": 3,
                                "row": 2,
                                "itemId": "dropdownItemExample",
                            },
                            "col3Row3": {
                                "type": "item",
                                "column": 3,
                                "row": 3,
                                "itemId": "checkboxItemExample",
                            },
                            "col3Row4": {
                                "type": "item",
                                "column": 3,
                                "row": 4,
                                "itemId": "radioItemExample",
                            },
                        },
                    },
                    "icon": "FaCogs",
                    "type": "pane",
                    "variant": "options",
                    "bar": "upper",
                    "order": 3,
                },
                "context": {
                    "name": "Context Pane",
                    "props": {
                        "numericContextProp": {
                            "type": "num",
                            "value": 100,
                            "enabled": True,
                            "help": "Numeric Context Prop Help",
                            "label": "%",
                            "variant": "slider",
                            "maxValue": 500,
                            "minValue": 0,
                            "selectableCategories": ["location", "sku"],
                        },
                    },
                    "data": {
                        "context_1": {
                            "prop": "numericContextProp",
                            "value": 110,
                            "applyCategories": {"location": ["locUsMi"]},
                        }
                    },
                    "icon": "BsInboxes",
                    "type": "pane",
                    "variant": "context",
                    "order": 4,
                    "bar": "upper",
                },
                "filter": {
                    "icon": "FaFilter",
                    "type": "pane",
                    "variant": "filter",
                    "order": 5,
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
                            "kpi": "kpi5",
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
                "enabledTypes": {
                    "arc": {"T1": True, "T2": True},
                    "node": {"nodeTypeA": True, "nodeTypeB": True},
                    "geo": {"state": True},
                },
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
                        "name": "Legend Group A",
                        "nodeTypes": ["nodeTypeA"],
                        "arcTypes": ["T1"],
                    },
                    {
                        "name": "Legend Group B",
                        "nodeTypes": ["nodeTypeB"],
                        "arcTypes": ["T2"],
                        "geoTypes": ["state", "country"],
                    },
                ],
            },
        },
        "arcs": {
            "types": {
                "T1": {
                    "name": "Flow Type 1",
                    "colorByOptions": {
                        "selectorPropForColor": {
                            "A": "rgb(128,255,255)",
                            "B": "rgb(0,153,51)",
                            "C": "rgb(0,0,128)",
                            "D": "rgb(204,0,0)",
                            "E": "rgb(153,77,0)",
                            "F": "rgb(255,25,255)",
                        },
                        "numericPropExampleA": {
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
                        "numericPropExampleB": {
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
                    "colorBy": "numericPropExampleA",
                    "lineBy": "solid",
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 50},
                        "numericPropExampleB": {"min": 0, "max": 40},
                    },
                    "sizeBy": "numericPropExampleB",
                    "startSize": "15px",
                    "endSize": "30px",
                    "order": 1,
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "numberFormat": {
                                "unit": "A units",
                            },
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "numberFormat": {
                                "unit": "B units",
                            },
                        },
                        "selectorPropForColor": {
                            "name": "Example Categorical Prop",
                            "type": "selector",
                            "variant": "dropdown",
                            "value": [
                                {"name": "A", "value": True},
                                {"name": "B", "value": False},
                                {"name": "C", "value": False},
                                {"name": "D", "value": False},
                                {"name": "E", "value": False},
                                {"name": "F", "value": False},
                            ],
                            "enabled": True,
                        },
                    },
                    "layout": {
                        "type": "grid",
                        "num_columns": "auto",
                        "num_rows": 1,
                        "data": {
                            "col1": {"type": "item", "itemId": "numericPropExampleA", "col": 1},
                            "col2": {
                                "type": "item",
                                "itemId": "numericPropExampleB",
                                "col": 2,
                            },
                            "col3": {
                                "type": "item",
                                "itemId": "selectorPropForColor",
                                "col": 3,
                            },
                        },
                    },
                },
                "T2": {
                    "name": "Flow Type 2",
                    "colorByOptions": {
                        "selectorPropForColor": {
                            "A": "rgb(128,255,255)",
                            "B": "rgb(0,153,51)",
                            "C": "rgb(0,0,128)",
                            "D": "rgb(204,0,0)",
                            "E": "rgb(153,77,0)",
                            "F": "rgb(255,25,255)",
                        },
                        "numericPropExampleA": {
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
                        "numericPropExampleB": {
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
                    "colorBy": "numericPropExampleA",
                    "lineBy": "dotted",
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 50},
                        "numericPropExampleB": {"min": 0, "max": 40},
                    },
                    "sizeBy": "numericPropExampleB",
                    "startSize": "15px",
                    "endSize": "30px",
                    "order": 2,
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "numberFormat": {
                                "unit": "A units",
                            },
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "numberFormat": {
                                "unit": "B units",
                            },
                        },
                        "selectorPropForColor": {
                            "name": "Example Categorical Prop",
                            "type": "selector",
                            "variant": "dropdown",
                            "value": [
                                {"name": "A", "value": True},
                                {"name": "B", "value": False},
                                {"name": "C", "value": False},
                                {"name": "D", "value": False},
                                {"name": "E", "value": False},
                                {"name": "F", "value": False},
                            ],
                            "enabled": True,
                        },
                    },
                    "layout": {
                        "type": "grid",
                        "num_columns": 1,
                        "num_rows": "auto",
                        "data": {
                            "row1": {
                                "type": "item",
                                "itemId": "numericPropExampleA",
                                "row": 1,
                            },
                            "row2": {
                                "type": "item",
                                "itemId": "numericPropExampleB",
                                "row": 2,
                            },
                            "row3": {
                                "type": "item",
                                "itemId": "selectorPropForColor",
                                "row": 3,
                            },
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
                        "location": ["locCaOn", "locUsIn"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 50,
                        },
                        "numericPropExampleB": {
                            "value": 40,
                        },
                        "selectorPropForColor": {
                            "value": [
                                {"name": "A", "value": False},
                                {"name": "B", "value": True},
                                {"name": "C", "value": False},
                                {"name": "D", "value": False},
                                {"name": "E", "value": False},
                                {"name": "F", "value": False},
                            ],
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
                        "location": ["locUsMi", "locUsIn"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 30,
                        },
                        "numericPropExampleB": {
                            "value": 20,
                        },
                        "selectorPropForColor": {
                            "value": [
                                {"name": "A", "value": False},
                                {"name": "B", "value": False},
                                {"name": "C", "value": False},
                                {"name": "D", "value": False},
                                {"name": "E", "value": True},
                                {"name": "F", "value": False},
                            ],
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
                        "location": ["locUsFl", "locUsIn"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 30,
                        },
                        "numericPropExampleB": {
                            "value": 14,
                        },
                        "selectorPropForColor": {
                            "value": [
                                {"name": "A", "value": False},
                                {"name": "B", "value": False},
                                {"name": "C", "value": False},
                                {"name": "D", "value": True},
                                {"name": "E", "value": False},
                                {"name": "F", "value": False},
                            ],
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
                        "location": ["locUsMa", "locUsIn"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 30,
                        },
                        "numericPropExampleB": {
                            "value": 6,
                        },
                        "selectorPropForColor": {
                            "value": [
                                {"name": "A", "value": False},
                                {"name": "B", "value": False},
                                {"name": "C", "value": False},
                                {"name": "D", "value": False},
                                {"name": "E", "value": False},
                                {"name": "F", "value": True},
                            ],
                        },
                    },
                },
            },
        },
        "nodes": {
            "types": {
                "nodeTypeA": {
                    "name": "Node Type A",
                    "colorByOptions": {
                        "numericPropExampleA": {
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
                        "numericPropExampleB": {
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
                        "booleanPropExample": {"false": "rgb(255,0,0)", "true": "rgb(0,255,0)"},
                    },
                    "colorBy": "booleanPropExample",
                    "minSizeRange": 0,
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 80},
                        "numericPropExampleB": {"min": 0, "max": 50},
                    },
                    "sizeBy": "numericPropExampleA",
                    "startSize": "30px",
                    "endSize": "45px",
                    "icon": "MdStore",
                    "order": 2,
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "numberFormat": {
                                "unit": "A units",
                            },
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "numberFormat": {
                                "unit": "B units",
                            },
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "Help for boolean prop",
                        },
                    },
                },
                "nodeTypeB": {
                    "name": "Node Type B",
                    "colorByOptions": {
                        "numericPropExampleA": {
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
                        "numericPropExampleB": {
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
                        "booleanPropExample": {"false": "rgb(233, 0, 0)", "true": "rgb(0, 233, 0)"},
                    },
                    "colorBy": "numericPropExampleA",
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 100},
                        "numericPropExampleB": {"min": 0, "max": 250},
                    },
                    "sizeBy": "numericPropExampleB",
                    "startSize": "30px",
                    "endSize": "45px",
                    "icon": "BsBuilding",
                    "order": 1,
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "numberFormat": {
                                "unit": "A units",
                            },
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "numberFormat": {
                                "unit": "B units",
                            },
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "value": True,
                            "enabled": True,
                            "help": "Help for boolean prop",
                        },
                    },
                },
            },
            "data": {
                "node_1": {
                    "latitude": 43.78,
                    "longitude": -79.63,
                    "type": "nodeTypeA",
                    "category": {
                        "location": ["locCaOn"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 100,
                        },
                        "numericPropExampleB": {
                            "value": 50,
                        },
                        "booleanPropExample": {
                            "value": True,
                        },
                    },
                },
                "node_2": {
                    "latitude": 39.82,
                    "longitude": -86.18,
                    "type": "nodeTypeA",
                    "category": {
                        "location": ["locUsIn"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 80,
                        },
                        "numericPropExampleB": {
                            "value": 40,
                        },
                        "booleanPropExample": {
                            "value": True,
                        },
                    },
                },
                "node_3": {
                    "latitude": 42.89,
                    "longitude": -85.68,
                    "type": "nodeTypeB",
                    "category": {
                        "location": ["locUsMi"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 500,
                        },
                        "numericPropExampleB": {
                            "value": 150,
                        },
                        "booleanPropExample": {
                            "value": True,
                        },
                    },
                },
                "node_4": {
                    "latitude": 28.49,
                    "longitude": -81.56,
                    "type": "nodeTypeB",
                    "category": {
                        "location": ["locUsFl"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 1000,
                        },
                        "numericPropExampleB": {
                            "value": 250,
                        },
                        "booleanPropExample": {
                            "value": True,
                        },
                    },
                },
                "node_5": {
                    "latitude": 42.361176,
                    "longitude": -71.084707,
                    "type": "nodeTypeB",
                    "category": {
                        "location": ["locUsMa"],
                        "sku": ["SKU2", "SKU1"],
                    },
                    "props": {
                        "numericPropExampleA": {
                            "value": 1000,
                        },
                        "numericPropExampleB": {
                            "value": 250,
                        },
                        "booleanPropExample": {
                            "value": True,
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
                        "numericPropExampleC": {
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
                    "colorBy": "numericPropExampleC",
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/world-states-provinces-md.json",
                        "geoJsonProp": "code_hasc",
                    },
                    "icon": "BsHexagon",
                    "props": {
                        "numericPropExampleC": {
                            "name": "Numeric Prop Example C",
                            "type": "num",
                            "enabled": True,
                            "help": "Help with the example numeric prop for this State",
                            "numberFormat": {
                                "unit": "C units",
                            },
                        },
                    },
                },
                "country": {
                    "name": "Country",
                    "colorByOptions": {
                        "numericPropExampleC": {
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
                    "colorBy": "numericPropExampleC",
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/countries-sm.json",
                        "geoJsonProp": "FIPS_10",
                    },
                    "icon": "BsHexagon",
                    "props": {
                        "numericPropExampleC": {
                            "name": "Numeric Prop Example C",
                            "type": "num",
                            "enabled": True,
                            "help": "Help with the example numeric prop for this Country",
                            "numberFormat": {
                                "unit": "units",
                            },
                        },
                    },
                },
            },
            "data": {
                "geo1": {
                    "name": "Ontario, Canada",
                    "geoJsonValue": "CA.ON",
                    "type": "state",
                    "category": {"location": ["locCaOn"]},
                    "props": {
                        "numericPropExampleC": {
                            "value": 50,
                        }
                    },
                },
                "geo2": {
                    "name": "Michigan, USA",
                    "geoJsonValue": "US.MI",
                    "type": "state",
                    "category": {"location": ["locUsMi"]},
                    "props": {
                        "numericPropExampleC": {
                            "value": 300,
                        }
                    },
                },
                "geo3": {
                    "name": "Massachusetts, USA",
                    "geoJsonValue": "US.MA",
                    "type": "state",
                    "category": {"location": ["locUsMi"]},
                    "props": {
                        "numericPropExampleC": {
                            "value": 250,
                        }
                    },
                },
                "geo4": {
                    "name": "Florida, USA",
                    "geoJsonValue": "US.FL",
                    "type": "state",
                    "category": {"location": ["locUsMi"]},
                    "props": {
                        "numericPropExampleC": {
                            "value": 100,
                        }
                    },
                },
                "geo5": {
                    "name": "Indiana, USA",
                    "geoJsonValue": "US.FL",
                    "type": "state",
                    "category": {"location": ["locUsMi"]},
                    "props": {
                        "numericPropExampleC": {
                            "value": 200,
                        }
                    },
                },
                "geoCountry1": {
                    "name": "Canada",
                    "geoJsonValue": "CA",
                    "type": "country",
                    "category": {"location": ["locCaOn"]},
                    "props": {
                        "numericPropExampleC": {
                            "value": 50,
                        }
                    },
                },
                "geoCountry2": {
                    "name": "USA",
                    "geoJsonValue": "US",
                    "type": "country",
                    "category": {
                        "location": [
                            "locUsFl",
                            "locUsMa",
                            "locUsIn",
                            "locUsMi",
                        ]
                    },
                    "props": {
                        "numericPropExampleC": {
                            "value": 800,
                        }
                    },
                },
            },
        },
        "stats": {
            "types": {
                "numericStatExampleA": {
                    "name": "Stat Example A",
                    "calculation": "numericStatExampleA",
                    "numberFormat": {
                        "unit": "units",
                    },
                    "order": 1,
                },
                "numericStatExampleB": {
                    "name": "Stat Example B",
                    "calculation": "numericStatExampleB",
                    "numberFormat": {
                        "unit": "units",
                    },
                    "order": 2,
                },
                "numericExampleCalculationStat": {
                    "name": "Stat A as a percentage of Stat B",
                    "calculation": 'numericStatExampleA / groupSum("numericStatExampleB")',
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
                        "location": ["locCaOn"],
                        "sku": ["SKU1"],
                    },
                    "values": {"numericStatExampleA": 5, "numericStatExampleB": 10},
                },
                "d2": {
                    "category": {
                        "location": ["locCaOn"],
                        "sku": ["SKU2"],
                    },
                    "values": {"numericStatExampleA": 4, "numericStatExampleB": 5},
                },
                "d3": {
                    "category": {
                        "location": ["locUsMi"],
                        "sku": ["SKU1"],
                    },
                    "values": {"numericStatExampleA": 6, "numericStatExampleB": 7},
                },
                "d4": {
                    "category": {
                        "location": ["locUsMi"],
                        "sku": ["SKU2"],
                    },
                    "values": {"numericStatExampleA": 3, "numericStatExampleB": 5},
                },
            },
        },
        "kpis": {
            "data": {
                "kpiHeader1": {
                    "type": "head",
                    "name": "Example KPI Header 1",
                    "icon": "BsInboxes",
                },
                "kpiHeader2": {
                    "type": "head",
                    "name": "Example KPI Header 2",
                    "icon": "BsTruck",
                },
                "key1": {
                    "name": "KPI Example 1",
                    "value": 18,
                    "icon": "BsFillEmojiFrownFill",
                    "map_kpi": True,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "frowns",
                    },
                },
                "key2": {
                    "name": "KPI Example 2",
                    "value": 32,
                    "icon": "BsFillEmojiSmileFill",
                    "map_kpi": True,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "smiles",
                    },
                },
                "key3": {
                    "name": "KPI Example 3",
                    "icon": "BsInboxes",
                    "numberFormat": {
                        "precision": 4,
                        "trailingZeros": True,
                        "unit": "units",
                    },
                    "value": 100,
                },
                "key4": {
                    "name": "A Big Number",
                    "icon": "BsTruck",
                    "value": 10000000000000,
                    "numberFormat": {
                        "precision": 0,
                        "unit": "units",
                    },
                },
                "key5": {
                    "name": "A Really Big Number",
                    "icon": "MdExpand",
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
                    "col1Row1": {
                        "type": "item",
                        "itemId": "kpiHeader1",
                        "column": 1,
                        "row": 1,
                    },
                    "col1Row2": {
                        "type": "item",
                        "itemId": "key1",
                        "column": 1,
                        "row": 2,
                    },
                    "col1Row3": {
                        "type": "item",
                        "itemId": "key4",
                        "column": 1,
                        "row": 3,
                    },
                    "col1Row4": {
                        "type": "item",
                        "itemId": "key5",
                        "column": 1,
                        "row": 4,
                    },
                    "col2Row1": {
                        "type": "item",
                        "itemId": "kpiHeader2",
                        "column": 2,
                        "row": 1,
                    },
                    "col2Row2": {
                        "type": "item",
                        "itemId": "key2",
                        "column": 2,
                        "row": 2,
                    },
                    "col2Row3": {
                        "type": "item",
                        "itemId": "key3",
                        "column": 2,
                        "row": 3,
                    },
                },
            },
        },
        "kwargs": {
            "wipe_existing": True,
        },
    }
    if command == "reset":
        print("The `reset` button has been pressed by the user!")
        return example
    elif command == "solve":
        print("The `solve` button has been pressed by the user!")
    elif command == "test":
        print("The `test` button has been pressed by the user!")
        raise Exception('Test Exception!')
    if session_data:
        for key, value in session_data.items():
            example[key] = value
    return example
