import math
from test.utilities import *
import os

test_folder = os.path.dirname(os.path.abspath(__file__))
static_test_folder = os.path.join(test_folder, 'static_tests')

# the constraint tests had to be created manually
ship_constraint_tests_folder = os.path.join(static_test_folder, 'ship_constaint_tests')
basic_test_folder = os.path.join(static_test_folder, 'basic_tests')


class BattleshipTest:
    def __init__(self, target_map,
                 board_size=None,
                 row_targets=None,
                 col_targets=None,
                 ships=None,
                 ship_map=None):
        self.target_map = target_map
        if not board_size or not row_targets or not col_targets or not ships or not ship_map:
            self.board_size = len(target_map)
            self.row_targets, self.col_targets = get_sum_targets(target_map)
            self.ships, self.ship_map = get_ships_and_map(target_map)
        else:
            self.board_size = board_size
            self.row_targets = row_targets
            self.col_targets = col_targets
            self.ships = ships
            self.ship_map = ship_map

    def __str__(self):
        return str((self.board_size,
                    self.target_map,
                    self.row_targets,
                    self.col_targets,
                    self.ships,
                    self.ship_map))


def generate_test_file_name(board_size, num_of_targets, num_of_ships, num_of_tests):
    """Generate test file name from inputs.

    Args:
        board_size (int): Height and width of the map.
        num_of_targets (int): Number of targets.
        num_of_ships (int): Number of ships.
        num_of_tests (int): Number of tests.

    Returns:
        file_name (str): Test file name.
    """
    file_name = 'test_{board_size}_{num_of_targets}_{num_of_ships}_{num_of_tests}.txt' \
        .format(board_size=board_size, num_of_targets=num_of_targets, num_of_ships=num_of_ships,
                num_of_tests=num_of_tests)
    return file_name


def parse_test_file_name(file_path):
    """Parse test file name.

    Args:
        file_path (str): File path string.

    Returns:
        (board_size, width, num_of_targets, num_of_tests) where
            board_size (int): Height and width of the map.
            num_of_targets (int): Number of targets.
            num_of_ships (int): Number of ships. 0 if unconstrained.
            num_of_tests (int): Number of tests.
    """
    file_name = os.path.basename(file_path).split('_')
    board_size = file_name[1]
    num_of_targets = file_name[2]
    num_of_ships = file_name[3]
    num_of_tests = file_name[4]
    return (board_size, num_of_targets, num_of_ships, num_of_tests)


def create_tests(board_size, num_of_targets, num_of_ships, num_of_tests, to_save=False, folder_path=static_test_folder):
    """Create tests and save to file if needed. If a file with same name exist, overwrite existing file.

    Args:
        board_size (int): Height and width of the map.
        num_of_targets (int): Number of targets.
        num_of_ships (int): Number of ships in the map. 0 is unconstrained.
        num_of_tests (int): Number of tests to generate.
        to_save (Optional[bool]): Whether or not to save.

    Returns:
        list of BattleshipTests
    """
    if num_of_ships == 0:
        # if there is no constraint
        tests = [BattleshipTest(generate_target_map(board_size, num_of_targets)) for _ in range(num_of_tests)]
    else:
        # there is constraint
        tests = []
        while len(tests) < num_of_tests:
            new_test = BattleshipTest(generate_target_map(board_size, num_of_targets))
            if len(new_test.ships) == num_of_ships:
                tests.append(new_test)
    if to_save:
        file_name = generate_test_file_name(board_size, num_of_targets, num_of_ships, num_of_tests)
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        save_list_to_file(tests, file_path)
    return tests


def load_tests(file_path):
    """Load tests from file. If file is empty, return an empty list of tests.

    Args:
        file_path: File to read.

    Returns:
        list of BattleshipTests
    """
    if os.path.isfile(file_path):
        return [BattleshipTest(*item) for item in read_list_from_file(file_path)]
    return []


def create_basic_test(starting_board_size, number_of_boards_to_test, number_of_tests_per_board_size_per_target_size):
    # we double board size for n times
    board_sizes = [starting_board_size * multiple for multiple in range(1, number_of_boards_to_test + 1)]
    for board_size in board_sizes:
        # we double target size till it reaches the maximum
        target_sizes = [target_size for target_size in range(1, board_size ** 2)]
        for target_size in target_sizes:
            create_tests(board_size, target_size, 0, number_of_tests_per_board_size_per_target_size, True,
                         basic_test_folder)


if __name__ == '__main__':
    # Create and save tests to file
    # 5x5 map with 5 targets, no ship constraint, 10 tests
    # create_tests(5, 5, 0, 10, True)
    #
    # # Load tests from file
    # tests = load_tests('./static_tests/test_5_5_0_10.txt')
    # ship_maps = [test.ship_map for test in tests]
    # print_ship_maps(ship_maps)
    create_basic_test(1, 20, 10)
