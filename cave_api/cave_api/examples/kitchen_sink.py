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
            "demo": {
                "map1": {
                    "scrollSpeed": 0.1,
                },
                "dash1": {
                    "displayTime": 30,
                },
            },
            "sync": {
                "panes": {
                    "name": "Open Pane",
                    "showToggle": True,
                    "value": False,
                    "data": {
                        "ab1": ["panes", "paneState", "left"],
                        "ab2": ["panes", "paneState", "right"],
                    },
                },
                "pageSelection": {
                    "name": "Page Selection",
                    "showToggle": True,
                    "value": False,
                    "data": {"ps1": ["pages", "currentPage"]},
                },
                "mapLayers": {
                    "name": "Map Layers",
                    "showToggle": True,
                    "value": False,
                    "data": {"ml1": ["maps", "data", "map1", "legendGroups"]},
                },
                "modals": {
                    "name": "Open Modal",
                    "showToggle": True,
                    "value": False,
                    "data": {"pn1": ["panes", "paneState", "center"]},
                },
                "pages": {
                    "name": "Dashboards",
                    "showToggle": True,
                    "value": False,
                    "data": {"db1": ["pages", "data"]},
                },
            },
            "iconUrl": "https://react-icons.mitcave.com/4.10.1",
            "order": {
                "sync": ["panes", "modals", "pageSelection", "mapLayers", "pages"],
            },
            "debug": True,
            "time": {
                "timeLength": 3,
                "timeUnits": "Century",
            },
            "defaults": {
                "precision": 4,
                "trailingZeros": True,
                "unitPlacement": "afterWithSpace",
                "showToolbar": True,
            },
        },
        "appBar": {
            "order": {
                "data": [
                    "session",
                    "appSettings",
                    "resetButton",
                    "buttonSolve",
                    "examplePropsPane",
                    "dash1",
                    "dash2",
                ],
            },
            "data": {
                "session": {
                    "icon": "md/MdApi",
                    "type": "session",
                    "bar": "upperLeft",
                },
                "appSettings": {
                    "icon": "md/MdOutlineSettings",
                    "type": "settings",
                    "bar": "upperLeft",
                },
                "resetButton": {
                    "icon": "md/MdSync",
                    "color": "rgba(255, 101, 101, 255)",
                    "apiCommand": "reset",
                    "type": "button",
                    "bar": "upperLeft",
                },
                "buttonSolve": {
                    "icon": "bs/BsLightningFill",
                    "color": "rgba(178, 179, 55, 255)",
                    "apiCommand": "solve",
                    "type": "button",
                    "bar": "upperLeft",
                },
                "examplePropsPane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "bar": "upperLeft",
                    "variant": "wall",
                },
                "dash1": {
                    "type": "page",
                    "icon": "md/MdInsertChart",
                    "bar": "lowerLeft",
                },
                "dash2": {
                    "type": "page",
                    "icon": "md/MdInsertChartOutlined",
                    "bar": "lowerLeft",
                },
                "exampleModal": {
                    "icon": "md/MdInfo",
                    "color": "rgba(195, 164, 222, 255)",
                    "type": "pane",
                    "bar": "upperRight",
                    "variant": "modal",
                },
            },
        },
        "panes": {
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
                                "t1_b1_tw1": {"name": "Twig1", "path": ["Tree1", "Branch1"]},
                                "t1_b1_tw2": {"name": "Twig2", "path": ["Tree1", "Branch1"]},
                                "t1_b1_tw3": {"name": "Twig3", "path": ["Tree1", "Branch1"]},
                                "t1_b2_tw1": {"name": "Twig1", "path": ["Tree1", "Branch2"]},
                                "t1_b2_tw2": {"name": "Twig2", "path": ["Tree1", "Branch2"]},
                                "t2_b1_tw1": {"name": "Twig1", "path": ["Tree2", "Branch1"]},
                                "t2_b1_tw2": {"name": "Twig2", "path": ["Tree2", "Branch1"]},
                                "t2_b2_tw1": {"name": "Twig1", "path": ["Tree2", "Branch2"]},
                                "t2_b2_tw2": {"name": "Twig2", "path": ["Tree2", "Branch2"]},
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
                            "views": ["hours", "minutes", "seconds"],
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
                        "nestedItemExample": [
                            "t1_b1_tw1",
                            "t1_b1_tw2",
                            "t1_b2_tw2",
                            "t2_b1_tw1",
                            "t2_b1_tw2",
                        ],
                        "dateItemExample": "1969-07-20",
                        "timeItemExample": "20:17:40",
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
            "currentPage": "dash2",
            "data": {
                "dash1": {
                    "pageLayout": [
                        {
                            "variant": "bar",
                            "statAggregation": "mean",
                        },
                        {
                            "type": "map",
                            "mapId": "map1",
                            "showToolbar": False,
                            "maximized": True,
                         },
                        {
                            "variant": "bar",
                            "groupingLevel": ["size"],
                            "groupingId": ["sku"],
                            "lockedLayout": True,
                            "statAggregation": "sum",
                            "groupedOutputDataId": "locationGroup",
                            "statId":"numericExampleCalculationStat",
                        },
                    ],
                    "lockedLayout": False,
                },
                "dash2": {
                    "pageLayout": [
                        {
                            "variant": "bar",
                            "statAggregation": "mean",
                            "groupedOutputDataId": "locationGroup",
                            "statId":"numericStatExampleB",
                        },
                        {
                            "type": "globalOutput",
                            "variant": "bar",
                            "statAggregation": "sum",
                            "sessions": [],
                            "globalOutput": ["key1", "key2"],
                            "showToolbar": False,
                        },
                        {
                            "variant": "box_plot",
                            "groupingLevel": ["size"],
                            "lockedLayout": True,
                            "groupingId": ["sku"],
                            "statAggregation": "mean",
                            "groupedOutputDataId": "locationGroup",
                            "statId":"numericExampleCalculationStat",
                        },
                        {
                            "variant": "cumulative_line",
                            "statAggregation": "sum",
                            "groupedOutputDataId": "locationGroup",
                            "statId":"numericStatExampleB",
                            "groupingId": ["location", "sku"],
                            "groupingLevel": ["state", "sku"],
                        },
                    ],
                    "lockedLayout": False,
                },
            },
        },
        "maps": {
            "additionalMapStyles": {
                "osmRasterTiles": {
                    "name": "OSM Raster Tiles",
                    "icon": "md/MdBrush",
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
                    "spec": "mapbox://styles/mapbox/streets-v12",
                },
                "outdoors": {
                    "name": "Outdoors",
                    "icon": "md/MdForest",
                    "spec": "mapbox://styles/mapbox/outdoors-v12",
                },
                "satellite": {
                    "name": "Satellite",
                    "icon": "md/MdSatelliteAlt",
                    "spec": "mapbox://styles/mapbox/satellite-v9",
                },
                "satellite_streets": {
                    "name": "Satellite Streets",
                    "icon": "md/MdSatellite",
                    "spec": "mapbox://styles/mapbox/satellite-streets-v12",
                },
            },
            "data": {
                "map1": {
                    "order": {
                        "optionalViewports": ["ov0", "ov1"],
                        "legendGroups": ["lga", "lgb"],
                    },
                    "name": "Example Map 1",
                    "currentStyle": "osmRasterTiles",
                    "currentProjection": "globe",
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 4.66,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                    "optionalViewports": {
                        "ov0": {
                            "icon": "fa/FaGlobeAsia",
                            "name": "Asia",
                            "zoom": 4,
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
                                    "value": True,
                                    "sizeBy": "numericPropExampleA",
                                    "colorBy": "booleanPropExample",
                                    "allowGrouping": True,
                                    "group": True,
                                    "groupCalcBySize": "sum",
                                    "groupCalcByColor": "mode",
                                    # "groupScaleWithZoom": True,
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
                                            "nullColor": "rgba(0,255,0, 255)",
                                        },
                                    },
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 80, "startSize": "30px", "endSize": "45px"},
                                        "numericPropExampleB": {"min": 0, "max": 50, "startSize": "15px", "endSize": "30px"},
                                    },
                                    "icon": "fa6/FaIgloo",
                                },
                                "T1": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 50, "startSize": "15px", "endSize": "30px"},
                                        "numericPropExampleB": {"min": 0, "max": 40, "startSize": "5px", "endSize": "15px"},
                                    },
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
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "data": {
                                "nodeTypeB": {
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
                                        "numericPropExampleA": {"min": 0, "max": 100, "startSize": "15px", "endSize": "30px"},
                                        "numericPropExampleB": {"min": 0, "max": 250, "startSize": "5px", "endSize": "15px"},
                                    },
                                    "icon": "bs/BsBuilding",
                                },
                                "T2": {
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
                                        "numericPropExampleA": {"min": 0, "max": 50, "startSize": "15px", "endSize": "30px"},
                                        "numericPropExampleB": {"min": 0, "max": 40, "startSize": "5px", "endSize": "15px"},
                                    },
                                },
                                "state": {
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
                        },
                    },
                },
                "map2": {
                    "order": {
                        "optionalViewports": ["ov0", "ov1"],
                        "legendGroups": ["lga", "lgb"],
                    },
                    "name": "Example Map 2",
                    "defaultViewport": {
                        "longitude": -75.447,
                        "latitude": 40.345,
                        "zoom": 4.66,
                        "pitch": 0,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                    "optionalViewports": {
                        "ov0": {
                            "icon": "fa/FaGlobeAsia",
                            "name": "Asia",
                            "zoom": 4,
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
                                        "numericPropExampleA": {"min": 0, "max": 80, "startSize": "30px", "endSize": "45px"},
                                        "numericPropExampleB": {"min": 0, "max": 50, "startSize": "15px", "endSize": "30px"},
                                    },
                                    "icon": "fa6/FaIgloo",
                                },
                                "T1": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "sizeByOptions": {
                                        "numericPropExampleA": {"min": 0, "max": 50, "startSize": "15px", "endSize": "30px"},
                                        "numericPropExampleB": {"min": 0, "max": 40, "startSize": "5px", "endSize": "15px"},
                                    },
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
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "data": {
                                "nodeTypeB": {
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
                                        "numericPropExampleA": {"min": 0, "max": 100, "startSize": "15px", "endSize": "30px"},
                                        "numericPropExampleB": {"min": 0, "max": 250, "startSize": "5px", "endSize": "15px"},
                                    },
                                    "icon": "bs/BsBuilding",
                                },
                                "T2": {
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
                                        "numericPropExampleA": {"min": 0, "max": 50, "startSize": "15px", "endSize": "30px"},
                                        "numericPropExampleB": {"min": 0, "max": 40, "startSize": "5px", "endSize": "15px"},
                                    },
                                },
                                "state": {
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
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "T1": {
                    "type": "arc",
                    "name": "Flow Type 1",
                    "geoJson": {
                        "geoJsonLayer": "https://raw.githubusercontent.com/MIT-CAVE/cave_app_extras/main/example_data/example.geojson",
                        "geoJsonProp": "arc_id",
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
                    "data": {
                        "location": {
                            "geoJsonValue": ["toronto-pittsburgh-indianapolis"],
                        },
                        "valueLists": {
                            "numericPropExampleA": [15],
                            "numericPropExampleB": [40],
                            "selectorPropForColor": [["b"]],
                        }
                    }
                },
                "T2": {
                    "type": "arc",
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
                    "data": {
                        "location": {
                            "startLatitude": [39.82, 39.82, 39.82],
                            "startLongitude": [-86.18, -86.18, -86.18],
                            "endLatitude": [42.89, 28.49, 42.361176],
                            "endLongitude": [-85.68, -81.56, -71.084707],
                        },
                        "valueLists": {
                            "numericPropExampleA": [30, 30, 30],
                            "numericPropExampleB": [20, 14, 6],
                            "selectorPropForColor": [["e"], ["d"], ["f"]],
                        },
                    }
                },
                "nodeTypeA": {
                    "type": "node",
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
                    "data": {
                        "location": {
                            "timeValues": {
                                0: { "latitude": [43.78, 39.82], },
                                1: { "latitude": [44.78, 39.82], },
                                2: { "latitude": [45.78, 39.82], },
                            },
                            "latitude": [43.78, 39.82],
                            "longitude": [-79.63, -86.18],
                        },
                        "valueLists": {
                            "numericPropExampleA": [100, 80],
                            "numericPropExampleB": [50, 40],
                            "booleanPropExample": [True, True],
                        },
                    }
                },
                "nodeTypeB": {
                    "type": "node",
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
                    "data": {
                        "location": {
                            "latitude": [42.89, 28.49, 42.361176],
                            "longitude": [-85.68, -81.56, -71.084707],
                        },
                        "valueLists": {
                            "numericPropExampleA": [500, 1000, 1000],
                            "numericPropExampleB": [150, 250, 250],
                            "booleanPropExample": [True, True, True],
                        },
                    }
                },
                "state": {
                    "type": "geo",
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
                            "help": "Help for boolean prop",
                        },
                    },
                    "data": {
                        "location": {
                            "geoJsonValue": ["CA.ON", "US.MI", "US.MA", "US.FL", "US.IN"],
                        },
                        "valueLists": {
                            "numericPropExampleC": [0, 300, 250, 100, 200],
                            "booleanPropExample": [True, True, False, False, False],
                        }
                    }
                },
                "country": {
                    "type": "geo",
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
                    "data": {
                        "location": {
                            "geoJsonValue": ["CA", "US"],
                        },
                        "valueLists": {
                            "numericPropExampleC": [50, 800],
                        }
                    }
                },
            }
        },
        "groupedOutputs": {
            "order": {
                "groupings": ["location", "sku"],
            },
            "groupings": {
                "location": {
                    "order": {
                        "levels": ["region", "country", "state"],
                    },
                    "data": {
                        "id": ["locUsMi", "locUsMa", "locUsFl", "locUsIn", "locCaOn"],
                        "region": ["North America", "North America", "North America", "North America", "North America"],
                        "country": ["USA", "USA", "USA", "USA", "Canada"],  
                        "state": ["Michigan", "Massachusetts", "Florida", "Indiana", "Ontario"],
                        },
                    "name": "Locations",
                    "levels": {
                        "region": {
                            "name": "Regions",
                        },
                        "country": {
                            "name": "Countries",
                            "ordering": ["USA", "Canada"],
                            "parent": "region",
                        },
                        "state": {
                            "name": "States",
                            "parent": "country",
                        },
                    },
                    "layoutDirection": "horizontal",
                    "grouping": "Solo",
                },
                "sku": {
                    "order": {
                        "levels": ["type", "size", "sku"],
                    },
                    "data": {
                        "id": ["SKU1", "SKU2"],
                        "type": ["Type A", "Type A"],
                        "size": ["Size A", "Size B"],
                        "sku": ["SKU1", "SKU2"],
                    },
                    "name": "SKUs",
                    "levels": {
                        "type": {
                            "name": "Types",
                        },
                        "size": {
                            "name": "Sizing",
                            "ordering": ["Size B", "Size A"],
                        },
                        "sku": {
                            "name": "SKU",
                        },
                    },
                    "layoutDirection": "horizontal",
                },
            },
            "data": {
                "locationGroup": {
                    "order": {
                        "stats": [
                            "numericStatExampleA",
                            "numericStatExampleB",
                            "numericExampleCalculationStat",
                        ],
                    },
                    "stats": {
                        "numericStatExampleA": {
                            "name": "Stat Example A",
                            "calculation": "numericStatExampleA",
                            "unit": "units",
                        },
                        "numericStatExampleB": {
                            "name": "Stat Example B",
                            "calculation": "numericStatExampleB",
                            "unit": "units",
                        },
                        "numericExampleCalculationStat": {
                            "name": "Stat A as a percentage of Stat B",
                            "calculation": 'numericStatExampleA / groupSum("numericStatExampleB")',
                            "precision": 2,
                            "trailingZeros": True,
                            "unit": "%",
                            "unitPlacement": "after",
                        },
                    },
                    "valueLists": {
                        "numericStatExampleA": [5, 4, 6, -3, -3, 1],
                        "numericStatExampleB": [10, 5, 7, 5, -2, -1],
                    },
                    "groupLists": {
                        "location": [
                            "locCaOn",
                            "locCaOn",
                            "locUsMi",
                            "locUsMi",
                            "locUsIn",
                            "locUsFl",
                        ],
                        "sku": ["SKU1", "SKU2", "SKU1", "SKU2", "SKU2", "SKU2"],
                    },
                },
                "skuGroup": {
                    "stats": {
                        "numericStatExampleD": {
                            "name": "Stat Example D",
                            "calculation": "numericStatExampleD",
                            "unit": "units",
                        },
                    },
                    "valueLists": {"numericStatExampleD": [10, 15]},
                    "groupLists": {
                        "sku": ["SKU1", "SKU2"],
                    },
                },
            },
        },
        "globalOutputs": {
            "props": {
                "kpiHeader1": {
                    "type": "head",
                    "name": "Example KPI Header 1",
                    "icon": "bs/BsInboxes",
                    "variant": "icon"
                },
                "kpiHeader2": {
                    "type": "head",
                    "name": "Example KPI Header 2",
                    "icon": "bs/BsTruck",
                    "variant": "icon"
                },
                "key1": {
                    "name": "KPI Example 1",
                    "icon": "bs/BsFillEmojiFrownFill",
                    "precision": 0,
                    "unit": "frowns",
                    "type": "num",
                    "variant": "icon",
                },
                "key2": {
                    "name": "KPI Example 2",
                    "icon": "bs/BsFillEmojiSmileFill",
                    "precision": 0,
                    "unit": "smiles",
                    "type": "num",
                    "variant": "icon",
                },
                "key3": {
                    "name": "KPI Example 3",
                    "icon": "bs/BsInboxes",
                    "precision": 4,
                    "notation": "scientific",
                    "notationDisplay": "E+",
                    "trailingZeros": True,
                    "unit": "units",
                    "type": "num",
                    "variant": "icon",
                },
                "key4": {
                    "name": "A Big Number",
                    "icon": "bs/BsTruck",
                    "notation": "engineering",
                    "notationDisplay": "x10^",
                    "precision": 0,
                    "unit": "units",
                    "type": "num",
                    "variant": "icon",
                },
                "key5": {
                    "name": "A Really Big Number",
                    "icon": "md/MdExpand",
                    "precision": 2,
                    "unit": "$",
                    "unitPlacement": "before",
                    "notation": "compact",
                    "notationDisplay": "long",
                    "trailingZeros": True,
                    "type": "num",
                    "variant": "icon",
                },
                "key6": {
                    "name": "A Decent Big Number",
                    "icon": "md/MdExpand",
                    "precision": 2,
                    "unit": "$",
                    "unitPlacement": "before",
                    "notation": "compact",
                    "notationDisplay": "long",
                    "trailingZeros": True,
                    "type": "num",
                    "variant": "icon",
                },
            },
            "values": {
                "key1": 18,
                "key2": 32,
                "key3": 100,
                "key4": 10000000000000,
                "key5": 9007199254740991,
                "key6": 199254740991,
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
        "extraKwargs": {
            "wipeExisting": True,
        },
    }
    if command == "init" or command == "reset":
        if command == "reset":
            print ("The `reset` button has been pressed by the user!")
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
