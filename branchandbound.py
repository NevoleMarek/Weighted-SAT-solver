from utils import FormulaAdjacencyList, FormulaClauseCounter, State
from copy import deepcopy
class BranchAndBound:
    """
    Branch and bound method used for solving literal weighted SAT problem.

    Parameters
    ----------
    formula : formula.Formula
        Formula in CNF with weigths.
    """
    def __init__(self, formula):
        self.formula = formula
        self.adj_list = FormulaAdjacencyList(formula)
        self.state = State(
            assignment = {
                var:-1
                for var in range(1, self.formula.n_vars+1)
            },
            counter = FormulaClauseCounter(formula)
        )
        self._stats = {
            'best_weight':0,
            'assignment': self.state.assignment
        }

    def run(self):
        """
        Run method of solver.

        Returns
        -------
        tuple
            best_weight and its assignment
        """
        self._backtrack( 1, sum(self.formula.weights), 0)
        return (
            (
                self._stats['best_weight'] + \
                len(self.formula.clauses) * \
                sum(self.formula.weights)
            ),
            self._stats['assignment']
        )

    def stats(self):
        return self._stats

    def _backtrack(
        self,
        var,
        weight_remaining,
        current_weight
    ):
        """
        Backtracking method of solver

        Parameters
        ----------
        var : int
            Index of variable that will be assigned to in the step of backtracking.
        weight_remaining : Numeric type
            Sum of weights of unassigned variables.
        current_weight : Numeric type
            Weight of current assignment.
        """
        if self._conflict():
            return

        if self._sat():
            if current_weight > self._stats['best_weight']:
                self._stats['best_weight'] = current_weight + weight_remaining
                self._stats['solution'] = deepcopy(self.state.assignment)

        if current_weight + weight_remaining < self._stats['best_weight']:
            return

        if var > self.formula.n_vars:
            return

        self._assign_variable(var, 0)
        self._backtrack(
            var + 1,
            weight_remaining - self.formula.weights[var],
            current_weight
        )
        self._unassign_variable(var)

        self._assign_variable(var, 1)
        self._backtrack(
            var + 1,
            weight_remaining - self.formula.weights[var],
            current_weight + self.formula.weights[var]
        )
        self._unassign_variable(var)
        return

    def _assign_variable(self, variable, value):
        """ Assign value to variable and update counters. """
        self.state.assignment[variable] = value
        for c in self.adj_list[variable][0]:
                self.state.counter[c][int(0==value)] += 1
        for c in self.adj_list[variable][1]:
                self.state.counter[c][int(1==value)] += 1

    def _unassign_variable(self, variable):
        """ Unassign value from variable and update counters. """
        value = self.state.assignment[variable]
        self.state.assignment[variable] = -1
        for c in self.adj_list[variable][0]:
                self.state.counter[c][int(0==value)] -= 1
        for c in self.adj_list[variable][1]:
                self.state.counter[c][int(1==value)] -= 1

    def _conflict(self):
        """
        Returns
        -------
        bool
            Returns True if any clause is in conflict under current assignment
            else False.
        """
        for i,c in enumerate(self.state.counter):
            if c[1] == c[2]:
                return True
        return False

    def _sat(self):
        """
        Returns
        -------
        bool
            Returns True if formula is satisfied under current assignment else
            False.
        """
        for c in self.state.counter:
            if c[0] == 0:
                return False
        return True
