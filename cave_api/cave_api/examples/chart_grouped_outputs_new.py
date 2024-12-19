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
                    "charts": {
                        # cumulative line chart
                        "chart1": {
                            "type": "groupedOutput",
                            "dataset": "salesData",  # changed groupedOutputDataId -> dataset
                            "chartType": "cumulative_line",  # changed variant -> chartType
                            "groupingId": ["product"],
                            "groupingLevel": ["color"],
                            # single-stat chart -> len(stats) == 1
                            "stats": [
                                {
                                    "statId": "sales",
                                    "aggregationType": "mean",
                                    "aggregationGroupingId": "product",
                                    "aggregationGroupingLevel": "color"
                                },
                            ],
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
                                    "aggregationType": "sum",
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
                            },
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
                                    "aggregationType": "divisor",
                                    "statIdDivisor": "sales",
                                },
                                {
                                    "statId": "sales",
                                    "aggregationType": "sum",
                                },
                            ],
                        },
                    },
                    "pageLayout": ["chart1", "chart2", "chart3", None],
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
                        "demand": [
                            100,
                            108,
                            115,
                            110,
                            70,
                            78,
                            67,
                            89,
                            95,
                            100,
                            100,
                            98,
                        ],
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
        "globalOutputs": {
            "props": {
                "loadingHead": {
                    "type": "head",
                    "name": "24H Loading Dock KPIs",
                    "icon": "fa/FaTruckLoading",
                    "variant": "icon",
                },
                "manufacturingHead": {
                    "type": "head",
                    "name": "24H Manufacturing KPIs",
                    "icon": "md/MdPrecisionManufacturing",
                    "variant": "icon",
                },
                "loadingPallets": {
                    "name": "Pallets Received",
                    "icon": "fa/FaPallet",
                    "precision": 0,
                    "unit": "pallets",
                    "type": "num",
                    "variant": "icon",
                },
                "loadingPalletDwellTime": {
                    "name": "Avg Pallet Dwell Time",
                    "icon": "md/MdTimer",
                    "precision": 1,
                    "unit": "minutes",
                    "type": "num",
                    "variant": "icon",
                },
                "manufacturingUnitsPerHour": {
                    "name": "Unit Rate",
                    "icon": "md/MdSpeed",
                    "precision": 2,
                    "notation": "scientific",
                    "notationDisplay": "E+",
                    "trailingZeros": True,
                    "unit": "units/hour",
                    "type": "num",
                    "variant": "icon",
                },
                "manufacturingUnits": {
                    "name": "Units Produced",
                    "icon": "bs/BsBoxes",
                    "notation": "engineering",
                    "notationDisplay": "x10^",
                    "precision": 0,
                    "unit": "units",
                    "type": "num",
                    "variant": "icon",
                },
            },
            "values": {
                "loadingPallets": 60,
                "loadingPalletDwellTime": 49.2,
                "manufacturingUnitsPerHour": 4987.347,
                "manufacturingUnits": round(4987.347 * 24),
            },
            "layout": {
                "type": "grid",
                "numColumns": "auto",
                "numRows": "auto",
                "data": {
                    "col1Row1": {
                        "type": "item",
                        "itemId": "loadingHead",
                        "column": 1,
                        "row": 1,
                    },
                    "col1Row2": {
                        "type": "item",
                        "itemId": "loadingPallets",
                        "column": 1,
                        "row": 2,
                    },
                    "col1Row3": {
                        "type": "item",
                        "itemId": "loadingPalletDwellTime",
                        "column": 1,
                        "row": 3,
                    },
                    "col2Row1": {
                        "type": "item",
                        "itemId": "manufacturingHead",
                        "column": 2,
                        "row": 1,
                    },
                    "col2Row2": {
                        "type": "item",
                        "itemId": "manufacturingUnitsPerHour",
                        "column": 2,
                        "row": 2,
                    },
                    "col2Row3": {
                        "type": "item",
                        "itemId": "manufacturingUnits",
                        "column": 2,
                        "row": 3,
                    },
                },
            },
        },
    }
