import copy

class FormulaAdjacencyList:
    """ Class for Adjacency list of formula. """
    def __init__(self, formula):
        self.adjacency_list = self._create_list(formula)

    def __getitem__(self, literal):
        return self.adjacency_list[literal]

    def __iter__(self):
        for k, v in self.adjacency_list.items():
            yield k, v

    def _create_list(self, formula):
        adj_list = {var:(set(),set()) for var in formula.variables[1:]}
        for i, clause in enumerate(formula.clauses):
            for l in clause.literals:
                if l.is_negated:
                    adj_list[l.var][1].add(i)
                else:
                    adj_list[l.var][0].add(i)
        return adj_list

class FormulaClauseCounter:
    """ Counter of satisfied and unsatisfied literals in clauses. """
    def __init__(self, formula):
        self.counter = self._create_counter(formula)

    def __getitem__(self, clause_id):
        return self.counter[clause_id]

    def __iter__(self):
        for clause in self.counter:
            yield clause

    def _create_counter(self, formula):
        counter = []
        for clause in formula.clauses:
            counter.append([0,0])
        return counter

class State:
    """
    Class representing one state in search state space.

    Parameters
    ----------
    assignment : dict
        Dictionary with key value pairs, where key is variable and value
        is truth value assigned to variable.
    counter : FormulaClauseCounter
        Counter data structure of 'assignment' used for efficient satisfied
        clause lookup.
    """
    def __init__(self, assignment, counter):
        self.assignment = assignment
        self.counter = counter

    def copy(self):
        """ Copy itself. """
        return copy.deepcopy(self)
