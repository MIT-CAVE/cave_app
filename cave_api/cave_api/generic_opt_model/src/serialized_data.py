from .serializer import Serializer

from .config import (
    node_types,
    arc_types,
    geo_types,
)


def get_node_arc_geo_categories(serializer):
    out = {}
    object_data = [serializer.node_data, serializer.arc_data, serializer.geo_data]
    object_types = [node_types, arc_types, geo_types]
    for i in range(3):
        obj_data = object_data[i]
        obj_type = object_types[i]
        for obj_key, obj_value in obj_type.items():
            out[obj_key] = {
                "data": serializer.get_categories_item_data(
                    items_dict=obj_data.get(obj_key),
                    additional_key_fn_dict={
                            "all": lambda x: "All",
                        },
                ),
                "name": obj_value["name"],
                "nestedStructure": {
                    'all': {'name': 'All', 'order': 0},
                    "item": {
                        "name": obj_value["name"],
                        "order": 1,
                    },
                },
                "order": 1,
            }
    return out


def get_serialized_data():
    serializer = Serializer()
    return {
        "settings": {
            "allowModification": False,
            "sendToApi": False,
            "sendToClient": True,
            "data": {
                "sync": {
                    "appBar": {
                        "name": "App Bar",
                        "showToggle": True,
                        "value": False,
                        "data": {
                            "ab1": ["appBar", "data", "dashboardId"],
                            "ab2": ["appBar", "paneState"],
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
                        items_dict={**serializer.nodes, **serializer.arcs, **serializer.geos},
                        additional_key_fn_dict={
                            "type": lambda x: x.get_pretty_type(),
                            "continent": lambda x: x.location.continent,
                            "all": lambda x: "All",
                        },
                    ),
                    "name": "All Network Objects",
                    "nestedStructure": {
                        "all": {"name": "All", "order": 0},
                        "type": {
                            "name": "Type",
                            "order": 1,
                        },
                        "continent": {
                            "name": "Continent",
                            "order": 2,
                        },
                        "item": {
                            "name": "Object",
                            "order": 3,
                        },
                    },
                    "layoutDirection": "vertical",
                    "order": 1,
                },
                **get_node_arc_geo_categories(serializer),
                "location": {
                    "data": serializer.get_categories_location_data(),
                    "name": "Locations",
                    "nestedStructure": {
                        "continent": {
                            "name": "Continents",
                            "order": 1,
                        },
                        "country": {
                            "name": "Countries",
                            "order": 2,
                        },
                        "region": {
                            "name": "Regions",
                            "order": 3,
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
                    "bar": "upper",
                    "order": 0,
                },
                "appSettings": {
                    "icon": "MdOutlineSettings",
                    "type": "pane",
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
                "resetButton": {
                    "icon": "MdSync",
                    "apiCommand": "reset",
                    "type": "button",
                    "bar": "upper",
                    "order": 2,
                },
                "map1": {
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
        "panes": {
            "data": {
                "session": {
                    "variant": "session",
                },
                "appSettings": {
                    "variant": "appSettings",
                },
            }
        },
        "dashboards": {
            "data": {
                "dash_1": {
                    "dashboardLayout": [
                        {
                            "chart": "Bar",
                            "grouping": "Sum",
                            "statistic": "processing_capacity",
                            "category": "network_object",
                            "level": "type",
                        },
                        {
                            "chart": "Bar",
                            "grouping": "Sum",
                            "statistic": "processing_capacity_utilization",
                            "category": "network_object",
                            "level": "type",
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
            },
        },
        "maps": {
            "data": {
                "map1": {
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
                            "name": "Asia",
                            "icon": "FaGlobeAsia",
                            "order": 1,
                            "longitude": 109,
                            "latitude": 27,
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
                        "network_objects": {
                            "name": "Network Objects",
                            "nodes": {
                                key: {
                                    "sizeBy": "output_total_units",
                                    "colorBy": "output_processing_capacity_utilization",
                                    "value": False,
                                    "order": 1,
                                }
                                for key in node_types.keys()
                            },
                            "geos": {
                                key: {
                                    "colorBy": "output_processing_capacity_utilization",
                                    "value": False,
                                    "order": 1,
                                }
                                for key in geo_types.keys()
                            },
                            "arcs": {
                                key: {
                                    "sizeBy": "output_total_units",
                                    "colorBy": "output_processing_capacity_utilization",
                                    "value": False,
                                    "order": 1,
                                }
                                for key in arc_types.keys()
                            },
                            "order": 2,
                        },
                    },
                },
            },
        },
        "arcs": {
            "types": {
                arc_key: {
                    "name": arc_value["name"],
                    "colorByOptions": serializer.get_dropdown_options(
                        serializer.arc_data[arc_key], include_categorical=True
                    ),
                    "lineBy": arc_value.get("lineBy", "Solid"),
                    "sizeByOptions": serializer.get_dropdown_options(serializer.arc_data[arc_key]),
                    "startSize": "8px",
                    "endSize": "15px",
                    "props": serializer.get_general_prop_defaults(),
                    "layout": serializer.get_general_prop_layout(),
                }
                for arc_key, arc_value in arc_types.items()
            },
            "data": serializer.get_serialized_item_data(serializer.arcs),
        },
        "nodes": {
            "types": {
                node_key: {
                    "name": node_value["name"],
                    "colorByOptions": serializer.get_dropdown_options(
                        serializer.node_data[node_key], include_categorical=True
                    ),
                    "sizeByOptions": serializer.get_dropdown_options(
                        serializer.node_data[node_key]
                    ),
                    "startSize": "40px",
                    "endSize": "60px",
                    "icon": node_value["icon"],
                    "props": serializer.get_general_prop_defaults(),
                    "layout": serializer.get_general_prop_layout(),
                }
                for node_key, node_value in node_types.items()
            },
            "data": serializer.get_serialized_item_data(serializer.nodes),
        },
        "geos": {
            "types": {
                geo_key: {
                    "name": geo_value["name"],
                    "colorByOptions": serializer.get_dropdown_options(
                        serializer.geo_data[geo_key], include_categorical=True
                    ),
                    "geoJson": {
                        "geoJsonLayer": geo_value["geoJsonLayer"],
                        "geoJsonProp": geo_value["geoJsonProp"],
                    },
                    "icon": geo_value["icon"],
                    "props": serializer.get_general_prop_defaults(),
                    "layout": serializer.get_general_prop_layout(),
                }
                for geo_key, geo_value in geo_types.items()
            },
            "data": serializer.get_serialized_item_data(serializer.geos),
        },
        "stats": {
            "types": serializer.get_stats_types(),
        },
        "kpis": {
            "data": serializer.get_kpi_data_template(),
            "layout": serializer.get_kpi_layout_template(),
        },
        "kwargs": {
            "wipe_existing": True,
        },
    }
