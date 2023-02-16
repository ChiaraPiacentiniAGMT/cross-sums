from ortools.sat.python import cp_model


class Solver:
    def __init__(self, grid):
        self.grid = grid
        self.prob = cp_model.CpModel() # OR tools cp model
        self._x = {}     # dict of cell -> CP Variable

        # Make a dictionary of integer variables. Every variable can
        # have a value from 1 to 9.
        for c in grid.cells.keys():
            if grid.cells[c] == 0:
                v = self.prob.NewIntVar(1, 9, "x%i_%i" % c)
                self._x[c] = v

        # Add the constraints
        for con in grid.constraints:
            v = [self._x[c] for c in con.cells]
            # Sum of cells
            self.prob.Add(sum(v) == con.sum)
            # All values are unique
            self.prob.AddAllDifferent(v)

        
    def solve(self):
        # solve the problem
        solver = cp_model.CpSolver()
        solver.Solve(self.prob)

        # print wall time
        print(f"Total time {solver.WallTime()} s")

        # create a copy of the input grid to store the solution
        grid = self.grid.clone()

        # fill in the solution values
        for c in grid.cells.keys():
            if grid.cells[c] == 0:
                grid.cells[c] = str(solver.Value(self._x[c]))
        return grid

                    
def solve_cp(grid):
    s = Solver(grid)
    return s.solve()


    
