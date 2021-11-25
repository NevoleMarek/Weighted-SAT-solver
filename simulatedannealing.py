from abc import ABC, abstractmethod
from random import random

import math

from utils import FormulaAdjacencyList

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

    init_state : str, optional
        Method used in initial state generation, by default 'zero'.
        Possible values:
        - 'zero' all variables set to value 0 (False)
        - 'one' all variables set to value 1 (True)

    next_state : str, optional
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
        init_state = 'zero',
        next_state = 'random'
    ):

        super().__init__(
            iter_limit,
            restart_limit
        )
        self.formula = formula
        self.alpha = alpha
        self.beta = beta
        self.temp_prob = temp_prob
        self.eval = eval
        self.init_state = init_state
        self.next_state = next_state
        self.adj_list = FormulaAdjacencyList(formula)
        self.clause_weight = sum(formula.weights) + 1

    def _initial_state(self):
        pass

    def _evaluate(self, state):
        pass

    def _next_state(self, current_state):
        pass

    def _cooling_schedule(self, temperature):
        return self.alpha * temperature + self.beta

    def _initial_temperature(self):
        pass
