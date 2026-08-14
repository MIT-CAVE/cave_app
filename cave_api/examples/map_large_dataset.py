import math
import random


def execute_command(session_data, socket, command="init", **kwargs):
    # Set random seed to keep generation deterministic
    random.seed(42)

    # Grid parameters
    rows = 45
    cols = 45
    lat_start = 38.0
    lon_start = -78.0
    lat_step = 0.1
    lon_step = 0.14

    # Generate node coordinates in a triangular lattice
    nodes_coords = []
    for r in range(rows):
        for c in range(cols):
            # Offset odd rows to create a triangular honeycomb structure
            lon_offset = 0.5 * lon_step if r % 2 == 1 else 0.0
            lat = lat_start + r * lat_step
            lon = lon_start + c * lon_step + lon_offset
            nodes_coords.append((lon, lat))

    N_nodes = len(nodes_coords)

    # Pick 25 hubs evenly spaced in the grid (using a 5x5 subgrid of block centers)
    hubs_indices = set()
    for hr in range(5):
        for hc in range(5):
            r = hr * 9 + 4
            c = hc * 9 + 4
            hubs_indices.add(r * cols + c)

    hubs_coords = {idx: nodes_coords[idx] for idx in hubs_indices}

    # Generate arcs: connect each spoke node to its closest hub with a curved path
    arcs_paths = []
    for idx, coord in enumerate(nodes_coords):
        if idx in hubs_indices:
            continue
        # Find closest hub
        nearest_hub_idx = None
        min_dist = float("inf")
        lon, lat = coord
        for h_idx, h_coord in hubs_coords.items():
            h_lon, h_lat = h_coord
            dist = (lon - h_lon) ** 2 + (lat - h_lat) ** 2
            if dist < min_dist:
                min_dist = dist
                nearest_hub_idx = h_idx

        # Calculate a curved path between spoke and hub
        h_coord = hubs_coords[nearest_hub_idx]
        p1 = coord
        p2 = h_coord
        lon1, lat1 = p1
        lon2, lat2 = p2
        mid_lon = (lon1 + lon2) / 2
        mid_lat = (lat1 + lat2) / 2

        d_lon = lon2 - lon1
        d_lat = lat2 - lat1

        # Use math.sin of index to vary the bend direction and magnitude slightly
        bend = 0.08 + 0.06 * math.sin(idx * 0.1)

        # Perpendicular offset
        offset_lon = -d_lat * bend
        offset_lat = d_lon * bend

        path = [
            [lon1, lat1],
            [mid_lon + offset_lon, mid_lat + offset_lat],
            [lon2, lat2],
        ]
        arcs_paths.append(path)

    # Helper function to generate closed hexagons around each center coordinate
    def get_hexagon_path(center_lon, center_lat, radius=0.045):
        points = []
        for i in range(6):
            angle = i * (math.pi / 3)
            # Adjust for longitude stretching at latitude 40 degrees
            lon = center_lon + radius * math.cos(angle) / 0.766
            lat = center_lat + radius * math.sin(angle)
            points.append([lon, lat])
        points.append(points[0])  # Close the loop
        return points

    # Return the app state containing settings, appBar, maps, mapFeatures, and pages
    return {
        "settings": {
            "iconUrl": "https://react-icons.mitcave.com/5.4.0",
        },
        "appBar": {
            "order": {
                "data": [
                    "mapPage",
                ],
            },
            "data": {
                "mapPage": {
                    "icon": "md/MdMap",
                    "type": "page",
                    "bar": "upperLeft",
                },
            },
        },
        "maps": {
            "data": {
                "exampleMap": {
                    "name": "Large Dataset Map",
                    "currentProjection": "globe",
                    "defaultViewport": {
                        "longitude": -74.92,
                        "latitude": 40.2,
                        "zoom": 6.5,
                        "pitch": 20,
                        "bearing": 0,
                        "maxZoom": 12,
                        "minZoom": 2,
                    },
                    "legendGroups": {
                        "networkNodes": {
                            "name": "Grid Nodes (Thousands)",
                            "data": {
                                "gridNode": {
                                    "value": True,
                                    "colorBy": "status",
                                    "colorByOptions": ["status", "metric", "demand", "reliability"],
                                    "sizeBy": "metric",
                                    "sizeByOptions": ["metric", "demand", "reliability"],
                                    "icon": "fa6/FaCircleDot",
                                },
                            },
                        },
                        "networkArcs": {
                            "name": "Flow Arcs (Thousands)",
                            "data": {
                                "flowArc": {
                                    "value": True,
                                    "colorBy": "flowRate",
                                    "colorByOptions": ["flowRate", "distance", "congested"],
                                    "sizeBy": "flowRate",
                                    "sizeByOptions": ["flowRate", "distance"],
                                },
                            },
                        },
                        "networkGeos": {
                            "name": "Coverage Zones (Thousands)",
                            "data": {
                                "zoneGeo": {
                                    "value": True,
                                    "colorBy": "zoneValue",
                                    "colorByOptions": ["zoneValue", "population", "environmentAlert"],
                                },
                            },
                        },
                    },
                },
            },
        },
        "mapFeatures": {
            "data": {
                "gridNode": {
                    "type": "node",
                    "name": "Grid Node",
                    "props": {
                        "status": {
                            "name": "Status",
                            "type": "toggle",
                            "help": "Operational status of the node",
                            "options": {
                                "false": {"color": "rgb(231, 76, 60)"},  # Red for inactive
                                "true": {"color": "rgb(46, 204, 113)"},  # Green for active
                            },
                        },
                        "metric": {
                            "name": "Latency",
                            "type": "num",
                            "unit": "ms",
                            "help": "Response latency of the node",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "size": "10px", "color": "rgb(52, 152, 219)"},  # Blue
                                    {"value": "max", "size": "24px", "color": "rgb(155, 89, 182)"},  # Purple
                                ],
                            },
                        },
                        "demand": {
                            "name": "Demand",
                            "type": "num",
                            "unit": "units",
                            "help": "Customer demand at this node location",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "size": "8px", "color": "rgb(255, 235, 204)"},  # Light orange
                                    {"value": "max", "size": "30px", "color": "rgb(230, 126, 34)"},  # Dark orange
                                ],
                            },
                        },
                        "reliability": {
                            "name": "Reliability Index",
                            "type": "num",
                            "unit": "%",
                            "help": "Reliability metric of the node",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "size": "10px", "color": "rgb(192, 57, 43)"},  # Dark Red
                                    {"value": "max", "size": "24px", "color": "rgb(39, 174, 96)"},  # Emerald Green
                                ],
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "latitude": [[lat] for lon, lat in nodes_coords],
                            "longitude": [[lon] for lon, lat in nodes_coords],
                        },
                        "valueLists": {
                            "status": [bool(i % 7 != 0) for i in range(N_nodes)],
                            "metric": [
                                20.0 + 80.0 * abs(math.sin(lat * 1.5) * math.cos(lon * 1.5))
                                for lon, lat in nodes_coords
                            ],
                            "demand": [
                                100.0 + 900.0 * abs(math.cos(lat * 3.0) * math.sin(lon * 3.0))
                                for lon, lat in nodes_coords
                            ],
                            "reliability": [
                                50.0 + 50.0 * abs(math.sin(idx * 0.01))
                                for idx in range(N_nodes)
                            ],
                        },
                    },
                },
                "flowArc": {
                    "type": "arc",
                    "name": "Flow Arc",
                    "props": {
                        "flowRate": {
                            "name": "Flow Rate",
                            "type": "num",
                            "unit": "Gbps",
                            "help": "Data flow rate through the arc",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "size": "1px", "color": "rgb(241, 196, 15)"},  # Yellow
                                    {"value": "max", "size": "5px", "color": "rgb(211, 84, 0)"},  # Orange
                                ],
                            },
                        },
                        "distance": {
                            "name": "Distance",
                            "type": "num",
                            "unit": "km",
                            "help": "Physical length of the connection",
                            "gradient": {
                                "notation": "precision",
                                "precision": 1,
                                "data": [
                                    {"value": "min", "size": "1px", "color": "rgb(189, 195, 199)"},  # Silver
                                    {"value": "max", "size": "6px", "color": "rgb(44, 62, 80)"},  # Midnight Blue
                                ],
                            },
                        },
                        "congested": {
                            "name": "Is Congested",
                            "type": "toggle",
                            "help": "Whether the connection is congested",
                            "options": {
                                "false": {"color": "rgb(46, 204, 113)"}, # Green for clear
                                "true": {"color": "rgb(231, 76, 60)"},  # Red for congested
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "path": arcs_paths,
                        },
                        "valueLists": {
                            "flowRate": [
                                10.0 + 90.0 * abs(math.sin(i * 0.05))
                                for i in range(len(arcs_paths))
                            ],
                            "distance": [
                                float(math.sqrt((path[0][0] - path[-1][0])**2 + (path[0][1] - path[-1][1])**2) * 111.0)
                                for path in arcs_paths
                            ],
                            "congested": [
                                bool(abs(math.sin(i * 0.2)) > 0.75)
                                for i in range(len(arcs_paths))
                            ],
                        },
                    },
                },
                "zoneGeo": {
                    "type": "geo",
                    "name": "Zone Geo",
                    "props": {
                        "zoneValue": {
                            "name": "Coverage Strength",
                            "type": "num",
                            "unit": "%",
                            "help": "Coverage strength percentage in the zone",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "color": "rgba(46, 204, 113, 0.05)"},  # Almost transparent green
                                    {"value": "max", "color": "rgba(46, 204, 113, 0.6)"},   # Vibrant semi-transparent green
                                ],
                            },
                        },
                        "population": {
                            "name": "Population Density",
                            "type": "num",
                            "unit": "/km²",
                            "help": "Estimated population density in this zone",
                            "gradient": {
                                "notation": "precision",
                                "precision": 0,
                                "data": [
                                    {"value": "min", "color": "rgba(52, 152, 219, 0.05)"},  # Light blue
                                    {"value": "max", "color": "rgba(52, 152, 219, 0.7)"},   # Strong blue
                                ],
                            },
                        },
                        "environmentAlert": {
                            "name": "Environmental Alert",
                            "type": "toggle",
                            "help": "Environmental alert status in this coverage zone",
                            "options": {
                                "false": {"color": "rgba(189, 195, 199, 0.2)"}, # Clear/grey
                                "true": {"color": "rgba(230, 126, 34, 0.7)"},  # Warning orange
                            },
                        },
                    },
                    "data": {
                        "location": {
                            "path": [get_hexagon_path(lon, lat, 0.045) for lon, lat in nodes_coords],
                        },
                        "valueLists": {
                            "zoneValue": [
                                30.0 + 70.0 * abs(math.sin(lat * 2.0) * math.cos(lon * 2.0))
                                for lon, lat in nodes_coords
                            ],
                            "population": [
                                1000.0 + 9000.0 * abs(math.cos(lat * 1.0) * math.sin(lon * 1.0))
                                for lon, lat in nodes_coords
                            ],
                            "environmentAlert": [
                                bool(abs(math.sin(idx * 0.03)) > 0.8)
                                for idx in range(N_nodes)
                            ],
                        },
                    },
                },
            },
        },
        "pages": {
            "currentPage": "mapPage",
            "data": {
                "mapPage": {
                    "charts": {
                        "map": {
                            "type": "map",
                            "mapId": "exampleMap",
                            "maximized": True,
                        },
                    },
                    "pageLayout": ["map", None, None, None],
                },
            },
        },
    }
