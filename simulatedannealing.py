from abc import ABC, abstractmethod
from random import random

import math

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

        best_score = 0
        best_state = None

        for _ in range(RESTART_LIMIT):

            current_state = self._initial_state()
            current_score = self._evaluate(current_state)
            temperature = self._initial_temperature()

            iter_count = 0
            while iter_count < ITER_LIMIT:
                next_state = self._next_state(current_state)
                next_score = self._evaluate(next_state)

                if  next_score > current_score or \
                    random() < math.exp((next_score - current_score)/temperature):
                    current_state = next_state
                    current_score = next_score
                    iter_count = 0
                else:
                    iter_count += 1

                temperature = self._cooling_schedule(temperature)

                if current_score > best_score:
                    best_score = current_score
                    best_state = current_state

        return best_score, best_state

