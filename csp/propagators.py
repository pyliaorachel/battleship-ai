'''
This file will contain different constraint propagators to be used within
bt_search.

propagator == a function with the following template
    propagator(csp, newly_instantiated_variable=None)
        ==> returns (True/False, [(Variable, Value), (Variable, Value) ...])

Consider implementing propagators for forward cehcking or GAC as a course project!        

'''
from collections import deque

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):

    def FC_check(c, check_var):
        vals = []
        vars = c.get_scope()
        for i in range(len(vars)):
            var = vars[i]
            if var != check_var:
                vals.append(var.get_assigned_value())
            else:
                check_varIdx = i
                vals.append(-1)

        domain = check_var.cur_domain()
        prunings = []
        for val in domain:
            vals[check_varIdx] = val
            if not c.check(vals):
                prunings.append((check_var,val))
                check_var.prune_value(val)
        
        if len(prunings) == len(domain):
            # DWO
            return False, prunings
        else:
            # no DWO, prune values
            return True, prunings

    '''main FC'''
    if not newVar:
        return True, []
    all_prunings = []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
        elif c.get_n_unasgn() == 1:
            unasgn_var = (set(c.get_scope()) - set([newVar])).pop()

            FC_check_ok,prunings = FC_check(c, unasgn_var)
            all_prunings = all_prunings + prunings
            if not FC_check_ok:
                return False, all_prunings
    return True, all_prunings

def prop_GAC(csp, newVar=None):

    def GAC_enforce(GAC_q):
        prunings = []
        while GAC_q:
            c = GAC_q.popleft()

            vars = c.get_scope()
            for var in vars:
                domain = var.cur_domain()
                for val in domain:
                    if not c.has_support(var, val):
                        prunings.append((var, val))
                        var.prune_value(val)
                        if var.cur_domain_size() == 0:
                            # DWO
                            GAC_q.clear()
                            return False, prunings
                        else:
                            cons = csp.get_cons_with_var(var)
                            for c in cons:
                                if GAC_q.count(c) == 0:
                                    GAC_q.append(c)
        # no DWO, prune values
        return True, prunings

    '''main GAC'''
    if not newVar:
        return True, []

    GAC_q = deque()
    cons = csp.get_cons_with_var(newVar)
    for c in cons:
        GAC_q.append(c)

    GAC_ok,prunings = GAC_enforce(GAC_q)

    if not GAC_ok:
        return False, prunings
    return True, prunings



















