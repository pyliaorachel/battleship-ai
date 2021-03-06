
'''
Construct and return battleship CSP models.
'''
from cspbase import *
import itertools
import re
from copy import deepcopy

#==================================================================
#================ Helper Functions ================================
#==================================================================

'''
   a function to map the index(i,j) from a 2D board
   to k in 1D list given the width w of the board
   @param w: board width
   @param i: row index in 2D board
   @param j: col index in 2D board
   @return : index in 1D list
'''
def index(w,i,j):
  return (i * w + j)

#==================================================================
#================ CSP model 1 =====================================
#==================================================================

'''
   a function to check whether the variables assignment in a line(col or row)
   satisfies the number of targets specified for that line.
   @param t : the tuple to check
   @param num_of_tar: the number of targets for the line
   @return : True when the number of targets is met, False otherwise
'''
def line_cons_model1(t, num_of_tar):
  sum = 0
  for i in range(len(t)):
    if t[i] > 0:
      sum += 1
  return (sum == num_of_tar)

def battleship_csp_model1(row_targets, col_targets, ships):
    '''Return a CSP object representing a battleship CSP problem along 
       with an array of variables for the problem. That is return

       battleship_csp, variable_array

       where battleship_csp is a csp representing battleship puzzle
       and variable_array is a list of lists

       Variable domain:
          possible ship_size or sea(represented as 0)

       Constraints:
          1. number of ships matching with row_targets for each row
          2. number of ships matching with col_targets for each column
    '''

# Get board width w, height h
    h = len(row_targets)
    w = len(col_targets)

# Get length of largest ship max_ship
    max_ship = len(ships) - 1

# Initialize variable_array with general domain 
    variable_array = []
    for i in range(h):
      row = []
      for j in range(w):
        dom = []
        for v in range(max_ship + 1):
          dom.append(v)
        var = Variable('({},{})'.format(i,j), dom)
        row.append(var)
      variable_array.append(row)

# Initialize variable list
    vs = []
    for i in range(h):
      for j in range(w):
        vs.append(variable_array[i][j])

# Initialize constraints
    cons = [] 

    # row constraint
    for i in range(h):
      con = Constraint('C(row{})'.format(i), variable_array[i])
      sat_tuples = []
      domains = []
      for var in variable_array[i]:
        domains.append(var.domain())
      for t in itertools.product(*domains):
        if line_cons_model1(t, row_targets[i]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)  

    # col constraint
    for j in range(w):
      col = []
      sat_tuples = []
      domains = []
      for i in range(h):
        col.append(variable_array[i][j])
        domains.append(variable_array[i][j].domain())
      con = Constraint('C(col{})'.format(j), col)
      for t in itertools.product(*domains):
        if line_cons_model1(t, col_targets[j]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con) 

# Create and return battleship_csp
    battleship_csp = battleship_csp_model('battleship', vs, row_targets, col_targets, ships, 1)
    for c in cons:
        battleship_csp.add_constraint(c)
    return battleship_csp, variable_array


#==================================================================
#================ CSP model 2 =====================================
#==================================================================

'''
   a function to check whether the variables assignment in a line(col or row)
   satisfies the number of targets specified for that line.
   @param t : the tuple to check
   @param num_of_tar: the number of targets for the line
   @return : True when the number of targets is met, False otherwise
'''
def line_cons_model2(t, num_of_tar):
  sum = 0
  for i in range(len(t)):
    if t[i][0] > 0:
      sum += 1
  return (sum == num_of_tar)

'''
   a function to check whether the variables assignment in the board
   satisfies the number of ships of a certain size specified.
   @param t : the tuple to check
   @param max_ship_size: the max size of the ships in this map
   @param ships: a list of number of ships of each ship_size 
   @return : True when the number of ships of each size is met, False otherwise
'''
def ship_num_cons(t, max_ship_size, ships):
  ships_t = [0] * (max_ship_size + 1)
  for l in range(1, max_ship_size + 1):
    ships_t[l] = ships[l] * l
  # initialize count_ship lists to all 0
  total_count_ship = [0] * (max_ship_size + 1)
  num_count_ship = []
  for l in range(0, max_ship_size + 1):
    num_count_ship.append([0] * (ships[l]))
  # count total ships of all length
  for i in range(0,len(t)):
    total_count_ship[t[i][0]] += 1
    if(t[i][0] > 0):
      num_count_ship[t[i][0]][t[i][1]] += 1
  # 0 is dummy
  total_count_ship[0] = 0
  if total_count_ship != ships_t:
    return False
  # check the numbered ship match length 
  for l in range(1, max_ship_size + 1):
    if num_count_ship[l] != [l] * (ships[l]):
      return False 
  return True


'''
   a function to check 
   whether the variables assignment in the board satisfies the ship of a certain length is intact, 
   namely the ship should occupy contiguous ship_size number of grids
   @param t : the tuple to check
   @param h: board height
   @param w: board width
   @return : True when ships of all length are intact, False otherwise
'''
def ship_intact_cons(t, h, w): 
  #print("intact cons") 
  for i in range(h):
    for j in range(w):
      l = t[index(w,i,j)][0]
      n = t[index(w,i,j)][1]
      if l > 1:
        count_row = 0  # count in row
        count_col = 0  # count in col
        inrow = 1
        incol = 1
        for a in range(-l+1,l): # scan the neighbors within size range in line
          if index(w,i,j+a) >= 0 and index(w,i,j+a) < min((i+1)*w,(w*h)):
            if t[index(w,i,j+a)][0] == l and t[index(w,i,j+a)][1] == n:
              count_row += 1
            else:
              if count_row > 0 and count_row < l:
                inrow = 0 # row broken
          if index(w,i+a,j) >= 0 and index(w,i+a,j) < (w*h) and (index(w,i+a,j)%w == index(w,i,j)%w) :
            if t[index(w,i+a,j)][0] == l and t[index(w,i+a,j)][1] == n:
              count_col += 1
            else:
              if count_col > 0 and count_col < l:
                incol = 0 # col broken
        if inrow == 0 and incol == 0:
          #print("broken")
          return False
        if count_row != l and count_col != l:
          #print("no match")
          return False
        if count_row == l and count_col == l:
          #print("cross")
          return False
  return True


def battleship_csp_model2(row_targets, col_targets, ships):

    '''Return a CSP object representing a battleship CSP problem along 
       with an array of variables for the problem. That is return
       
       battleship_csp, variable_array
       
       where battleship_csp is a csp representing battleship puzzle
       and variable_array is a list of lists

      Variable domain:
          tuples in the format of (ship_size, ship_number)
          ship_size is the possible ship_size for this cell or sea as 0 
          ship_number is the number for the ship
          each ship of size l will be given a number from 0 to ships[l]-1 to identify as different ship

      Constraints:
          1. number of ships matching with row_targets for each row
          2. number of ships matching with col_targets for each column
          3. number of ships matching the given ship number & is valid (i.e. no overlapping, misplacement, etc.)
    '''

# Get board width w, height h
    h = len(row_targets)
    w = len(col_targets)

# Get length of largest ship max_ship
    max_ship = len(ships) - 1

# Initialize variable_array with general domain, domain value is in the format of: (ship_size, number) 
    dom = []
    dom.append((0,0))
    for v in range(max_ship + 1):
      for n in range(ships[v]):
        dom.append((v,n))

    variable_array = []
    for i in range(h):
      row = []
      for j in range(w):
        var = Variable('({},{})'.format(i,j), dom)
        row.append(var)
      variable_array.append(row)

# Initialize variable list
    '''
    vs = []
    for i in range(h):  # row
      for j in range(w):  # scan row
        vs.append(variable_array[i][j])
    '''
    vs = [i for row in variable_array for i in row]

# Initialize constraints
    cons = [] 

# row constraint
    for i in range(h):
      con = Constraint('C(row{})'.format(i), variable_array[i])
      sat_tuples = []
      '''
      domains = []
      for var in variable_array[i]:
        domains.append(var.domain())
			'''
      domains = [var.domain() for domain in variable_array[i]]
			
      for t in itertools.product(*domains):
        if line_cons_model2(t, row_targets[i]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)  

# col constraint
    for j in range(w):
      col = []
      sat_tuples = []
      '''
      domains = []
      for i in range(h):
        col.append(variable_array[i][j])
        domains.append(variable_array[i][j].domain())
      '''
      for i in range(h):
        col.append(variable_array[i][j])
      domains = [var.domain() for var in col]

      con = Constraint('C(col{})'.format(j), col)
      for t in itertools.product(*domains):
        if line_cons_model2(t, col_targets[j]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con) 

# ship constraint
    sat_tuples = []
    domains = []
    for k in range(0, w * h):
      domains.append(vs[k].domain())
    con = Constraint('C(ship)', vs)
    #n = 0
    for t in itertools.product(*domains):
      #print(n)
      #n += 1
      if (ship_num_cons(t, max_ship, ships) and ship_intact_cons(t, h, w)):
        sat_tuples.append(t)
    con.add_satisfying_tuples(sat_tuples)
    cons.append(con)

# Create and return battleship_csp
    battleship_csp = battleship_csp_model('battleship', vs, row_targets, col_targets, ships, 2)
    for c in cons:
        battleship_csp.add_constraint(c)
    return battleship_csp, variable_array

#==================================================================
#================ CSP model 3 =====================================
#==================================================================

'''
   a function to count the grids occupied by variables (ships) in a line(col or row),
   if the ship direction is in the major direction we check.
   @param t : the tuple to check
   @return : Number of grids occupied by variables (ships)
'''
def line_count_multi(t):
  sum = 0
  for i in range(len(t)):
    sum += t[i]
  return sum 

'''
   a function to count the grids occupied by variables (ships) in a line(col or row),
   if the ship direction is not in the major direction we check.
   @param t : the tuple to check
   @return : Number of grids occupied by variables (ships)
'''
def line_count_single(t):
  sum = 0
  for i in range(len(t)):
    sum += (t[i] != 0)
  return sum

'''
   a function to count the total number of variables (ships) of a certain length.
   @param t : the tuple to check
   @param ship : the number of variables (ships) to match
   @return : True if matched, False otherwise
'''
def single_ship_num_cons(t, ship):
  cnt = 0
  for l in t:
    if l != 0:
      cnt += 1
  return (ship == cnt)

'''
   a function to check if multiple variables (ships) are occupying the same grid.
   At most 1 variable can have non-zero value assigned.
   @param t : the tuple to check
   @return : True if not overlapping, False otherwise
'''
def cell_overlap_cons(t):
  num_of_vars = len(t)
  return (t.count(0) >= (num_of_vars-1))

def battleship_csp_model3(row_targets, col_targets, ships):

    '''Return a CSP object representing a battleship CSP problem along 
       with an array of variables for the problem. That is return
       
       battleship_csp, variable_array
       
       where battleship_csp is a csp representing battleship puzzle
       and variable_array is a list of lists

      Variable domain:
          1 ship_size or sea(represented as 0)

      Constraints:
          1. number of ships matching with row_targets for each row
          2. number of ships matching with col_targets for each column
          3. number of ships matching the given ship number
          4. ships occupying a certain cell not overlapping (i.e. at most 1 variable has non-zero assigned value)
    '''

# Get board width w, height h
    h = len(row_targets)
    w = len(col_targets)

# Get length of largest ship max_ship
    max_ship = len(ships) - 1

# Initialize variable_ship_l_array to put variables concerning different ship lengths
    variable_ship_l_array = [[] for i in range(len(ships))]

# Create variables touching each cell
    cell_array = [[[] for j in range(w)] for i in range(h)]

# Create variables in each row for each ship size: (x,y,ship_length,0), 0 for ships heading right 
    variable_row_array = []
    col_in_row = [[] for j in range(w)]
    for i in range(h):
      row = []
      for ship_length in range(1, max_ship + 1):
        dom = [0, ship_length]
        ship_length_group = []
        for j in range((w - ship_length + 1)):
          var = Variable('({},{},{},0)'.format(i,j,ship_length), dom)
          ship_length_group.append(var)
          row.append(var)
          # also keep in col_in_row & cell_array
          for k in range(j, j+ship_length):
            col_in_row[k] = col_in_row[k] + [var]
            cell_array[i][k] = cell_array[i][k] + [var]
        variable_ship_l_array[ship_length] = variable_ship_l_array[ship_length] + ship_length_group
      variable_row_array.append(row)

# Create variables in each column for each ship size: (x,y,ship_length,1), 1 for ships heading down
    variable_col_array = []
    row_in_col = [[] for i in range(h)]
    for j in range(w):
      col = []
      for ship_length in range(2, max_ship + 1): # start from 2 to avoid redundant variable of ship length 1
        dom = [0, ship_length]
        ship_length_group = []
        for i in range((h - ship_length + 1)):
          var = Variable('({},{},{},1)'.format(i,j,ship_length), dom)
          ship_length_group.append(var)
          col.append(var)
          # also keep in row_in_col & cell_array
          for k in range(i, i+ship_length):
            row_in_col[k] = row_in_col[k] + [var]
            cell_array[k][j] = cell_array[k][j] + [var]
        variable_ship_l_array[ship_length] = variable_ship_l_array[ship_length] + ship_length_group
      variable_col_array.append(col)

# Initialize variable list
    vs = [var for row in variable_row_array for var in row]
    vs = vs + [var for col in variable_col_array for var in col]

# Initialize constraints
    cons = [] 

# row constraint: row number has to match
    for i in range(h):
      # gather all row variables
      row_vars = variable_row_array[i] + row_in_col[i]

      domains_row = [var.domain() for var in variable_row_array[i]]
      domains_col = [var.domain() for var in row_in_col[i]]

      con = Constraint('C(row{})'.format(i), row_vars)
      sat_tuples = []

      for t1 in itertools.product(*domains_row):
        for t2 in itertools.product(*domains_col):
          if (line_count_multi(t1) + line_count_single(t2)) == row_targets[i]:
            sat_tuples.append(t1 + t2)

      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)  

# col constraint: col number has to match
    for j in range(w):
      # gather all col variables
      col_vars = variable_col_array[j] + col_in_row[j]

      domains_col = [var.domain() for var in variable_col_array[j]]
      domains_row = [var.domain() for var in col_in_row[j]]

      con = Constraint('C(col{})'.format(j), col_vars)
      sat_tuples = []

      domains = [var.domain() for var in col_vars]

      for t1 in itertools.product(*domains_col):
        for t2 in itertools.product(*domains_row):        
          if (line_count_multi(t1) + line_count_single(t2)) == col_targets[j]:
            sat_tuples.append(t1 + t2)

      con.add_satisfying_tuples(sat_tuples)
      cons.append(con) 

# ship constraint: ship number has to match
    for ship_length in range(1, max_ship + 1):
      ship_l_vars = variable_ship_l_array[ship_length]
      con = Constraint('C(ship_length {})'.format(ship_length), ship_l_vars)
      sat_tuples = []

      domains = [var.domain() for var in ship_l_vars]      

      for t in itertools.product(*domains):
        if single_ship_num_cons(t, ships[ship_length]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con)

# cell constraint: cannot have multiple assignments in a single cell
    for i in range(h):
      for j in range(w):
        cell_vars = cell_array[i][j]
        
        cnt = 0
        iter_l = [list(range(len(cell_vars))), list(range(len(cell_vars)))]
        for pair in itertools.product(*iter_l):
          if pair[0] != pair[1]:
            cell_vars_pair = [cell_vars[pair[0]], cell_vars[pair[1]]]
            con = Constraint('C(cell ({},{})-{}th pair)'.format(i,j,cnt), cell_vars_pair)
            cnt += 1
            sat_tuples = []

            domains = [var.domain() for var in cell_vars_pair]     

            for t in itertools.product(*domains):
              if cell_overlap_cons(t):
                sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)

# Create and return battleship_csp
    battleship_csp = battleship_csp_model('battleship', vs, row_targets, col_targets, ships, 3)
    for c in cons:
        battleship_csp.add_constraint(c)
    return battleship_csp, vs

#==================================================================
#================ General CSP model Wrapper =======================
#==================================================================

class battleship_csp_model(CSP):
  '''
  A wrapper class for battleship CSP model to address the issue that different models may have differnt domain structure for each variable.
  '''

  def __init__(self, name, vars=[], row_targets=[], col_targets=[], ships=[], model=1):
    CSP.__init__(self, name, vars)
    self.row_targets = row_targets
    self.col_targets = col_targets
    self.h = len(row_targets)
    self.w = len(col_targets)
    self.ships = ships
    self.model = model
    self.updated_ships = deepcopy(ships)
    self.alloc_board = []

  def get_sol_board(self):
    '''
    Format and return a 2D-list solution board with tuples at each entry in the form (ship_length, ship_id).
    '''

    if self.model == 1:
      return self.alloc_board

    elif self.model == 2:
      vars = self.get_all_vars()
      sol_board = []

      for i in range(self.h):
        row = []
        for j in range(self.w):
          row.append(vars[i * self.w + j].get_assigned_value())
        sol_board.append(row)
      return sol_board
    elif self.model == 3:
      id_cnt = [0 for i in range(len(self.ships))]
      vars = self.get_all_vars()
      sol_board = [[(0,0) for j in range(self.w)] for i in range(self.h)]

      for var in vars:
        if var.get_assigned_value() != 0:
          split_list = re.split('\(|,|\)', var.name)
          i = int(split_list[1])
          j = int(split_list[2])
          l = int(split_list[3])
          direction = int(split_list[4])
          if direction == 0: # right
            for k in range(j, j+l):
              sol_board[i][k] = (l, id_cnt[l])
            id_cnt[l] += 1
          elif direction == 1: # down
            for k in range(i, i+l):
              sol_board[k][j] = (l, id_cnt[l])
            id_cnt[l] += 1

      return sol_board
    else:
      return []












