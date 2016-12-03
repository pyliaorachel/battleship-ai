from .cspbase import BT
from copy import deepcopy
import time
import math

'''
This file will contain a subclass of BT search which is customized for 
battleship problem.

bt_search is basically the same as general bt_search in cspbase with 
some additional initializations.

bt_recurse is a lot different. 
    1. Instead of assigning to one variable at a time, we assign MULTIPLE variables, i.e. assigning a ship at a time. 
        This makes sure that no variable assignments will have ships overlapping with each other, since we will trace which cells have already been assigned values when assigning the next ship.

    2. The number of ships of different sizes assigned are tracked, so we guarantee that any final assignment will have the correct number of ships of various sizes.

    Hence we can savely get rid of the constraints checking valid ship placements & correct number of ships, which saves a lot of space and time.
'''

class battleship_BT(BT):

    def bt_search(self,propagator,var_ord,val_ord):

        self.clear_stats()
        stime = time.process_time()

        self.restore_all_variable_domains()
        
        self.unasgn_vars = []
        for v in self.csp.vars:
            if not v.is_assigned():
                self.unasgn_vars.append(v)

        for i in range(self.csp.h):
            self.csp.alloc_board.append([0] * self.csp.w)
        self.csp.updated_ships = deepcopy(self.csp.ships)

        status, prunings = propagator(self.csp) #initial propagate no assigned variables.
        self.nPrunings = self.nPrunings + len(prunings)

        if self.TRACE:
            print(len(self.unasgn_vars), " unassigned variables at start of search")
            print("Root Prunings: ", prunings)

        if status == False:
            print("CSP{} detected contradiction at root".format(
                self.csp.name))
        else:
            status = self.bt_recurse(propagator, var_ord,val_ord, 1, 0, 0)   #now do recursive search


        self.restoreValues(prunings)
        if status == False:
            print("CSP{} unsolved. Has no solutions".format(self.csp.name))
        if status == True:
            print("CSP {} solved. CPU Time used = {}".format(self.csp.name,
                                                             time.process_time() - stime))
            self.csp.print_soln()

        print("bt_search finished")
        self.print_stats()

    def bt_recurse(self, propagator, var_ord, val_ord, level, row, col):

        vars = self.csp.get_all_vars()
        updated_ships = self.csp.updated_ships
        alloc_board = self.csp.alloc_board

        if self.TRACE:
            print('  ' * level, "bt_recurse level ", level, " (%d,%d)" % (row, col))
            
            for i in range(self.csp.h):
                for j in range(self.csp.w):
                    print('{:<6}'.format(str(alloc_board[i][j])), end="")
                print("")

        if not self.unasgn_vars:
            #all variables assigned
            return True
        elif alloc_board[row][col] != 0:
            #current variable assigned, try next variable
            new_row = row + math.floor((col + 1) / self.csp.w)
            new_col = (col + 1) % self.csp.w
            if self.bt_recurse(propagator, var_ord,val_ord, level, new_row, new_col):
                return True            
        else:
            ##Assign ship from large small sizes, from top-left to bottom-right
            ##Then remove all ship cells from the list of unassigned vars

            # head of ship to assign
            var = vars[row * self.csp.w + col]
            self.unasgn_vars.remove(var) 

            if self.TRACE:
                print('  ' * level, "bt_recurse var = ", var)

            # length of ship to assign
            value_order = val_ord(self.csp,var)
            for ship_length in value_order:
                if ship_length == 0:
                    # don't assign ship if ship_length is 0; assign 0
                    alloc_board[row][col] = (0, 0)
                    var.assign(ship_length)

                    if self.TRACE:
                        print('  ' * level, "bt_recurse trying", var, "=", ship_length)

                    self.nDecisions = self.nDecisions+1

                    status, prunings = propagator(self.csp, var)
                    self.nPrunings = self.nPrunings + len(prunings)

                    if self.TRACE:
                        print('  ' * level, "bt_recurse prop status = ", status)
                        print('  ' * level, "bt_recurse prop pruned = ", prunings)

                    if status:
                        new_row = row + math.floor((col + 1) / self.csp.w)
                        new_col = (col + 1) % self.csp.w
                        if self.bt_recurse(propagator, var_ord,val_ord, level+1, new_row, new_col):
                            return True

                    if self.TRACE:
                        print('  ' * level, "bt_recurse restoring ", prunings)
                    
                    # restore prunings & assigned values
                    self.restoreValues(prunings)

                    alloc_board[row][col] = 0
                    var.unassign()   

                elif updated_ships[ship_length] != 0:
                    # assign ship towards the right

                    # check if ship won't occupy already allocated cell
                    cnt = 1 # count the cell itself
                    if col+ship_length <= self.csp.w:
                        for j in range(col+1,col+ship_length):
                            if (alloc_board[row][j] == 0) and (ship_length in vars[row * self.csp.w + j].cur_domain()):
                                cnt += 1
                            else:
                                break

                    if cnt == ship_length:
                        # pass check, assign values
                        assgn_vars = []
                        
                        alloc_board[row][col] = (ship_length, updated_ships[ship_length])
                        var.assign(ship_length)
                        assgn_vars.append(var)

                        for j in range(col+1,col+ship_length):
                            assgn_var = vars[row * self.csp.w + j]
                            self.unasgn_vars.remove(assgn_var)
                            alloc_board[row][j] = (ship_length, updated_ships[ship_length])
                            assgn_var.assign(ship_length)
                            assgn_vars.append(assgn_var)

                        updated_ships[ship_length] -= 1
                        
                        if self.TRACE:
                            print('  ' * level, "bt_recurse trying", var, "=", ship_length, "to the right")

                        self.nDecisions = self.nDecisions+ship_length

                        status = True
                        prunings = []
                        for assgn_var in assgn_vars:
                            temp_status, temp_prunings = propagator(self.csp, assgn_var)
                            prunings = list(set(prunings) | set(temp_prunings))
                            if not temp_status:
                                status = False
                                break

                        self.nPrunings = self.nPrunings + len(prunings)

                        if self.TRACE:
                            print('  ' * level, "bt_recurse prop status = ", status)
                            print('  ' * level, "bt_recurse prop pruned = ", prunings)

                        if status:
                            new_row = row + math.floor((col + ship_length) / self.csp.w)
                            new_col = (col + ship_length) % self.csp.w
                            if self.bt_recurse(propagator, var_ord,val_ord, level+1, new_row, new_col):
                                return True

                        if self.TRACE:
                            print('  ' * level, "bt_recurse restoring ", prunings)
                        
                        # restore prunings & assigned values
                        self.restoreValues(prunings)

                        alloc_board[row][col] = 0
                        var.unassign()
                        for j in range(col+1,col+ship_length):
                            assgn_var = vars[row * self.csp.w + j]
                            assgn_var.unassign()
                            self.restoreUnasgnVar(assgn_var)
                            alloc_board[row][j] = 0

                        updated_ships[ship_length] += 1

                    # assign ship towards the bottom, only if ship_length > 1

                    if ship_length > 1:
                        # check if ship won't occupy already allocated cell
                        cnt = 1 # count the cell itself
                        if row+ship_length <= self.csp.h:
                            for i in range(row+1,row+ship_length):
                                if (alloc_board[i][col] == 0) and (ship_length in vars[i * self.csp.w + col].cur_domain()):
                                    cnt += 1
                                else:
                                    break

                        if cnt == ship_length:
                            # pass check, assign values
                            assgn_vars = []

                            alloc_board[row][col] = (ship_length, updated_ships[ship_length])
                            var.assign(ship_length)
                            assgn_vars.append(var)

                            for i in range(row+1,row+ship_length):
                                assgn_var = vars[i * self.csp.w + col]
                                self.unasgn_vars.remove(assgn_var)
                                alloc_board[i][col] = (ship_length, updated_ships[ship_length])
                                assgn_var.assign(ship_length)
                                assgn_vars.append(assgn_var)

                            updated_ships[ship_length] -= 1
                            
                            if self.TRACE:
                                print('  ' * level, "bt_recurse trying", var, "=", ship_length, "to the bottom")

                            self.nDecisions = self.nDecisions+ship_length

                            status = True
                            prunings = []
                            for assgn_var in assgn_vars:
                                temp_status, temp_prunings = propagator(self.csp, assgn_var)
                                prunings = prunings + temp_prunings
                                if not temp_status:
                                    status = False
                                    break

                            self.nPrunings = self.nPrunings + len(prunings)

                            if self.TRACE:
                                print('  ' * level, "bt_recurse prop status = ", status)
                                print('  ' * level, "bt_recurse prop pruned = ", prunings)

                            if status:
                                new_row = row + math.floor((col + 1) / self.csp.w)
                                new_col = (col + 1) % self.csp.w
                                if self.bt_recurse(propagator, var_ord,val_ord, level+1, new_row, new_col):
                                    return True

                            if self.TRACE:
                                print('  ' * level, "bt_recurse restoring ", prunings)
                            
                            # restore prunings & assigned values
                            self.restoreValues(prunings)

                            alloc_board[row][col] = 0
                            var.unassign()
                            for i in range(row+1,row+ship_length):
                                assgn_var = vars[i * self.csp.w + col]
                                assgn_var.unassign()
                                self.restoreUnasgnVar(assgn_var)
                                alloc_board[i][col] = 0

                            updated_ships[ship_length] += 1

            self.restoreUnasgnVar(var)
            return False

