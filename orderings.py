#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
import functools

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.  var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var

def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()

def val_increasing_order(csp,var):
    '''
    val_increasing_ordery(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain in increasing order.
    '''
    return sorted(var.cur_domain())

def val_decreasing_order(csp,var):
    '''
    val_decreasing_ordery(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain in decreasing order.
    '''
    return sorted(var.cur_domain(), reverse=True)

def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var, 
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.  
    MRV returns the variable with the most constrained current domain 
    (i.e., the variable with the fewest legal values).
    '''

    min_ = 9999999
    min_var = None
    vars = csp.get_all_unasgn_vars()
    for var in vars:
        if var.cur_domain_size() < min_:
            min_ = var.cur_domain_size()
            min_var = var
    return min_var


def ord_dh(csp):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node, 
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''    

    vars = csp.get_all_unasgn_vars()
    max_ = -1
    max_var = None

    for var in vars:
        cons = csp.get_cons_with_var(var)
        unasgn_vars = set()
        for con in cons:
            unasgn_vars = unasgn_vars.union(set(con.get_unasgn_vars()))
        if (len(unasgn_vars) > max_):
            max_ = len(unasgn_vars)
            max_var = var
    return max_var


def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the 
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index, 
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.) 
    The best value, according to LCV, is the one that rules out the fewest domain values in other 
    variables that share at least one constraint with var.
    '''    

    cons = csp.get_cons_with_var(var)
    val_count = {}
    var_domain = var.cur_domain()
    for val in var_domain:
        val_count[val] = 0
        var.assign(val)    
        for con in cons:
            scope = con.get_scope()
            for affected_var in scope:
                if not affected_var.is_assigned():
                    domain = affected_var.cur_domain()
                    for potential_val in domain:
                        if not con.has_support(affected_var, potential_val):
                            val_count[val] = val_count[val] + 1
        var.unassign()
    l = sorted(val_count.keys(), key=lambda x: val_count[x])
    return l

def val_decrease_lcv(csp,var):
    '''
    val_decrease_lcv(csp,var):
    Same as val_lcv, break tie with decreasing order of values
    '''    

    cons = csp.get_cons_with_var(var)
    val_count = {}
    var_domain = var.cur_domain()
    for val in var_domain:
        val_count[val] = 0
        var.assign(val)    
        for con in cons:
            scope = con.get_scope()
            for affected_var in scope:
                if not affected_var.is_assigned():
                    domain = affected_var.cur_domain()
                    for potential_val in domain:
                        if not con.has_support(affected_var, potential_val):
                            val_count[val] = val_count[val] + 1
        var.unassign()

    if type(var_domain[0]) == tuple:
        l = sorted(val_count.keys(), key=functools.cmp_to_key(lambda a,b: (b[0] - a[0]) if (val_count[a] == val_count[b]) else (val_count[a] - val_count[b])))
    else:
        l = sorted(val_count.keys(), key=functools.cmp_to_key(lambda a,b: (b - a) if (val_count[a] == val_count[b]) else (val_count[a] - val_count[b])))
    
    return l











