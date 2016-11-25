  
'''
Construct and return battleship CSP models.
'''
from cspbase import *
import itertools

'''
   a function to check whether the variables assignment in a line(col or row)
   satisfies the number of targets specified for that line.
   @param t : the tuple to check
   @param num_of_tar: the number of targets for the line
   @return : True when the number of targets is met, False otherwise
'''
def lineConstraint(t, num_of_tar):
  sum = 0
  for i in range(len(t)):
    sum += t[i]
  return (sum == num_of_tar)


'''
   a function to check whether the variables assignment in the board
   satisfies the number of ships of a certain size specified.
   @param t : the tuple to check
   @param max_ship_size: the max size of the ships in this map
   @param ships: a list of number of ships of each ship_size 
   @return : True when the number of ships of each size is met, False otherwise
'''
def shipNumConstraint(t, max_ship_size, ships):
  count_ship = []
  # initialize count_ship array to all 0
  for l in range(0, max_ship_size +1):
    count_ship.append(0);
  # count ships of all length
  for i in range(len(t)):
    for j in range(1, max_ship_size + 1):
      if t[i] == j:
        count_ship[j] += 1
  return (count_ship == ships)


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


'''
   a function to check whether the variables assignment in the board
   satisfies the ship of a certain length is intact, 
   namely the ship should occupying contiguous ship_size number of grids.
   @param t : the tuple to check
   @param h: board height
   @param w: board width
   @param max_ship: the largest ship size
   @return : True when ships of all length are intact, False otherwise
'''
def shipIntactConstraint(t, h, w, max_ship):
  for l in range(2, max_ship + 1):
    for i in range(h):
      for j in range(w):
        if t[index(w,i,j)] == l:
          count_row = 1
          count_col = 1
          for a in range(1,l):
            if t[index(w,i,j+a)] == l:
              count_row += 1
            if t[index(w,i+a,j)] == l:
              count_col += 1
          if not (count_row == l or count_col == l):
            return False
  return True

def battleship_csp_model(row_targets, col_targets, num_of_targets, ships):
    '''Return a CSP object representing a battleship CSP problem along 
       with an array of variables for the problem. That is return

       battleship_csp, variable_array

       where battleship_csp is a csp representing battleship puzzle
       and variable_array is a list of lists
       '''

# Get board width w, height h
    w = len(row_targets)
    h = len(col_targets)

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
        if lineConstraint(t, row_targets[i]):
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
        if lineConstraint(t, col_targets[j]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con) 

    #shipNum constraint
    sat_tuples = []
    domains = []
    for k in range(0, w + h):
      domains.append(vs[l].domain())
    con = Constraint('C(shipNum)', vs)
    for t in itertools.product(*domains):
      if shipNumConstraint(t, max_ship, ships):
        sat_tuples.append(t)
    con.add_satisfying_tuples(sat_tuples)
    cons.append(con)

    #shipIntact constraint
    sat_tuples = []
    domains = []
    for k in range(0, w + h):
      domains.append(vs[l].domain())
    con = Constraint('C(shipIntact)', vs)
    for t in itertools.product(*domains):
      if shipIntactConstraint(t, h, w, max_ship):
        sat_tuples.append(t)
    con.add_satisfying_tuples(sat_tuples)
    cons.append(con)

# Create and return battleship_csp
    battleship_csp = CSP('battleship', vs)
    for c in cons:
        battleship_csp.add_constraint(c)
    return battleship_csp, variable_array

