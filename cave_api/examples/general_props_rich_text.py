def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0"
        },
        "appBar": {
            "order": {"data": ["richTextPane"]},
            "data": {
                "richTextPane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "variant": "wall",
                    "bar": "upperLeft",
                },
            },
        },
        "panes": {
            "paneState": {"left": {"type": "pane", "open": "richTextPane", "pin": True}},
            "data": {
                "richTextPane": {
                    "name": "Rich Text Props",
                    "props": {
                        # `richText` can be set on an individual prop
                        "areaExample": {
                            "name": "**Area** of the _site_",
                            "subtitle": "Measured in `square` meters",
                            "unit": "$m^2$",
                            "type": "num",
                            "help": "Labels support **bold**, _italics_, `code`, [links](https://example.com) and math like $E = mc^2$.",
                            "richText": True,
                        },
                        # Without `richText` the labels are plain text,
                        # so special characters are shown as they are
                        "plainExample": {
                            "name": "snake_case and **stars**",
                            "type": "num",
                            "help": "`help` is still rendered as **markdown** by default.",
                        },
                        # With `richText` set to `False`, `help` is plain text too
                        "plainHelpExample": {
                            "name": "Plain Help",
                            "type": "num",
                            "help": "# This is not a heading\n\nThis is **not** bold.",
                            "richText": False,
                        },
                        # The option names of a prop inherit its `richText`
                        "dropdownExample": {
                            "name": "Rich _Dropdown_",
                            "type": "selector",
                            "variant": "dropdown",
                            "richText": True,
                            "options": {
                                "a": {"name": "**Bold** option"},
                                "b": {"name": "CO$_2$ emissions"},
                                "c": {"name": "A [linked](https://example.com) option"},
                            },
                        },
                        # `richText` cascades from the nested layout grid below
                        "cascadedExample": {
                            "name": "Cascaded **Radio**",
                            "type": "selector",
                            "variant": "radio",
                            "options": {
                                "a": {"name": "_Italic_ option"},
                                "b": {"name": "`Code` option"},
                            },
                        },
                        # Opt out of the value cascading from the nested layout grid
                        "optOutExample": {
                            "name": "Opt **out** of the cascade",
                            "type": "num",
                            "richText": False,
                        },
                    },
                    "values": {
                        "areaExample": 10,
                        "plainExample": 5,
                        "plainHelpExample": 1,
                        "dropdownExample": ["a"],
                        "cascadedExample": ["a"],
                        "optOutExample": 3,
                    },
                    "layout": {
                        "type": "grid",
                        "numColumns": 2,
                        "data": {
                            "item1": {"type": "item", "itemId": "areaExample"},
                            "item2": {"type": "item", "itemId": "plainExample"},
                            "item3": {"type": "item", "itemId": "plainHelpExample"},
                            # Enable `richText` for every prop of a nested grid at once
                            "richGrid": {
                                "type": "grid",
                                "numColumns": 1,
                                "richText": True,
                                "data": {
                                    "item4": {"type": "item", "itemId": "dropdownExample"},
                                    "item5": {"type": "item", "itemId": "cascadedExample"},
                                    "item6": {"type": "item", "itemId": "optOutExample"},
                                },
                            },
                        },
                    },
                },
            },
        },
    }
