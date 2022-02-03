from .utils import *

# Represents the constraint of the sum of a run of adjacent grid cells
class Constraint:
    def __init__(self, sum, row, col, vertical, length):
        self.sum = sum           # the constraint value (sum of cell values)
        self.row = row           # row index of left-most cell in run
        self.col = col           # col index of top-most cell in run
        self.vertical = vertical # True iff this is vertical constraint
        self.length = length     # number of cells in this constraint
        self.cells = []          # list of (rol,col) tuples

        self._populate_cells()

    def intersects(self, other):
        """Returns true if this constraints intersects another
        """
        # parallel constraints don't intersect
        if self.vertical == other.vertical:
            return False

        # determine which is vertical and horizontal
        if self.vertical:
            v = self
            h = other
        else:
            v = other
            h = self

        # check if the they are bounded away from each other
        if h.row < v.row:
            return False
        if h.row >= v.row + v.length:
            return False
        if h.col + h.length <= v.col:
            return False
        if h.col > v.col:
            return False

        return True

    def _populate_cells(self):
        cell = (self.row, self.col)
        step = (1,0) if self.vertical else (0,1)
        for i in range(self.length):
            self.cells.append(cell)
            cell = (cell[0] + step[0], cell[1] + step[1])
        
    def __str__(self):
        dir = "vertical" if self.vertical else "horizontal"
        c = coord(self.row, self.col)
        return "Constraint{} {} length({})".format(c, dir, self.length)
