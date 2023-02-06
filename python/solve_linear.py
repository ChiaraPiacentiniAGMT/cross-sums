import sys
import pulp


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.prob = None # pulp LpProblem
        self._x = {}     # dict of string key -> LpVariable

        # make the problem object
        self.prob = pulp.LpProblem("crosssums")

        # Make a dictionary of binary variables indexed as (see
        # self._key() for definition of key).  There are 9 variables
        # for each grid cell.  Per cell, the variables represent
        # whether the value in the cell is the (idx+1).  In a
        # solution, only one of the 9 variables has value 1 and the
        # rest have value 0.
        for c in grid.cells.keys():
            if grid.cells[c] == 0:
                for idx in range(0,9):
                    key = self.key(c, idx)
                    v = pulp.LpVariable(key, cat="Binary")
                    self._x[key] = v

        # Add constraints for the encoding of the cells.  Each cell
        # should have a value, meaning that the sum of the 9 variables should
        # be 1.
        for c in grid.cells.keys():
            if grid.cells[c] == 0:
                values = [self.x(c, idx) for idx in range(0,9)]
                self.prob += pulp.lpSum(values) == 1

        # Add the sum constraints in the grid.
        for con in grid.constraints:
            # The numbers in the cells of the constraint should be
            # unique.  Therefore only one of the per-cell variables
            # representing the same number can be set.
            for idx in range(0,9):
                v = [self.x(c, idx) for c in con.cells]
                self.prob += pulp.lpSum(v) <= 1

            # Add the constraint for the sum of the cells.
            sum_expr = []
            for c in con.cells:
                cell_expr = [(idx+1)*self.x(c, idx) for idx in range(0,9)]
                sum_expr.extend(cell_expr)
            self.prob += pulp.lpSum(sum_expr) == con.sum

    def x(self, cell, idx):
        key = self.key(cell, idx)
        return self._x[key]

    def solve(self):
        # solve the problem
        self.prob.solve()

        # create a copy of the input grid to store the solution
        grid = self.grid.clone()

        # fill in the solution values
        for c in grid.cells.keys():
            if grid.cells[c] == 0:
                v = [(idx+1)*pulp.value(self.x(c, idx)) for idx in range(0,9)]
                grid.cells[c] = str(sum([int(a) for a in v]))

        return grid

    def key(self, cell, idx):
        """Return a key into self.x based on a cell and per-cell index"""
        return "{}-{}-{}".format(cell[0], cell[1], idx)


def solver_example():        
    # Objective of the optimization.  Represents a linear expression
    # to minimize.  Values are the coefficients of the list of
    # variables.
    obj = [-1, -2]

    # Matrix of LHS coefficients of <= inequality constraints.
    lhs_ineq = [[ 2,  1],  # Red constraint left side
                [-4,  5],  # Blue constraint left side
                [ 1, -2]]  # Yellow constraint left side

    # Vector of RHS of inequality constraints.
    rhs_ineq = [20,  # Red constraint right side
                10,  # Blue constraint right side
                2]  # Yellow constraint right side

    # Matrix of LHS coefficients of equality constraints.
    lhs_eq = [[-1, 5]]  # Green constraint left side

    # Vector of RHS of equality constraints.
    rhs_eq = [15]

    # Vector of bounds of variables.
    bnd = [(0, float("inf")),  # Bounds of x
           (0, float("inf"))]  # Bounds of y

    # call the solver
    opt = opt.linprog(
        c=obj,
        A_ub=lhs_ineq,
        b_ub=rhs_ineq,
        A_eq=lhs_eq,
        b_eq=rhs_eq,
        bounds=bnd,
        method="highs")

    print(opt)
                    
def solve_linear(grid):
    s = Solver(grid)
    return s.solve()
    
