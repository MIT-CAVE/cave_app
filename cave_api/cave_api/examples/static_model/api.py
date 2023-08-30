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
                    "map2": {
                        "show": False,
                    },
                    "map1": {
                        "scrollSpeed": 2,
                    },
                    "dash1": {
                        "displayTime": 1,
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
                        "data": {"ps1": ["appBar", "data", "appBarId"]},
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
        "categories": {
            "allowModification": False,
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
        },
        "appBar": {
            "data": {
                "session": {
                    "icon": "md/MdApi",
                    "type": "pane",
                    "bar": "upperLeft",
                    "order": 0,
                },
                "appSettings": {
                    "icon": "md/MdOutlineSettings",
                    "type": "pane",
                    "bar": "upperLeft",
                    "order": 1,
                },
                "resetButton": {
                    "icon": "md/MdSync",
                    "color": {
                        "dark": "rgb(255, 101, 101)",
                        "light": "rgb(212, 0, 0)",
                    },
                    "apiCommand": "reset",
                    "type": "button",
                    "bar": "upperLeft",
                    "order": 2,
                },
                "buttonSolve": {
                    "icon": "bs/BsLightningFill",
                    "color": {
                        "dark": "rgb(178, 179, 55)",
                        "light": "rgb(79, 79, 24)",
                    },
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
                "context1": {
                    "icon": "bs/BsInboxes",
                    "type": "pane",
                    "order": 5,
                    "bar": "upperLeft",
                },
                "filter": {
                    "icon": "fa/FaFilter",
                    "type": "pane",
                    "order": 6,
                    "bar": "upperLeft",
                },
                "map1": {
                    "type": "map",
                    "icon": "fa/FaMapMarkedAlt",
                    "bar": "lowerLeft",
                    "order": 0,
                },
                "map2": {
                    "type": "map",
                    "icon": "fa/FaMapMarked",
                    "bar": "lowerLeft",
                    "order": 1,
                },
                "dash1": {
                    "type": "stats",
                    "icon": "md/MdInsertChart",
                    "order": 1,
                    "bar": "lowerLeft",
                },
                "dash2": {
                    "type": "stats",
                    "icon": "md/MdInsertChartOutlined",
                    "order": 2,
                    "bar": "lowerLeft",
                },
                "kpi1": {
                    "type": "kpi",
                    "icon": "md/MdSpeed",
                    "bar": "lowerLeft",
                    "order": 2,
                },
                "exampleModal": {
                    "icon": "md/MdInfo",
                    "color": {
                        "dark": "rgb(195, 164, 222)",
                        "light": "rgb(84, 60, 107)",
                    },
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
                            "value": "Press",
                            "type": "button",
                            "apiCommand": "viewInfo",
                            "enabled": True,
                            "help": "Press this button to view info",
                        },
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
                "session": {
                    "variant": "session",
                    "name": "Sessions Pane",
                },
                "appSettings": {
                    "name": "App Settings Pane",
                    "variant": "appSettings",
                },
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
                            "value": 50,
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
                            "value": 50,
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
                        "pictureExample": {
                            "name": "Picture Example",
                            "type": "media",
                            "variant": "picture",
                            "value": "https://ctl.mit.edu/sites/ctl.mit.edu/files/inline-images/MIT_CTL_CAVE_Lab_2.png",
                            "help": "Click the expand button to view an enlarged version",
                        },
                        "videoExample": {
                            "name": "Video Example",
                            "type": "media",
                            "variant": "video",
                            "value": "https://www.youtube.com/embed/6q5R1TDmKnU",
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
                            "value": "Example Text Here",
                            "enabled": True,
                            "help": "Help for the text input example",
                        },
                        "textAreaInputExample": {
                            "name": "TextArea Input Example",
                            "type": "text",
                            "variant": "textarea",
                            "rows": 6,
                            "value": "Velit non incididunt velit quis commodo consequat velit nulla. Id sunt sint consequat do in. Et adipisicing aliqua voluptate eu consequat et dolore mollit sit veniam minim nisi tempor. Enim laboris proident ex magna. Duis culpa veniam et officia irure id qui id ad laborum deserunt dolor proident elit.",
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
                            "value": ["option_c"],
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
                            "value": ["option_a", "option_c"],
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
                            "value": ["option_a"],
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
                                "value": ["option_c"],
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
                                "value": ["option_c"],
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
                                "value": ["option_c"],
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
                            "value": ["option_b"],
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
                            "value": ["t1_b1_tw1", "t1_b1_tw2", "t1_b2_tw2", "t2_b1_tw1", "t2_b1_tw2"],
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
                            "value": "07/20/1969",
                            "enabled": True,
                            "help": "The Eagle has landed!",
                        },
                        "timeItemExample": {
                            "name": "Time Example",
                            "type": "date",
                            "variant": "time",
                            "value": "1969-07-20T20:17:40",
                            "enabled": True,
                            "help": "The Eagle has landed!",
                        },
                        "dateTimeItemExample": {
                            "name": "Date and Time Example",
                            "type": "date",
                            "variant": "datetime",
                            "value": "1969-07-20T20:17:40",
                            "enabled": True,
                            "help": "The Eagle has landed!",
                        },
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
                "filter": {
                    "name": "Filter",
                    "variant": "filter",
                },
                "context1": {
                    "name": "Context Pane",
                    "variant": "context",
                    "props": {
                        "numericContextProp": {
                            "name": "Numeric Context Prop",
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
                        "context1": {
                            "prop": "numericContextProp",
                            "value": 110,
                            "applyCategories": {"location": ["locUsMi"]},
                        }
                    },
                },
            },
        },
        "dashboards": {
            "data": {
                "dash1": {
                    "dashboardLayout": [
                        {
                            "chart": "Bar",
                            "grouping": "Average",
                            "statistic": "numericStatExampleA",
                        },
                        {
                            "type": "kpis",
                            "chart": "Line",
                            "grouping": "Sum",
                            "sessions": [],
                            "kpi": ["key1", "key2"],
                        },
                        {
                            "chart": "Bar",
                            "level": "size",
                            "category": "sku",
                            "grouping": "Sum",
                            "statistic": "numericExampleCalculationStat",
                        },
                        {
                            "chart": "Stacked Waterfall",
                            "grouping": "Sum",
                            "statistic": "numericStatExampleA",
                            "category": "location",
                            "level": "state",
                            "category2": "sku",
                            "level2": "sku",
                        },
                    ],
                    "lockedLayout": False,
                },
                "dash2": {
                    "dashboardLayout": [
                        {
                            "chart": "Bar",
                            "grouping": "Average",
                            "statistic": "numericStatExampleB",
                        },
                        {
                            "type": "kpis",
                            "chart": "Bar",
                            "grouping": "Sum",
                            "sessions": [],
                            "kpi": ["key1", "key2"],
                        },
                        {
                            "chart": "Box Plot",
                            "level": "size",
                            "category": "sku",
                            "grouping": "Average",
                            "statistic": "numericExampleCalculationStat",
                        },
                        {
                            "chart": "Cumulative Line",
                            "grouping": "Sum",
                            "statistic": "numericStatExampleB",
                            "category": "location",
                            "level": "state",
                            "category2": "sku",
                            "level2": "sku",
                        },
                    ],
                    "lockedLayout": False,
                },
            }
        },
        "maps": {
            "data": {
                "map1": {
                    "currentStyle": "watercolor",
                    "currentProjection": "globe",
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
                            "nodes": {
                                "nodeTypeA": {
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
                                    # # Allow group matching only when a category value matches
                                    # "groupMatchCategory": "location",
                                    # "groupMatchCategoryLevel": "state",
                                }
                            },
                            "arcs": {
                                "T1": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                }
                            },
                            "order": 1,
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "nodes": {
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
                                    # # Allow group matching only when a category value matches
                                    # "groupMatchCategory": "location",
                                    # "groupMatchCategoryLevel": "state",
                                }
                            },
                            "arcs": {
                                "T2": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                }
                            },
                            "geos": {
                                "state": {
                                    "value": True,
                                    "colorBy": "numericPropExampleC",
                                },
                                "country": {
                                    "value": False,
                                    "colorBy": "numericPropExampleC",
                                },
                            },
                            "order": 2,
                        },
                    },
                },
                "map2": {
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
                            "nodes": {
                                "nodeTypeA": {
                                    "value": True,
                                    "sizeBy": "numericPropExampleA",
                                    "colorBy": "booleanPropExample",
                                }
                            },
                            "arcs": {
                                "T1": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                }
                            },
                            "order": 1,
                        },
                        "lgb": {
                            "name": "Legend Group B",
                            "nodes": {
                                "nodeTypeB": {
                                    "value": True,
                                    "sizeBy": "numericPropExampleB",
                                    "colorBy": "booleanPropExample",
                                }
                            },
                            "arcs": {
                                "T2": {
                                    "colorBy": "numericPropExampleA",
                                    "sizeBy": "numericPropExampleB",
                                    "value": True,
                                }
                            },
                            "geos": {
                                "state": {
                                    "value": True,
                                    "colorBy": "numericPropExampleC",
                                },
                                "country": {
                                    "value": False,
                                    "colorBy": "numericPropExampleC",
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
                    "colorByOptions": {
                        "selectorPropForColor": {
                            "a": "rgb(128,255,255)",
                            "b": "rgb(0,153,51)",
                            "c": "rgb(0,0,128)",
                            "d": "rgb(204,0,0)",
                            "e": "rgb(153,77,0)",
                            "f": "rgb(255,25,255)",
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
                    "geoJson": {
                        "geoJsonLayer": "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart.geo.json",
                        "geoJsonProp": "name",
                    },
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 50},
                        "numericPropExampleB": {"min": 0, "max": 40},
                    },
                    "startSize": "15px",
                    "endSize": "30px",
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
                            "value": ["a"],
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
                },
                "T2": {
                    "name": "Flow Type 2",
                    "colorByOptions": {
                        "selectorPropForColor": {
                            "a": "rgb(128,255,255)",
                            "b": "rgb(0,153,51)",
                            "c": "rgb(0,0,128)",
                            "d": "rgb(204,0,0)",
                            "e": "rgb(153,77,0)",
                            "f": "rgb(255,25,255)",
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
                    "lineBy": "dotted",
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 50},
                        "numericPropExampleB": {"min": 0, "max": 40},
                    },
                    "startSize": "15px",
                    "endSize": "30px",
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
                            "value": ["a"],
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
                },
            },
            "data": {
                "arc1": {
                    "geoJsonValue": "DUBL-DALY (ROUTE 11/12)",
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
                            "value": ["b"],
                        },
                    },
                },
                "arc2": {
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
                            "value": ["e"],
                        },
                    },
                },
                "arc3": {
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
                            "value": ["d"],
                        },
                    },
                },
                "arc4": {
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
                            "value": ["f"],
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
                            "timeValues": {
                                0: {"min": 50},
                                1: {"min": 0},
                                2: {"min": 20},
                            },
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
                        "booleanPropExample": {
                            "false": "rgb(255,0,0)",
                            "true": "rgb(0,255,0)",
                        },
                    },
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 80},
                        "numericPropExampleB": {"min": 0, "max": 50},
                    },
                    "startSize": "30px",
                    "endSize": "45px",
                    "icon": "fa6/FaIgloo",
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
                        "booleanPropExample": {
                            "false": "rgb(233, 0, 0)",
                            "true": "rgb(0, 233, 0)",
                        },
                    },
                    "sizeByOptions": {
                        "numericPropExampleA": {"min": 0, "max": 100},
                        "numericPropExampleB": {"min": 0, "max": 250},
                    },
                    "startSize": "30px",
                    "endSize": "45px",
                    "icon": "bs/BsBuilding",
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
                            "value": True,
                            "enabled": True,
                            "help": "Help for boolean prop",
                        },
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
                "node2": {
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
                "node3": {
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
                "node4": {
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
                "node5": {
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
                        },
                        "booleanPropExample": {
                            "false": "rgb(233, 0, 0)",
                            "true": "rgb(0, 233, 0)",
                        },
                    },
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/world-states-provinces-md.json",
                        "geoJsonProp": "code_hasc",
                    },
                    "icon": "bs/BsHexagon",
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
                            "enabled": True,
                            "help": "Help for boolean prop",
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
                    "geoJson": {
                        "geoJsonLayer": "https://geojsons.mitcave.com/world/countries-sm.json",
                        "geoJsonProp": "FIPS_10",
                    },
                    "icon": "bs/BsHexagon",
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
                    "category": {"location": ["locCaOn"]},
                    "props": {
                        "numericPropExampleC": {
                            "timeValues": {
                                0: { "value": 0 },
                                1: { "value": 100 },
                                2: { "value": 300 },
                            }
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
                        },
                        "booleanPropExample": {
                            "value": True,
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
                        },
                        "booleanPropExample": {
                            "value": False,
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
                        },
                        "booleanPropExample": {
                            "value": False,
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
                        },
                        "booleanPropExample": {
                            "value": False,
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
                    "groupByOptions": ["location"],
                    "precision": 2,
                    "trailingZeros": True,
                    "unit": "%",
                    "unitPlacement": "after",
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
                    "values": {"numericStatExampleA": -3, "numericStatExampleB": 5},
                },
                "d5": {
                    "category": {
                        "location": ["locUsIn"],
                        "sku": ["SKU2"],
                    },
                    "values": {"numericStatExampleA": -3, "numericStatExampleB": -2},
                },
                "d6": {
                    "category": {
                        "location": ["locUsFl"],
                        "sku": ["SKU2"],
                    },
                    "values": {"numericStatExampleA": 1, "numericStatExampleB": -1},
                },
            },
        },
        "kpis": {
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
                    "mapKpi": True,
                },
                "key2": {
                    "name": "KPI Example 2",
                    "icon": "bs/BsFillEmojiSmileFill",
                    "value": 32,
                    "precision": 0,
                    "unit": "smiles",
                    "mapKpi": True,
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
                },
            },
        },
        "kwargs": {
            "wipeExisting": True,
        },
    }
    if command == "reset":
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