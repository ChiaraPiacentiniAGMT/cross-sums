import pandas as pd

from .constraint import *
from .utils import *

class Grid:
    def __init__(self):
        # Dict where key is (row,col) tuples, value is integer in cell
        self.cells = {}

        # list of sum constraints
        self.constraints = []


    def parse_df(self, df):
        """Populate this object from a pandas dataframe.
        """
        # parse the numerical cells in one pass
        (rows, cols) = df.shape
        for j in range(cols):
            col = df.iloc[:, j]
            for i in range(len(col)):
                cell = col[i]
                if cell == "*":
                    pass # not recorded
                elif cell == "0":
                    self.cells[(i,j)] = 0

        # parse the constraint cells in a second pass
        for j in range(cols):
            col = df.iloc[:, j]
            for i in range(len(col)):
                cell = col[i]
                if "\\" in cell:
                    self._parse_constraint_cell(cell, i, j)

    def df(self):
        """Return a dataframe representing the grid and constraints."""
        nrows = max([c[0] for c in self.cells]) + 2
        ncols = max([c[1] for c in self.cells]) + 2

        # initialize the columns to "*"
        cols = [["*"] * nrows for _ in range(ncols)]

        # fill in the values for the cells
        for c in self.cells:
            cols[c[1]][c[0]] = self.cells[c]

        def get_row_col(constraint):
            row = c.row
            col = c.col
            if c.vertical:
                row -= 1
            else:
                col -= 1
            return row, col

        # initialize the constraint indicators
        for c in self.constraints:
            row, col = get_row_col(c)
            cols[col][row] = "\\"

        # fill in the constraint indicators
        for c in self.constraints:
            row, col = get_row_col(c)
            vertical, horizontal = cols[col][row].split("\\")
            if c.vertical:
                cols[col][row] = str(c.sum) + "\\" + horizontal
            else:
                cols[col][row] = vertical + "\\" + str(c.sum)

        data = {i: col for i, col in enumerate(cols)}
        df = pd.DataFrame(data)
        print(df)
        return df
        

    def read_cells(self, coords):
        """Return values corresponding coordinate tuples.

        Arguments
        ---------
        coords    list of (row,col) tuples
        """
        return [self.cells[c] for c in coords]

    def write_cells(self, coords, values):
        """Write values into the the specified coordinate tuples.

        Arguments
        ---------
        coords    list of (row,col) tuples
        values    list of values for the corresponding cells
        """
        for item in zip(coords, values):
            self.cells[item[0]] = item[1]

    def clone(self):
        """Return a deep copy.
        """
        grid = Grid()
        grid.cells = dict(self.cells)
        grid.constraints = list(self.constraints)
        return grid
        
    def _parse_constraint_cell(self, cell, i, j):
        constraints = cell.split("\\")
        if len(constraints) != 2:
            msg = "invalid constraint in cell {}".format(coord(i,j))
            raise RuntimeError(msg)
        if constraints[0] != "":
            self._parse_constraint(i, j, True, constraints[0])
        if constraints[1] != "":
            self._parse_constraint(i, j, False, constraints[1])

    def _parse_constraint(self, i, j, vertical, constraint_str):
        # set some variables based on direction
        if vertical:
            dir = "vertical"
            start_cell = (i+1, j)
            step = (1, 0)
        else:
            dir = "horizontal"
            start_cell = (i, j+1)
            step = (0, 1)
        
        s = int(constraint_str)
        if s < 1:
            msg = "invalid {} sum '{}' in cell {}".format(dir, s, coord(i,j))
            raise RuntimeError(msg)

        # determine the constraint length
        length = self._get_constraint_length(start_cell, step)
        if length < 1:
            msg = "{} sum in cell {} not next to empty cell".format(dir, coord(i,j))
            raise RuntimeError(msg)

        # store the constraint
        c = Constraint(s, start_cell[0], start_cell[1], vertical, length)
        self.constraints.append(c)
            
    def _get_constraint_length(self, cell, step):
        length = 0
        while cell in self.cells:
            length = length + 1
            cell = (cell[0] + step[0], cell[1] + step[1])
        return length
