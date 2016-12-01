from test.test_generator import *


def is_valid(assignment_map, problem):
    """Check whether or not the map is valid.

    Args:
        assignment_map (list[list[tuple]]): Assignment map from CSP solver.
        problem (BattleshipTest): The problems we are solving.

    Returns:
        is_valid (bool): Whether or not the map is valid
    """
    target_map, ship_map, ships = strip_assignment_map(assignment_map)
    # step 1: check if targets are correct
    if not problem.check_targets(target_map):
        return False

    # step 2: check if assignment_map has the right ships count
    if ships != problem.ships:
        return False

    # step 3: check if assignment_map has valid ship assignment
    # TODO: figure out a way to check ship assignment

    return True
