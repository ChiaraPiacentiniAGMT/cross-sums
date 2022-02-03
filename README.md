# Solve Cross Sum Puzzles

A python program to solve cross sum puzzles (similar to Sudoku).  It's
easy to find a description of the rules.  Here is an example puzzle:

![](images/cross-sums.png?raw=true)

To invoke this solver, the puzzle can be edited in a spreadsheet like this:

![](images/cross-sums-spreadsheet.png?raw=true)

and saved out as CSV, which the solver can read.  It outputs the
solution back to CSV:

![](images/cross-sums-solution.png?raw=true)

The solver is rather brute force, and not very efficiently written.
It was kind fun writing the function to generate possible
combinations/permutations of a particular constraint as a recursive
generator.