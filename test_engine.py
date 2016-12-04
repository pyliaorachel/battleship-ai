import os
import time
from concurrent.futures import ThreadPoolExecutor, wait
from test_generator import *
from orderings import *
from propagators import *
from battleship_BT import *
from battleship_csp import battleship_csp_model1, battleship_csp_model2, battleship_csp_model3

HEADER = 'model,board size,target size,propagation type,variable ordering type,value ordering type,runtime,assignment,pruning\n'
results_folder = os.path.join(root, 'results')
tests = []
for file in sorted(os.listdir(basic_test_folder), key=lambda x: (int(x.split('_')[1]), int(x.split('_')[2]))):
    tests.extend(load_tests(os.path.join(basic_test_folder, file)))

prop_types = ['BT', 'FC', 'GAC']
var_ord_types = [ord_random, ord_mrv, ord_dh]
val_ord_types = [val_arbitrary, val_decrease_lcv, val_decreasing_order, val_increasing_order, val_lcv]


def basic_test_model1(filename, max_workers):
    futures = []
    model = battleship_csp_model1
    var_ord_type = ord_random  # was originally default_var_ord_type
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for test in tests:
            for prop_type in prop_types:
                for val_ord_type in val_ord_types:
                    futures.append(
                        executor.submit(_run, model, test, battleship_BT, prop_type, var_ord_type, val_ord_type))
    wait(futures)
    _save_result_to_file(filename, futures)


def basic_test_model23(filename, max_workers):
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for test in tests:
            for model in [battleship_csp_model2, battleship_csp_model3]:
                for prop_type in prop_types:
                    for var_ord_type in var_ord_types:
                        for val_ord_type in val_ord_types:
                            futures.append(
                                executor.submit(_run, model, test, BT, prop_type, var_ord_type, val_ord_type))
    wait(futures)
    _save_result_to_file(filename, futures)


def _save_result_to_file(filename, futures):
    with open(os.path.join(results_folder, filename), 'w') as f:
        f.write(HEADER)
        for future in futures:
            f.write(future.result())


def _run(model, test, bt_type, prop_type, var_ord_type, val_ord_type):
    # prepare a test
    board_size = test.board_size
    target_size = sum(test.row_targets)
    row_targets = test.row_targets
    col_targets = test.col_targets
    ships = test.ships

    # start timing
    start_time = time.time()

    # run the test
    battleship_csp, variable_array = model(row_targets, col_targets, ships)
    solver = bt_type(battleship_csp)
    if prop_type == 'BT':
        solver.bt_search(prop_BT, var_ord_type, val_ord_type)
    elif prop_type == 'FC':
        solver.bt_search(prop_FC, var_ord_type, val_ord_type)
    elif prop_type == 'GAC':
        solver.bt_search(prop_GAC, var_ord_type, val_ord_type)

    # end timing
    run_time = time.time() - start_time

    # model,board size,target size,propagation type,variable ordering type,value ordering type,runtime,assignment,pruning
    return '{model},{board_size},{target_size},{propagation_type},{variable_ordering_type},{value_ordering_type},{runtime},{assignment},{pruning}\n'.format(
        model=model.__name__, board_size=board_size, target_size=target_size, propagation_type=prop_type,
        variable_ordering_type=var_ord_type.__name__, value_ordering_type=val_ord_type.__name__, runtime=run_time,
        assignment=solver.nDecisions, pruning=solver.nPrunings)


if __name__ == '__main__':
    basic_test_model1('basic_test_model1.csv', 24)
    # basic_test_model23('basic_test_model23.csv', 48)
