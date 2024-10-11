def execute_command(session_data, socket, command="init", **kwargs):
    # Return the following app state (create a static app with no custom logic)
    return {
        "settings": {
            # Icon Url is used to load icons from a custom icon library
            # See the available versions provided by the cave team here:
            # https://react-icons.mitcave.com/versions.txt
            # Once you select a version, you can see the available icons in the version
            # EG: https://react-icons.mitcave.com/5.0.1/icon_list.txt
            "iconUrl": "https://react-icons.mitcave.com/5.0.1"
        },
        "appBar": {
            # Specify the order of items as they will appear in the app bar
            "order": {"data": ["refreshButton", "chartPage"]},
            "data": {
                # Add a simple button to the app bar to trigger the `init` command
                # This is useful for resetting the app to its initial state
                "refreshButton": {
                    "icon": "md/MdRefresh",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                },
                # Add an app bar button to launch a chart dashboard
                "chartPage": {
                    "icon": "md/MdBarChart",
                    "type": "page",
                    "bar": "upperLeft",
                },
            },
        },
        # Add a chart page to the app using the example map specified above
        "pages": {
            "currentPage": "chartPage",
            "data": {
                "chartPage": {
                    "charts": {
                        # cumulative line chart
                        "chart1": {
                            "type": "groupedOutput",
                            "dataset": "salesData", # changed groupedOutputDataId -> dataset
                            "chartType": "line", # changed variant -> chartType
                            "groupingId": ["product"],
                            "groupingLevel": ["color"],
                            # single-stat chart -> len(stats) == 1
                            "stats": [
                                    {
                                        "statId": "sales",
                                        "aggregationType": "divisor",
                                        "statIdDivisor": "demand",
                                    },
                            ],
                            # optional chartOptions to configure 
                            "chartOptions": {
                                "cumulative": True, # optional parameter to turn line -> cumulative line
                            }
                        },
                        # mixed chart
                        "chart2": {
                            "type": "groupedOutput",
                            "dataset": "salesData",
                            "chartType": "mixed",
                            "groupingId": ["product", "location"],
                            "groupingLevel": ["color", "state"],
                            "stats": [
                                    # stat[0] = left stat
                                    {
                                        "statId": "demand",
                                        "aggregationType": "mean",
                                        # no aggregation grouping specified -> default None
                                    },
                                    # stat[1] = right stat
                                    {
                                        "statId": "sales",
                                        "aggregationType": "sum",
                                    },
                            ],
                            "chartOptions": {
                                "leftChartType": "bar",
                                "rightChartType": "cumulative_line",
                            }
                        },
                        # table chart
                        "chart3": {
                            "type": "groupedOutput",
                            "dataset": "salesData",
                            "chartType": "table",
                            "groupingId": ["product"],
                            "groupingLevel": ["color"],
                            "stats": [
                                    {
                                        "statId": "demand",
                                        "aggregationType": "sum",
                                    },
                                    {
                                        "statId": "sales",
                                        "aggregationType": "mean",
                                        "aggregationGroupingId": "product", # specifies aggregation grouping
                                        "aggregationGroupingLevel": "size",
                                    },
                                    {
                                        "statId": "pctDemandMet",
                                        "aggregationType": "sum",
                                    },
                            ],
                        },
                        # distribution chart
                        "type": "groupedOutput",
                        "dataset": "salesData",
                        "chartType": "distribution",
                        "groupingId": ["product", "location"],
                        "groupingLevel": ["color", "state"],
                        "stats": [
                                {
                                    "statId": "demand",
                                    "aggregationType": "sum",
                                },
                        ],
                        "chartOptions": {
                            "cumulative": True,
                            "yAxis": "density",
                            "variant": "bar" # not 100% with this name
                        }
                    },
                    "pageLayout": ["chart1", "chart2", "chart3", "chart4"],
                },
            },
        },
        "groupedOutputs": {
            "order": {
                "groupings": ["location", "product"],
            },
            "groupings": {
                "location": {
                    "order": {
                        "levels": ["country", "state"],
                    },
                    "data": {
                        "id": ["UsMi", "UsMa", "CaOn", "CaQc"],
                        "country": ["USA", "USA", "Canada", "Canada"],
                        "state": ["Michigan", "Massachusetts", "Ontario", "Quebec"],
                    },
                    "name": "Locations",
                    "levels": {
                        "country": {
                            "name": "Countries",
                            "ordering": ["USA", "Canada"],
                        },
                        "state": {
                            "name": "States",
                            "parent": "country",
                        },
                    },
                    "layoutDirection": "horizontal",
                },
                "product": {
                    "order": {
                        "levels": ["color", "size", "product"],
                    },
                    "data": {
                        "id": ["apple", "grape", "strawberry"],
                        "color": ["Red", "Purple", "Red"],
                        "size": ["Medium", "Small", "Small"],
                        "product": ["Apple", "Grape", "Strawberry"],
                    },
                    "name": "Products",
                    "levels": {
                        "color": {
                            "name": "Colors",
                        },
                        "size": {
                            "name": "Sizes",
                            "ordering": ["Small", "Medium"],
                        },
                        "product": {
                            "name": "Products",
                        },
                    },
                    "layoutDirection": "horizontal",
                },
            },
            "data": {
                "salesData": {
                    "order": {
                        "stats": [
                            "demand",
                            "sales",
                            "pctDemandMet",
                        ],
                    },
                    "stats": {
                        "demand": {
                            "name": "Demand",
                            "calculation": "demand",
                            "unit": "units",
                        },
                        "sales": {
                            "name": "Sales",
                            "calculation": "sales",
                            "unit": "units",
                        },
                        "pctDemandMet": {
                            "name": "Percent of Demand Met",
                            "calculation": 'sales / groupSum("demand")',
                            "precision": 2,
                            "trailingZeros": True,
                            "unit": "%",
                            "unitPlacement": "after",
                        },
                    },
                    "valueLists": {
                        "demand": [100, 108, 115, 110, 70, 78, 67, 89, 95, 100, 100, 98],
                        "sales": [95, 100, 100, 98, 60, 65, 67, 75, 80, 90, 99, 98],
                    },
                    "groupLists": {
                        "location": [
                            "UsMi",
                            "UsMa",
                            "CaOn",
                            "CaQc",
                            "UsMi",
                            "UsMa",
                            "CaOn",
                            "CaQc",
                            "UsMi",
                            "UsMa",
                            "CaOn",
                            "CaQc",
                        ],
                        "product": [
                            "apple",
                            "apple",
                            "apple",
                            "apple",
                            "grape",
                            "grape",
                            "grape",
                            "grape",
                            "strawberry",
                            "strawberry",
                            "strawberry",
                            "strawberry",
                        ],
                    },
                },
            },
        },
    }
