# Battleship

[Battleship Game](https://en.wikipedia.org/wiki/Battleship_(game))

## Problem Formalization

A ship_map is a 2D array where 0 represents ocean and any connected integer n represents a ship with length n.

```
# sample map 

~ ~ 1 ~ 4
~ 1 ~ 1 4
~ ~ 1 ~ 4
1 ~ ~ ~ 4
~ ~ ~ 1 ~
```

In order to find out how many targets there are in each row and columns, we have:
- `row_targets` to show the number of targets in each row   
	e.g. `row_targets = [2, 3, 2, 2, 1]`   
    This means there are 2 targets in row 0, 3 targets in row 1, and so on.

- `column_targets` to show the number of targets in each column  
    e.g. `column_targets = [1, 1, 2, 2, 4]`   
    This means there are 1 target in column 0, 1 targets in column 1, and so on.

For the sample ship map above, we also have:
- `ships` to show us the number of ships of each length   
    e.g. `ships = [0, 6, 0, 0, 1]`  
    This means there are 0 ship of length 0, 6 of length 1, and 1 of length 4.

## Solution Board Structure

Instead of using a single number to indicate the ship size, use a tuple where the first number indicates ship size, the second number indicates the identifier of the specific ship in the ship size group.

```
# sample 5x5 grid:

ships [0,3,3,1,1]

(0,0)(0,0)(1,0)(2,0)(2,0)
(2,1)(2,1)(3,0)(4,0)(0,0)
(0,0)(0,0)(3,0)(4,0)(0,0)
(1,1)(1,2)(3,0)(4,0)(2,2)
(0,0)(0,0)(0,0)(4,0)(2,2)

# ships on board:

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
```

## Methods

Please see our [report](./csc384-project.pdf)

## Creating Tests

If you run `create_tests` or `create_basic_test`, you can generate and save test cases into .txt files. The difference between `create_tests` and `create_basic_test` is that you can increase the board size by a multiple and for every board size, it will generate tests from 1 targets to n-squared targets (essentially filling up the game board).

## Running Tests

By running main method in `test_engine.py`, you will take advantage of ProcessPoolExecutor and split the running of each basic test into processes.

You can configurate the number of worker your processors allow by changing the parameters, and the test results will be saved to the results folder with the filename you pass to the `basic_test_model1` and `basic_test_model23` methods.

If you would like to manually load a saved tests, you can use `load_tests` in `test_generator.py` or feed a target map into a new `BattleshipTest` object.
