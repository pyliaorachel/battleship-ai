  
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
def line_constraint(t, num_of_tar):
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
def ship_num_constraint(t, max_ship_size, ships):
  # initialize count_ship array to all 0
  count_ship = [0] * (max_ship_size + 1)
  
  # version_1
  # count ships of all length
  for i in range(len(t)):
    count_ship[t[i]] += 1
  # 0 is dummy
  count_ship[0] = 0
  # divide by ship size to get number of shipss
  for l in range(1, max_ship_size + 1):
    count_ship[l] /= l
  return (count_ship == ships)
'''
  # version_2
  # count ships of all length
  for l in range(1, max_ship_size + 1):
    for i in range(len(t)):
      if t[i] == l:
        count_ship[l] += 1
    count_ship[l] /= l
  return (count_ship == ships)
'''

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
   a function to check 
   whether the variables assignment in the board satisfies the ship of a certain length is intact, 
   namely the ship should occupying contiguous ship_size number of grids
   and 
   whether the variables assignment in the boardsatisfies that no ship cross any other ship
   @param t : the tuple to check
   @param h: board height
   @param w: board width
   @return : True when ships of all length are intact, False otherwise
'''
def ship_intact_noCross_constraint(t, h, w):
  # ship_intact
  may_cross = []
  pot = [] * len(t) 
  for i in range(h):
    for j in range(w):
      l = t[index(w,i,j)]
      if l > 1:
        row_potential_ship = [0] * (l)
        col_potential_ship = [0] * (l)
        for b in range(0,l):
          count_row = 0
          count_col = 0
          for a in range(-b,l-b):
            if index(w,i,j+a) >= 0 and index(w,i,j+a) < h*w:
              if t[index(w,i,j+a)] == l: 
                count_row += 1
            if index(w,i+a,j) >= 0 and index(w,i+a,j) < h*w:
              if t[index(w,i+a,j)] == l: 
                count_col += 1
          row_potential_ship[b] = 1 if count_row == l else 0
          col_potential_ship[b] = 1 if count_col == l else 0
        pot[index(w,i,j)] = [row_potential_ship, col_potential_ship]
        if row_potential_ship == [0]*(l) and col_potential_ship == [0]*(l):
          return False
        if row_potential_ship != [0]*(l) and col_potential_ship != [0]*(l):
          may_cross.append([i,j])

  # ship_noCross 
  # only check the grids with crossing potential     
  for grid in may_cross:
    i = grid[0]
    j = grid[1]
    l = t[index(w,i,j)]
      row_pot = pot[index(w,i,j)][0]
      col_pot = pot[index(w,i,j)][1]
      for a in range(0,l):
        for b in range(0,l):
          # check possible crossing situations based on potential ship placement
          if row_pot[a] == 1 and col_pot[b] == 1:
            # consider placing the ship in row
            # check if other ship could be placed horizontally
            inrow = 1 if (index(w,i,j+l) == l and pot[index(w,i,j+l)][1][b] > 0 or index(w,i,j-l) == l and pot[index(w,i,j-l)][1][b] > 0) else 0
            if inrow == 0:
              # check if other ships could be placed vertically
              inrow = 1
              for x in range(0,l):
                if pot[index(w,i,j+b-l+x+1)][0] != [0]*(l):
                  inrow = 0
                  break
            # consider placing the ship in col
            # check if other ship could be placed vertically
            incol = 1 if (index(w,i+l,j) == l and pot[index(w,i+l,j)][1][a] > 0 or index(w,i-l,j) == l and pot[index(w,i-l,j)][1][a] > 0) else 0
            if incol == 0:
              # check if other ships could be place horizontally
              incol = 1
              for y in range(0,l):
                if pot[index(w,i+a-l+y+1,j)][0] != [0]*(l):
                  incol = 0
                  break
      if inrow == 0 and incol == 0: 
      # cannot put ship in row or col without crossing, violate constraint
        return False
  return True

'''
  def ship_intact_constraint(t, h, w): 
  for i in range(h):
    for j in range(w):
      l = t[index(w,i,j)]
      if l > 1:
        row_potential_ship = [0] * (l)
        col_potential_ship = [0] * (l)
        for b in range(0,l):
          count_row = 0
          count_col = 0
          for a in range(-b,l-b):
            if index(w,i,j+a) >= 0 and index(w,i,j+a) < h*w:
              if t[index(w,i,j+a)] == l: 
                count_row += 1
            if index(w,i+a,j) >= 0 and index(w,i+a,j) < h*w:
              if t[index(w,i+a,j)] == l: 
                count_col += 1
          row_potential_ship[b] = 1 if count_row == l else 0
          col_potential_ship[b] = 1 if count_col == l else 0
        if row_potential_ship == [0]*(l) and col_potential_ship == [0]*(l):
          return False
  return True
'''


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
        if line_constraint(t, row_targets[i]):
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
        if line_constraint(t, col_targets[j]):
          sat_tuples.append(t)
      con.add_satisfying_tuples(sat_tuples)
      cons.append(con) 

    '''
      ship constraint is the constraint for ships which operates over all variables in the board, it includes three components:
      1. ship_num: the number of ships for each ship size (obtained by #grids with size / size) agrees with the given input list ships, i.e: number of ships is correct for each size
      2. ship_intact: each grid of value size should be able to form a ship of size with size-1 number of neighboring grids, i.e: each ship is intact
      3. ship_noCross: there should be no overlapping of ships, i.e: each ship should not cross with any other ship
    '''
    #ship constraint
    sat_tuples = []
    domains = []
    for k in range(0, w * h):
      domains.append(vs[l].domain())
    con = Constraint('C(ship)', vs)
    for t in itertools.product(*domains):
      if ship_num_constraint(t, max_ship, ships) and ship_intact_noCross_constraint(t, h, w):
        sat_tuples.append(t)
    con.add_satisfying_tuples(sat_tuples)
    cons.append(con)

# Create and return battleship_csp
    battleship_csp = CSP('battleship', vs)
    for c in cons:
        battleship_csp.add_constraint(c)
    return battleship_csp, variable_array

