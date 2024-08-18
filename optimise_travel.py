import math
from itertools import combinations

# Coordinates are converted to UTM format for analysis in metres.
# We will assume they are in same zone for this problem.
import utm


def convert_to_utm_xy(coordinates: list) -> list:
    """Converts a list of lat/lon coordinates to UTM format.
    Takes a list of lat/lon coords and extracts out the easting and northing
    vectors (in m).

    NOTE: For the purposes of this exercise we can ignore differing zone
          letters and numbers.

    Args:
        coordinates (list): A list of lat/lon coordinates.

    Returns:
        list: A list of UTM coordinates in the form (easting, northing).
    """
    return [utm.from_latlon(*c)[:2] for c in coordinates]


def calc_total_distance(coordinates_xy: list, indices: list) -> float:
    """Calculates the total distance between a list of coordinates.

    Args:
        coordinates_xy (list): A list of UTM coordinates in the form
            (easting, northing).
        indices (list): A list of indices to use to calculate the distance.

    Returns:
        float: The total distance between the coordinates.
    """
    total_distance = 0
    for i in range(1, len(indices)):
        dx = coordinates_xy[indices[i]][0] - coordinates_xy[indices[i-1]][0]
        dy = coordinates_xy[indices[i]][1] - coordinates_xy[indices[i-1]][1]
        total_distance += math.sqrt(dx*dx + dy*dy)
    return total_distance

def optimise_travel_order(coordinates: list) -> list:
    """The main function to optimise the travel order.

    Args:
        coordinates (list): A list of lat/lon coordinates

    Returns:
        list: A list of indices in the optimised order.
    """
    coordinates_xy = convert_to_utm_xy(coordinates)
    
    # TODO Devise an algorithm to optimise the order
    distance_matrix = calc_distance_matrix(coordinates_xy)
    n = len(distance_matrix)
    memo = make_memo(distance_matrix)
    
    cost = math.inf    
    for key in memo:
        # via_set that has traversed all places
        if len(key[1]) == n-2:
            new_cost = memo[key][0]
            if new_cost < cost:
                cost = new_cost
                to_node = key[0]
                from_node = memo[key][1]
    path = [to_node, from_node]
    via_set = frozenset(range(1, n)) - {from_node, to_node}

    while via_set:
        next_node = memo[(from_node, via_set)][1]
        path.append(next_node)
        via_set = via_set - {next_node}

    path.append(0)
    path.reverse()
    
    return path
    

def make_memo(distance_matrix) -> dict:
    n = len(distance_matrix)
    p1 = 0  # Arbitrary starting point
    # Memoization dictionary
    memo = {}

    # Initialize memoization for p2 places from p1
    for p2 in range(1, n):
        via_set = frozenset()
        # min cost from a place in via_set to p2
        cost = distance_matrix[p1][p2]
        # memo[from_node, via_set] = [cost, to_node]
        memo[(p2, via_set)] = [cost, p1]
        
    # all possible to_nodes
    p2_set = frozenset(range(1,n))
    for set_size in range(1, n-1):
        for via_set in combinations(range(1, n), set_size):
            via_set = frozenset(via_set)
            # decide p2 from p2s
            p2s = p2_set-via_set
            for p2 in p2s:
                cost = math.inf
                from_node = None
                for p1 in via_set:
                    new_cost = memo[(p1, via_set-{p1})][0] + distance_matrix[p1][p2]
                    if new_cost < cost:
                        cost = new_cost
                        from_node = p1
                memo[(p2, via_set)] = [cost, from_node]
                
    return memo

def traveling_salesperson_problem(coordinates=None, distance_matrix=None, memo=None):
    if distance_matrix and memo:
        pass
    elif coordinates is None:
        return
    else:
        coordinates_xy = convert_to_utm_xy(coordinates)
        distance_matrix = calc_distance_matrix(coordinates_xy)
    
    n = len(distance_matrix)
    memo = make_memo(distance_matrix)
    p2_set = frozenset(range(1,n))
    
    # Return to the starting place (node 0) from the last node p1
    cost = math.inf
    for p1 in range(1, n):
        new_cost = memo[(p1, p2_set-{p1})][0] + distance_matrix[p1][0]
        # Find the minimum cost to complete the tour
        if new_cost < cost:
            cost = new_cost
            from_node = p1
    
    path = [0, from_node]
    via_set = frozenset(range(1, n)) - {from_node}

    while via_set:
        next_node = memo[(from_node, via_set)][1]
        path.append(next_node)
        via_set = via_set - {next_node}

    path.append(0)
    path.reverse()

    return path

def calc_distance_matrix(coordinates_xy):
    # num points
    n = len(coordinates_xy)
    distance_matrix = [[0] * n for i in range(n)]
    
    for i in range(n):
        for j in range(i, n):
            # the same place
            if i == j:
                continue
            else:
                x1, y1 = coordinates_xy[i]
                x2, y2 = coordinates_xy[j]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance
    
    return distance_matrix