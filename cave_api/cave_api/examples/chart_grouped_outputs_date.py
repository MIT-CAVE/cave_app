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
                    "pageLayout": ["chart", None, None, None],
                        "charts": {
                            "chart": {
                            "type": "groupedOutput",
                            "variant": "line",
                            "groupingId": ["date", "product"],
                            "groupingLevel": ["year_month_day", "product"],
                            "statAggregation": "sum",
                            "groupedOutputDataId": "salesData",
                            "statId": "sales",
                        }
                    },
                },
            },
        },
        "groupedOutputs": {
            "order": {
                "groupings": ["date", "product"],
            },
            "groupings": {
                "date": {
                    "order": {
                        "levels": ["year", "year_month", "year_month_day"],
                    },
                    "data": {
                        "id": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
                        "year": ["2024", "2024", "2024", "2024"],
                        "year_month": ["2024-01", "2024-01", "2024-01", "2024-01"],
                        "year_month_day": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
                    },
                    "name": "Dates",
                    "levels": {
                        "year": {
                            "name": "Years",
                            "ordering": ["2024"],
                        },
                        "year_month": {
                            "name": "Months",
                            "ordering": ["2024-01"],
                        },
                        "year_month_day": {
                            "name": "Days",
                            "ordering": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
                        },
                    },
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
                        "demand": [100, 108, 115, 110, 70, 78, 67, 89, 100, 100, 98],
                        "sales": [95, 100, 100, 98, 60, 65, 67, 75, 90, 99, 98],
                    },
                    "groupLists": {
                        "date": [
                            "2024-01-01",
                            "2024-01-02",
                            "2024-01-03",
                            "2024-01-04",
                            "2024-01-01",
                            "2024-01-02",
                            "2024-01-03",
                            "2024-01-04",
                            "2024-01-01",
                            "2024-01-03",
                            "2024-01-04",
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
                        ],
                    },
                },
            },
        },
    }
