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
    def __init__(self):
        self.literals = []
        self.weights = []
        self.clauses = []

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
        frml = cls()
        with open(path) as f:
            clause = []
            for line in f:
                if line.startswith('w'):
                    line = [i.strip() for i in line.split()[1:-1]]
                    weights = [int(w) for w in line]
                    frml.weights = weights
                elif    not line.startswith('c') and\
                        not line.startswith('\n') and\
                        not line.startswith('p') and\
                        not line.startswith('%'):
                    line = [int(i.strip()) for i in line.split()]
                    for literal in line:
                        if abs(literal) not in frml.literals and\
                                abs(literal) > 0:
                            frml.literals.append(abs(literal))
                        if literal != 0:
                            clause.append(literal)
                        else:
                            if clause:
                                frml.clauses.append(Clause(clause))
                                clause = []
            if clause: # For when 0 is not after last clause in file
                frml.clauses.append(Clause(clause))
        return frml

    def __str__(self):
        clauses = str()
        for clause in self.clauses:
            clauses += '('
            for literal in clause.literals:
                literal_str = str()
                sign = str()
                if literal < 0:
                    sign = '-'
                    literal *= -1
                quotient = literal
                while quotient > 26:
                    res = quotient % 26
                    quotient = quotient // 26
                    literal_str = chr(res + 64) + literal_str
                literal_str = chr(quotient + 64) + literal_str
                clauses += f'{sign}{literal_str}'
                clauses += ' V '
            clauses = clauses[:-3]
            clauses += ') ∧ '
        return clauses[:-3]
