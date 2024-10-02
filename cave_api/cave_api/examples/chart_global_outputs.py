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
            "order": {"data": ["refreshButton", "session", "chartPage"]},
            "data": {
                # Add a simple button to the app bar to trigger the `init` command
                # This is useful for resetting the app to its initial state
                "refreshButton": {
                    "icon": "md/MdRefresh",
                    "apiCommand": "init",
                    "type": "button",
                    "bar": "upperLeft",
                },
                # Add an appBar button to launch the sessions pane
                "session": {
                    "icon": "md/MdApi",
                    "type": "session",
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
                        "chart1": {
                            "type": "globalOutput",
                            "variant": "overview",
                        }
                    },
                    "pageLayout": ["chart1", None, None, None],
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
