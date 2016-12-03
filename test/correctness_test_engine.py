import time

from test.validity_check import is_valid
from test.test_generator import BattleshipTest
from test.utilities import *
from csp.battleship_csp import battleship_csp_model1, battleship_csp_model2
from csp.battleship_BT import *
from csp.propagators import *
from csp.orderings import *


def test_model1(trace_BT=False):
    model = battleship_csp_model1
    for prop_type in ['BT', 'FC', 'GAC']:
        for val_ord_type in [val_arbitrary, val_decrease_lcv, val_decreasing_order, val_increasing_order, val_lcv]:
            for i in range(1, 10):
                for j in range(1, i ** 2):
                    # prepare a test
                    test = BattleshipTest(generate_target_map(i, j))
                    row_targets = test.row_targets
                    col_targets = test.col_targets
                    ships = test.ships

                    # start timing
                    start_time = time.time()

                    # run the test
                    battleship_csp, variable_array = model(row_targets, col_targets, ships)
                    print('Board Size: {size}x{size} | Target count: {count}'.format(size=i, count=j))
                    print((model.__name__, prop_type, 'default_ord_type', val_ord_type.__name__))
                    if battleship_csp.model == 1:
                        bt = battleship_BT
                    elif battleship_csp.model == 2:
                        bt = BT

                    solver = bt(battleship_csp)
                    if trace_BT:
                        solver.trace_on()
                    if prop_type == 'BT':
                        solver.bt_search(prop_BT, 'default_ord_type', val_ord_type)
                    elif prop_type == 'FC':
                        solver.bt_search(prop_FC, 'default_ord_type', val_ord_type)
                    elif prop_type == 'GAC':
                        solver.bt_search(prop_GAC, 'default_ord_type', val_ord_type)

                    # end timing
                    run_time = time.time() - start_time

                    solution = battleship_csp.get_sol_board()
                    print()

                    # check if is valid
                    if not is_valid(solution, test):
                        print('Output is not valid!')
                        print('Input:')
                        print('Target_Map:')
                        print_target_map(test.target_map)
                        print('Ships:')
                        print(ships)
                        print('Output:')
                        print_assignment_map(solution)
                        raise Exception


def test_model2(trace_BT=False):
    model = battleship_csp_model2
    for prop_type in ['BT', 'FC', 'GAC']:
        for var_ord_type in [ord_random, ord_mrv, ord_dh]:
            for val_ord_type in [val_arbitrary, val_decrease_lcv, val_decreasing_order, val_increasing_order,
                                 val_lcv]:
                for i in range(1, 10):
                    for j in range(1, i ** 2):
                        # prepare a test
                        test = BattleshipTest(generate_target_map(i, j))
                        row_targets = test.row_targets
                        col_targets = test.col_targets
                        ships = test.ships

                        # start timing
                        start_time = time.time()

                        # run the test
                        battleship_csp, variable_array = model(row_targets, col_targets, ships)
                        print('Board Size: {size}x{size} | Target count: {count}'.format(size=i, count=j))
                        print((model.__name__, prop_type, var_ord_type.__name__, val_ord_type.__name__))
                        if battleship_csp.model == 1:
                            bt = battleship_BT
                        elif battleship_csp.model == 2:
                            bt = BT

                        solver = bt(battleship_csp)
                        if trace_BT:
                            solver.trace_on()
                        if prop_type == 'BT':
                            solver.bt_search(prop_BT, var_ord_type, val_ord_type)
                        elif prop_type == 'FC':
                            solver.bt_search(prop_FC, var_ord_type, val_ord_type)
                        elif prop_type == 'GAC':
                            solver.bt_search(prop_GAC, var_ord_type, val_ord_type)

                        # end timing
                        run_time = time.time() - start_time

                        solution = battleship_csp.get_sol_board()
                        print()

                        # check if is valid
                        if not is_valid(solution, test):
                            print('Output is not valid!')
                            print('Input:')
                            print('Target_Map:')
                            print_target_map(test.target_map)
                            print('Ships:')
                            print(ships)
                            print('Output:')
                            print_assignment_map(solution)
                            raise Exception


if __name__ == '__main__':
    test_model1()
    test_model2()
