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
                    "chartPage",
                ],
            },
            "data": {
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
                            "dataset": "salesData",
                            "chartType": "line",
                            "stats": [
                                {
                                    "statId": "sales",
                                    "aggregationType": "sum",
                                }
                            ],
                            "groupingId": ["date", "product"],
                            "groupingLevel": ["year_month_day", "product"],
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
                        "year_month_day": [
                            "2024-01-01",
                            "2024-01-02",
                            "2024-01-03",
                            "2024-01-04",
                        ],
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
                            "ordering": [
                                "2024-01-01",
                                "2024-01-02",
                                "2024-01-03",
                                "2024-01-04",
                            ],
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
                        ],
                    },
                    "stats": {
                        "demand": {
                            "name": "Demand",
                            "unit": "units",
                        },
                        "sales": {
                            "name": "Sales",
                            "unit": "units",
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
