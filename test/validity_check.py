import numpy as np
from collections import Counter, defaultdict
from .utilities import *


def is_valid(assignment_map, problem):
    """Check whether or not the map is valid.

    Args:
        assignment_map (list[list[tuple]]): Assignment map from CSP solver.
        problem (BattleshipTest): The problems we are solving.

    Returns:
        is_valid (bool): Whether or not the map is valid
    """
    target_map, ship_dict, ships = strip_assignment_map(assignment_map)
    # step 1: check if targets are correct
    row_targets, column_targets = get_sum_targets(target_map)
    if row_targets != problem.row_targets or column_targets != problem.col_targets:
        print('Row or column targets are not correct!')
        return False

    # step 2: check if assignment_map has the right ships count
    if ships != problem.ships:
        print('Ship count is not correct!!')
        return False

    # step 3: check if assignment_map has valid ship assignment
    for ship, locations in ship_dict.items():
        length, _ = ship
        if not valid_location_patterns(length, locations):
            print('Ships do not have valid locations!')
            return False
    return True


##################
# Helper Methods #
##################

def strip_assignment_map(assignment_map):
    """Return crucial information from assignment map.

    Args:
        assignment_map (list[list[tuple]]): A solution map generated by the CSP solver.

    Returns:
        target_map (list[list[int]]): A target map with 0 as ocean and 1 as target.
        ship_dict (dict[list[tuple]]): A dictionary of a ship's locations.
        ships (list[int]): Number of each length of ships.
    """

    def convert(x):
        return 1 if x[0] > 0 else 0

    target_map = [list(map(convert, row)) for row in assignment_map]

    ship_dict = dict()
    for i in range(len(assignment_map)):
        for j in range(len(assignment_map)):
            ship = assignment_map[i][j]
            if ship != (0, 0):
                if ship in ship_dict:
                    ship_dict[ship].append((i, j))
                else:
                    ship_dict[ship] = [(i, j)]

    count = defaultdict(int, Counter([i for i, _ in sorted(ship_dict.keys())]))
    ships = [count[i] for i in range(max(count.keys()) + 1)]

    return target_map, ship_dict, ships


def valid_location_patterns(length, locations):
    if len(locations) != length:
        return False
    row_coordinates, col_coordinates = zip(*sorted(locations))
    row_coordinates = list(map(lambda x: x - row_coordinates[0], row_coordinates))
    col_coordinates = list(map(lambda x: x - col_coordinates[0], col_coordinates))
    if row_coordinates == list(range(length)) and col_coordinates == [0] * length:
        return True
    elif row_coordinates == [0] * length and col_coordinates == list(range(length)):
        return True
    return False
