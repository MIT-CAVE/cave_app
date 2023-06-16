from pamda import pamda
import math

cost_per_km = {"truck": 0.0012, "rail": 0.0007, "ocean": 0.0003, "air": 0.0048}

setup_cost = {"truck": 1, "rail": 1.5, "ocean": 0.1, "air": 2}


def haversine_distance(origin, destination):
    lat1 = origin['meta']["latitude"]
    lon1 = origin['meta']["longitude"]
    lat2 = destination['meta']["latitude"]
    lon2 = destination['meta']["longitude"]
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) * math.cos(
        math.radians(lat2)
    ) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d


def calc_cost(origin, destination, arc_type):
    distance = haversine_distance(origin, destination)
    cost = distance * cost_per_km[arc_type] + setup_cost[arc_type]
    return -round(cost, 2)


def get_arcs(origin_nodes, destination_nodes, arc_type, distance=None, match_country=False):
    arcs = []
    for origin in origin_nodes:
        for destination in destination_nodes:
            if match_country:
                if (
                    origin["name"].split("(")[-1].split(")")[0]
                    != destination["name"].split("(")[-1].split(")")[0]
                ):
                    continue
            if distance is not None:
                if haversine_distance(origin, destination) > distance:
                    continue
            arcs.append(
                {
                    "id": f'{origin["id"]}_{destination["id"]}',
                    "type": arc_type,
                    "origin": origin["id"],
                    "destination": destination["id"],
                    "processing_cashflow_per_unit": calc_cost(origin, destination, arc_type),
                    "processing_capacity": 999999999,
                }
            )
    return arcs


nodes = pamda.read_csv("nodes.csv", cast_items=True)

mfgs = [node for node in nodes if node["type"] == "mfg"]
foreign_ports = [node for node in nodes if node["type"] == "port" and "(US)" not in node["name"]]
foreign_airports = [
    node for node in nodes if node["type"] == "airport" and "(US)" not in node["name"]
]

domestic_ports = [node for node in nodes if node["type"] == "port" and "(US)" in node["name"]]
domestic_airports = [node for node in nodes if node["type"] == "airport" and "(US)" in node["name"]]

dcs = [node for node in nodes if node["type"] == "dc"]
dzs = [node for node in nodes if node["type"] == "dz"]


arcs = [
    *get_arcs(mfgs, foreign_ports, "truck", match_country=True, distance=500),
    *get_arcs(mfgs, foreign_airports, "truck", match_country=True, distance=500),
    *get_arcs(foreign_ports, domestic_ports, "ocean"),
    *get_arcs(foreign_airports, domestic_airports, "air"),
    *get_arcs(domestic_ports, dcs, "truck", distance=2000),
    *get_arcs(domestic_airports, dcs, "truck", distance=2000),
    *get_arcs(dcs, dzs, "truck", distance=1400),
]

pamda.write_csv("arcs.csv", arcs)
