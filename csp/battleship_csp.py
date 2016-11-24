  
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
   @param ship_size: the size of the ship for this constraint
   @param num_of_ship: the number of ships of ship_size
   @return : True when the number of targets is met, False otherwise
'''
def shipConstraint(t, ship_size, num_of_ship):
  sum = 0
  for i in range(len(t)):
    if t[i] == ship_size:
      sum += 1
  return (sum == num_of_ship)


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
    for i in range(n):
      for j in range(n):
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

    #ship constraint
    for l in range(1, max_ship + 1):
      sat_tuples = []
      domains = []
      for k in range(0, w + h):
        domains.append(vs[l].domain())
      con = Constraint('C(ship{})'.format(l), vs)
      for t in itertools.product(*domains):
        if shipConstraint(t, l, ships[l]):
          sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
      cons.append(con)

# Create and return battleship_csp
    battleship_csp = CSP('battleship', vs)
    for c in cons:
        battleship_csp.add_constraint(c)
    return battleship_csp, variable_array

