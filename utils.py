class FormulaAdjacencyList:
    """ Class for Adjacency list of formula. """
    def __init__(self, formula):
        self.adjacency_list = self._create_list(formula)

    def __getitem__(self, literal):
        return self.adjacency_list[literal]

    def _create_list(self, formula):
        adj_list = dict()
        for i, clause in enumerate(formula.clauses):
            for l in clause.literals:
                if l not in adj_list:
                    adj_list[l] = set()
                if -l not in adj_list:
                    adj_list[-l] = set()
                adj_list[l].add(i)
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
