from collections import defaultdict
from random import shuffle

import numpy as np


def generate_battleship_map(height, width, num_of_targets):
    """Randomly generate a 2D battleship map in the dimension with the number of targets.

    Args:
        height (int): Height of the map
        width (int): Width of the map
        num_of_targets (int): Number of targets to randomly add to map

    Returns:
        battleship_map (list[list[int]]): A 2D battleship map with 0 as ocean and 1 as target.
    """
    total_elements = height * width
    intermediate_map = [1] * num_of_targets
    intermediate_map.extend([0] * (total_elements - num_of_targets))
    shuffle(intermediate_map)
    battleship_map = [intermediate_map[i * width:i * width + width] for i in range(height)]
    return battleship_map


def get_sum_targets(battleship_map):
    """Get sum of rows and sum of columns

    Args:
        battleship_map (list[list[int]]): A 2D battleship map with 0 as ocean and 1 as target.

    Returns:
        sum_row_targets (list[int]): Sum of targets in each row.
        sum_column_targets (list[int]): Sum of targets in each column.
    """
    sum_row_targets = [sum(row) for row in battleship_map]
    sum_column_targets = [sum(column) for column in zip(*battleship_map)]
    return sum_row_targets, sum_column_targets


def get_ships(battleship_map):
    """Get the number of each length of ships.

    Args:
        battleship_map (list[list[int]]): A 2D battleship map with 0 as ocean and 1 as target.

    Returns:
        ships (list[int]): Number of each length of ships.
    """
    ships_map = defaultdict(lambda: 0)
    intermediate_map = battleship_map[:]

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
        if max_row >= max_col:
            length = len(max_row)
            for index, row in enumerate(intermediate_map):
                string = ''.join(map(str, row))
                if max_row in string:
                    ships_map[length] += string.count(max_row)
                    string = string.replace(max_row, '0' * length)
                    intermediate_map[index] = list(map(int, list(string)))
        else:
            length = len(max_col)
            transposed_map = np.array(intermediate_map).T.tolist()
            for index, row in enumerate(transposed_map):
                string = ''.join(map(str, row))
                if max_col in string:
                    ships_map[length] += string.count(max_col)
                    string = string.replace(max_col, '0' * length)
                    transposed_map[index] = list(map(int, list(string)))
            intermediate_map = np.array(transposed_map).T.tolist()

    # create ships list
    ships = []
    for i in range(max(ships_map.keys())):
        ships.append(ships_map[i])
    return ships


def print_battleship_map(battleship_map):
    """Print battleship map in a presentable form with '~' as ocean and 'x' as target.

    Args:
        battleship_map (list[list[int]]): A 2D battleship map with 0 as ocean and 1 as target.
    """
    for row in battleship_map:
        print(str(row)
              .replace(', ', ' ')
              .replace('[', '')
              .replace(']', '')
              .replace('0', '~')
              .replace('1', 'x'))
    print()


def print_battleship_maps(battleship_maps):
    """Print each battleship map in the list.

    Args:
        battleship_maps (list[list[list[int]]]): A list of battleship maps.
    """
    for index, battleship_map in enumerate(battleship_maps):
        print('Map {}/{}'.format(index + 1, len(battleship_maps)))
        print_battleship_map(battleship_map)


def read_battleship_maps_from_file(file_path):
    """Return a list of batteship maps from file.

    Args:
        file_path (str): Path to read the file from.

    Returns:
        battleship_maps (list[list[list[int]]]): A list of battleship maps.
    """
    battleship_maps = []
    with open(file_path, 'r') as f:
        for battleship_map in f.read().splitlines():
            battleship_maps.append(eval(battleship_map))
    return battleship_maps


def save_battleship_maps_to_file(battleship_maps, file_path):
    """Save a list of battleship maps to file. If a file exist and to_overwrite is False, append to file.
    Else, overwrite the file.

    Args:
        battleship_maps (list[list[list[int]]]): A list of battleship maps.
        file_path (str): Path to save the file to.
    """
    with open(file_path, 'a') as f:
        for battleship_map in battleship_maps:
            f.write(str(battleship_map) + '\n')


if __name__ == '__main__':
    import os

    # Sample usages of the methods above
    battleship_map = generate_battleship_map(5, 5, 10)

    print('Original Battleship Map = {}'.format(battleship_map))
    print()
    print('Formatted Battleship Map:')
    print_battleship_map(battleship_map)

    sum_row_targets, sum_column_targets = get_sum_targets(battleship_map)
    print('sum_row_targets = {}'.format(sum_row_targets))
    print('sum_column_targets = {}'.format(sum_column_targets))

    ships = get_ships(battleship_map)
    print('ships = {}'.format(ships))

    # Test reading map from and writing map to file
    path = os.path.dirname(__file__)
    battleship_maps = [battleship_map]

    file_name = 'sample.txt'
    save_battleship_maps_to_file(battleship_maps, os.path.join(path, file_name))
    battleship_maps = read_battleship_maps_from_file(os.path.join(path, file_name))
    print()
    print('Test reading map from and writing map to file...')
    print_battleship_maps(battleship_maps)
    os.remove(os.path.join(path, file_name))
