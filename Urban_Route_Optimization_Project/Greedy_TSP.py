#result is saved in Greedy_TSP_Demo.html

import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance
from itertools import cycle
import folium
import time
PLACE_NAME = "Vancouver, Canada"
# START_LOCATION must be one of the keys in the LOCATIONS dictionary
START_LOCATION = 'Lotus Land Tours'
# LOCATIONS is a dictionary of location names and their coordinates
# LOCATIONS must contain at least two locations
# LOCATIONS must be in the same city as PLACE_NAME
LOCATIONS = {
    'Lotus Land Tours': (49.27306, -123.1252),
    'Harbour Cruises': (49.29351, -123.1339),
    'Playland Amusement Park': (49.28278, -123.0373),
    'VanDusen Botanical Garden': (49.23903, -123.1346),
    'Vancouver Maritime Museum': (49.27752, -123.1474),
    'Granville Island': (49.27211, -123.1358),
    'PNE - Pacific National Exhibition': (49.28066, -123.0413),
    'Bloedel Conservatory': (49.24337, -123.1173),
    'Arts Club Theatre Company': (49.26134, -123.1385),
    'CHI, the Spa at Shangri-la': (49.28587, -123.124),
    'Douglas Reynolds Gallery': (49.26485, -123.1387),
    'The Comedy Department': (49.28695, -123.1407)
}
COLORS = ['red', 'blue', 'green', 'brown', 'orange','yellow','pink']




 

def get_graph(place_name):
    graph = ox.graph_from_place(place_name, network_type='drive')
    return graph

def get_nearest_node(graph, point):
    return ox.distance.nearest_nodes(graph, point[1], point[0])

def navigate(graph, start_point, end_point):
    start_node = ox.distance.nearest_nodes(graph, start_point[1], start_point[0])
    end_node = ox.distance.nearest_nodes(graph, end_point[1], end_point[0])
    route = nx.shortest_path(graph, start_node, end_node, weight='length')
    return route

def print_path_info(graph, path):
    total_distance = 0
    street_distance = 0
    previous_street_name = None
    for i in range(len(path) - 1):
        edge_data = graph.get_edge_data(path[i], path[i + 1], 0)
        street_name = edge_data.get('name', 'Unnamed street')
        length = edge_data.get('length', 0)
        total_distance += length
        if street_name == previous_street_name or previous_street_name is None:
            # If the street name is the same as the previous one, add up the distance
            street_distance += length
        else:
            # If the street name has changed, print the total distance for the previous street
            print(f"Edge from '{previous_street_name}': Length = {street_distance:.2f} meters")
            street_distance = length
        previous_street_name = street_name
    # Print the total distance for the last street
    print(f"Edge from '{previous_street_name}': Length = {street_distance:.2f} meters")
    return total_distance


def main():
    start_time = time.time()
    color_cycle = cycle(COLORS)

    graph = get_graph(PLACE_NAME)

    # Use a greedy algorithm 
    locations_list = list(LOCATIONS.values())
    start_location = LOCATIONS[START_LOCATION]
    locations_list.remove(start_location)
    ordered_locations = [start_location]
    while locations_list:
        current_location = ordered_locations[-1]
        nearest_location = min(locations_list, key=lambda location: distance.euclidean(current_location, location))
        locations_list.remove(nearest_location)
        ordered_locations.append(nearest_location)

    # Create a new Folium map
    m = folium.Map(location=[LOCATIONS[START_LOCATION][0], LOCATIONS[START_LOCATION][1]], zoom_start=14)

    # Initialize a counter before the loop
    counter = 1
    total_distance = 0
    path_sequence = []
    for i in range(len(ordered_locations) - 1):
        start_coords = ordered_locations[i]
        end_coords = ordered_locations[i + 1]
        start_name = next(name for name, coords in LOCATIONS.items() if coords == start_coords)
        end_name = next(name for name, coords in LOCATIONS.items() if coords == end_coords)
        path = navigate(graph, start_coords, end_coords)
        color = next(color_cycle)

        # Create a tooltip string
        tooltip = f"{counter}. Path from {start_name} to {end_name}"

        # Create a LineString from the path and add it to the map
        line = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in path]
        folium.PolyLine(locations=line, color=color, weight=3, tooltip=tooltip).add_to(m)

        # Calculate the distance of the path
        path_distance = print_path_info(graph, path)
        total_distance += path_distance

        print(f"{counter}. Path from {start_name} to {end_name}: Distance = {path_distance:.2f} meters\n")

        # Add the path and the distance to the sequence
        path_sequence.append((counter, start_name, end_name, path_distance))

        counter += 1

    # Print the path sequence
    print("Path sequence:")
    for counter, start_name, end_name, path_distance in path_sequence:
        print(f"{counter}. Path from {start_name} to {end_name}: Distance = {path_distance:.2f} meters")

    print(f"Total Distance for all paths: {total_distance:.2f} meters\n")
    # Add markers for each location
    for place, coords in LOCATIONS.items():
        folium.Marker(location=[coords[0], coords[1]], popup=place).add_to(m)
    # Record the end time
    end_time = time.time()

    # Calculate and print the runtime
    runtime = end_time - start_time
    print(f"Runtime: {runtime:.2f} seconds")
    # Save the map to an HTML file
    m.save('Greedy_TSP_Demo.html')
if __name__ == '__main__':
    main()