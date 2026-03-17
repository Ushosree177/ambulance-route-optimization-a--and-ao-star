
# 1. Import Libraries

import osmnx as ox
import networkx as nx
import folium
import random

# 2. AO* Decision Graph (Costs Explained)

graph_decision = {
    "Patient": {"OR": ["AMRI", "Apollo"]},

    "AMRI": {"AND": ["Ambulance_AMRI", "Route_AMRI"]},
    "Apollo": {"AND": ["Ambulance_Apollo", "Route_Apollo"]},

    # Simulated costs (you can tune these)
    "Ambulance_AMRI": 6,
    "Route_AMRI": 8,

    "Ambulance_Apollo": 4,
    "Route_Apollo": 12
}

def ao_star(node):
    value = graph_decision[node]

    # Leaf cost
    if isinstance(value, int):
        return value

    # OR node
    if "OR" in value:
        options = []
        for child in value["OR"]:
            options.append((child, ao_star(child)))
        best = min(options, key=lambda x: x[1])
        return best

    # AND node
    if "AND" in value:
        total_cost = 0
        for child in value["AND"]:
            total_cost += ao_star(child)
        return total_cost

decision = ao_star("Patient")
print("AO* decision (hospital, cost):", decision)

# Show detailed costs
amri_cost = graph_decision["Ambulance_AMRI"] + graph_decision["Route_AMRI"]
apollo_cost = graph_decision["Ambulance_Apollo"] + graph_decision["Route_Apollo"]

print("AMRI total cost:", amri_cost)
print("Apollo total cost:", apollo_cost)

# 3. Hospital Names

amri_name = "AMRI Hospital, Kolkata"
apollo_name = "Apollo Hospital, Kolkata"

best_hospital = amri_name if decision[0] == "AMRI" else apollo_name
print("AO* selected hospital:", best_hospital)


# 4. Load Kolkata Road Network

place = "Kolkata, West Bengal, India"
graph = ox.graph_from_place(place, network_type="drive")
print("Road network loaded")

# 5. Geocode Start + Hospitals

start_location = ox.geocode("Park Street, Kolkata")
amri_location = ox.geocode(amri_name)
apollo_location = ox.geocode(apollo_name)

print("Start:", start_location)
print("AMRI:", amri_location)
print("Apollo:", apollo_location)

# 6. Convert to Graph Nodes

orig_node = ox.distance.nearest_nodes(graph, start_location[1], start_location[0])

amri_node = ox.distance.nearest_nodes(graph, amri_location[1], amri_location[0])
apollo_node = ox.distance.nearest_nodes(graph, apollo_location[1], apollo_location[0])


# 7. Add Traffic Weights

for u, v, key, data in graph.edges(keys=True, data=True):
    road_length = data["length"]
    traffic_factor = random.uniform(1.0, 2.0)  # simulate traffic
    data["traffic_weight"] = road_length * traffic_factor


# 8. Run A* Routes to BOTH Hospitals

route_amri = nx.astar_path(graph, orig_node, amri_node, weight="traffic_weight")
route_apollo = nx.astar_path(graph, orig_node, apollo_node, weight="traffic_weight")

print("Routes calculated")

# 9. Calculate Distances

dist_amri = nx.path_weight(graph, route_amri, weight="length")
dist_apollo = nx.path_weight(graph, route_apollo, weight="length")

dist_amri_km = round(dist_amri / 1000, 2)
dist_apollo_km = round(dist_apollo / 1000, 2)

print("Distance to AMRI (km):", dist_amri_km)
print("Distance to Apollo (km):", dist_apollo_km)

# 10. Create Interactive Map
route_coords_amri = [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in route_amri]
route_coords_apollo = [(graph.nodes[n]['y'], graph.nodes[n]['x']) for n in route_apollo]

m = folium.Map(location=route_coords_amri[0], zoom_start=13)

# AMRI route (red)
folium.PolyLine(route_coords_amri, color="red", weight=5, opacity=0.8).add_to(m)

# Apollo route (blue)
folium.PolyLine(route_coords_apollo, color="blue", weight=5, opacity=0.8).add_to(m)

# Start marker
folium.Marker(
    route_coords_amri[0],
    popup="Ambulance Start",
    icon=folium.Icon(color="green")
).add_to(m)

# AMRI marker with distance + AO* cost
folium.Marker(
    route_coords_amri[-1],
    popup=f"AMRI Hospital\nDistance: {dist_amri_km} km\nAO* Cost: {amri_cost}",
    icon=folium.Icon(color="red")
).add_to(m)

# Apollo marker with distance + AO* cost
folium.Marker(
    route_coords_apollo[-1],
    popup=f"Apollo Hospital\nDistance: {dist_apollo_km} km\nAO* Cost: {apollo_cost}",
    icon=folium.Icon(color="blue")
).add_to(m)

# Highlight AO* selected hospital
best_coords = route_coords_amri[-1] if best_hospital == amri_name else route_coords_apollo[-1]
folium.Marker(
    best_coords,
    popup=f"⭐ Selected by AO*: {best_hospital}",
    icon=folium.Icon(color="purple")
).add_to(m)

# 11. Save Map

m.save("kolkata_ambulance_comparison.html")
print("Map saved as kolkata_ambulance_comparison.html")