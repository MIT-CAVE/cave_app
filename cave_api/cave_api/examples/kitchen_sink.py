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
            "iconUrl": "https://react-icons.mitcave.com/5.0.1",
            "order": {
                "sync": ["panes", "modals", "pageSelection", "mapLayers", "pages"],
            },
            "time": {
                "timeLength": 3,
                "timeUnits": "Century",
                "looping": False,
                "speed": 1,
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
                    "buttonSolve",
                    "examplePropsPane",
                    "dash1",
                    "dash2",
                ],
            },
            "data": {
                "buttonSolve": {
                    "icon": "bs/BsLightningFill",
                    "color": "rgba(178, 179, 55, 1)",
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
                    "color": "rgba(195, 164, 222, 1)",
                    "type": "pane",
                    "bar": "upperRight",
                    "variant": "modal",
                },
            },
        },
        "panes": {
            "paneState": {"left": {}, "right": {}, "center": {}},
            "data": {
                "exampleModal": {
                    "name": "Example Modal",
                    "props": {
                        "buttonViewInfo": {
                            "name": "Info Button",
                            "type": "button",
                            "apiCommand": "viewInfo",
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
                            "variant": "slider",
                            "help": "Help for the numeric slider example",
                            "maxValue": 100,
                            "minValue": 0,
                            "unit": "%",
                        },
                        "incrementalSliderExample": {
                            "name": "Incrimental Slider Example",
                            "type": "num",
                            "variant": "incslider",
                            "help": "Help for the incremental slider example",
                            "valueOptions": [0, 25, 50, 75, 100],
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
                            "help": "Help for the toggle input example",
                        },
                        "buttonInputExample": {
                            "name": "Button Input Example (Creates an Error)",
                            "type": "button",
                            "apiCommand": "test",
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
                            "help": "Help for the text input example",
                        },
                        "textAreaInputExample": {
                            "name": "TextArea Input Example",
                            "type": "text",
                            "variant": "textarea",
                            "rows": 6,
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
                            "help": "Select an option from the radio",
                        },
                        "comboBoxItemExample": {
                            "name": "ComboBox Item Example",
                            "type": "selector",
                            "variant": "combobox",
                            "placeholder": "Options",
                            "options": {
                                "option_a": {"name": "Option A"},
                                "option_b": {"name": "Option B"},
                                "option_c": {"name": "Option C"},
                            },
                            "help": "Select an option from the combobox",
                        },
                        "comboBoxMultiExample": {
                            "name": "ComboBox Multi Example",
                            "type": "selector",
                            "variant": "comboboxMulti",
                            "placeholder": "Select multiple options",
                            "options": {
                                "option_a": {"name": "Option A"},
                                "option_b": {"name": "Option B"},
                                "option_c": {"name": "Option C"},
                            },
                            "help": "Select multiple options from the combobox",
                        },
                        "nestedItemExample": {
                            "name": "Nested Item Example",
                            "type": "selector",
                            "variant": "nested",
                            "options": {
                                "t1_b1_tw1": {
                                    "name": "Twig1",
                                    "path": ["Tree1", "Branch1"],
                                },
                                "t1_b1_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree1", "Branch1"],
                                },
                                "t1_b1_tw3": {
                                    "name": "Twig3",
                                    "path": ["Tree1", "Branch1"],
                                },
                                "t1_b2_tw1": {
                                    "name": "Twig1",
                                    "path": ["Tree1", "Branch2"],
                                },
                                "t1_b2_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree1", "Branch2"],
                                },
                                "t2_b1_tw1": {
                                    "name": "Twig1",
                                    "path": ["Tree2", "Branch1"],
                                },
                                "t2_b1_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree2", "Branch1"],
                                },
                                "t2_b2_tw1": {
                                    "name": "Twig1",
                                    "path": ["Tree2", "Branch2"],
                                },
                                "t2_b2_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree2", "Branch2"],
                                },
                            },
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
                            "help": "The Eagle has landed!",
                        },
                        "timeItemExample": {
                            "name": "Time Example",
                            "type": "date",
                            "variant": "time",
                            "views": ["hours", "minutes", "seconds"],
                            "help": "The Eagle has landed!",
                        },
                        "dateTimeItemExample": {
                            "name": "Date and Time Example",
                            "type": "date",
                            "variant": "datetime",
                            "help": "The Eagle has landed!",
                        },
                        "coordinateHeader": {
                            "name": "Coordinate Props",
                            "type": "head",
                            "help": "Some help for Coordinate Props",
                        },
                        "latLngInputExample": {
                            "name": "Lat/Lng Input Example",
                            "type": "coordinate",
                            "variant": "latLngInput",
                            "help": "Help for the latLngInput example",
                        },
                        "latLngMapExample": {
                            "name": "Lat/Lng Map Example",
                            "type": "coordinate",
                            "variant": "latLngMap",
                            "help": "Help for the latLngMap example",
                        },
                        "latLngPathExample": {
                            "name": "Lat/Lng Path Example",
                            "type": "coordinate",
                            "variant": "latLngPath",
                            "help": "Help for the latLngPath example",
                        },
                    },
                    "values": {
                        "numericInputExample": 50,
                        "numericSliderExample": 50,
                        "incrementalSliderExample": 50,
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
                        "comboBoxMultiExample": ["option_a", "option_b"],
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
                        "latLngInputExample": [[-71.092003, 42.360001]],
                        "latLngMapExample": [[-71.092003, 42.360001]],
                        "latLngPathExample": [
                            [-71.092003, 42.360001],
                            [-71.093003, 42.361001],
                        ],
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
                            "col1Row4": {
                                "type": "item",
                                "column": 1,
                                "row": 4,
                                "itemId": "incrementalSliderExample",
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
                                "itemId": "comboBoxMultiExample",
                            },
                            "col4Row7": {
                                "type": "item",
                                "column": 4,
                                "row": 7,
                                "itemId": "hstepperItemExample",
                            },
                            "col4Row8": {
                                "type": "item",
                                "column": 4,
                                "row": 8,
                                "itemId": "vstepperItemExample",
                            },
                            "col4Row9": {
                                "type": "item",
                                "column": 4,
                                "row": 9,
                                "itemId": "hradioItemExample",
                            },
                            "col4Row10": {
                                "type": "item",
                                "column": 4,
                                "row": 10,
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
                            "col6Row1": {
                                "type": "item",
                                "column": 6,
                                "row": 1,
                                "itemId": "coordinateHeader",
                            },
                            "col6Row2": {
                                "type": "item",
                                "column": 6,
                                "row": 2,
                                "itemId": "latLngInputExample",
                            },
                            "col6Row3": {
                                "type": "item",
                                "column": 6,
                                "row": 3,
                                "itemId": "latLngMapExample",
                            },
                            "col6Row4": {
                                "type": "item",
                                "column": 6,
                                "row": 4,
                                "itemId": "latLngPathExample",
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
                    "charts": {
                        "allBar": {
                            "variant": "bar",
                            "statAggregation": "mean",
                        },
                        "map1": {
                            "type": "map",
                            "mapId": "map1",
                            "showToolbar": False,
                            "maximized": True,
                        },
                        "statBar": {
                            "variant": "bar",
                            "groupingLevel": ["size"],
                            "groupingId": ["sku"],
                            "lockedLayout": True,
                            "statAggregation": "sum",
                            "groupedOutputDataId": "locationGroup",
                            "statId": "numericExampleCalculationStat",
                        },
                    },
                    "pageLayout": ["allBar", "map1", None, "statBar"],
                    "lockedLayout": False,
                },
                "dash2": {
                    "charts": {
                        "allBar": {
                            "variant": "bar",
                            "statAggregation": "mean",
                            "groupedOutputDataId": "locationGroup",
                            "statId": "numericStatExampleB",
                            "showNA": True,
                        },
                        "mixed": {
                            "variant": "mixed",
                            "statAggregation": "sum",
                            "groupedOutputDataId": ["locationGroup", "locationGroup"],
                            "statId": ["numericStatExampleA", "numericStatExampleB"],
                            "groupingId": ["location"],
                            "groupingLevel": ["state"],
                            "leftVariant": "bar",
                            "rightVariant": "cumulative_line",
                        },
                        "boxPlot": {
                            "variant": "box_plot",
                            "groupingLevel": ["size"],
                            "lockedLayout": True,
                            "groupingId": ["sku"],
                            "statAggregation": "mean",
                            "groupedOutputDataId": "locationGroup",
                            "statId": "numericExampleCalculationStat",
                        },
                        "cumulativeLine": {
                            "variant": "cumulative_line",
                            "statAggregation": "sum",
                            "groupedOutputDataId": "locationGroup",
                            "statId": "numericStatExampleB",
                            "groupingId": ["location", "sku"],
                            "groupingLevel": ["state", "sku"],
                            "defaultToZero": True,
                        },
                    },
                    "pageLayout": [
                        "allBar",
                        "mixed",
                        "boxPlot",
                        "cumulativeLine",
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
                    "legendView": "minimal",
                    "showLegendGroupNames": True,
                    "legendGroups": {
                        "lga": {
                            "name": "Legend Group A",
                            "data": {
                                "nodeTypeA": {
                                    "value": True,
                                    "colorBy": "booleanPropExample",
                                    "sizeBy": "numericPropExampleA",
                                    "allowGrouping": True,
                                    "group": True,
                                    "groupCalcBySize": "sum",
                                    "groupCalcByColor": "mode",
                                    # "groupScaleWithZoom": True,
                                    # "groupScale": 10,
                                    "icon": "fa6/FaIgloo",
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "booleanPropExample",
                                        "selectorPropExample",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "booleanPropExample",
                                        "selectorPropExample",
                                    ],
                                },
                                "T1": {
                                    "colorBy": "numericPropExampleB",
                                    "sizeBy": "numericPropExampleA",
                                    "value": True,
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "selectorPropExample",
                                    ],
                                },
                            },
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "data": {
                                "nodeTypeB": {
                                    "value": True,
                                    "colorBy": "numericPropExampleB",
                                    "sizeBy": "numericPropExampleA",
                                    "allowGrouping": True,
                                    "group": True,
                                    "groupCalcBySize": "count",
                                    "groupCalcByColor": "and",
                                    # "groupScaleWithZoom": True,
                                    # # Equivalent to zoom level unless groupScale is set
                                    # "groupScale": 10,
                                    "icon": "bs/BsBuilding",
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "booleanPropExample",
                                    ],
                                },
                                "T2": {
                                    "colorBy": "selectorPropExample",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "lineBy": "dotted",
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "selectorPropExample",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "selectorPropExample",
                                    ],
                                },
                                "state": {
                                    "value": True,
                                    "colorBy": "numericPropExampleC",
                                    "icon": "bs/BsHexagon",
                                    "colorByOptions": [
                                        "numericPropExampleC",
                                        "booleanPropExample",
                                    ],
                                },
                                "country": {
                                    "value": False,
                                    "colorBy": "numericPropExampleC",
                                    "icon": "bs/BsHexagon",
                                    "colorByOptions": ["numericPropExampleC"],
                                },
                                "custom": {
                                    "value": False,
                                    "colorBy": "numericPropExampleC",
                                    "icon": "md/MdOutlineTouchApp",
                                    "colorByOptions": [
                                        "numericPropExampleC",
                                        "booleanPropExample",
                                    ],
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
                                    "colorBy": "booleanPropExample",
                                    "sizeBy": "numericPropExampleA",
                                    "icon": "fa6/FaIgloo",
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "booleanPropExample",
                                        "selectorPropExample",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "booleanPropExample",
                                        "selectorPropExample",
                                    ],
                                },
                                "T1": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "selectorPropExample",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "selectorPropExample",
                                    ],
                                },
                            },
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "data": {
                                "nodeTypeB": {
                                    "value": True,
                                    "colorBy": "booleanPropExample",
                                    "sizeBy": "numericPropExampleB",
                                    "icon": "bs/BsBuilding",
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "booleanPropExample",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "booleanPropExample",
                                    ],
                                },
                                "T2": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                    "lineBy": "dotted",
                                    "colorByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "selectorPropExample",
                                    ],
                                    "sizeByOptions": [
                                        "numericPropExampleA",
                                        "numericPropExampleB",
                                        "selectorPropExample",
                                    ],
                                },
                                "state": {
                                    "value": True,
                                    "colorBy": "numericPropExampleC",
                                    "icon": "bs/BsHexagon",
                                    "colorByOptions": [
                                        "numericPropExampleC",
                                        "booleanPropExample",
                                    ],
                                },
                                "country": {
                                    "value": False,
                                    "colorBy": "numericPropExampleC",
                                    "icon": "bs/BsHexagon",
                                    "colorByOptions": ["numericPropExampleC"],
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
                            "min": 0,
                            "max": 50,
                            "unit": "A units",
                            "colorGradient": {
                                "scale": "linear",
                                "notation": "compact",
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(233, 0, 0, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(96, 2, 2, 1)",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "data": [
                                    {"value": "min", "size": "15px", "label": "Small"},
                                    {"value": "max", "size": "30px"},
                                ],
                            },
                            "help": "Help for numeric prop example A",
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "min": 0,
                            "max": 40,
                            "colorGradient": {
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgb(0, 128, 255)",
                                        "label": "Very Low",
                                    },
                                    {
                                        "value": 5,
                                        "color": "rgb(0, 200, 150)",
                                        "label": "Low-Mid",
                                    },
                                    {
                                        "value": 15,
                                        "color": "rgb(255, 165, 0)",
                                        "label": "Moderate-High",
                                    },
                                    {
                                        "value": 28,
                                        "color": "rgb(255, 69, 0)",
                                        "label": "Very High",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgb(255, 0, 0)",
                                        "label": "Critical",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "data": [
                                    {"value": "min", "size": "5px"},
                                    {"value": 20, "size": "8px"},
                                    {"value": "max", "size": "15px"},
                                ],
                            },
                            "unit": "B units",
                            "help": "Help for numeric prop example B",
                        },
                        "selectorPropExample": {
                            "name": "Example Categorical Prop",
                            "type": "selector",
                            "variant": "dropdown",
                            "options": {
                                "a": {
                                    "name": "A",
                                    "color": "rgba(128, 255, 255, 1)",
                                    "size": "3px",
                                },
                                "b": {
                                    "name": "B",
                                    "color": "rgba(0, 153, 51, 1)",
                                    "size": "8px",
                                },
                                "c": {
                                    "name": "C",
                                    "color": "rgba(0, 0, 128, 1)",
                                    "size": "13px",
                                },
                                "d": {
                                    "name": "D",
                                    "color": "rgba(204, 0, 0, 1)",
                                    "size": "18px",
                                },
                                "e": {
                                    "name": "E",
                                    "color": "rgba(153, 77, 0, 1)",
                                    "size": "23px",
                                },
                                "f": {
                                    "name": "F",
                                    "color": "rgba(255, 25, 255, 1)",
                                    "size": "28px",
                                },
                                "g": {
                                    "name": "G",
                                    "color": "rgba(0, 255, 0, 1)",
                                    "size": "33px",
                                },
                                "h": {
                                    "name": "H",
                                    "color": "rgba(255, 255, 0, 1)",
                                    "size": "38px",
                                },
                            },
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
                                "itemId": "selectorPropExample",
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
                            "selectorPropExample": [["b"]],
                        },
                    },
                },
                "T2": {
                    "type": "arc",
                    "name": "Flow Type 2",
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "min": 0,
                            "max": 50,
                            "colorGradient": {
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(233, 0, 0, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(96, 2, 2, 1)",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "data": [
                                    {"value": "min", "size": "15px"},
                                    {"value": "max", "size": "30px"},
                                ],
                            },
                            "help": "Help for numeric prop example A",
                            "unit": "A units",
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "min": 0,
                            "max": 40,
                            "colorGradient": {
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(233, 0, 0, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(96, 2, 2, 1)",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "data": [
                                    {"value": "min", "size": "5px"},
                                    {"value": 20, "size": "8px"},
                                    {"value": "max", "size": "15px"},
                                ],
                            },
                            "help": "Help for numeric prop example B",
                            "unit": "B units",
                        },
                        "selectorPropExample": {
                            "name": "Example Categorical Prop",
                            "type": "selector",
                            "variant": "dropdown",
                            "options": {
                                "a": {
                                    "name": "A",
                                    "color": "rgba(128, 255, 255, 1)",
                                    "size": "3px",
                                },
                                "b": {
                                    "name": "B",
                                    "color": "rgba(0, 153, 51, 1)",
                                    "size": "8px",
                                },
                                "c": {
                                    "name": "C",
                                    "color": "rgba(0, 0, 128, 1)",
                                    "size": "13px",
                                },
                                "d": {
                                    "name": "D",
                                    "color": "rgba(204, 0, 0, 1)",
                                    "size": "18px",
                                },
                                "e": {
                                    "name": "E",
                                    "color": "rgba(153, 77, 0, 1)",
                                    "size": "23px",
                                },
                                "f": {
                                    "name": "F",
                                    "color": "rgba(255, 25, 255, 1)",
                                    "size": "28px",
                                },
                                "g": {
                                    "name": "G",
                                    "color": "rgba(0, 255, 0, 1)",
                                    "size": "33px",
                                },
                                "h": {
                                    "name": "H",
                                    "color": "rgba(255, 255, 0, 1)",
                                    "size": "38px",
                                },
                            },
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
                                "itemId": "selectorPropExample",
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
                            "selectorPropExample": [["e"], ["d"], ["f"]],
                        },
                    },
                },
                "nodeTypeA": {
                    "type": "node",
                    "name": "Node Type A",
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "timeValues": {
                                0: {"min": 50},
                                1: {"min": 0},
                                2: {"min": 20},
                            },
                            "max": 80,
                            "unit": "A units",
                            "colorGradient": {
                                "notation": "precision",
                                "precision": 5,
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(233, 0, 0, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(96, 2, 2, 1)",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "notation": "precision",
                                "precision": 5,
                                "data": [
                                    {"value": "min", "size": "30px"},
                                    {"value": "max", "size": "45px"},
                                ],
                            },
                            "fallback": {
                                "name": "Outlier",
                                "color": "rgba(128, 128, 128, 1)",
                                "size": "20px",
                            },
                            "help": "Help for numeric prop example A",
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "min": 0,
                            "max": 50,
                            "unit": "B units",
                            "colorGradient": {
                                "notation": "scientific",
                                "notationDisplay": "x10^",
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(233, 0, 0, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(96, 2, 2, 1)",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "notation": "scientific",
                                "notationDisplay": "x10^",
                                "data": [
                                    {"value": "min", "size": "10px"},
                                    {"value": 10, "size": "40px"},
                                    {"value": "max", "size": "70px"},
                                ],
                            },
                            "help": "Help for numeric prop example B",
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "options": {
                                "false": {
                                    "name": "Idle",
                                    "color": "rgba(255, 0, 0, 1)",
                                    "size": "15px",
                                },
                                "true": {
                                    "name": "Active",
                                    "color": "rgba(0, 255, 0, 1)",
                                    "size": "30px",
                                },
                            },
                            "fallback": {
                                "name": "Unknown",
                                "color": "rgba(128, 128, 128, 1)",
                                "size": "100px",
                            },
                            "help": "Help for boolean prop",
                        },
                        "selectorPropExample": {
                            "name": "Example Categorical Prop",
                            "type": "selector",
                            "variant": "dropdown",
                            "options": {
                                "a": {
                                    "name": "A",
                                    "color": "rgba(128, 255, 255, 1)",
                                    "size": "3px",
                                },
                                "b": {
                                    "name": "B",
                                    "color": "rgba(0, 153, 51, 1)",
                                    "size": "8px",
                                },
                                "c": {
                                    "name": "C",
                                    "color": "rgba(0, 0, 128, 1)",
                                    "size": "13px",
                                },
                                "d": {
                                    "name": "D",
                                    "color": "rgba(204, 0, 0, 1)",
                                    "size": "18px",
                                },
                                "e": {
                                    "name": "E",
                                    "color": "rgba(153, 77, 0, 1)",
                                    "size": "23px",
                                },
                                "f": {
                                    "name": "F",
                                    "color": "rgba(255, 25, 255, 1)",
                                    "size": "28px",
                                },
                                "g": {
                                    "name": "G",
                                    "color": "rgba(0, 255, 0, 1)",
                                    "size": "33px",
                                },
                                "h": {
                                    "name": "H",
                                    "color": "rgba(255, 255, 0, 1)",
                                    "size": "38px",
                                },
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "timeValues": {
                                0: {
                                    "latitude": [[43.78], [39.82]],
                                },
                                1: {
                                    "latitude": [[44.78], [39.82]],
                                },
                                2: {
                                    "latitude": [[45.78], [39.82]],
                                },
                            },
                            "latitude": [[43.78], [39.82]],
                            "longitude": [[-79.63], [-86.18]],
                        },
                        "valueLists": {
                            "numericPropExampleA": [100, 80],
                            "numericPropExampleB": [50, 40],
                            "booleanPropExample": [True, True],
                            "selectorPropExample": [["a"], ["b"]],
                        },
                    },
                },
                "nodeTypeB": {
                    "type": "node",
                    "name": "Node Type B",
                    "props": {
                        "numericPropExampleA": {
                            "name": "Numeric Prop Example A",
                            "type": "num",
                            "min": 0,
                            "max": 1000,
                            "unit": "A units",
                            "colorGradient": {
                                "notation": "precision",
                                "precision": 5,
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(233, 0, 0, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(96, 2, 2, 1)",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "notation": "precision",
                                "precision": 5,
                                "data": [
                                    {"value": "min", "size": "15px"},
                                    {"value": "max", "size": "30px"},
                                ],
                            },
                            "help": "Help for numeric prop example A",
                        },
                        "numericPropExampleB": {
                            "name": "Numeric Prop Example B",
                            "type": "num",
                            "min": 0,
                            "max": 50,
                            "unit": "B units",
                            "colorGradient": {
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(233, 0, 0, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(96, 2, 2, 1)",
                                    },
                                ],
                            },
                            "sizeGradient": {
                                "data": [
                                    {"value": "min", "size": "10px", "label": "Lo"},
                                    {"value": 10, "size": "40px"},
                                    {"value": "max", "size": "70px", "label": "Hi"},
                                ],
                            },
                            "help": "Help for numeric prop example B",
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "options": {
                                "false": {"color": "rgba(233, 0, 0, 1)"},
                                "true": {"color": "rgba(0, 233, 0, 1)"},
                            },
                            "help": "Help for boolean prop",
                        },
                    },
                    "data": {
                        "location": {
                            "latitude": [[42.89], [28.49], [42.361176]],
                            "longitude": [[-85.68], [-81.56], [-71.084707]],
                        },
                        "valueLists": {
                            "numericPropExampleA": [500, 1000, 1000],
                            "numericPropExampleB": [150, 250, 250],
                            "booleanPropExample": [True, True, True],
                        },
                    },
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
                            "min": 1,
                            "max": 10000,
                            "unit": "C units",
                            "colorGradient": {
                                "scale": "log",
                                "scaleParams": {
                                    "exponent": 0.5,
                                    "base": 10,
                                },
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgb(200, 230, 255)",
                                        "label": "Very Sparse",
                                    },
                                    {
                                        "value": 100,
                                        "color": "rgb(120, 180, 240)",
                                        "label": "Sparse",
                                    },
                                    {
                                        "value": 1000,
                                        "color": "rgb(50, 130, 220)",
                                        "label": "Moderate",
                                    },
                                    {
                                        "value": 5000,
                                        "color": "rgb(255, 140, 0)",
                                        "label": "Dense",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgb(255, 0, 0)",
                                        "label": "Very Dense",
                                    },
                                ],
                            },
                            "help": "Help with the example numeric prop for this State",
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "options": {
                                "false": {"color": "rgba(233, 0, 0, 1)"},
                                "true": {"color": "rgba(0, 233, 0, 1)"},
                            },
                            "help": "Help for boolean prop",
                        },
                    },
                    "data": {
                        "location": {
                            "geoJsonValue": [
                                "CA.ON",
                                "US.MI",
                                "US.MA",
                                "US.FL",
                                "US.IN",
                            ],
                        },
                        "valueLists": {
                            "numericPropExampleC": [1, 8000, 250, 50, 2000],
                            "booleanPropExample": [True, True, False, False, False],
                        },
                    },
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
                            "min": 0,
                            "max": 800,
                            "unit": "units",
                            "colorGradient": {
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(100, 100, 100, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(20, 205, 20, 1)",
                                    },
                                ],
                            },
                            "help": "Help with the example numeric prop for this Country",
                        },
                    },
                    "data": {
                        "location": {
                            "geoJsonValue": ["CA", "US"],
                        },
                        "valueLists": {
                            "numericPropExampleC": [50, 800],
                        },
                    },
                },
                "custom": {
                    "type": "geo",
                    "name": "Custom",
                    "props": {
                        "numericPropExampleC": {
                            "name": "Numeric Prop Example C",
                            "type": "num",
                            "min": 0,
                            "max": 800,
                            "unit": "units",
                            "colorGradient": {
                                "data": [
                                    {
                                        "value": "min",
                                        "color": "rgba(100, 100, 100, 1)",
                                    },
                                    {
                                        "value": "max",
                                        "color": "rgba(20, 205, 20, 1)",
                                    },
                                ],
                            },
                            "help": "Help with the example numeric prop for this Custom",
                        },
                        "booleanPropExample": {
                            "name": "Boolean Prop Example",
                            "type": "toggle",
                            "options": {
                                "false": {"color": "rgba(233, 0, 0, 1)"},
                                "true": {"color": "rgba(0, 233, 0, 1)"},
                            },
                            "help": "Help for boolean prop",
                        },
                    },
                    "data": {
                        "location": {
                            "path": [
                                [
                                    [-75.447, 40.345],
                                    [-77.447, 42.345],
                                    [-77.447, 44.345],
                                    [-75.447, 40.345],
                                ]
                            ],
                        },
                        "valueLists": {
                            "numericPropExampleC": [100],
                            "booleanPropExample": [True],
                        },
                    },
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
                        "region": [
                            "North America",
                            "North America",
                            "North America",
                            "North America",
                            "North America",
                        ],
                        "country": ["USA", "USA", "USA", "USA", "Canada"],
                        "state": [
                            "Michigan",
                            "Massachusetts",
                            "Florida",
                            "Indiana",
                            "Ontario",
                        ],
                    },
                    "name": "Locations",
                    "levels": {
                        "region": {
                            "name": "Regions",
                            "coloring": {"North America": "rgba(255, 255, 255, 1)"},
                        },
                        "country": {
                            "name": "Countries",
                            "ordering": ["Canada", "USA"],
                            "parent": "region",
                            "coloring": {
                                "Canada": "rgba(0, 0, 255, 1)",
                                "USA": "rgba(255, 0, 0, 1)",
                            },
                        },
                        "state": {
                            "name": "States",
                            "parent": "country",
                            "ordering": [
                                "Michigan",
                                "Florida",
                                "Indiana",
                                "Massachusetts",
                                "Ontario",
                            ],
                            "orderWithParent": False,  # True if not specified
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
                    "variant": "icon",
                },
                "kpiHeader2": {
                    "type": "head",
                    "name": "Example KPI Header 2",
                    "icon": "bs/BsTruck",
                    "variant": "icon",
                },
                "key1": {
                    "name": "KPI Example 1",
                    "icon": "bs/BsFillEmojiFrownFill",
                    "precision": 0,
                    "unit": "frowns",
                    "type": "num",
                    "variant": "icon",
                    "draggable": True,
                },
                "key2": {
                    "name": "KPI Example 2",
                    "icon": "bs/BsFillEmojiSmileFill",
                    "precision": 0,
                    "unit": "smiles",
                    "type": "num",
                    "variant": "icon",
                    "draggable": True,
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
            print("The `reset` button has been pressed by the user!")
        return example
    elif command == "solve":
        print("The `solve` button has been pressed by the user!")
        time.sleep(3)
        socket.notify(
            "Priming Thrusters...", title="Initialization", theme="info", duration=3
        )
        time.sleep(3)
        socket.notify("Ignition...", title="Initialization", theme="info")
        time.sleep(3)
        socket.notify(
            "Leak detected in primary power core!", title="Warning:", theme="warning"
        )
        time.sleep(3)
        socket.notify("Engine Failure!", title="Error:", theme="error")
        time.sleep(3)
        socket.notify(
            "Recalibrating Gravitons!", title="Attempting Fix:", theme="warning"
        )
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
