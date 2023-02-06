# Solve Cross Sum Puzzles

A python program to solve cross sum puzzles (similar to Sudoku).  It's
easy to find a description of the rules.  Here is an example puzzle:

![](images/cross-sums.png?raw=true)

To invoke this solver, the puzzle can be edited in a spreadsheet like this:

![](images/cross-sums-spreadsheet.png?raw=true)

and saved out as CSV, which the solver can read.  It outputs the
solution back to CSV:

![](images/cross-sums-solution.png?raw=true)

The solver uses the linear programming library PuLP which has clever
syntax for defining the constraints.  Some test puzzles solve in less
than a second.
