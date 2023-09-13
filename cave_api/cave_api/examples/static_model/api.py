import time


def execute_command(session_data, socket, command="init", **kwargs):
    """
    Usage:
    - Execute a command to mutate the current session_data

    Requires:

    - `session_data`:
        - Type: dict
        - What: A dict of `session_data` objects to use when configuring this session
        - See: https://github.com/MIT-CAVE/cave_app/blob/0.2.0/cave_api/README_API_STRUCTURE.md

    - `socket`:
        - Type: Initialized Socket Object
        - What: A socket object to use to communicate with clients (or print to the console if testing)
        - Methods:
            - `notify`:
                - Requires:
                    - `message`:
                        - Type: str
                        - What: The message to display to the user
                - Optional:
                    - `title`:
                        - Type: str
                        - What: The title of the message
                    - `show`:
                        - Type: bool
                        - What: Whether or not to show the message
                        - Default: True
                    - `theme`:
                        - Type: str
                        - What: The theme of the message
                        - Default: "info"
                        - Allowed Values: "primary", "secondary", "error", "warning", "info", "success"
                    - `duration`:
                        - Type: int
                        - What: The duration in seconds to show the message
                        - Default: 10
                    - `**kwargs`:
                        - Type: dict (json serializable)
                        - What: Any additional data to serialize and pass to the user
                - EG: socket.notify(message="Hello World!", title="Hello:", show=True, theme="info", duration=10)
        - Note: This comes from one of the following places:
            - If you are running the cave server:
                - your_app.cave_core.utils.broadcasting.Socket
            - If you are running non server tests:
                - cave_utils.socket.Socket
                    - See: https://github.com/MIT-CAVE/cave_utils/blob/main/cave_utils/socket.py
                    - EG: https://github.com/MIT-CAVE/cave_app/blob/main/cave_api/tests/test_init.py
                - Your own custom socket object with a `notify` method accepting the same arguments as the method described above


    Optional:

    - `command`:
        - Type: str
        - What: A string to indicate a command to be processed by the api
        - Default: 'init'

    Returns:

    - `output`:
        - Type: dict of dicts
        - What: A dict of dictionaries to mutate the current session given the current `session_data`
        - See: https://github.com/MIT-CAVE/cave_app/blob/main/cave_api/README_API_STRUCTURE.md
    """
    example = {
        "settings": {
            "allowModification": False,
            "data": {
                "demo": {
                    "map1": {
                        "scrollSpeed": 0.1,
                    },
                    "dash1": {
                        "displayTime": 30,
                    },
                },
                "sync": {
                    "appBar": {
                        "name": "App Bar",
                        "showToggle": True,
                        "value": False,
                        "data": {
                            "ab1": ["appBar", "paneState"],
                        },
                    },
                    "pageSelection": {
                        "name": "Page Selection",
                        "showToggle": True,
                        "value": False,
                        "data": {"ps1": ["appBar", "appBarId"]},
                    },
                    "mapLayers": {
                        "name": "Map Layers",
                        "showToggle": True,
                        "value": False,
                        "data": {"ml1": ["maps", "data", "map1", "legendGroups"]},
                    },
                    "dashboards": {
                        "name": "Dashboards",
                        "showToggle": True,
                        "value": False,
                        "data": {"db1": ["dashboards", "data"]},
                    },
                },
                "iconUrl": "https://react-icons.mitcave.com/4.10.1",
                "numberFormat": {
                    "precision": 4,
                    "trailingZeros": False,
                    "unitPlacement": "afterWithSpace",
                },
                "additionalMapStyles": {
                    "watercolor": {
                        "name": "Watercolor",
                        "icon": "md/MdBrush",
                        "order": 1,
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
                    "streets": {
                        "name": "Streets",
                        "icon": "md/MdStreetview",
                        "order": 2,
                        "spec": "mapbox://styles/mapbox/streets-v12",
                    },
                    "outdoors": {
                        "name": "Outdoors",
                        "icon": "md/MdForest",
                        "order": 3,
                        "spec": "mapbox://styles/mapbox/outdoors-v12",
                    },
                    "satellite": {
                        "name": "Satellite",
                        "icon": "md/MdSatelliteAlt",
                        "order": 4,
                        "spec": "mapbox://styles/mapbox/satellite-v9",
                    },
                    "satellite_streets": {
                        "name": "Satellite Streets",
                        "icon": "md/MdSatellite",
                        "order": 5,
                        "spec": "mapbox://styles/mapbox/satellite-streets-v12",
                    },
                },
                "debug": True,
                "timeLength": 3,
                "timeUnits": "Century",
            },
        },
        "appBar": {
            "appBarId": "dash1",
            "data": {
                "session": {
                    "icon": "md/MdApi",
                    "type": "session",
                    "bar": "upperLeft",
                    "order": 0,
                },
                "appSettings": {
                    "icon": "md/MdOutlineSettings",
                    "type": "settings",
                    "bar": "upperLeft",
                    "order": 1,
                },
                "resetButton": {
                    "icon": "md/MdSync",
                    "color": "rgba(255, 101, 101, 255)",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                    "order": 2,
                },
                "buttonSolve": {
                    "icon": "bs/BsLightningFill",
                    "color": "rgba(178, 179, 55, 255)",
                    "apiCommand": "solve",
                    "type": "button",
                    "bar": "upperLeft",
                    "order": 3,
                },
                "examplePropsPane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "bar": "upperLeft",
                    "order": 4,
                },
                "dash1": {
                    "type": "page",
                    "icon": "md/MdInsertChart",
                    "order": 1,
                    "bar": "lowerLeft",
                },
                "dash2": {
                    "type": "page",
                    "icon": "md/MdInsertChartOutlined",
                    "order": 2,
                    "bar": "lowerLeft",
                },
                "exampleModal": {
                    "icon": "md/MdInfo",
                    "color": "rgba(195, 164, 222, 255)",
                    "type": "modal",
                    "bar": "upperRight",
                    "order": 0,
                },
            },
        },
        "modals": {
            "data": {
                "exampleModal": {
                    "name": "Example Modal",
                    "props": {
                        "buttonViewInfo": {
                            "name": "Info Button",
                            "type": "button",
                            "apiCommand": "viewInfo",
                            "enabled": True,
                            "help": "Press this button to view info",
                        },
                    },
                    "values": {
                        "buttonViewInfo": "Press",
                    },
                    "layout": {
                        "type": "grid",
                        "numColumns": 1,
                        "numRows": 1,
                        "data": {
                            "col1Row1": {
                                "type": "item",
                                "column": 1,
                                "row": 1,
                                "itemId": "buttonViewInfo",
                            },
                        },
                    },
                },
            },
        },
        "panes": {
            "data": {
                "examplePropsPane": {
                    "name": "Example Props Pane",
                    "variant": "options",
                    "props": {
                        "numericHeader": {
                            "name": "Numeric Props",
                            "type": "head",
                            "help": "Some help for numeric props",
                        },
                        "numericInputExample": {
                            "name": "Numeric Input Example",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for the numeric input example",
                            "maxValue": 100,
                            "minValue": 0,
                            "notation": "scientific",
                            "notationDisplay": "x10^+",
                            "precision": 0,
                            "unit": "units",
                        },
                        "numericSliderExample": {
                            "name": "Numeric Slider Example",
                            "type": "num",
                            "enabled": True,
                            "variant": "slider",
                            "help": "Help for the numeric slider example",
                            "maxValue": 100,
                            "minValue": 0,
                            "unit": "%",
                        },
                        "miscHeader": {
                            "name": "Misc Props",
                            "type": "head",
                            "help": "Some help for miscelanous props",
                        },
                        "toggleInputExample": {
                            "name": "Toggle Input Example",
                            "type": "toggle",
                            "enabled": True,
                            "help": "Help for the toggle input example",
                        },
                        "buttonInputExample": {
                            "name": "Button Input Example (Creates an Error)",
                            "type": "button",
                            "apiCommand": "test",
                            "enabled": True,
                            "help": "Press this button to create an error",
                        },
                        "pictureExample": {
                            "name": "Picture Example",
                            "type": "media",
                            "variant": "picture",
                            "help": "Click the expand button to view an enlarged version",
                        },
                        "videoExample": {
                            "name": "Video Example",
                            "type": "media",
                            "variant": "video",
                            "help": "Click the play button to start the video",
                        },
                        "textHeader": {
                            "name": "Text Props",
                            "type": "head",
                            "help": "Some help for Text Props",
                        },
                        "textInputExample": {
                            "name": "Text Input Example",
                            "type": "text",
                            "enabled": True,
                            "help": "Help for the text input example",
                        },
                        "textAreaInputExample": {
                            "name": "TextArea Input Example",
                            "type": "text",
                            "variant": "textarea",
                            "rows": 6,
                            "enabled": True,
                            "help": "Help for the text area input example",
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
                            "options": {
                                "option_a": {"name": "Option A"},
                                "option_b": {"name": "Option B"},
                                "option_c": {"name": "Option C"},
                            },
                            "enabled": True,
                            "help": "Select an option from the dropdown",
                        },
                        "checkboxItemExample": {
                            "name": "Checkbox Item Example",
                            "type": "selector",
                            "variant": "checkbox",
                            "options": {
                                "option_a": {"name": "Option A"},
                                "option_b": {"name": "Option B"},
                                "option_c": {"name": "Option C"},
                            },
                            "enabled": True,
                            "help": "Select all relevant items",
                        },
                        "radioItemExample": {
                            "name": "Radio Item Example",
                            "type": "selector",
                            "variant": "radio",
                            "options": {
                                "option_a": {"name": "Option A"},
                                "option_b": {"name": "Option B"},
                                "option_c": {"name": "Option C"},
                            },
                            "enabled": True,
                            "help": "Select one item from the list",
                        },
                        "hstepperItemExample": {
                                "name": "Horizontal Stepper Item Example",
                                "type": "selector",
                                "variant": "hstepper",
                                "options": {
                                    "option_a": {"name": "Option A"},
                                    "option_b": {"name": "Option B"},
                                    "option_c": {"name": "Option C"},
                                    },
                                "enabled": True,
                                "help": "Select an option from the stepper",
                        },
                        "vstepperItemExample": {
                                "name": "Vertical Stepper Item Example",
                                "type": "selector",
                                "variant": "vstepper",
                                "options": {
                                    "option_a": {"name": "Option A"},
                                    "option_b": {"name": "Option B"},
                                    "option_c": {"name": "Option C"},
                                    },
                                "enabled": True,
                                "help": "Select an option from the stepper",
                        },
                        "hradioItemExample": {
                                "name": "Horizontal Radio Item Example",
                                "type": "selector",
                                "variant": "hradio",
                                "options": {
                                    "option_a": {"name": "Option A"},
                                    "option_b": {"name": "Option B"},
                                    "option_c": {"name": "Option C"},
                                    },
                                "enabled": True,
                                "help": "Select an option from the radio",
                        },
                        "comboBoxItemExample": {
                            "name": "ComboBox Item Example",
                            "type": "selector",
                            "variant": "combobox",
                            "placeholder": "Option",
                            "options": {
                                "option_a": {"name": "Option A"},
                                "option_b": {"name": "Option B"},
                                "option_c": {"name": "Option C"},
                            },
                            "enabled": True,
                            "help": "Select an option from the combobox",
                        },
                        "nestedItemExample": {
                            "name": "Nested Item Example",
                            "type": "selector",
                            "variant": "nested",
                            "options": {
                                "t1_b1_tw1": {"name": "Twig1", "path": ['Tree1', 'Branch1']},
                                "t1_b1_tw2": {"name": "Twig2", "path": ['Tree1', 'Branch1']},
                                "t1_b1_tw3": {"name": "Twig3", "path": ['Tree1', 'Branch1']},
                                "t1_b2_tw1": {"name": "Twig1", "path": ['Tree1', 'Branch2']},
                                "t1_b2_tw2": {"name": "Twig2", "path": ['Tree1', 'Branch2']},
                                "t2_b1_tw1": {"name": "Twig1", "path": ['Tree2', 'Branch1']},
                                "t2_b1_tw2": {"name": "Twig2", "path": ['Tree2', 'Branch1']},
                                "t2_b2_tw1": {"name": "Twig1", "path": ['Tree2', 'Branch2']},
                                "t2_b2_tw2": {"name": "Twig2", "path": ['Tree2', 'Branch2']},
                            },
                            "enabled": True,
                            "help": "Select all relevant items",
                        },
                        "dateTimeHeader": {
                            "name": "Date and Time Props",
                            "type": "head",
                            "help": "Some help for Date and Time Props",
                        },
                        "dateItemExample": {
                            "name": "Date Example",
                            "type": "date",
                            "variant": "date",
                            "enabled": True,
                            "help": "The Eagle has landed!",
                        },
                        "timeItemExample": {
                            "name": "Time Example",
                            "type": "date",
                            "variant": "time",
                            "enabled": True,
                            "help": "The Eagle has landed!",
                        },
                        "dateTimeItemExample": {
                            "name": "Date and Time Example",
                            "type": "date",
                            "variant": "datetime",
                            "enabled": True,
                            "help": "The Eagle has landed!",
                        },
                    },
                    "values": {
                        "numericInputExample": 50,
                        "numericSliderExample": 50,
                        "toggleInputExample": True,
                        "buttonInputExample": "Press Me!",
                        "pictureExample": "https://ctl.mit.edu/sites/ctl.mit.edu/files/inline-images/MIT_CTL_CAVE_Lab_2.png",
                        "videoExample": "https://www.youtube.com/embed/6q5R1TDmKnU",
                        "textInputExample": "Example Text Here",
                        "textAreaInputExample": "Velit non incididunt velit quis commodo consequat velit nulla. Id sunt sint consequat do in. Et adipisicing aliqua voluptate eu consequat et dolore mollit sit veniam minim nisi tempor. Enim laboris proident ex magna. Duis culpa veniam et officia irure id qui id ad laborum deserunt dolor proident elit.",
                        "dropdownItemExample": ["option_c"],
                        "checkboxItemExample": ["option_a", "option_c"],
                        "radioItemExample": ["option_a"],
                        "hstepperItemExample": ["option_c"],
                        "vstepperItemExample": ["option_c"],
                        "hradioItemExample": ["option_c"],
                        "comboBoxItemExample": ["option_b"],
                        "nestedItemExample": ["t1_b1_tw1", "t1_b1_tw2", "t1_b2_tw2", "t2_b1_tw1", "t2_b1_tw2"],
                        "dateItemExample": "07/20/1969",
                        "timeItemExample": "1969-07-20T20:17:40",
                        "dateTimeItemExample": "1969-07-20T20:17:40",
                    },
                    "layout": {
                        "type": "grid",
                        "numColumns": 5,
                        "numRows": "auto",
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
                                "itemId": "textHeader",
                            },
                            "col2Row2": {
                                "type": "item",
                                "column": 2,
                                "row": 2,
                                "itemId": "textInputExample",
                            },
                            "col2Row3": {
                                "type": "item",
                                "column": 2,
                                "row": 3,
                                "itemId": "textAreaInputExample",
                            },
                            "col3Row1": {
                                "type": "item",
                                "column": 3,
                                "row": 1,
                                "itemId": "miscHeader",
                            },
                            "col3Row2": {
                                "type": "item",
                                "column": 3,
                                "row": 2,
                                "itemId": "toggleInputExample",
                            },
                            "col3Row3": {
                                "type": "item",
                                "column": 3,
                                "row": 3,
                                "itemId": "buttonInputExample",
                            },
                            "col3Row4": {
                                "type": "item",
                                "column": 3,
                                "row": 4,
                                "itemId": "pictureExample",
                            },
                            "col3Row5": {
                                "type": "item",
                                "column": 3,
                                "row": 5,
                                "itemId": "videoExample",
                            },
                            "col4Row1": {
                                "type": "item",
                                "column": 4,
                                "row": 1,
                                "itemId": "selectorHeader",
                            },
                            "col4Row2": {
                                "type": "item",
                                "column": 4,
                                "row": 2,
                                "itemId": "dropdownItemExample",
                            },
                            "col4Row3": {
                                "type": "item",
                                "column": 4,
                                "row": 3,
                                "itemId": "checkboxItemExample",
                            },
                            "col4Row4": {
                                "type": "item",
                                "column": 4,
                                "row": 4,
                                "itemId": "radioItemExample",
                            },
                            "col4Row5": {
                                "type": "item",
                                "column": 4,
                                "row": 5,
                                "itemId": "comboBoxItemExample",
                            },
                            "col4Row6": {
                                "type": "item",
                                "column": 4,
                                "row": 6,
                                "itemId": "hstepperItemExample",
                            },
                            "col4Row7": {
                                "type": "item",
                                "column": 4,
                                "row": 7,
                                "itemId": "vstepperItemExample",
                            },
                            "col4Row8": {
                                "type": "item",
                                "column": 4,
                                "row": 8,
                                "itemId": "hradioItemExample",
                            },
                            "col4Row9": {
                                "type": "item",
                                "column": 4,
                                "row": 9,
                                "itemId": "nestedItemExample",
                            },
                            "col5Row1": {
                                "type": "item",
                                "column": 5,
                                "row": 1,
                                "itemId": "dateTimeHeader",
                            },
                            "col5Row2": {
                                "type": "item",
                                "column": 5,
                                "row": 2,
                                "itemId": "dateItemExample",
                            },
                            "col5Row3": {
                                "type": "item",
                                "column": 5,
                                "row": 3,
                                "itemId": "timeItemExample",
                            },
                            "col5Row4": {
                                "type": "item",
                                "column": 5,
                                "row": 4,
                                "itemId": "dateTimeItemExample",
                            },
                        },
                    },
                },
            },
        },
        "pages": {
            "data": {
                "dash1": {
                    "pageLayout": [
                        {
                            "chart": "Bar",
                            "grouping": "Average",
                        },
                        {
                            "type": "maps",
                            "mapId": "map1"
                        },
                        {
                            "chart": "Bar",
                            "level": ["size"],
                            "category": ["sku"],
                            "grouping": "Sum",
                            "statistic": ["locationGroup", "numericExampleCalculationStat"],
                        },
                    ],
                    "lockedLayout": False,
                },
                "dash2": {
                    "pageLayout": [
                        {
                            "chart": "Bar",
                            "grouping": "Average",
                            "statistic": ["locationGroup", "numericStatExampleB"],
                        },
                        {
                            "type": "globalOutputs",
                            "chart": "Bar",
                            "grouping": "Sum",
                            "sessions": [],
                            "globalOutput": ["key1", "key2"],
                        },
                        {
                            "chart": "Box Plot",
                            "level": ["size"],
                            "category": ["sku"],
                            "grouping": "Average",
                            "statistic": ["locationGroup", "numericExampleCalculationStat"],
                        },
                        {
                            "chart": "Cumulative Line",
                            "grouping": "Sum",
                            "statistic": ["locationGroup", "numericStatExampleB"],
                            "category": ["location", "sku"],
                            "level": ["state", "sku"],
                        },
                    ],
                    "lockedLayout": False,
                },
            }
        },
        "maps": {
            "data": {
                "map1": {
                    "name": "Example Map 1",
                    "currentStyle": "watercolor",
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
                    "optionalViewports": {
                        "ov0": {
                            "icon": "fa/FaGlobeAsia",
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
                            "icon": "fa/FaGlobeEurope",
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
                    "legendGroups": {
                        "lga": {
                            "name": "Legend Group A",
                            "data": {
                                "nodeTypeA": {
                                    "type": "nodes",
                                    "value": True,
                                    "sizeBy": "numericPropExampleA",
                                    "colorBy": "booleanPropExample",
                                    "allowGrouping": True,
                                    "group": True,
                                    "groupCalcBySize": "sum",
                                    "groupCalcByColor": "mode",
                                    # "groupScaleWithZoom": True,
                                    # # Equivalent to zoom level unless groupScale is set
                                    # "groupScale": 10,
                                    "colorByOptions": {
                                        "numericPropExampleA": {
                                            "timeValues": {
                                                0: {"min": 50},
                                                1: {"min": 0},
                                                2: {"min": 20},
                                            },
                                            "max": 80,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "booleanPropExample": {
                                            "false": "rgba(255,0,0, 255)",
                                            "true": "rgba(0,255,0, 255)",
                                        },
                                    },
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 80},
                                        "numericPropExampleB": {"min": 0, "max": 50},
                                    },
                                    "startSize": "30px",
                                    "endSize": "45px",
                                    "icon": "fa6/FaIgloo",
                                },
                                "T1": {
                                    "type": "arcs",
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 50},
                                        "numericPropExampleB": {"min": 0, "max": 40},
                                    },
                                    "startSize": "15px",
                                    "endSize": "30px",
                                    "colorByOptions": {
                                        "selectorPropForColor": {
                                            "a": "rgba(128,255,255, 255)",
                                            "b": "rgba(0,153,51, 255)",
                                            "c": "rgba(0,0,128, 255)",
                                            "d": "rgba(204,0,0, 255)",
                                            "e": "rgba(153,77,0, 255)",
                                            "f": "rgba(255,25,255, 255)",
                                        },
                                        "numericPropExampleA": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 40,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                    },
                                },
                            },
                            "order": 1,
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "data": {
                                "nodeTypeB": {
                                    "type": "nodes",
                                    "value": True,
                                    "sizeBy": "numericPropExampleB",
                                    "colorBy": "booleanPropExample",
                                    "allowGrouping": True,
                                    "group": True,
                                    "groupCalcBySize": "count",
                                    "groupCalcByColor": "and",
                                    # "groupScaleWithZoom": True,
                                    # # Equivalent to zoom level unless groupScale is set
                                    # "groupScale": 10,
                                    "colorByOptions": {
                                        "numericPropExampleA": {
                                            "min": 0,
                                            "max": 1000,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                            
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "booleanPropExample": {
                                            "false": "rgba(233, 0, 0, 255)",
                                            "true": "rgba(0, 233, 0, 255)",
                                        },
                                    },
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 100},
                                        "numericPropExampleB": {"min": 0, "max": 250},
                                    },
                                    "startSize": "30px",
                                    "endSize": "45px",
                                    "icon": "bs/BsBuilding",
                                },
                                "T2": {
                                    "type": "arcs",
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "colorByOptions": {
                                        "selectorPropForColor": {
                                            "a": "rgba(128,255,255, 255)",
                                            "b": "rgba(0,153,51, 255)",
                                            "c": "rgba(0,0,128, 255)",
                                            "d": "rgba(204,0,0, 255)",
                                            "e": "rgba(153,77,0, 255)",
                                            "f": "rgba(255,25,255, 255)",
                                        },
                                        "numericPropExampleA": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 40,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                    },
                                    "lineBy": "dotted",
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 50},
                                        "numericPropExampleB": {"min": 0, "max": 40},
                                    },
                                    "startSize": "15px",
                                    "endSize": "30px",
                                },
                                "state": {
                                    "type": "geos",
                                    "value": True,
                                    "colorBy": "numericPropExampleC",
                                    "colorByOptions": {
                                        "numericPropExampleC": {
                                            "min": 0,
                                            "max": 300,
                                            "startGradientColor": "rgba(100, 100, 100, 255)",
                                            "endGradientColor": "rgba(20, 205, 20, 255)",
                                        },
                                        "booleanPropExample": {
                                            "false": "rgba(233, 0, 0, 255)",
                                            "true": "rgba(0, 233, 0, 255)",
                                        },
                                    }, 
                                    "icon": "bs/BsHexagon",
                                },
                                "country": {
                                    "type": "geos",
                                    "value": False,
                                    "colorBy": "numericPropExampleC",
                                    "colorByOptions": {
                                        "numericPropExampleC": {
                                            "min": 0,
                                            "max": 800,
                                            "startGradientColor": "rgba(100, 100, 100, 255)",
                                            "endGradientColor": "rgba(20, 205, 20, 255)",
                                        }
                                    },
                                "icon": "bs/BsHexagon",
                                },
                            },
                            "order": 2,
                        },
                    },
                },
                "map2": {
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
                    "optionalViewports": {
                        "ov0": {
                            "icon": "fa/FaGlobeAsia",
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
                            "icon": "fa/FaGlobeEurope",
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
                    "legendGroups": {
                        "lga": {
                            "name": "Legend Group A",
                            "data": {
                                "nodeTypeA": {
                                    "type": "nodes",
                                    "value": True,
                                    "sizeBy": "numericPropExampleA",
                                    "colorBy": "booleanPropExample",
                                    "colorByOptions": {
                                        "numericPropExampleA": {
                                            "timeValues": {
                                                0: {"min": 50},
                                                1: {"min": 0},
                                                2: {"min": 20},
                                            },
                                            "max": 80,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "booleanPropExample": {
                                            "false": "rgba(255,0,0, 255)",
                                            "true": "rgba(0,255,0, 255)",
                                        },
                                    },
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 80},
                                        "numericPropExampleB": {"min": 0, "max": 50},
                                    },
                                    "startSize": "30px",
                                    "endSize": "45px",
                                    "icon": "fa6/FaIgloo",
                                },
                                "T1": {
                                    "type": "arcs",
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 50},
                                        "numericPropExampleB": {"min": 0, "max": 40},
                                    },
                                    "startSize": "15px",
                                    "endSize": "30px",
                                    "colorByOptions": {
                                        "selectorPropForColor": {
                                            "a": "rgba(128,255,255, 255)",
                                            "b": "rgba(0,153,51, 255)",
                                            "c": "rgba(0,0,128, 255)",
                                            "d": "rgba(204,0,0, 255)",
                                            "e": "rgba(153,77,0, 255)",
                                            "f": "rgba(255,25,255, 255)",
                                        },
                                        "numericPropExampleA": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 40,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                    },
                                },                                
                            },
                            "order": 1,
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "data": {
                                "nodeTypeB": {
                                    "type": "nodes",
                                    "value": True,
                                    "sizeBy": "numericPropExampleB",
                                    "colorBy": "booleanPropExample",
                                    "colorByOptions": {
                                        "numericPropExampleA": {
                                            "min": 0,
                                            "max": 1000,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "booleanPropExample": {
                                            "false": "rgba(233, 0, 0, 255)",
                                            "true": "rgba(0, 233, 0, 255)",
                                        },
                                    },
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 100},
                                        "numericPropExampleB": {"min": 0, "max": 250},
                                    },
                                    "startSize": "30px",
                                    "endSize": "45px",
                                    "icon": "bs/BsBuilding",
                                },
                                "T2": {
                                    "type": "arcs",
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "colorByOptions": {
                                        "selectorPropForColor": {
                                            "a": "rgba(128,255,255, 255)",
                                            "b": "rgba(0,153,51, 255)",
                                            "c": "rgba(0,0,128, 255)",
                                            "d": "rgba(204,0,0, 255)",
                                            "e": "rgba(153,77,0, 255)",
                                            "f": "rgba(255,25,255, 255)",
                                        },
                                        "numericPropExampleA": {
                                            "min": 0,
                                            "max": 50,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                        "numericPropExampleB": {
                                            "min": 0,
                                            "max": 40,
                                            "startGradientColor": "rgba(233, 0, 0, 255)",
                                            "endGradientColor": "rgba(96, 2, 2, 255)",
                                        },
                                    },
                                    "lineBy": "dotted",
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 50},
                                        "numericPropExampleB": {"min": 0, "max": 40},
                                    },
                                    "startSize": "15px",
                                    "endSize": "30px",
                                },
                                "state": {
                                    "type": "geos",
                                    "value": True,
                                    "colorBy": "numericPropExampleC",
                                    "colorByOptions": {
                                        "numericPropExampleC": {
                                            "min": 0,
                                            "max": 300,
                                            "startGradientColor": "rgba(100, 100, 100, 255)",
                                            "endGradientColor": "rgba(20, 205, 20, 255)",
                                        },
                                        "booleanPropExample": {
                                            "false": "rgba(233, 0, 0, 255)",
                                            "true": "rgba(0, 233, 0, 255)",
                                        },
                                    }, 
                                    "icon": "bs/BsHexagon",
                                },
                                "country": {
                                    "type": "geos",
                                    "value": False,
                                    "colorBy": "numericPropExampleC",
                                    "colorByOptions": {
                                        "numericPropExampleC": {
                                            "min": 0,
                                            "max": 800,
                                            "startGradientColor": "rgba(100, 100, 100, 255)",
                                            "endGradientColor": "rgba(20, 205, 20, 255)",
                                        }
                                    },
                                    "icon": "bs/BsHexagon",
                                },
                            },
                            "order": 2,
                        },
                    },
                },
            },
        },
        "arcs": {
            "types": {
                "T1": {
                    "name": "Flow Type 1",
                    "geoJson": {
                        "geoJsonLayer": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart.geo.json",
                        "geoJsonProp": "name",
                    },
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "unit": "A units",
                            "legendNotation": "compact",
                            "legendMinLabel": "small",
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "unit": "B units",
                        },
                        "selectorPropForColor": {
                            "name": "Example Categorical Prop",
                            "type": "selector",
                            "variant": "dropdown",
                            "options": {
                                "a": {"name": "A"},
                                "b": {"name": "B"},
                                "c": {"name": "C"},
                                "d": {"name": "D"},
                                "e": {"name": "E"},
                                "f": {"name": "F"},
                            },
                            "enabled": True,
                        },
                    },
                    "values": {
                        "selectorPropForColor": ["a"],
                    },
                    "layout": {
                        "type": "grid",
                        "numColumns": "auto",
                        "numRows": 1,
                        "data": {
                            "col1": {
                                "type": "item",
                                "itemId": "numericPropExampleA",
                                "column": 1,
                            },
                            "col2": {
                                "type": "item",
                                "itemId": "numericPropExampleB",
                                "column": 2,
                            },
                            "col3": {
                                "type": "item",
                                "itemId": "selectorPropForColor",
                                "column": 3,
                            },
                        },
                    },
                },
                "T2": {
                    "name": "Flow Type 2",
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "unit": "A units",
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "unit": "B units",
                        },
                        "selectorPropForColor": {
                            "name": "Example Categorical Prop",
                            "type": "selector",
                            "variant": "dropdown",
                            "options": {
                                "a": {"name": "A"},
                                "b": {"name": "B"},
                                "c": {"name": "C"},
                                "d": {"name": "D"},
                                "e": {"name": "E"},
                                "f": {"name": "F"},
                            },
                            "enabled": True,
                        },
                    },
                    "values": {
                        "selectorPropForColor": ["a"],
                    },
                    "layout": {
                        "type": "grid",
                        "numColumns": 1,
                        "numRows": "auto",
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
                "arc1": {
                    "geoJsonValue": "DUBL-DALY (ROUTE 11/12)",
                    "type": "T1",
                    "values": {
                        "numericPropExampleA": 15,
                        "numericPropExampleB": 40,
                        "selectorPropForColor": ["b"],
                    },
                },
                "arc2": {
                    "startLatitude": 39.82,
                    "startLongitude": -86.18,
                    "endLatitude": 42.89,
                    "endLongitude": -85.68,
                    "type": "T2",
                    "values": {
                        "numericPropExampleA": 30,
                        "numericPropExampleB": 20,
                        "selectorPropForColor": ["e"],
                    },
                },
                "arc3": {
                    "startLatitude": 39.82,
                    "startLongitude": -86.18,
                    "endLatitude": 28.49,
                    "endLongitude": -81.56,
                    "type": "T2",
                    "values": {
                        "numericPropExampleA": 30,
                        "numericPropExampleB": 14,
                        "selectorPropForColor": ["d"],
                    },
                },
                "arc4": {
                    "startLatitude": 39.82,
                    "startLongitude": -86.18,
                    "endLatitude": 42.361176,
                    "endLongitude": -71.084707,
                    "type": "T2",
                    "values": {
                        "numericPropExampleA": 30,
                        "numericPropExampleB": 6,
                        "selectorPropForColor": ["f"],
                    },
                },
            },
        },
        "nodes": {
            "types": {
                "nodeTypeA": {
                    "name": "Node Type A",
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "unit": "A units",
                            "legendNotation": "precision",
                            "legendPrecision": 5,
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "unit": "B units",
                            "legendNotation": "scientific",
                            "legendNotationDisplay": "x10^",
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "enabled": True,
                            "help": "Help for boolean prop",
                        },
                    },
                    "values": {
                        "booleanPropExample": True,
                    },
                },
                "nodeTypeB": {
                    "name": "Node Type B",
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example A",
                            "precision": 2,
                            "unit": "A units",
                            "legendNotation": "precision",
                            "legendPrecision": 5,
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "enabled": True,
                            "help": "Help for numeric prop example B",
                            "unit": "B units",
                            "legendMinLabel": "Lo",
                            "legendMaxLabel": "Hi",
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "enabled": True,
                            "help": "Help for boolean prop",
                        },
                    },
                    "values": {
                        "booleanPropExample": True,
                    },
                },
            },
            "data": {
                "node1": {
                    "timeValues": {
                        0: { "latitude": 43.78, },
                        1: { "latitude": 44.78, },
                        2: { "latitude": 45.78, },
                    },
                    "longitude": -79.63,
                    "type": "nodeTypeA",
                    "values": {
                        "numericPropExampleA": 100,
                        "numericPropExampleB": 50,
                        "booleanPropExample": True,
                    },
                },
                "node2": {
                    "latitude": 39.82,
                    "longitude": -86.18,
                    "type": "nodeTypeA",
                    "values": {
                        "numericPropExampleA": 80,
                        "numericPropExampleB": 40,
                        "booleanPropExample": True,
                    },
                },
                "node3": {
                    "latitude": 42.89,
                    "longitude": -85.68,
                    "type": "nodeTypeB",
                    "values": {
                        "numericPropExampleA": 500,
                        "numericPropExampleB": 150,
                        "booleanPropExample": True,
                    },
                },
                "node4": {
                    "latitude": 28.49,
                    "longitude": -81.56,
                    "type": "nodeTypeB",
                    "values": {
                        "numericPropExampleA": 1000,
                        "numericPropExampleB": 250,
                        "booleanPropExample": True,
                    },
                },
                "node5": {
                    "latitude": 42.361176,
                    "longitude": -71.084707,
                    "type": "nodeTypeB",
                    "values": {
                        "numericPropExampleA": 1000,
                        "numericPropExampleB": 250,
                        "booleanPropExample": True,
                    },
                },
            },
        },
        "geos": {
            "types": {
                "state": {
                    "name": "State",
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/world-states-provinces-md.json",
                        "geoJsonProp": "code_hasc",
                    },
                    "props": {
                        "numericPropExampleC": {
                            "name": "Numeric Prop Example C",
                            "type": "num",
                            "enabled": True,
                            "help": "Help with the example numeric prop for this State",
                            "unit": "C units",
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "value": True,
                            "help": "Help for boolean prop",
                        },
                    },
                    "values": {
                        "booleanPropExample": True,
                    },
                },
                "country": {
                    "name": "Country",
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/countries-sm.json",
                        "geoJsonProp": "FIPS_10",
                    },
                    "props": {
                        "numericPropExampleC": {
                            "name": "Numeric Prop Example C",
                            "type": "num",
                            "enabled": True,
                            "help": "Help with the example numeric prop for this Country",
                            "unit": "units",
                        },
                    },
                },
            },
            "data": {
                "geo1": {
                    "name": "Ontario, Canada",
                    "geoJsonValue": "CA.ON",
                    "type": "state",
                    "values": {
                        "timeValues": {
                            0: { "numericPropExampleC": 0 },
                            1: { "numericPropExampleC": 100 },
                            2: { "numericPropExampleC": 300 },
                        }
                    }

                },
                "geo2": {
                    "name": "Michigan, USA",
                    "geoJsonValue": "US.MI",
                    "type": "state",
                    "values": {
                        "numericPropExampleC": 300,                        
                        "booleanPropExample": True,                      
                    },
                },
                "geo3": {
                    "name": "Massachusetts, USA",
                    "geoJsonValue": "US.MA",
                    "type": "state",
                    "values": {
                        "numericPropExampleC": 250,                    
                        "booleanPropExample": False,                        
                    },
                },
                "geo4": {
                    "name": "Florida, USA",
                    "geoJsonValue": "US.FL",
                    "type": "state",
                    "values": {
                        "numericPropExampleC": 100,                        
                        "booleanPropExample": False,                
                    },
                },
                "geo5": {
                    "name": "Indiana, USA",
                    "geoJsonValue": "US.FL",
                    "type": "state",
                    "values": {
                        "numericPropExampleC": 200,
                        "booleanPropExample": False,  
                    },
                },    
                "geoCountry1": {
                    "name": "Canada",
                    "geoJsonValue": "CA",
                    "type": "country",
                    "values": {
                        "numericPropExampleC": 50,
                        },
                },
                "geoCountry2": {
                    "name": "USA",
                    "geoJsonValue": "US",
                    "type": "country",
                    "values": {
                        "numericPropExampleC": 800,
                    },
                },
            },
        },
        "groupedOutputs": {
            "groupings": {
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
                                "parent": "region",
                                "order": 2,
                            },
                            "state": {
                                "name": "States",
                                "parent": "country",
                                "order": 3,
                            },
                        },
                        "layoutDirection": "horizontal",
                        "grouping": "Solo",
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
                            "ordering": ["Size B", "Size A"],
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
            "data":{
                'locationGroup':  {
                    "stats": {
                        "numericStatExampleA": {
                            "name": "Stat Example A",
                            "calculation": "numericStatExampleA",
                            "unit": "units",
                            "order": 1,
                        },
                        "numericStatExampleB": {
                            "name": "Stat Example B",
                            "calculation": "numericStatExampleB",
                            "unit": "units",
                            "order": 2,
                        },
                        "numericExampleCalculationStat": {
                            "name": "Stat A as a percentage of Stat B",
                            "calculation": 'numericStatExampleA / groupSum("numericStatExampleB")',
                            "precision": 2,
                            "trailingZeros": True,
                            "unit": "%",
                            "unitPlacement": "after",
                            "order": 3,
                        },
                    },
                    "valueLists": {
                        'numericStatExampleA': [5, 4, 6, -3, -3, 1],
                        'numericStatExampleB': [10, 5, 7, 5, -2, -1],
                    },
                    "groupLists":{
                        "location": ['locCaOn', 'locCaOn', 'locUsMi', 'locUsMi', 'locUsIn', 'locUsFl'],
                        "sku": ["SKU1", "SKU2", "SKU1", "SKU2", "SKU2", "SKU2"],
                    },
                },
                'skuGroup':  {
                    "stats": {
                        "numericStatExampleD": {
                            "name": "Stat Example D",
                            "calculation": "numericStatExampleD",
                            "unit": "units",
                            "order": 1,
                        },
                    },
                    "valueLists": {
                        'numericStatExampleD': [10, 15]
                    },
                    "groupLists": {
                        "sku": ["SKU1", "SKU2"],
                    },
                },
            }
        },
        "globalOutputs": {
            "data": {
                "kpiHeader1": {
                    "type": "head",
                    "name": "Example KPI Header 1",
                    "icon": "bs/BsInboxes",
                },
                "kpiHeader2": {
                    "type": "head",
                    "name": "Example KPI Header 2",
                    "icon": "bs/BsTruck",
                },
                "key1": {
                    "name": "KPI Example 1",
                    "icon": "bs/BsFillEmojiFrownFill",
                    "value": 18,
                    "precision": 0,
                    "unit": "frowns",
                },
                "key2": {
                    "name": "KPI Example 2",
                    "icon": "bs/BsFillEmojiSmileFill",
                    "value": 32,
                    "precision": 0,
                    "unit": "smiles",
                },
                "key3": {
                    "name": "KPI Example 3",
                    "icon": "bs/BsInboxes",
                    "value": 100,
                    "precision": 4,
                    "notation": "scientific",
                    "notationDisplay": "E+",
                    "trailingZeros": True,
                    "unit": "units",
                },
                "key4": {
                    "name": "A Big Number",
                    "icon": "bs/BsTruck",
                    "value": 10000000000000,
                    "notation": "engineering",
                    "notationDisplay": "x10^",
                    "precision": 0,
                    "unit": "units",
                },
                "key5": {
                    "name": "A Really Big Number",
                    "icon": "md/MdExpand",
                    "value": 9007199254740991,
                    "precision": 2,
                    "unit": "$",
                    "unitPlacement": "before",
                    "notation": "compact",
                    "notationDisplay": "long",
                    "trailingZeros": True,
                },
                 "key6": {
                    "name": "A Decent Big Number",
                    "icon": "md/MdExpand",
                    "value": 199254740991,
                    "precision": 2,
                    "unit": "$",
                    "unitPlacement": "before",
                    "notation": "compact",
                    "notationDisplay": "long",
                    "trailingZeros": True,
                },
            },
            "layout": {
                "type": "grid",
                "numColumns": "auto",
                "numRows": "auto",
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
                    "col1Row5": {
                        "type": "item",
                        "itemId": "key6",
                        "column": 1,
                        "row": 5,
                    },
                },
            },
        },
        "kwargs": {
            "wipeExisting": True,
        },
    }
    if command == "init":
        print("The `reset` button has been pressed by the user!")
        return example
    elif command == "solve":
        print("The `solve` button has been pressed by the user!")
        time.sleep(3)
        socket.notify("Priming Thrusters...", title="Initialization", theme="info", duration=3)
        time.sleep(3)
        socket.notify("Ignition...", title="Initialization", theme="info")
        time.sleep(3)
        socket.notify("Leak detected in primary power core!", title="Warning:", theme="warning")
        time.sleep(3)
        socket.notify("Engine Failure!", title="Error:", theme="error")
        time.sleep(3)
        socket.notify("Recalibrating Gravitons!", title="Attempting Fix:", theme="warning")
        time.sleep(3)
        socket.notify("Fix Succeded!", title="Attempting Fix:", theme="success")
        time.sleep(3)
        socket.notify("All Systems Normal!", title="Status:", theme="info")
        time.sleep(3)
        socket.notify("Liftoff Achieved!", title="Status:", theme="success")
    elif command == "test":
        print("The `test` button has been pressed by the user!")
        raise Exception("Test Exception!")
    if command == "viewInfo":
        socket.notify("The info button has been pressed!", title="Info", theme="info")
    if session_data:
        for key, value in session_data.items():
            example[key] = value
    return example
