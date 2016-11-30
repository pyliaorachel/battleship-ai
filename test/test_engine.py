from test.test_generator import *
from test.utilities import *
import time
import timeit
import math

if __name__ == '__main__':
    # config
    starting_board_size = 5
    number_of_boards_to_test = 5

    starting_target_size = 1
    number_of_tests_per_board_size_per_target_size = 100

    # create tests
    board_sizes = [starting_board_size * (2 ** power) for power in range(number_of_boards_to_test)]
    for board_size in board_sizes:
        target_sizes = [starting_target_size * (2 ** power) for power in range(math.ceil(math.log2(board_size ** 2)))]
        for target_size in target_sizes:
            create_tests(board_size, board_size, target_size, number_of_tests_per_board_size_per_target_size, True)

    # TODO: Implement test running + timing
            # start = time.time()
            #
            # runtime = time.time() - start
