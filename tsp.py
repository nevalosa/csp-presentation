import random
import sys


""" Holds a route represented by a list of node numbers, and the route's total distance
"""
class Route:
    def __init__(self, path=[0], distance=0):
        self.path = path
        self.distance = distance

    """ Returns a new route by adding provided node to current route
    """
    def create_next_route(self, node, distance):
        return Route(self.path + [node], self.distance + distance)


""" Returns a deterministically generated matrix representing distances between nodes.

intended usage: matrix[row_idx][col_idx] represents distance from node 'row_idx' to node 'col_idx'
"""
def generate_distance_matrix(num_vertices):
    def create_2d_array(size):
        return [[0 for _ in range(size)] for _ in range(size)]
    distance_matrix = create_2d_array(num_vertices)
    random.seed(2)
    for i in range(0, num_vertices):
        for j in range(0, num_vertices):
            distance_matrix[i][j] = random.randint(1, 5)
    return distance_matrix


""" Returns a list of sub routes of maximum length/depth starting from provided route
"""
def get_sub_routes(distance_matrix, depth, current_route=Route()):
    max_path_length = len(distance_matrix)

    def get_remaining_vertices():
        return list(set(range(0, max_path_length)) - set(current_route.path))

    if len(current_route.path) == depth:
        return [current_route]
    else:
        vertices = get_remaining_vertices()
        sub_routes = []
        for vertex in vertices:
            from_vertex = current_route.path[-1]
            to_vertex = vertex
            distance = distance_matrix[from_vertex][to_vertex]
            new_current_route = current_route.create_next_route(vertex, distance)

            sub_routes += get_sub_routes(distance_matrix, depth, new_current_route)
        return sub_routes


""" Returns shortest route starting from provided sub route. Implements branch and bound optimization.

Assumes that start node is 0,0 in distance matrix
"""
def find_shortest_route(distance_matrix, current_route, current_shortest_distance=sys.maxint):
    max_path_length = len(distance_matrix)

    def get_remaining_vertices():
        return list(set(range(0, max_path_length)) - set(current_route.path))

    if len(current_route.path) == max_path_length:
        # Add distance back to start vertices if all vertices have been visited
        current_route.distance += distance_matrix[0][0]
        return current_route
    else:
        vertices = get_remaining_vertices()
        shortest_final_route = None
        for vertex in vertices:
            from_vertex = current_route.path[-1]
            to_vertex = vertex
            distance = distance_matrix[from_vertex][to_vertex]
            new_current_route = current_route.create_next_route(vertex, distance)

            if new_current_route.distance < current_shortest_distance:
                # Still possible to find a shorter route, continue search
                if shortest_final_route is None:
                    final_route = find_shortest_route(distance_matrix, new_current_route, current_shortest_distance)
                else:
                    final_route = find_shortest_route(distance_matrix, new_current_route, min(shortest_final_route.distance, current_shortest_distance))
                if final_route is not None and (shortest_final_route is None or final_route.distance < shortest_final_route.distance):
                    shortest_final_route = final_route
            else:
                # Branch and bound optimization:
                # Route is already longer than the current shortest know route
                pass

        return shortest_final_route
