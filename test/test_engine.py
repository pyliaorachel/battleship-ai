from test.test_generator import *
from test.utilities import *
import time
import math

scaling_tests_folder = os.path.join(static_test_folder, 'scaling_tests')

# the constraint tests had to be created manually
ship_constraint_tests_folder = os.path.join(static_test_folder, 'ship_constaint_tests')


def create_scaling_test(starting_board_size, number_of_boards_to_test, starting_target_size,
                        number_of_tests_per_board_size_per_target_size):
    # we double board size for n times
    board_sizes = [starting_board_size * (2 ** power) for power in range(number_of_boards_to_test)]
    for board_size in board_sizes:
        # we double target size till it reaches the maximum
        target_sizes = [starting_target_size * (2 ** power) for power in range(math.ceil(math.log2(board_size ** 2)))]
        for target_size in target_sizes:
            create_tests(board_size, target_size, 0, number_of_tests_per_board_size_per_target_size, True,
                         scaling_tests_folder)


if __name__ == '__main__':
    # config
    starting_board_size = 5
    number_of_boards_to_test = 5

    starting_target_size = 1
    number_of_tests_per_board_size_per_target_size = 100

    # create tests
    create_scaling_test(starting_board_size, number_of_boards_to_test, starting_target_size,
                        number_of_tests_per_board_size_per_target_size)

    # TODO: write testing methods to keep track of time
    # running tests
    # print(os.path.dirname(os.path.abspath(__file__)))
    # start = time.time()
    #
    # runtime = time.time() - start
