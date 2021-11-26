class Literal:
    """
    Literal class

    Parameters
        ----------
        var : int
            Variable
        is_negated : bool
            True if literal is negated else False
    """
    def __init__(self, var, is_negated):
        self.var = var
        self.is_negated = is_negated

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        sign = '-' if self.is_negated else ''
        return f'{sign}{self.var}'

class Clause:
    """ Clause representing sum of literals. """

    def __init__(self, literals):
        self.literals = literals
        self.size = len(literals)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'Literals = {self.literals}, size = {self.size}'

class Formula:
    """ Formula in CNF with weights of literals. """
    def __init__(self, variables, weights, clauses, n_vars):
        self.variables = variables
        self.weights = weights
        self.clauses = clauses
        self.n_vars = n_vars

    @classmethod
    def from_file(cls, path):
        """
        Parse file in DIMACS format extended by weights line denoted
        by 'w' letter at start of the line into Formula class.

        Parameters
        ----------
        path : str
            Path to file with instance.

        Returns
        -------
        Formula
            Instance of Formula class
        """

        with open(path) as f:
            clauses = []
            clause = []
            for line in f:
                if line.startswith('p'):
                    n_vars = int(line.split()[2])
                    variables = [i for i in range(n_vars + 1)]
                elif line.startswith('w'):
                    weights = [int(i.strip()) for i in line.split()[1:-1]]
                    weights.insert(0,0)

                elif not line.startswith(('c','\n','%')):
                    line = [int(i.strip()) for i in line.split()]
                    for literal in line:
                        if literal == 0:
                            if clause:
                                clauses.append(Clause(clause))
                                clause = []
                        else:
                            var = abs(literal)
                            negated = True if literal < 0 else False
                            clause.append(Literal(var, negated))
            if clause: # For when 0 is not after last clause in file
                clauses.append(Clause(clause))
        return cls(variables, weights, clauses, n_vars)

    def __str__(self):
        clauses = ''
        for clause in self.clauses:
            clauses += f'{"".join(str(clause.literals))}\n'
        return (
            f'# of vars: {self.n_vars}\n'
            f'Weights  :{self.weights}\n'
            f'Variables:{self.variables}\n'
            f'Clauses  :\n{clauses}'
        )
