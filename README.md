# Battleship

[Battleship Game](https://en.wikipedia.org/wiki/Battleship_(game))

## File/Directory Description

#### Files

`cspbase.py` - CSP base model.  
`battleship_csp.py` - Battleship CSP models. Including 3 models.  
`battleship_BT.py` - Extends BT in `cspbase.py`; customized for model 1 to solve battleship problems.  
`orderings.py` - Some variable and value orderings.  
`propagators.py` - Implementations for BT, FC, GAC propagators.  
`little_test.py` - Sample functionality test for small boards (<= 3x3)  
`sample_test.py` - Sample functionality test for larger boards (>= 4x4)  
`test_generator.py` - Generating test cases.  
`test_engine.py` - Test driver.  
`validity_check.py` - Checking for solution correctness.  
`utilities.py` - Other utility functions.  

#### Directories

`results` - csv files of data generated from test & parsed data.  
`static_tests` - Static test cases.  
`data_visualization` - R files to parse & visualize data.  
`plotes` - Images of plotted data.  

---
## Usage

`cd` into the `battleship` folder. This is the folder containing all source files.  

#### Basic Functionality Testing

To run basic test with board size 3x3 with the 3 models, run: `python3 ./little_test.py`  
To run basic test with board size larger than 3x3 with the 3 models, run: `python3 ./sample_test.py`  

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

To create tests, run: `python3 test_generator.py`

With `create_tests` or `create_basic_test` in `test_generator.py`, you can generate and save test cases into .txt files. The difference between the two is that with `create_tests`, you can specify each parameter and create 1 static test case; with `create_basic_test`, mutiple test cases are created automatically where board size is increased by a multiple, and for every board size, tests from 1 targets to n-squared targets will be generated (essentially filling up the game board). See the main function in `test_generator.py` for sample usage.

A sample result below:

```
Ship Map 10/10
~ ~ ~ ~ ~
1 ~ ~ ~ ~
~ ~ ~ ~ 2
~ ~ ~ ~ 2
1 ~ 1 ~ ~
```

###### Running Tests

To run the tests, run: `python3 test_engine.py`

In this engine, the tests in `static_tests/basic_tests` will be run, i.e. running 3 models on board size 1x1 to 4x4. By running this, you will take advantage of ProcessPoolExecutor and split the run of each basic test into processes. 3 processes are used in this engine, each running one model.

A sample result below:

```
CSP battleship solved. CPU Time used = 0.02035451199998306
CSP battleship  Assignments = 
Var--(0,0)  =  (0, 0)     Var--(0,1)  =  (1, 0)     Var--(0,2)  =  (1, 1)     Var--(1,0)  =  (2, 0)     Var--(1,1)  =  (0, 0)     Var--(1,2)  =  (1, 2)     Var--(2,0)  =  (2, 0)     Var--(2,1)  =  (0, 0)     Var--(2,2)  =  (0, 0)     
bt_search finished
Search made 331 variable assignments and pruned 563 variable values
```

You can configurate the number of workers your processors allow by changing the parameters for `basic_test_model1` or `basic_test_model23` in the main method, and the test results will be saved to the results folder with the filename you passed in.

If you would like to manually load a saved test, you can use `load_tests` in `test_generator.py`, or feed a target map into a new `BattleshipTest` object. Details please see `test_generator.py`.

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

