################
# Introduction #
################

A target map is a 2D array where 0 represents ocean and 1 represents target.
~ ~ x ~ x
~ x ~ x x
~ ~ x ~ x
x ~ ~ ~ x
~ ~ ~ x ~

A ship_map is a 2D array where 0 represents ocean and any connected integer n represents a ship with length n.
~ ~ 1 ~ 4
~ 1 ~ 1 4
~ ~ 1 ~ 4
1 ~ ~ ~ 4
~ ~ ~ 1 ~

In order to find out how many targets there are in each row and columns, we have:
- row_targets to show the number of targets in each row
    e.g. row_targets = [2, 3, 2, 2, 1]
        This means there are 2 targets in row 0, 3 targets in row 1, and so on.

- column_targets to show the number of targets in each column
    e.g. column_targets = [1, 1, 2, 2, 4]
        This means there are 1 target in column 0, 1 targets in column 1, and so on.

For the example ship map above, we also have:
- ships to show us the number of ships of each length
    e.g. ships = [0, 6, 0, 0, 1]
        This means there are 0 ship of length 0, 6 of length 1, and 1 of length 4.

#### result structure example

Instead of using a single number to indicate the ship size, use a tuple where the first number indicates ship size,
the second number is the identifier of the specific ship in the ship size group.

5x5 grid:

ships [0,3,3,1,1]

(0,0)(0,0)(1,0)(2,0)(2,0)
(2,1)(2,1)(3,0)(4,0)(0,0)
(0,0)(0,0)(3,0)(4,0)(0,0)
(1,1)(1,2)(3,0)(4,0)(2,2)
(0,0)(0,0)(0,0)(4,0)(2,2)

the 3 1-sized ships:
(1,0), (1,1), (1,2)

the 3 2-sized ships:
(2,0)(2,0), (2,1)(2,1), (2,2)
                        (2,2)
the 3-sized ship:
(3,0)
(3,0)
(3,0)

the 4-sized ship:
(4,0)
(4,0)
(4,0)
(4,0)
