def execute_command(session_data, socket, command="init", **kwargs):
    # Rich text: inline markdown (`**bold**`, `_italic_`, `` `code` ``, `[links](url)`) and
    # inline math (`$x^2$`) in labels, controlled by the generic `richText` key.
    #
    # `richText` cascades. The closest value that is set wins:
    #   prop > layout item > ancestor layout grids > pane / global outputs
    #   For a map legend: prop > feature type > `settings.defaults.richText`
    #   For the text of a map: map > `settings.defaults.richText`
    #
    # Note: `settings.defaults.richText` is the app-wide default. It is not set here, as it
    # would make every label of this example rich and hide the differences shown below.
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            "iconUrl": "https://react-icons.mitcave.com/5.4.0"
        },
        "appBar": {
            "order": {"data": ["richTextPane", "richRootPane", "richPage", "richChartPage"]},
            "data": {
                "richTextPane": {
                    "icon": "fa/FaCogs",
                    "type": "pane",
                    "variant": "wall",
                    "bar": "upperLeft",
                },
                "richRootPane": {
                    "icon": "im/ImFont",
                    "type": "pane",
                    "variant": "wall",
                    "bar": "upperLeft",
                },
                # A page with a map
                "richPage": {
                    "icon": "md/MdMap",
                    "type": "page",
                    "bar": "lowerLeft",
                },
                # A page with tables of grouped outputs and global outputs
                "richChartPage": {
                    "icon": "md/MdTableChart",
                    "type": "page",
                    "bar": "lowerLeft",
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
                        # The helper text of a prop is rich text too
                        "textExample": {
                            "name": "Project _name_",
                            "type": "text",
                            "helperText": "Use **lowercase** letters, digits and `-`",
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
                        "textExample": "cave-routing",
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
                            "item2": {"type": "item", "itemId": "textExample"},
                            "item3": {"type": "item", "itemId": "plainExample"},
                            "item4": {"type": "item", "itemId": "plainHelpExample"},
                            # Enable `richText` for every prop of a nested grid at once
                            "richGrid": {
                                "type": "grid",
                                "numColumns": 1,
                                "richText": True,
                                "data": {
                                    "item5": {"type": "item", "itemId": "dropdownExample"},
                                    "item6": {"type": "item", "itemId": "cascadedExample"},
                                    "item7": {"type": "item", "itemId": "optOutExample"},
                                },
                            },
                        },
                    },
                },
                # `richText` on a pane makes its `name` rich and cascades to all of its props
                "richRootPane": {
                    "name": "**Pane** root: $x^2$",
                    "richText": True,
                    "props": {
                        # No `richText` on the prop or on a layout: it comes from the pane
                        "rootExample": {
                            "name": "Inherits the **pane** root",
                            "subtitle": "Without a `richText` of its own",
                            "type": "num",
                        },
                        # A prop can still opt out
                        "optOutExample": {
                            "name": "Opts **out** of the pane root",
                            "type": "num",
                            "richText": False,
                        },
                    },
                    "values": {"rootExample": 1, "optOutExample": 2},
                },
            },
        },
        # `richText` on the global outputs is the root of the cascade for their props
        "globalOutputs": {
            "richText": True,
            "props": {
                "throughput": {
                    "name": "**Throughput**",
                    "icon": "md/MdSpeed",
                    "precision": 0,
                    "unit": "$m^3$/h",
                    "type": "num",
                    "variant": "icon",
                },
                "cost": {
                    "name": "_Cost_ per unit",
                    "icon": "md/MdAttachMoney",
                    "precision": 2,
                    "unit": "USD",
                    "type": "num",
                    "variant": "icon",
                },
            },
            "values": {"throughput": 1250, "cost": 4.75},
        },
        "maps": {
            "data": {
                "exampleMap": {
                    # `richText` on a map makes the text that belongs to the map rich:
                    # its name, its legend groups and the names in its map modals
                    "name": "**Rich** text map",
                    "richText": True,
                    "currentProjection": "mercator",
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
                            "name": "_Facilities_ of the network",
                            "data": {
                                "warehouse": {
                                    "value": True,
                                    "colorBy": "capacity",
                                    "colorByOptions": ["capacity", "includesAutomation"],
                                    "sizeBy": "capacity",
                                    "sizeByOptions": ["capacity"],
                                    "icon": "fa6/FaWarehouse",
                                    # Allow the user to group the warehouses in clusters,
                                    # and group them by default
                                    "allowGrouping": True,
                                    "group": True,
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
                    # `richText` on a feature type makes its `name`, the text of its legend
                    # (prop names, units, gradient labels, option names) and its modals rich
                    "name": "**Warehouse**",
                    "richText": True,
                    "props": {
                        "capacity": {
                            "name": "**Capacity**",
                            "type": "num",
                            "unit": "$ft^3$",
                            "help": "The warehouse capacity in cubic feet",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {
                                        "value": "min",
                                        "label": "_Small_",
                                        "size": "30px",
                                        "color": "rgb(233 0 0)",
                                    },
                                    {
                                        "value": "max",
                                        "label": "**Large**",
                                        "size": "45px",
                                        "color": "rgb(96 2 2)",
                                    },
                                ],
                            },
                        },
                        "includesAutomation": {
                            "name": "Includes _automation_",
                            "type": "toggle",
                            "help": "Whether the warehouse includes automation",
                            "options": {
                                "false": {"name": "_Manual_", "color": "rgb(255 0 0)"},
                                "true": {"name": "**Automated**", "color": "rgb(0 255 0)"},
                            },
                        },
                        # A prop can opt out of the `richText` of its feature type
                        "scenario": {
                            "name": "Scenario *1*",
                            "type": "text",
                            "enabled": False,
                            "richText": False,
                            "help": "The scenario name",
                        },
                    },
                    "data": {
                        # The warehouses are close to each other, so they can be grouped
                        "location": {
                            "latitude": [[43.78], [39.82], [43.65], [43.9], [39.77], [40.0]],
                            "longitude": [
                                [-79.63],
                                [-86.18],
                                [-79.38],
                                [-79.9],
                                [-86.16],
                                [-86.4],
                            ],
                        },
                        "valueLists": {
                            "capacity": [100, 80, 90, 120, 70, 60],
                            "includesAutomation": [True, False, True, True, False, False],
                            "scenario": [
                                "Scenario 1",
                                "Scenario 2",
                                "Scenario 1",
                                "Scenario 1",
                                "Scenario 2",
                                "Scenario 2",
                            ],
                        },
                    },
                },
            }
        },
        # The names of a chart come from the grouped outputs. `richText` can be set on a stat,
        # on its dataset, on a grouping level or on its grouping
        "groupedOutputs": {
            "groupings": {
                "location": {
                    "name": "_Location_",
                    "richText": True,
                    "order": {"levels": ["country", "state"]},
                    "data": {
                        "id": ["UsMi", "UsMa", "CaOn"],
                        "country": ["USA", "USA", "Canada"],
                        "state": ["Michigan", "Massachusetts", "Ontario"],
                    },
                    "levels": {
                        "country": {"name": "**Country**"},
                        "state": {"name": "**State**", "parent": "country"},
                    },
                },
            },
            "data": {
                "salesData": {
                    "richText": True,
                    "stats": {
                        "sales": {"name": "**Sales**", "unit": "$m^3$"},
                        # A stat can opt out of the `richText` of its dataset
                        "demand": {"name": "snake_case **demand**", "richText": False},
                    },
                    "valueLists": {"sales": [95, 100, 60], "demand": [100, 108, 70]},
                    "groupLists": {"location": ["UsMi", "UsMa", "CaOn"]},
                },
            },
        },
        # Add a page with the map specified above
        "pages": {
            "currentPage": "richPage",
            "data": {
                "richPage": {
                    "charts": {
                        "map": {
                            "type": "map",
                            "mapId": "exampleMap",
                            "maximized": True,
                        },
                    },
                    "pageLayout": ["map", None, None, None],
                },
                "richChartPage": {
                    "charts": {
                        # The headers of a table are rich when the stat (or dataset) and the
                        # grouping (or level) are. Canvas text (axes, legends, tooltips) shows
                        # the plain text instead.
                        "groupedTable": {
                            "dataset": "salesData",
                            "chartType": "table",
                            "stats": [{"statId": "sales", "aggregationType": "sum"}],
                            "groupingId": ["location"],
                            "groupingLevel": ["state"],
                        },
                        "groupedBar": {
                            "dataset": "salesData",
                            "chartType": "bar",
                            "stats": [{"statId": "sales", "aggregationType": "sum"}],
                            "groupingId": ["location"],
                            "groupingLevel": ["state"],
                        },
                        # An overview of the global outputs, which are rich
                        "overview": {
                            "type": "globalOutput",
                            "chartType": "overview",
                        },
                        # The columns follow the `richText` of the global outputs props
                        "outputsTable": {
                            "type": "globalOutput",
                            "chartType": "table",
                            "globalOutput": ["throughput", "cost"],
                        },
                    },
                    "pageLayout": ["groupedTable", "groupedBar", "outputsTable", "overview"],
                },
            },
        },
    }
