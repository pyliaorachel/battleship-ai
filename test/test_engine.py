import time
import os

from test.validity_check import is_valid
from test.test_generator import *
from test.utilities import *
from csp.battleship_csp import battleship_csp_model1, battleship_csp_model2
from csp.battleship_BT import *
from csp.propagators import *
from csp.orderings import *

HEADER = 'model,board size,target size,propagation type,variable ordering type,value ordering type,avg runtime\n'
results = os.path.join(test_folder, 'results')


def basic_test_model1(filename, validity_check=False, trace_BT=False):
    with open(os.path.join(results, filename), 'w') as f:
        f.write(HEADER)
        model = battleship_csp_model1
        for prop_type in ['BT', 'FC', 'GAC']:
            for val_ord_type in [val_arbitrary, val_decrease_lcv, val_decreasing_order, val_increasing_order,
                                 val_lcv]:
                for file in sorted(os.listdir(basic_test_folder)):
                    tests = load_tests(os.path.join(basic_test_folder, file))
                    run_times = []
                    for test in tests:
                        # prepare a test
                        i = test.board_size
                        j = sum(test.rol_targets)
                        row_targets = test.row_targets
                        col_targets = test.col_targets
                        ships = test.ships
                        # start timing
                        start_time = time.time()

                        # run the test
                        battleship_csp, variable_array = model(row_targets, col_targets, ships)
                        print('Board Size: {size}x{size} | Target count: {count}'.format(size=i, count=j))
                        print((model.__name__, prop_type, 'default_ord_type', val_ord_type.__name__))

                        solver = battleship_BT(battleship_csp)
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
                        run_times.append(run_time)

                        print()
                        # check if is valid
                        if validity_check:
                            solution = battleship_csp.get_sol_board()
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
                    # model,board size,target size,propagation type,variable ordering type,value ordering type,runtime
                    avg_runtime = sum(run_times) / len(run_times)
                    f.write(
                        '{model},{board_size},{target_size},{propagation_type},{variable_ordering_type},{value_ordering_type},{runtime}\n'
                            .format(model=model.__name__, board_size=i, target_size=j, propagation_type=prop_type,
                                    variable_ordering_type='default_ord_type',
                                    value_ordering_type=val_ord_type.__name__,
                                    runtime=avg_runtime))


def basic_test_model2(filename, validity_check=False, trace_BT=False):
    with open(os.path.join(results, filename), 'w') as f:
        f.write(HEADER)
        model = battleship_csp_model2
        for prop_type in ['BT', 'FC', 'GAC']:
            for var_ord_type in [ord_random, ord_mrv, ord_dh]:
                for val_ord_type in [val_arbitrary, val_decrease_lcv, val_decreasing_order,
                                     val_increasing_order, val_lcv]:
                    for file in sorted(os.listdir(basic_test_folder)):
                        tests = load_tests(os.path.join(basic_test_folder, file))
                        run_times = []
                        for test in tests:
                            # prepare a test
                            i = test.board_size
                            j = sum(test.rol_targets)
                            row_targets = test.row_targets
                            col_targets = test.col_targets
                            ships = test.ships

                            # start timing
                            start_time = time.time()

                            # run the test
                            battleship_csp, variable_array = model(row_targets, col_targets, ships)
                            print('Board Size: {size}x{size} | Target count: {count}'.format(size=i, count=j))
                            print((model.__name__, prop_type, var_ord_type.__name__, val_ord_type.__name__))

                            solver = BT(battleship_csp)
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
                            run_times.append(run_time)

                            print()
                            # check if is valid
                            if validity_check:
                                solution = battleship_csp.get_sol_board()
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

                        # model,board size,target size,propagation type,variable ordering type,value ordering type,runtime
                        avg_runtime = sum(run_times) / len(run_times)
                        f.write(
                            '{model},{board_size},{target_size},{propagation_type},{variable_ordering_type},{value_ordering_type},{runtime}\n'
                                .format(model=model.__name__, board_size=i, target_size=j,
                                        propagation_type=prop_type,
                                        variable_ordering_type='default_ord_type',
                                        value_ordering_type=val_ord_type.__name__,
                                        runtime=avg_runtime))


if __name__ == '__main__':
    basic_test_model1('basic_test_model1.csv')
    basic_test_model2('basic_test_model2.csv')
