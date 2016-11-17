from collections import defaultdict
from random import shuffle

import numpy as np


##########################
# Map Generation Methods #
##########################
def generate_target_map(height, width, num_of_targets):
    """Randomly generate a target map in the dimension with the number of targets.

    Args:
        height (int): Height of the map
        width (int): Width of the map
        num_of_targets (int): Number of targets to randomly add to map

    Returns:
        target_map (list[list[int]]): A target map with 0 as ocean and 1 as target.
    """
    total_elements = height * width
    intermediate_map = [1] * num_of_targets
    intermediate_map.extend([0] * (total_elements - num_of_targets))
    shuffle(intermediate_map)
    target_map = [intermediate_map[i * width:i * width + width] for i in range(height)]
    return target_map


def get_sum_targets(target_map):
    """Get sum of rows and sum of columns

    Args:
        target_map (list[list[int]]): A target map with 0 as ocean and 1 as target.

    Returns:
        row_targets (list[int]): Sum of targets in each row.
        column_targets (list[int]): Sum of targets in each column.
    """
    row_targets = [sum(row) for row in target_map]
    column_targets = [sum(column) for column in zip(*target_map)]
    return row_targets, column_targets


def get_ships_and_map(target_map):
    """Get the number of each length of ships.

    Args:
        target_map (list[list[int]]): A target map with 0 as ocean and 1 as target.

    Returns:
        ships (list[int]): Number of each length of ships.
        ship_map (list[list[int]]): A ship map with 0 as ocean and i > 0 as ships with i length.
    """
    # initialize ship map, ship count and intermediate map
    height = len(target_map)
    width = len(target_map[0])
    ship_map = np.array([[0] * width for _ in range(height)])
    ships_count = defaultdict(lambda: 0)
    intermediate_map = target_map[:]

    # use greedy algorithm to remove ships until there is no more ship on the map
    while sum([sum(row) for row in intermediate_map]) > 0:
        # find the largest connected ship by row and column
        row_lengths = []
        col_lengths = []
        for row in intermediate_map:
            row_lengths.extend(''.join(map(str, row)).split('0'))
        for column in zip(*intermediate_map):
            col_lengths.extend(''.join(map(str, column)).split('0'))
        max_row = max(row_lengths)
        max_col = max(col_lengths)

        # remove largest ship from the map
        snapshot = intermediate_map[:]
        if max_row >= max_col:
            length = len(max_row)
            for index, row in enumerate(intermediate_map):
                string = ''.join(map(str, row))
                if max_row in string:
                    ships_count[length] += string.count(max_row)
                    string = string.replace(max_row, '0' * length)
                    intermediate_map[index] = list(map(int, list(string)))
        else:
            length = len(max_col)
            transposed_map = np.array(intermediate_map).T.tolist()
            for index, row in enumerate(transposed_map):
                string = ''.join(map(str, row))
                if max_col in string:
                    ships_count[length] += string.count(max_col)
                    string = string.replace(max_col, '0' * length)
                    transposed_map[index] = list(map(int, list(string)))
            intermediate_map = np.array(transposed_map).T.tolist()
        diff = np.array(snapshot) - np.array(intermediate_map)
        diff *= length
        ship_map += diff

    # create ships list
    ships = []
    for i in range(max(ships_count.keys()) + 1):
        ships.append(ships_count[i])
    return ships, ship_map.tolist()


####################
# Printing Methods #
####################
def print_ship_map(ship_map):
    """Print ship map in a presentable form with '~' as ocean and i > 0 as target.

    Args:
        ship_map (list[list[int]]): A ship map with 0 as ocean and 1 as target.
    """

    def convert(number):
        if number == 0:
            return '~'
        else:
            return str(number)

    for row in ship_map:
        print(str(list(map(convert, row)))
              .replace(', ', ' ')
              .replace('[', '')
              .replace(']', '')
              .replace('\'', ''))
    print()


def print_ship_maps(ship_maps):
    """Print each ship map in the list.

    Args:
        ship_maps (list[list[list[int]]]): A list of ship maps.
    """
    for index, ship_map in enumerate(ship_maps):
        print('Ship Map {}/{}'.format(index + 1, len(ship_maps)))
        print_ship_map(ship_map)


def print_target_map(target_map):
    """Print target map in a presentable form with '~' as ocean and 'x' as target.

    Args:
        target_map (list[list[int]]): A target map with 0 as ocean and 1 as target.
    """

    def convert(number):
        if number == 0:
            return '~'
        else:
            return 'x'

    for row in target_map:
        print(str(list(map(convert, row)))
              .replace(', ', ' ')
              .replace('[', '')
              .replace(']', '')
              .replace('\'', ''))
    print()


def print_target_maps(target_maps):
    """Print each target map in the list.

    Args:
        target_maps (list[list[list[int]]]): A list of target maps.
    """
    for index, target_map in enumerate(target_maps):
        print('Target Map {}/{}'.format(index + 1, len(target_maps)))
        print_target_map(target_map)


####################
# File I/O Methods #
####################
def read_target_maps_from_file(file_path):
    """Return a list of target maps from file.

    Args:
        file_path (str): Path to read the file from.

    Returns:
        target_maps (list[list[list[int]]]): A list of target maps.
    """
    target_maps = []
    with open(file_path, 'r') as f:
        for target_map in f.read().splitlines():
            target_maps.append(eval(target_map))
    return target_maps


def save_target_maps_to_file(target_maps, file_path):
    """Save a list of target maps to file. If a file exist and to_overwrite is False, append to file.
    Else, overwrite the file.

    Args:
        target_maps (list[list[list[int]]]): A list of target maps.
        file_path (str): Path to save the file to.
    """
    with open(file_path, 'a') as f:
        for target_map in target_maps:
            f.write(str(target_map) + '\n')


if __name__ == '__main__':
    import os

    # Sample usages of the methods above
    target_map = generate_target_map(5, 5, 10)

    print('Raw Target Map = {}'.format(target_map))
    print()
    print('Formatted Target Map:')
    print_target_map(target_map)

    row_targets, column_targets = get_sum_targets(target_map)
    print('row_targets = {}'.format(row_targets))
    print('column_targets = {}'.format(column_targets))
    print()

    ships, ship_map = get_ships_and_map(target_map)
    print('ships = {}'.format(ships))
    print('Formatted Ship Map:')
    print_ship_map(ship_map)

    # Test reading map from and writing target map to file
    path = os.path.dirname(__file__)
    target_maps = [generate_target_map(5, 5, 10)]
    target_maps.append(generate_target_map(5, 5, 10))

    file_name = 'sample.txt'
    save_target_maps_to_file(target_maps, os.path.join(path, file_name))
    target_maps = read_target_maps_from_file(os.path.join(path, file_name))

    print('Test writing map to and reading map from file...')
    print_target_maps(target_maps)
    os.remove(os.path.join(path, file_name))
