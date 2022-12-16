from .serializer import (
    Serializer,
    currency_format,
    percent_format,
    product_format,
)

serializer = Serializer()

serialized_data = {
    "settings": {
        "allowModification": False,
        "sendToApi": False,
        "sendToClient": True,
        "data": {
            "syncToggles": {
                "Map Layers": {
                    "ml1": ["map", "data", "legendGroups"],
                    "ml2": ["nodes", "types"],
                    "ml3": ["arcs", "types"],
                    "ml4": ["geos", "types"],
                },
            },
            "defaultDesync": {
                "Map Layers": {
                    "ml1": ["map", "data", "legendGroups"],
                    "ml2": ["nodes", "types"],
                    "ml3": ["arcs", "types"],
                    "ml4": ["geos", "types"],
                },
                "App Bar": {
                    "ab1": ["appBar", "data", "dashboardId"],
                    "ab2": ["appBar", "paneState"],
                },
            },
            "iconUrl": "https://react-icons.mitcave.com/0.0.1",
            "numberFormat": {
                "precision": 2,
                "trailingZeros": False,
            },
            "debug": True,
        },
    },
    "categories": {
        "allowModification": False,
        "data": {
            "network_object": {
                "data": serializer.get_categories_item_data(
                    {**serializer.nodes, **serializer.arcs}, all="All"
                ),
                "name": "All Network Objects",
                "nestedStructure": {
                    "all": {"name": "All", "order": 0},
                    "continent": {
                        "name": "Continent",
                        "order": 2,
                    },
                    "type": {
                        "name": "Type",
                        "order": 1,
                    },
                    "item": {
                        "name": "Object",
                        "order": 3,
                    },
                },
                "layoutDirection": "vertical",
                "order": 1,
            },
            "warehouse": {
                "data": serializer.get_categories_item_data(serializer.warehouses),
                "name": "Warehouses",
                "nestedStructure": {
                    "continent": {
                        "name": "Continent",
                        "order": 1,
                    },
                    "item": {
                        "name": "Warehouse",
                        "order": 2,
                    },
                },
                "layoutDirection": "horizontal",
                "order": 3,
            },
            "factory": {
                "data": serializer.get_categories_item_data(serializer.factories),
                "name": "Factories",
                "nestedStructure": {
                    "continent": {
                        "name": "Continent",
                        "order": 1,
                    },
                    "item": {
                        "name": "Factory",
                        "order": 2,
                    },
                },
                "layoutDirection": "horizontal",
                "order": 3,
            },
            "demand": {
                "data": serializer.get_categories_item_data(serializer.demand_zones),
                "name": "Demand Zones",
                "nestedStructure": {
                    "continent": {
                        "name": "Continent",
                        "order": 1,
                    },
                    "item": {
                        "name": "Demand Zone",
                        "order": 2,
                    },
                },
                "layoutDirection": "horizontal",
                "order": 4,
            },
            "transportation": {
                "data": serializer.get_categories_item_data(serializer.arcs),
                "name": "Transportation",
                "nestedStructure": {
                    "continent": {
                        "name": "Continent",
                        "order": 2,
                    },
                    "type": {
                        "name": "Type",
                        "order": 1,
                    },
                    "item": {
                        "name": "Object",
                        "order": 3,
                    },
                },
                "layoutDirection": "vertical",
                "order": 6,
            },
            "location": {
                "data": serializer.get_categories_location_data(),
                "name": "Locations",
                "nestedStructure": {
                    "continent": {
                        "name": "Continents",
                        "order": 1,
                    },
                    "region": {
                        "name": "Regions",
                        "order": 2,
                    },
                },
                "layoutDirection": "horizontal",
                "order": 0,
            },
        },
    },
    "appBar": {
        "data": {
            "session": {
                "icon": "MdApi",
                "type": "pane",
                "variant": "session",
                "bar": "upper",
                "order": 0,
            },
            "appSettings": {
                "icon": "MdOutlineSettings",
                "type": "pane",
                "variant": "appSettings",
                "bar": "upper",
                "order": 0,
            },
            "solveButton": {
                "name": "Solve Button",
                "icon": "BsLightningFill",
                "apiCommand": "solve",
                "type": "button",
                "bar": "upper",
                "order": 1,
            },
            "map_1": {
                "type": "map",
                "icon": "FaMapMarkedAlt",
                "bar": "lower",
                "order": 0,
            },
            "dash_1": {
                "icon": "GoPackage",
                "name": "Dashboard 1",
                "type": "stats",
                "bar": "lower",
                "order": 1,
                "dashboardLayout": [
                    {
                        "chart": "Bar",
                        "grouping": "Sum",
                        "statistic": "pct_demand_met",
                        "category": "demand",
                        "level": "item",
                    },
                    {
                        "chart": "Bar",
                        "grouping": "Sum",
                        "statistic": "revenue",
                        "category": "demand",
                        "level": "item",
                    },
                    {
                        "chart": "Bar",
                        "grouping": "Sum",
                        "statistic": "fixed_cashflow",
                        "category": "network_object",
                        "level": "type",
                    },
                    {
                        "chart": "Bar",
                        "grouping": "Sum",
                        "statistic": "processing_cashflow",
                        "category": "network_object",
                        "level": "type",
                    },
                ],
                "lockedLayout": False,
            },
            "kpi_1": {
                "name": "KPI Dashboard",
                "type": "kpi",
                "bar": "lower",
                "icon": "MdSpeed",
                "order": 4,
            },
        }
    },
    "map": {
        "data": {
            "defaultViewport": {
                "longitude": 40,
                "latitude": 0,
                "zoom": 2,
                "pitch": 0,
                "bearing": 0,
                "maxZoom": 12,
                "minZoom": 2,
            },
            "optionalViewports": {
                "ov1": {
                    "name": "EMEA",
                    "icon": "FaGlobeEurope",
                    "order": 1,
                    "longitude": 14,
                    "latitude": 47,
                    "zoom": 4,
                    "minZoom": 2,
                    "maxZoom": 12,
                    "pitch": 0,
                    "bearing": 0,
                },
                "ov2": {
                    "name": "Americas",
                    "icon": "FaGlobeAmericas",
                    "order": 1,
                    "longitude": -94,
                    "latitude": 39,
                    "zoom": 4,
                    "minZoom": 2,
                    "maxZoom": 12,
                    "pitch": 0,
                    "bearing": 0,
                },
            },
            "legendGroups": {
                "Transportation": {
                    "name": "Transportation",
                    "arcs": {
                        "transport": {"value": True, "order": 1},
                        "last_mile": {"value": True, "order": 2},
                    },
                    "order": 1,
                },
                "Facilities": {
                    "name": "Facilities",
                    "nodes": {
                        "factory": {"value": True, "order": 1},
                        "warehouse": {"value": True, "order": 2}
                    },
                    "order": 2,
                },
                "Demand": {
                    "name": "Demand",
                    "nodes": {
                        "factory": {"value": True, "order": 1},
                        "warehouse": {"value": True, "order": 2}
                    },
                    "geos": {"demand": {"value": True}},
                    "order": 3,
                },
            },
        },
    },
    "arcs": {
        "types": {
            "last_mile": {
                "name": "Last Mile",
                "colorByOptions": serializer.get_dropdown_options(
                    serializer.arcs, include_categorical=True
                ),
                "colorBy": "processing_capacity",
                "lineBy": "solid",
                "sizeByOptions": serializer.get_dropdown_options(serializer.arcs),
                "sizeBy": "cashflow_per_unit",
                "startSize": "8px",
                "endSize": "15px",
                "order": 0,
                "props": serializer.get_general_prop_defaults(),
                "layout": serializer.get_general_prop_layout(),
            },
            "transport": {
                "name": "Transport",
                "colorByOptions": serializer.get_dropdown_options(
                    serializer.arcs, include_categorical=True
                ),
                "colorBy": "processing_capacity",
                "lineBy": "solid",
                "height": 0.3,
                "sizeByOptions": serializer.get_dropdown_options(serializer.arcs),
                "sizeBy": "processing_capacity",
                "startSize": "8px",
                "endSize": "15px",
                "order": 0,
                "props": serializer.get_general_prop_defaults(),
                "layout": serializer.get_general_prop_layout(),
            },
        },
        "data": serializer.get_serialized_item_data(serializer.arcs),
    },
    "nodes": {
        "types": {
            "factory": {
                "name": "Factories",
                "colorByOptions": serializer.get_dropdown_options(
                    serializer.factories, include_categorical=True
                ),
                "colorBy": "open",
                "sizeByOptions": serializer.get_dropdown_options(serializer.factories),
                "sizeBy": "processing_capacity",
                "startSize": "15px",
                "endSize": "30px",
                "icon": "GiFactory",
                "order": 1,
                "props": serializer.get_general_prop_defaults(),
                "layout": serializer.get_general_prop_layout(),
            },
            "warehouse": {
                "name": "Warehouses",
                "colorByOptions": serializer.get_dropdown_options(
                    serializer.warehouses, include_categorical=True
                ),
                "colorBy": "open",
                "sizeByOptions": serializer.get_dropdown_options(serializer.warehouses),
                "sizeBy": "processing_capacity",
                "startSize": "15px",
                "endSize": "30px",
                "icon": "FaWarehouse",
                "order": 1,
                "props": serializer.get_general_prop_defaults(),
                "layout": serializer.get_general_prop_layout(),
            },
        },
        "data": serializer.get_serialized_item_data(
            {**serializer.warehouses, **serializer.factories}
        ),
    },
    "geos": {
        "types": {
            "demand": {
                "name": "Regional Demand Zones",
                "colorByOptions": serializer.get_dropdown_options(
                    serializer.demand_zones, include_categorical=True
                ),
                "colorBy": "processing_capacity",
                "geoJson": {
                    "geoJsonLayer": "https://cave-geojsons.s3.amazonaws.com/custom/example_app_continent_region.json",
                    "geoJsonProp": "region_id",
                },
                "icon": "BsHexagon",
                "props": serializer.get_geo_prop_defaults(),
                "layout": serializer.get_geo_prop_layout(),
            },
        },
        "data": serializer.get_serialized_item_data(serializer.demand_zones),
    },
    "stats": {
        "types": serializer.get_stats_types(),
    },
    "kpis": {
        "data": {
            # Factories
            "factory_header": {
                "name": "Factory KPIs",
                "icon": "GiFactory",
                "type": "head",
            },
            "num_open_factories": {
                "name": "Open Factories",
                "value": 0,
                "numberFormat": {
                    "unit": "factories",
                },
                "icon": "AiOutlineNumber",
            },
            "factory_units_processed": {
                "name": "Factory Units Processed",
                "value": 0,
                "numberFormat": product_format,
                "icon": "FaBox",
            },
            "factory_processing_costs": {
                "name": "Factory Processing Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
            },
            "factory_fixed_costs": {
                "name": "Factory Fixed Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
            },
            "factory_processing_utilization": {
                "name": "Factory Processing Utilization",
                "value": 0,
                "percentage": True,
                "numberFormat": {
                    "unit": f"%",
                    "unitSpace": False,
                },
                "icon": "MdDataUsage",
            },
            # Warehouses
            "warehouse_header": {
                "name": "Warehouse KPIs",
                "icon": "FaWarehouse",
                "type": "head",
            },
            "num_open_warehouses": {
                "name": "Open Warehouses",
                "value": 0,
                "numberFormat": {
                    "unit": "warehouses",
                },
                "icon": "AiOutlineNumber",
            },
            "warehouse_units_processed": {
                "name": "Warehouse Units Processed",
                "value": 0,
                "numberFormat": product_format,
                "icon": "FaBox",
            },
            "warehouse_processing_costs": {
                "name": "Warehouse Processing Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
            },
            "warehouse_fixed_costs": {
                "name": "Warehouse Fixed Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
            },
            "warehouse_processing_utilization": {
                "name": "Warehouse Processing Utilization",
                "value": 0,
                "percentage": True,
                "numberFormat": percent_format,
                "icon": "MdDataUsage",
            },
            # Demand Zones
            "demand_header": {
                "name": "Demand Zone KPIs",
                "icon": "FaBoxOpen",
                "type": "head",
            },
            "total_demand": {
                "name": "Total Units Demanded",
                "value": 0,
                "numberFormat": product_format,
                "icon": "FaBox",
            },
            "total_demand_met": {
                "name": "Total Demand Met",
                "value": 0,
                "numberFormat": product_format,
                "icon": "FaBoxOpen",
            },
            "pct_total_demand_met": {
                "name": "Percent Demand Met",
                "value": 0,
                "percentage": True,
                "numberFormat": percent_format,
                "icon": "FaPercent",
            },
            "revenue": {
                "name": "Revenue",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaRegMoneyBillAlt",
            },
            # Totals
            "total_costs_header": {
                "name": "Total Costs",
                "icon": "FaMoneyBill",
                "type": "head",
            },
            "total_transportation_costs": {
                "name": "Transportation Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
            },
            "total_processing_costs": {
                "name": "Processing Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
            },
            "total_fixed_costs": {
                "name": "Fixed Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
            },
            "total_profit_header": {
                "name": "Total Profits",
                "icon": "FaRegMoneyBillAlt",
                "type": "head",
            },
            "total_costs": {
                "name": "Total Costs",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBill",
                "mapKpi": True,
            },
            "total_revenue": {
                "name": "Total Revenue",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaRegMoneyBillAlt",
                "mapKpi": True,
            },
            "total_profit": {
                "name": "Total Profit",
                "value": 0,
                "numberFormat": currency_format,
                "icon": "FaMoneyBillWave",
                "mapKpi": True,
            },
        },
        "layout": {
            "type": "grid",
            "numColumns": "4",
            "numRows": "auto",
            "data": {
                "col1_row1": {
                    "type": "item",
                    "itemId": "factory_header",
                    "column": 1,
                    "row": 1,
                },
                "col1_row2": {
                    "type": "item",
                    "itemId": "num_open_factories",
                    "column": 1,
                    "row": 2,
                },
                "col1_row3": {
                    "type": "item",
                    "itemId": "factory_units_processed",
                    "column": 1,
                    "row": 3,
                },
                "col1_row4": {
                    "type": "item",
                    "itemId": "factory_processing_costs",
                    "column": 1,
                    "row": 4,
                },
                "col1_row5": {
                    "type": "item",
                    "itemId": "factory_processing_utilization",
                    "column": 1,
                    "row": 5,
                },
                "col2_row1": {
                    "type": "item",
                    "itemId": "warehouse_header",
                    "column": 2,
                    "row": 1,
                },
                "col2_row2": {
                    "type": "item",
                    "itemId": "num_open_warehouses",
                    "column": 2,
                    "row": 2,
                },
                "col2_row3": {
                    "type": "item",
                    "itemId": "warehouse_units_processed",
                    "column": 2,
                    "row": 3,
                },
                "col2_row4": {
                    "type": "item",
                    "itemId": "warehouse_processing_costs",
                    "column": 2,
                    "row": 4,
                },
                "col2_row5": {
                    "type": "item",
                    "itemId": "warehouse_fixed_costs",
                    "column": 2,
                    "row": 5,
                },
                "col2_row6": {
                    "type": "item",
                    "itemId": "warehouse_processing_utilization",
                    "column": 2,
                    "row": 6,
                },
                "col3_row1": {
                    "type": "item",
                    "itemId": "demand_header",
                    "column": 3,
                    "row": 1,
                },
                "col3_row2": {
                    "type": "item",
                    "itemId": "total_demand",
                    "column": 3,
                    "row": 2,
                },
                "col3_row3": {
                    "type": "item",
                    "itemId": "total_demand_met",
                    "column": 3,
                    "row": 3,
                },
                "col3_row4": {
                    "type": "item",
                    "itemId": "pct_total_demand_met",
                    "column": 3,
                    "row": 4,
                },
                "col3_row5": {
                    "type": "item",
                    "itemId": "revenue",
                    "column": 3,
                    "row": 5,
                },
                "col4_row1": {
                    "type": "item",
                    "itemId": "total_costs_header",
                    "column": 4,
                    "row": 1,
                },
                "col4_row2": {
                    "type": "item",
                    "itemId": "total_transportation_costs",
                    "column": 4,
                    "row": 2,
                },
                "col4_row3": {
                    "type": "item",
                    "itemId": "total_processing_costs",
                    "column": 4,
                    "row": 3,
                },
                "col4_row4": {
                    "type": "item",
                    "itemId": "total_fixed_costs",
                    "column": 4,
                    "row": 4,
                },
                "col4_row5": {
                    "type": "item",
                    "itemId": "total_costs",
                    "column": 4,
                    "row": 5,
                },
                "col5_row1": {
                    "type": "item",
                    "itemId": "total_profit_header",
                    "column": 5,
                    "row": 1,
                },
                "col5_row2": {
                    "type": "item",
                    "itemId": "total_revenue",
                    "column": 5,
                    "row": 2,
                },
                "col5_row3": {
                    "type": "item",
                    "itemId": "total_costs",
                    "column": 5,
                    "row": 3,
                },
                "col5_row4": {
                    "type": "item",
                    "itemId": "total_profit",
                    "column": 5,
                    "row": 4,
                },
            },
        },
    },
}
