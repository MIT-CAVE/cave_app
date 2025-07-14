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
                    "examplePane",
                ],
            },
            "data": {
                # Add a pane to the app bar
                # This will add a button to the app bar that opens a pane
                # Panes are used to display additional options / data to the user
                # See the panes top level key below for more details
                "examplePane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "variant": "wall",
                    "bar": "upperLeft",
                },
            },
        },
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "examplePane", "pin": True}},
            "data": {
                # Create an options pane with all of the available props
                "examplePane": {
                    "name": "Example Props Pane",
                    # Use an example of each prop and variant available in the api
                    "props": {
                        "hiddenProp": {
                            "name": "Hidden Prop",
                            "type": "num",
                            "display": False,
                            "help": "This prop is hidden",
                        },
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
                            "name": "Incremental Slider Example",
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
                            "name": "Button Input Example",
                            "type": "button",
                            "apiCommand": "test",
                            "help": "Press this button to test the api",
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
                                "option_a": {
                                    "name": "Option A",
                                    "color": "rgb(255 0 0)",
                                    "size": "10px",
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "size": "20px",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "rgb(0 0 255)",
                                    "size": "30px",
                                },
                                "option_d": {"name": "Option D"},
                            },
                            "help": "Select an option from the dropdown",
                        },
                        "checkboxItemExample": {
                            "name": "Checkbox Item Example",
                            "type": "selector",
                            "variant": "checkbox",
                            "color": "#8010a6",
                            "options": {
                                "option_a": {
                                    "name": "Option A",
                                    "color": "#f44336",
                                    "activeColor": "#f0fa08"
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "color": "#66bb6a",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "#29b6f6",
                                },
                                "option_d": {
                                    "name": "Option D",
                                    "color": "#ffa726",
                                },
                                "option_e": {"name": "Option E"},
                            },
                            "help": "Select all relevant items",
                        },
                        "radioItemExample": {
                            "name": "Radio Item Example",
                            "type": "selector",
                            "variant": "radio",
                            "options": {
                                "option_a": {
                                    "name": "Option A",
                                    "color": "#f44336",
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "color": "#66bb6a",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "#29b6f6",
                                },
                                "option_d": {
                                    "name": "Option D",
                                    "color": "#ffa726",
                                },
                                "option_e": {"name": "Option E"},
                            },
                            "help": "Select one item from the list",
                        },
                        "hstepperItemExample": {
                            "name": "Horizontal Stepper Item Example",
                            "type": "selector",
                            "variant": "hstepper",
                            "options": {
                                "option_a": {
                                    "name": "Option A",
                                    "color": "#f44336",
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "color": "#66bb6a",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "#29b6f6",
                                },
                                "option_d": {
                                    "name": "Option D",
                                    "color": "#ffa726",
                                },
                                "option_e": {"name": "Option E"},
                            },
                            "help": "Select an option from the stepper",
                        },
                        "vstepperItemExample": {
                            "name": "Vertical Stepper Item Example",
                            "type": "selector",
                            "variant": "vstepper",
                            "color": "#ce93d8",
                            "options": {
                                "option_a": {
                                    "name": "Option A",
                                    "color": "#f44336",
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "color": "#66bb6a",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "#29b6f6",
                                },
                                "option_d": {
                                    "name": "Option D",
                                    "color": "#ffa726",
                                },
                                "option_e": {"name": "Option E"},
                            },
                            "help": "Select an option from the stepper",
                        },
                        "hradioItemExample": {
                            "name": "Horizontal Radio Item Example",
                            "type": "selector",
                            "variant": "hradio",
                            "options": {
                                "option_a": {
                                    "name": "Option A",
                                    "color": "#f44336",
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "color": "#66bb6a",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "#29b6f6",
                                },
                                "option_d": {
                                    "name": "Option D",
                                    "color": "#ffa726",
                                },
                                "option_e": {"name": "Option E"},
                            },
                            "help": "Select an option from the radio",
                        },
                        "comboBoxItemExample": {
                            "name": "ComboBox Item Example",
                            "type": "selector",
                            "variant": "combobox",
                            "placeholder": "Options",
                            "options": {
                                "option_a": {
                                    "name": "Option A",
                                    "color": "#f44336",
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "color": "#66bb6a",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "#29b6f6",
                                },
                                "option_d": {
                                    "name": "Option D",
                                    "color": "#ffa726",
                                },
                                "option_e": {"name": "Option E"},
                            },
                            "help": "Select an option from the combobox",
                        },
                        "comboBoxMultiExample": {
                            "name": "ComboBox Multi Example",
                            "type": "selector",
                            "variant": "comboboxMulti",
                            "placeholder": "Select multiple options",
                            "options": {
                                "option_a": {
                                    "name": "Option A",
                                    "color": "#f44336",
                                },
                                "option_b": {
                                    "name": "Option B",
                                    "color": "#66bb6a",
                                },
                                "option_c": {
                                    "name": "Option C",
                                    "color": "#29b6f6",
                                },
                                "option_d": {
                                    "name": "Option D",
                                    "color": "#ffa726",
                                },
                                "option_e": {"name": "Option E"},
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
                                    "color": "rgb(0 128 255)",
                                },
                                "t1_b1_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree1", "Branch1"],
                                    "color": "rgb(0 0 255)",
                                },
                                "t1_b1_tw3": {
                                    "name": "Twig3",
                                    "path": ["Tree1", "Branch1"],
                                    "color": "rgb(128 0 255)",
                                },
                                "t1_b2_tw1": {
                                    "name": "Twig1",
                                    "path": ["Tree1", "Branch2"],
                                    "color": "rgb(128 255 0)",
                                },
                                "t1_b2_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree1", "Branch2"],
                                    "color": "rgb(0 255 0)",
                                },
                                "t2_b1_tw1": {
                                    "name": "Twig1",
                                    "path": ["Tree2", "Branch1"],
                                    "color": "rgb(255 128 255)",
                                },
                                "t2_b1_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree2", "Branch1"],
                                    "color": "rgb(0 128 0)",
                                },
                                "t2_b2_tw1": {
                                    "name": "Twig1",
                                    "path": ["Tree2", "Branch2"],
                                    "color": "rgb(255 0 255)",
                                },
                                "t2_b2_tw2": {
                                    "name": "Twig2",
                                    "path": ["Tree2", "Branch2"],
                                    "color": "rgb(0 128 128)",
                                },
                                "t2_b2_tw3": {
                                    "name": "Twig3",
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
                            "views": ["year", "month", "day"],
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
                    # Specify the values for each prop listed above
                    "values": {
                        "hiddenProp": 0,
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
                    # Create a custom grid layout for the pane items
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
    }
