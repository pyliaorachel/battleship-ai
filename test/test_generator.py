import os

from test.utilities import *

static_test_folder = './static_tests'


class BattleshipTest:
    def __init__(self, target_map,
                 height=None,
                 width=None,
                 row_targets=None,
                 col_targets=None,
                 ships=None,
                 ship_map=None):
        self.target_map = target_map
        if not height or not width or not row_targets or not col_targets or not ships or not ship_map:
            self.height = len(target_map)
            self.width = len(target_map[0])
            self.row_targets, self.col_targets = get_sum_targets(target_map)
            self.ships, self.ship_map = get_ships_and_map(target_map)
        else:
            self.height = height
            self.width = width
            self.row_targets = row_targets
            self.col_targets = col_targets
            self.ships = ships
            self.ship_map = ship_map

    def check_targets(self, target_map):
        # assume the input map is valid
        return self.target_map == target_map

    def check_ships(self, ship_map):
        # assume the input map is valid
        return self.ship_map == ship_map

    def __str__(self):
        return str((self.height,
                    self.width,
                    self.target_map,
                    self.row_targets,
                    self.col_targets,
                    self.ships,
                    self.ship_map))


def generate_test_file_name(height, width, num_of_targets, num_of_tests):
    """Generate test file name from inputs.

    Args:
        height (int): Height of the map.
        width (int): Width of the map.
        num_of_targets (int): Number of targets.
        num_of_tests (int): Number of tests.

    Returns:
        file_name (str): Test file name.
    """
    file_name = 'test_{height}_{width}_{num_of_targets}_{num_of_tests}.txt' \
        .format(height=height, width=width, num_of_targets=num_of_targets, num_of_tests=num_of_tests)
    return file_name


def parse_test_file_name(file_path):
    """Parse test file name.

    Args:
        file_path (str): File path string.

    Returns:
        (height, width, num_of_targets, num_of_tests) where
            height (int): Height of the map.
            width (int): Width of the map.
            num_of_targets (int): Number of targets.
            num_of_tests (int): Number of tests.
    """
    file_name = os.path.basename(file_path).split('_')
    height = file_name[1]
    width = file_name[2]
    num_of_targets = file_name[3]
    num_of_tests = file_name[4]
    return (height, width, num_of_targets, num_of_tests)


def create_tests(height, width, num_of_targets, num_of_tests, to_save=False):
    """Create tests and save to file if needed. If a file with same name exist, overwrite existing file.

    Args:
        height (int): Height of the map.
        width (int): Width of the map.
        num_of_targets (int): Number of targets.
        num_of_tests (int): Number of tests to generate.
        to_save (Optional[bool]): Whether or not to save.

    Returns:
        list of BattleshipTests
    """
    tests = [BattleshipTest(generate_target_map(height, width, num_of_targets)) for _ in range(num_of_tests)]
    if to_save:
        file_name = generate_test_file_name(height, width, num_of_targets, num_of_tests)
        file_path = os.path.join(static_test_folder, file_name)
        if os.path.isfile(file_path):
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


if __name__ == '__main__':
    # Create and save tests to file
    create_tests(5, 5, 10, 10, True)

    # Load tests from file
    tests = load_tests('./static_tests/test_5_5_10_10.txt')
    ship_maps = [test.ship_map for test in tests]
    print_ship_maps(ship_maps)
