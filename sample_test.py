from cspbase import *
from propagators import *
import orderings as orderings
from battleship_BT import *
import battleship_csp as models
import itertools
import traceback

'''
Tests for larger (4x4 up) board sizes.
'''

def test_sample_run(model, BT, propType, var_ord_type, val_ord_type, trace_model=False, trace_BT=False, name=""):
    try:

        '''
        0 0 2 2
        0 2 0 0
        0 2 0 1
        3 3 3 0
        '''

        row_targets = [2, 1, 2, 3]
        col_targets = [1, 3, 2, 2]
        ships = [0, 1, 2, 1]

        '''
        3 0 1 0
        3 1 0 0
        3 2 2 0
        4 4 4 4
        '''

        # row_targets = [2, 2, 3, 4]
        # col_targets = [4, 3, 3, 1]
        # ships = [0, 2, 1, 1, 1]

        '''
        0 0 0 0 2 0 0
        0 0 0 0 2 0 6
        4 4 4 4 0 0 6
        0 0 0 0 2 2 6
        0 0 0 1 0 0 6
        3 3 3 0 0 0 6
        0 0 2 2 0 0 6
        '''

        # row_targets = [1, 2, 5, 3, 2, 4, 3]
        # col_targets = [2, 2, 3, 3, 3, 1, 6]
        # ships = [0, 1, 3, 1, 1, 0, 1]

        '''
        1 2
        0 2
        '''

        # row_targets = [2, 1]
        # col_targets = [1, 2]
        # ships = [0, 1, 1]


        csp,vars = model(row_targets, col_targets, ships)

        if trace_model:
            print("variables: ")
            for var in vars:
                print(var, var.domain())

            print("****************************************")

            cons = csp.get_all_cons()
            print("constraints: ")
            for con in cons:
                print(con)
                print(con.sat_tuples)

        solver = BT(csp)

        if trace_BT:
            solver.trace_on()
        if propType == 'BT':
            solver.bt_search(prop_BT,var_ord_type,val_ord_type)
        elif propType == 'FC':
            solver.bt_search(prop_FC,var_ord_type,val_ord_type)
        elif propType == 'GAC':
            solver.bt_search(prop_GAC,var_ord_type,val_ord_type)

        print(csp.get_sol_board())

        details = "OK"

    except Exception:

        details = "One or more runtime errors occurred while trying a sample test run on %s: %r" % (name, traceback.format_exc())
    return details

trace_model = False
trace_BT = False

print("---model 1 sample test---\n")
print("---BT with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model1, battleship_BT, 'BT', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---BT with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model1, battleship_BT, 'BT', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---FC with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model1, battleship_BT, 'FC', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---FC with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model1, battleship_BT, 'FC', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---GAC with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model1, battleship_BT, 'GAC', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---GAC with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model1, battleship_BT, 'GAC', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---finished model 1 sample test---\n")


print("---model 2 sample test---\n")
print("---BT with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model2, BT, 'BT', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---BT with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model2, BT, 'BT', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---FC with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model2, BT, 'FC', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---FC with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model2, BT, 'FC', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---GAC with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model2, BT, 'GAC', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---GAC with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model2, BT, 'GAC', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---finished model 2 sample test---\n")

print("---model 3 sample test---\n")
print("---BT with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model3, BT, 'BT', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---BT with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model3, BT, 'BT', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---FC with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model3, BT, 'FC', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---FC with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model3, BT, 'FC', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---GAC with val_decrease_lcv---\n")
details = test_sample_run(models.battleship_csp_model3, BT, 'GAC', orderings.ord_random, orderings.val_decrease_lcv, trace_model, trace_BT)
print(details)
print("---GAC with val_decreasing_order---\n")
details = test_sample_run(models.battleship_csp_model3, BT, 'GAC', orderings.ord_random, orderings.val_decreasing_order, trace_model, trace_BT)
print(details)
print("---finished model 3 sample test---\n")

