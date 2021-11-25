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
    def __init__(
        self,
        formula,
        iter_limit,
        restart_limit,
        alpha = 0.99,
        beta = 0,
        temp_prob = 0.8,
        init_state = '',
        next_state = ''
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
        pass

    def _initial_temperature(self):
        pass
