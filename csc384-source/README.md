# Battleship

[Battleship Game](https://en.wikipedia.org/wiki/Battleship_(game))

---
## Usage

`cd` into the `battleship` folder. This is the folder containing all source files.  

#### Functionality Testing

To run basic test with board size 3x3 with the 3 models, run:  
`python3 ./little_test.py`  

To run basic test with board size larger than 3x3 with the 3 models, run:  
`python3 ./sample_test.py`  

Please be reminded that it took some time running model 2 and 3 with board size larger than 3x3. 

A sample result below:

```
---model 1 sample test---

---BT with val_decrease_lcv---

CSP battleship solved. CPU Time used = 0.0017570000000000086
CSP battleship  Assignments = 
Var--(0,0)  =  3     Var--(0,1)  =  3     Var--(0,2)  =  3     Var--(1,0)  =  2     Var--(1,1)  =  2     Var--(1,2)  =  1     Var--(2,0)  =  2     Var--(2,1)  =  2     Var--(2,2)  =  0     
bt_search finished
Search made 12 variable assignments and pruned 0 variable values
[[(3, 1), (3, 1), (3, 1)], [(2, 2), (2, 2), (1, 1)], [(2, 1), (2, 1), (0, 0)]]
OK
---BT with val_decreasing_order---
...
---FC with val_decrease_lcv---
...
---FC with val_decreasing_order---
...
---GAC with val_decrease_lcv---
...
---GAC with val_decreasing_order---
...
---finished model 1 sample test---
```

The nested list before `OK` is the solution board.  

To create your own tests, open `sample_test.py` and follow the samples to create a new input in `test_sample_run` function. Comment out the other test cases.  

#### Performance Testing

###### Creating Tests

If you run `create_tests` or `create_basic_test` in `test_generator.py`, you can generate and save test cases into .txt files. The difference between the two is that you can increase the board size by a multiple, and for every board size, it will generate tests from 1 targets to n-squared targets (essentially filling up the game board).

Sample usage:

1. Open test_generator.py, and at the bottom inside the main function, you will see:
	
	```
	# Create and save tests to file
	# 5x5 map with 5 targets, no ship constraint, 10 tests
	create_tests(5, 5, 0, 10, True)

	# # Load tests from file
	tests = load_tests('./static_tests/test_5_5_0_10.txt')
	ship_maps = [test.ship_map for test in tests]
	print_ship_maps(ship_maps)
	```
	

###### Running Tests

By running main method in `test_engine.py`, you will take advantage of ProcessPoolExecutor and split the run of each basic test into processes.

You can configurate the number of worker your processors allow by changing the parameters, and the test results will be saved to the results folder with the filename you pass to the `basic_test_model1` and `basic_test_model23` methods.

If you would like to manually load a saved test, you can use `load_tests` in `test_generator.py` or feed a target map into a new `BattleshipTest` object.

---
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

Please see csc384-project.pdf.
