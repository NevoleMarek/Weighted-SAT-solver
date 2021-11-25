class FormulaAdjacencyList:
    """
    Class for Adjacency list of formula.
    """
    def __init__(self, formula):
        self.adjacency_list = self._create_list(formula)

    def __getitem__(self, key):
        return self.adjacency_list[key]

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
