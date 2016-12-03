from test.validity_check import is_valid
from test.test_generator import BattleshipTest
from test.utilities import *
from csp.battleship_csp import battleship_csp_model1, battleship_csp_model2
from csp.battleship_BT import BT
from csp.propagators import *
from csp.orderings import *
import traceback


def basic_check(model, prop_type, var_ord_type, val_ord_type, trace_BT=False):
    for i in range(1, 3):
        for j in range(1, i ** 2):
            # prepare a test
            test = BattleshipTest(generate_target_map(i, j))
            row_targets = test.row_targets
            col_targets = test.col_targets
            ships = test.ships
            print()
            print(ships)
            print_target_map(test.target_map)

            # run the test
            battleship_csp, variable_array = model(row_targets, col_targets, ships)

            try:
                solver = BT(battleship_csp)
                if trace_BT:
                    solver.trace_on()
                if prop_type == 'BT':
                    solver.bt_search(prop_BT, var_ord_type, val_ord_type)
                elif prop_type == 'FC':
                    solver.bt_search(prop_FC, var_ord_type, val_ord_type)
                elif prop_type == 'GAC':
                    solver.bt_search(prop_GAC, var_ord_type, val_ord_type)
                solution = battleship_csp.get_sol_board()

                #TODO: there is an issue with printing out the solutions... need to figure this out
                print('{} {} {} {}'.format(model.__name__, prop_type, var_ord_type, val_ord_type))
                print(solution)

                # check if is valid
                if not is_valid(solution, test):
                    print('Output is not valid!')
                    print('{} {} {} {}'.format(model.__name__, prop_type, var_ord_type, val_ord_type))
                    print('Assignment:')
                    print_assignment_map(solution)
                    print('Test:')
                    print('Target_Map:')
                    print_target_map(test.target_map)
                    print('Ships:')
                    print(ships)
            except:
                print("One or more runtime errors occurred while trying a sample test run on %s: %r" % (
                    model.__name__, traceback.format_exc()))


if __name__ == '__main__':
    basic_check(battleship_csp_model1, 'BT', ord_random, val_arbitrary)
    basic_check(battleship_csp_model1, 'BT', ord_random, val_decrease_lcv)
    basic_check(battleship_csp_model1, 'BT', ord_random, val_decreasing_order)
    basic_check(battleship_csp_model1, 'BT', ord_random, val_increasing_order)
    basic_check(battleship_csp_model1, 'BT', ord_random, val_lcv)
    basic_check(battleship_csp_model1, 'BT', ord_mrv, val_decreasing_order)
    basic_check(battleship_csp_model1, 'BT', ord_dh, val_decreasing_order)
    basic_check(battleship_csp_model2, 'BT', ord_random, val_arbitrary)