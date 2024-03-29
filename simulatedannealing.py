from abc import ABC, abstractmethod
from random import random, randint, choice
from collections import deque

import math

from utils import FormulaAdjacencyList, FormulaClauseCounter, State, StoppingCriterion

class SimulatedAnnealing(ABC):
    """ Abstract class of simulated annealing. """
    def __init__(
        self,
        iter_limit = 100,
        restart_limit = 1,
        threshold = 1e-6
    ):
        self._iter_limit = iter_limit
        self._restart_limit = restart_limit
        self._threshold = threshold
        self._stats = {
            'iterations':0,
            'init':[]
        }

    def stats(self):
        return self._stats

    @abstractmethod
    def _initial_state(self):
        """
        Create initial state of given problem.
        Return the state.
        """
        pass

    @abstractmethod
    def _evaluate(self, state):
        """
        Evaluate 'state' using the score function that is to be maximized by
        the algorithm.
        Return the value of a score function.
        """
        pass

    @abstractmethod
    def _next_state(self, current_state):
        """
        Find 'next_state' from 'current_state' using neighborhood operator.
        This method can return signal to force stop current search.
        Signal has to be of value equal to True to work correctly.
        Return next_state and signal value to force stop.
        Return next_state and None to not use signal.
        """
        pass

    @abstractmethod
    def _cooling_schedule(self, temperature):
        """
        Calculate new temperature using cooling schedule.
        Return new temperature.
        """
        pass

    @abstractmethod
    def _initial_temperature(self):
        """
        Initialize temperature.
        Return temperature.
        """
        pass

    def stop_criterion(self):
        if not self.buffer.full():
            return False
        if self.buffer.avg() < self._threshold:
            return True
        return False

    def run(self):
        ITER_LIMIT = self._iter_limit
        RESTART_LIMIT = self._restart_limit
        TEMP = self._initial_temperature()

        best_score = 0
        best_state = None

        for _ in range(RESTART_LIMIT):
            SIGNAL = None
            temperature = TEMP

            current_state = self._initial_state()
            current_score = self._evaluate(current_state)
            self.buffer = StoppingCriterion(current_score, ITER_LIMIT)
            self._stats['init'].append(current_score)


            while not self.stop_criterion():

                if SIGNAL:
                    break
                next_state, SIGNAL = self._next_state(current_state)
                next_score = self._evaluate(next_state)

                if  next_score > current_score or \
                    random() < math.exp((next_score - current_score)/temperature):
                    current_state = next_state
                    current_score = next_score

                    if current_score > best_score:
                        best_score = current_score
                        best_state = current_state

                self.buffer.add(current_score)
                temperature = self._cooling_schedule(temperature)
                self._stats['iterations'] +=1

        return best_score, best_state


class SA_WeightedSAT(SimulatedAnnealing):
    """
    Simulated annealing solver class for weighted SAT derived from
    SimulatedAnnealing abstract class.

    Parameters
    ----------
    formula : formula.Formula
        Formula in CNF with weigths.

    iter_limit : int, optional
        Simulated annealing algorithm is stopped if it hasn't found
        better next state (in terms of score function) in last iter_limit
        iterations,
        by default 100.

    restart_limit : int, optional
        Number of times simulated annealing is used on one instance,
        by default 1.

    alpha : float, optional
        Parameter used in geometric cooling schedule, by default 0.99.

    beta : int, optional
        If set to value other than zero then geometric + linear cooling
        schedule is used instead, by default 0.

    temp_prob : float, optional
        Value used in calculation of initial temperature, by default 0.8.

    init_method : str, optional
        Method used in initial state generation, by default 'zero'.
        Possible values:
        - 'zero' all variables set to value 0 (False)
        - 'one' all variables set to value 1 (True)
        - 'random' variables are assign values of 0 or 1 randomly
        - 'greedy' assign value according to counts of non-negated and negated
                occurances of literals

    next_method : str, optional
        Heuristic of neighborhood operator used in searching for next state,
        by default 'random'.
        Ties broken randomly.
        Possible values:
        - 'random' flip value of random variable
        - 'greedy' flip value of variable that results in highest possible score in
                neighborhood of current state
        - 'greediest' flip value of variable that results in highest possible
                score in neighborhood of current state or keep current state if
                its score is higher.
        - 'walksat' WalkSAT heuristic. If there are no unsat clauses, greedy
                heuristic is used.
    """
    def __init__(
        self,
        formula,
        iter_limit = 100,
        restart_limit = 1,
        alpha = 0.99,
        beta = 0,
        temp_prob = 0.8,
        init_method = 'greedy',
        next_method = 'greedy'
    ):
        threshold = sum(formula.weights)/(formula.n_vars*iter_limit)
        super().__init__(
            iter_limit,
            restart_limit,
            threshold
        )
        self.formula = formula
        self.alpha = alpha
        self.beta = beta
        self.temp_prob = temp_prob
        self.init_method = init_method
        self.next_method = next_method
        self.adj_list = FormulaAdjacencyList(formula)
        self.clause_weight = sum(formula.weights) + 1

        self.init_m = {
            'zero':self.__zero,
            'one':self.__one,
            'random':self.__random_init,
            'greedy':self.__greedy_init
        }
        self.next_m = {
            'random':self.__random_next,
            'greedy':self.__greedy_next,
            'greediest':self.__greediest_next,
            'walksat':self.__walksat_next
        }

    def _initial_state(self):
        return self.init_m[self.init_method]()

    def _evaluate(self, state):
        """
        Evaluate score function. The way this score function is written,
        it first prioritizes satisfying clauses over maximizing weight.

        Parameters
        ----------
        state : State
            State to be evaluated.

        Returns
        -------
        int
            Value of score function.
        """
        score = 0
        for c in state.counter:
            if c[0] > 0:
                score += self.clause_weight
        for var, val in state.assignment.items():
            if val == 1:
                score += self.formula.weights[var]
        return score


    def _next_state(self, current_state):
        return self.next_m[self.next_method](current_state)

    def _cooling_schedule(self, temperature):
        """
        Recalculate temperature with respect to attributes 'alpha' and 'beta'.

        Parameters
        ----------
        temperature : Numeric type
            Temperature

        Returns
        -------
        Numeric type
            New temperature
        """
        return self.alpha * temperature + self.beta

    def _initial_temperature(self):
        """
        Initial temperature calculation is divided to 2 steps.
        First step is to find average delta of evaluate function of 2 neighbouring
        moves.
        In second step calculate the temperature as if the average move in step one
        was to be accepted with 'temp_prob' probability.

        Returns
        -------
        Numeric type
            Temperature
        """
        #cntr = dict()
        #for var in self.formula.variables[1:]:
        #    cntr[var] = abs(len(self.adj_list[var][0]) - len(self.adj_list[var][1]))
        CNT = 100
        sum_delta = 0
        for i in range(CNT):
            st = self.__random_init()
            nst, _ = self.__random_next(st)
            sum_delta += abs(self._evaluate(st)-self._evaluate(nst))
        delta = sum_delta/CNT
        return abs(delta/math.log(self.temp_prob))

    """
    Initial state methods
    Using heuristic initialize new state.

    Returns
    -------
    State
        Instance of State class generated using heuristic.
    """
    def __zero(self):
        """ Assign 0 to all variables. """
        assignment = {var:0 for var in range(1, self.formula.n_vars+1)}
        counter = self._compute_counter(assignment)
        return State(assignment, counter)

    def __one(self):
        """ Assign 1 to all variables. """
        assignment = {var:1 for var in range(1, self.formula.n_vars+1)}
        counter = self._compute_counter(assignment)
        return State(assignment, counter)

    def __random_init(self):
        """ Randomly assign value of 0 or 1 to variables. """
        assignment = {var:randint(0,1) for var in range(1, self.formula.n_vars+1)}
        counter = self._compute_counter(assignment)
        return State(assignment, counter)

    def __greedy_init(self):
        """
        Assign values greedily according to counts of occurances of negated
        literals and non-negated literals.
        """
        def value(adj_list_var):
            non_negated = len(adj_list_var[0])
            negated = len(adj_list_var[1])
            if non_negated != negated:
                return 1 if non_negated > negated else 0
            else:
                return randint(0, 1)

        assignment = {var:value(tpl) for var,tpl in self.adj_list}
        counter = self._compute_counter(assignment)
        return State(assignment, counter)


    """
    Next state methods
    Using heuristic find next state.

    Parameters
    ----------
    current_state : State
        Instance of State class

    Returns
    -------
    State
        Instance of State class which altered current_state using heuristic
        and neighborhood operator.
    None or Bool-like
        If equals to True then 1 restart will be force stopped.

    """
    def __random_next(self, current_state):
        """ Randomly choose variable whose value will be flipped. """
        next_state = current_state.copy()
        variable = choice(list(next_state.assignment.keys()))
        return self._flip(next_state, variable), None

    def __greedy_next(self, current_state):
        """ Find the best state in neighborhood of 'current_state'. """
        next_state = current_state.copy()
        best_score = -1
        best_variable = 0
        best_variables = []
        for variable in self.formula.variables[1:]:
            next_state = self._flip(next_state, variable)
            score = self._evaluate(next_state)
            next_state = self._flip(next_state, variable)
            if score > best_score:
                best_score = score
                best_variable = variable
                best_variables.clear()
                best_variables.append(variable)
            elif score == best_score:
                best_variables.append(variable)
        if best_variable:
            return self._flip(next_state, choice(best_variables)), None
        else:
            return next_state, True

    def __greediest_next(self, current_state):
        """
        Find the best state in neighborhood of 'current_state'.
        State has to be better than 'current_state'
        """
        next_state = current_state.copy()
        best_score = self._evaluate(current_state)
        best_variable = 0
        best_variables = []
        for variable in self.formula.variables[1:]:
            next_state = self._flip(next_state, variable)
            score = self._evaluate(next_state)
            next_state = self._flip(next_state, variable)
            if score > best_score:
                best_score = score
                best_variable = variable
                best_variables.clear()
                best_variables.append(variable)
            elif score == best_score:
                best_variables.append(variable)
        if best_variable:
            return self._flip(next_state, choice(best_variables)), None
        else:
            return current_state, True

    def __walksat_next(self, current_state):
        """
        WalkSAT heuristic
        """
        next_state = current_state.copy()
        unsat_clauses = []
        for clause in range(len(self.formula.clauses)):
            if next_state.counter[clause][0] == 0:
                unsat_clauses.append(clause)
        if not unsat_clauses:
            return self.__greedy_next(current_state)
        unsat_clause = self.formula.clauses[choice(unsat_clauses)]
        if random() > 0.5: #random move
            return self._flip(next_state, choice(unsat_clause.literals).var), None
        else: #greedy move
            best_score = -1
            best_variable = 0
            best_variables = []
            for literal in unsat_clause.literals:
                next_state = self._flip(next_state, literal.var)
                score = self._evaluate(next_state)
                next_state = self._flip(next_state, literal.var)
                if score > best_score:
                    best_score = score
                    best_variable = literal.var
                    best_variables.clear()
                    best_variables.append(literal.var)
                elif score == best_score:
                    best_variables.append(literal.var)
            if best_variable:
                return self._flip(next_state, choice(best_variables)), None
            else:
                return self._flip(next_state, choice(unsat_clause.literals).var), None

    """
    State manipulation methods
    """
    def _compute_counter(self, assignment):
        """
        Adjust counter data structure to correspond to 'assignment'.

        Parameters
        ----------
        assignment : Dict
            key-value pairs where key is variable and value is 0 or 1.

        Returns
        -------
        FormulaClauseCounter
            Updated counter data structure.
        """
        counter = FormulaClauseCounter(self.formula)
        for variable, value in assignment.items():
            for c in self.adj_list[variable][0]:
                counter[c][int(0==value)] += 1
            for c in self.adj_list[variable][1]:
                counter[c][int(1==value)] += 1
        return counter

    def _flip(self, state, variable):
        """
        Flip value of 'variable' and update counters.

        Parameters
        ----------
        state : State
            State where where 'variable' will be flipped.
        variable : int
            Integer index of variable.

        Returns
        -------
        State
            State with value of 'variable' flipped.
        """
        new_value = int (not state.assignment[variable])
        state.assignment[variable] = new_value
        for c in self.adj_list[variable][0]:
            state.counter[c][int(0==new_value)] += 1
            state.counter[c][int(1==new_value)] -= 1
        for c in self.adj_list[variable][1]:
            state.counter[c][int(0==new_value)] -= 1
            state.counter[c][int(1==new_value)] += 1
        return state

    def eval(self, state):
        """
        Compute weight of 'state'.

        Parameters
        ----------
        state : State
            Instance of State class.

        Returns
        -------
        Numeric type
            Weight of assignment of 'state'.
        """
        score = 0
        for var, val in state.assignment.items():
            if val == 1:
                score += self.formula.weights[var]
        return score
