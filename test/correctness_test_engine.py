from test.validity_check import is_valid
from test.test_generator import BattleshipTest
from test.utilities import *


def basic_check(method):
    for i in range(1, 3):
        for j in range(i ** 2):
            # prepare a test
            test = BattleshipTest(generate_target_map(i, j))
            row = column = test.board_size
            row_targets = test.row_targets
            col_targets = test.col_targets
            ships = test.ships

            # run the test
            # TODO: figure out how to bind the method with the test
            output = ...

            # check if is valid
            if not is_valid(output, test):
                print('Output is not valid!')
                print('Assignment:')
                print_assignment_map(output)
                print('Test:')
                print('Target_Map:')
                print_target_map(test.target_map)
                print('Ships:')
                print(ships)


if __name__ == '__main__':
    pass
