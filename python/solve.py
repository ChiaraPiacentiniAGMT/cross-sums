import sys

def generate_sums(sum, count, choices):
    """Generate all ordered lists adding to a particular value.
    
    Arguments
    ---------
    sum      value that the returned lists should add to
    count    length of lists to be returned
    choices  list of possible addends

    Yields
    ------
    Lists of all ordered sums of the specified size.
    """
    # handle the base case
    if count == 1:
        for i in range(len(choices)):
            n = choices[i]
            if sum == n:
                yield [n]
    else:
        # there are 2 or more choices left to be made
        for i in range(len(choices)):
            n = choices[i]
            if n < sum:
                sub_choices = choices[0:i] + choices[i+1:]
                for sub_list in generate_sums(sum - n, count-1, sub_choices):
                    yield [n] + sub_list


def constraint_adjacency(grid):
    """Returns the constraint adjacency list.

    Returns
    -------
    Dictionary of Constraint -> list[Constraint]
    """
    # constraint -> list of adjacent constraints
    adj = {c: [] for c in grid.constraints}
    for c1 in grid.constraints:
        for c2 in grid.constraints:
            # intersection should be symmetric
            assert c1.intersects(c2) == c2.intersects(c1)
            
            if c1.intersects(c2):
                adj[c1].append(c2)

    return adj
    

def get_ordered_constraints(grid, adj):
    """Return a somewhat ordering of the constraints.
    """
    # initialize the set of consumed and available constraints
    consumed = set() # set of used constraints
    constraints = [] # ordered list of constraints
    constraints.append(grid.constraints[0])
    consumed.add(grid.constraints[0])
    available = set(adj[constraints[0]]) # set of unconsumed constraints on front

    # repeatedly find an unconsumed constraint adjacent to a consumed one
    while len(available) > 0:
        # find the smallest constraint next
        c1 = None
        for c in available:
            if c1 is None:
                c1 = c
            elif len(c.cells) < len(c1.cells):
                c1 = c

        available.remove(c1)
        if c1 not in consumed:
            constraints.append(c1)
            consumed.add(c1)
            for c2 in adj[c1]:
                if c2 not in consumed:
                    available.add(c2)

    return constraints


class Solver:
    def __init__(self, grid, adj, constraints):
        self.grid = grid                 # grid to solve
        self.adj = adj                   # constraint adjacency list
        self.constraints = constraints   # ordered list of constraints
        self.results = []                # list of grids satisfying constraints

    def solve(self):
        self._satisfy_constraints(0)
        pass

    def _satisfy_constraints(self, index):
        """Satisfy a list of constraints starting from an index.
        """
        if index == len(self.constraints):
            # success!
            print("found solution!")
            self.results.append(self.grid.clone())
            raise StopIteration()
        
        print("Satisfying constraint {}/{}".format(index, len(self.constraints)))
            
        # get the first constraint
        constraint = self.constraints[index]
        
        # determine the constraint's fixed cells
        fixed_cells = [c for c in constraint.cells if self.grid.cells[c] != 0]
        
        # find the values in the fixed cells
        fixed_values = [self.grid.cells[c] for c in fixed_cells]
        
        # check that the fixed values have no repeats
        fixed_values.sort()
        for i in range(1, len(fixed_values)):
            if fixed_values[i-1] == fixed_values[i]:
                return # unsatisfiable: repeated values in fixed cells
        
        # maybe all cells in the constraint are fixed
        if len(fixed_values) == constraint.length:
            # the sum must be right
            if sum(fixed_values) != constraint.sum:
                return # unsatisfiable: all cells fixed with incorrect sum
        
            # proceed to next constraint
            self._satisfy_constraints(index+1)
        else:
            # check that the sum of the fixed constraints is small enough
            fixed_sum = sum(fixed_values)
            if fixed_sum >= constraint.sum:
                return # unsatisfiable: sum in fixed values too high
        
            # determine the free cells
            free_cells = [c for c in constraint.cells if self.grid.cells[c] == 0]
        
            # determine the free sum
            free_sum = constraint.sum - fixed_sum
        
            # determine the available choices for values for the free sum
            choices = [v for v in range(1,10) if v not in fixed_values]
        
            # generate fixed values that satisfy this constraint
            for free_values in generate_sums(free_sum, len(free_cells), choices):
                # apply the change to the grid
                for item in zip(free_cells, free_values):
                    self.grid.cells[item[0]] = item[1]

                # optimization: check if adjacent constraints are
                # still satisfiable
                if not self._check_adjacent_constraints(constraint):
                    continue
        
                # proceed to the next constraint
                self._satisfy_constraints(index+1)
            
            # restore the free cells to zero
            for c in free_cells:
                self.grid.cells[c] = 0

    def _check_adjacent_constraints(self, constraint):
        """Check that the adjacent constraints are still satisfiable."""
        for c in self.adj[constraint]:
            if not self._satisfiable(c):
                return False
        return True

    def _satisfiable(self, constraint):
        """Approximately check that this constraint is still satisfiable."""
        # find the values of the constraint's cells
        values = [self.grid.cells[c] for c in constraint.cells]
        return sum(values) <= constraint.sum
        
                    
def solve(grid):
    print("num constraints: {}".format(len(grid.constraints)))
    for c in grid.constraints:
        print("  ", c)
    print("num cells: {}".format(len(grid.cells)))
    adj = constraint_adjacency(grid)
    constraints = get_ordered_constraints(grid, adj)
    print("constraints in ordering: {}".format(len(constraints)))

    solver = Solver(grid, adj, constraints)
    try:
        solver.solve()
    except StopIteration:
        return solver.results[0]
    
