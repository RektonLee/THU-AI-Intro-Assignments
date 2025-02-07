from game import State
from mcts import MCTS, MCTSPlayer
from typing import Mapping


class AlphaZero(MCTS):
    """
    A modification on pure MCTS, replacing randomly playout with using an evaluation function.
    """
    def __init__(self, start_state: State, evaluation_func: Mapping[State, float], c=1):
        """
        Parameters:
            evaluation_func: a function taking a state as input and
                outputs the value in the current player's perspective.
        """
        super().__init__(start_state, c)
        self.evaluation_func = evaluation_func

    def get_leaf_value(self, state: State):
        # TODO
        pass


class AlphaZeroPlayer(MCTSPlayer):
    """AI player based on AlphaZero"""
    def __init__(self, evaluation_func: Mapping[State, float], c=1, n_sample=5000):
        super().__init__()
        self.evaluation_func = evaluation_func
        self.c = c
        self.n_sample = n_sample
    
    def create_algorithm(self, state: State):
        return AlphaZero(state, self.evaluation_func, self.c)
