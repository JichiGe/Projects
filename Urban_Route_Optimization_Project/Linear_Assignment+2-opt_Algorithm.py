#result is saved in Linear_Assignment+2-opt_Algorithm_Demo.html

import osmnx as ox
import networkx as nx
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import linear_sum_assignment
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


def get_path_length(graph, path):
    total_distance = 0
    for i in range(len(path) - 1):
        edge_data = graph.get_edge_data(path[i], path[i + 1], 0)
        length = edge_data.get('length', 0)
        total_distance += length
    return total_distance

def two_opt_swap(route, i, k):
    new_route = route[0:i]
    new_route.extend(reversed(route[i:k + 1]))
    new_route.extend(route[k+1:])
    return new_route

def two_opt(route, dist_matrix):
    improvement = True
    best_route = route
    best_distance = get_total_distance(route, dist_matrix)

    while improvement: 
        improvement = False
        for i in range(1, len(route) - 1):
            for k in range(i+1, len(route)):
                new_route = two_opt_swap(best_route, i, k)
                new_distance = get_total_distance(new_route, dist_matrix)
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_route = new_route
                    improvement = True
        route = best_route
    return best_route

def get_total_distance(route, dist_matrix):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += dist_matrix[route[i]][route[i+1]]
    return total_distance

def navigate(graph, start_coords, end_coords):
    start_node = ox.distance.nearest_nodes(graph, start_coords[1], start_coords[0])
    end_node = ox.distance.nearest_nodes(graph, end_coords[1], end_coords[0])
    return nx.shortest_path(graph, start_node, end_node, weight='length')
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
    # Record the start time
    start_time = time.time()
    # Create a graph from the OpenStreetMap data
    graph = ox.graph_from_place(PLACE_NAME, network_type='drive')

    # Calculate the distance matrix
    distances = pdist(list(LOCATIONS.values()), metric='euclidean')
    dist_matrix = squareform(distances)

    # Solve the TSP
    row_ind, col_ind = linear_sum_assignment(dist_matrix)

    # Order the locations according to the TSP solution
    ordered_indices = col_ind.tolist()

    # Ensure the START_LOCATION is the first location
    start_index = list(LOCATIONS.keys()).index(START_LOCATION)
    ordered_indices.remove(start_index)
    ordered_indices.insert(0, start_index)

    # Apply 2-opt to improve the solution
    optimized_route_indices = two_opt(ordered_indices, dist_matrix)

    # Create a new Folium map
    m = folium.Map(location=[LOCATIONS[START_LOCATION][0], LOCATIONS[START_LOCATION][1]], zoom_start=14)

    # Define a list of colors to cycle through
    colors = COLORS

    # Keep track of the paths that have already been plotted
    plotted_paths = set()

    # Keep track of the total distance
    total_distance = 0

    # Convert the optimized route indices back into coordinates
    optimized_route = [list(LOCATIONS.values())[i] for i in optimized_route_indices]

    # Initialize a counter
    counter = 1
    # Initialize an empty list to store the location sequence and distances
    location_sequence = []
    # Plot the TSP path
    for i in range(len(optimized_route) - 1):
        start_coords = optimized_route[i]
        end_coords = optimized_route[i + 1]
        start_name = next(name for name, coords in LOCATIONS.items() if coords == start_coords)
        end_name = next(name for name, coords in LOCATIONS.items() if coords == end_coords)
        path = navigate(graph, start_coords, end_coords)

        # Check if the path has already been plotted
        path_tuple = tuple(path)
        if path_tuple in plotted_paths:
            continue
        plotted_paths.add(path_tuple)

        # Create a LineString from the path and add it to the map
        line = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in path]
        color = colors[i % len(colors)]  # Cycle through the colors

        # Create a tooltip string
        tooltip = f"{counter}. Path from {start_name} to {end_name}"

        # Add the tooltip to the PolyLine
        folium.PolyLine(locations=line, color=color, weight=4, tooltip=tooltip).add_to(m)

        # Calculate the path length and add it to the total distance
        path_length = print_path_info(graph, path)
        total_distance += path_length

        print(f"{counter}. Path from {start_name} to {end_name}: Length = {path_length:.2f} meters\n")
        # Add the location and distance to the list
        location_sequence.append((start_name, end_name, path_length))
        # Increment the counter
        counter += 1
    print()
    # Print the location sequence and distances
    for i, (start_name, end_name, distance) in enumerate(location_sequence, start=1):
        print(f"{i}. From {start_name} to {end_name}: Distance = {distance:.2f} meters")

    print(f"\nTotal Distance: {total_distance:.2f} meters\n")


    # Add markers for each location
    for place, coords in LOCATIONS.items():
        folium.Marker(location=[coords[0], coords[1]], popup=place).add_to(m)

    # Record the end time
    end_time = time.time()

    # Calculate and print the runtime
    runtime = end_time - start_time
    m.save('Linear_Assignment+2-opt_Algorithm_Demo.html')
    print(f"Runtime: {runtime:.2f} seconds")
if __name__ == '__main__':
    main()