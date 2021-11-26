from abc import ABC, abstractmethod
from random import random

import math

from utils import FormulaAdjacencyList, FormulaClauseCounter, State

class SimulatedAnnealing(ABC):
    """ Abstract class of simulated annealing. """
    def __init__(
        self,
        iter_limit = 100,
        restart_limit = 1
    ):
        self._iter_limit = iter_limit
        self._restart_limit = restart_limit

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

    def run(self):
        ITER_LIMIT = self._iter_limit
        RESTART_LIMIT = self._restart_limit
        TEMP = self._initial_temperature()

        best_score = 0
        best_state = None

        for _ in range(RESTART_LIMIT):
            current_state = self._initial_state()
            current_score = self._evaluate(current_state)
            temperature = TEMP

            iter_count = 0
            while iter_count < ITER_LIMIT:
                next_state = self._next_state(current_state)
                next_score = self._evaluate(next_state)

                if  next_score > current_score or \
                    random() < math.exp((next_score - current_score)/temperature):
                    current_state = next_state
                    current_score = next_score
                    iter_count = 0

                    if current_score > best_score:
                        best_score = current_score
                        best_state = current_state
                else:
                    iter_count += 1

                temperature = self._cooling_schedule(temperature)
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

    next_method : str, optional
        Operator used in searching for next state, by default 'random'.
        Possible values:
        - 'random' flip value of random variable
    """
    def __init__(
        self,
        formula,
        iter_limit,
        restart_limit,
        alpha = 0.99,
        beta = 0,
        temp_prob = 0.8,
        init_method = 'zero',
        next_method = 'random'
    ):

        super().__init__(
            iter_limit,
            restart_limit
        )
        self.formula = formula
        self.alpha = alpha
        self.beta = beta
        self.temp_prob = temp_prob
        self.init_method = init_method
        self.next_method = next_method
        self.adj_list = FormulaAdjacencyList(formula)
        self.counter = FormulaClauseCounter(formula)
        self.clause_weight = sum(formula.weights) + 1

        self.init_m = {
            'zero':self.__zero,
            'one':self.__one
        }
        self.next_m = {
            'random':self.__random
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
        for c in self.counter:
            if c[0] > 0:
                score += self.clause_weight
        for var, val in self.assignment.items():
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
        First step is to find maximum delta of clauses that would be satisfied
        and unsatisfied by any variable flip. Which approximates the worst
        possible flip.
        In second step calculate the temperature as if the flip found in step one
        was to be accepted with 'temp_prob' probability.

        Returns
        -------
        Numeric type
            Temperature
        """
        cntr = dict()
        for i in range(self.formula.n_vars):
            idx = i+1
            cntr[idx] = abs(len(self.adj_list[idx]) - len(self.adj_list[-idx]))

        delta = max(cntr.values()) * self.clause_weight
        return abs(delta/math.log(self.temp_prob))

    """
    Initial state methods
    """
    def __zero(self):
        pass

    def __one(self):
        pass

    """
    Next state methods
    """
    def __random(self, current_state):
        pass

