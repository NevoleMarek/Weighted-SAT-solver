class FormulaAdjacencyList:
    """ Class for Adjacency list of formula. """
    def __init__(self, formula):
        self.adjacency_list = self._create_list(formula)

    def __getitem__(self, literal):
        return self.adjacency_list[literal]

    def _create_list(self, formula):
        adj_list = {var:set() for var in formula.variables[1:]}
        adj_list.update({-var:set() for var in formula.variables[1:]})
        for i, clause in enumerate(formula.clauses):
            for l in clause.literals:
                if l.is_negated:
                    adj_list[-l.var].add(i)
                else:
                    adj_list[l.var].add(i)
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
