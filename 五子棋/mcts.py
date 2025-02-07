import random
import numpy as np
from game import State, Player

from typing import Union


class TreeNode(object):
    """A node in the MCTS tree. Each node keeps track of its total utility U, and its visit-count n_visit.
    """

    def __init__(self, parent: Union['TreeNode', None], all_actions):
        """
        Parameters:
            parent (TreeNode | None): the parent node of the new node.
            state (State): the state corresponding to the new node.
        """
        self.parent = parent
        self.all_actions = all_actions
        self.children = {}  # a map from action to TreeNode
        self.n_visits = 0
        self.U = 0  # total utility

    def expand(self, action, next_all_actions):
        """
        Expand tree by creating a new child.

        Parameters:
            action: the action taken to achieve the child.
            next_all_actions: the actions available in the next state.
        """
        self.children[action] = TreeNode(self, next_all_actions)

    def get_ucb(self, c):
        """Calculate and return the ucb value for this node **in the parent's perspective**.
        It is a combination of leaf evaluations U/N and the ``uncertainty'' from the number
        of visits of this node and its parent.

        Parameters:
            c: the trade-off hyperparameter.
        
        Note:
            Since U is in current node's perspective, a negation is required (already added).
        """
        U, N = -self.U, self.n_visits
        # TODO
        pass

    def select(self, c):
        """Select action among children that gives maximum UCB value.

        Parameters:
            c: the hyperparameter in the UCB value.

        Return: A tuple of (action, next_node)
        """
        # TODO
        pass

    def update(self, leaf_value):
        """
        Update node values from leaf evaluation.

        Parameters:
            leaf_value: the value of subtree evaluation from the current player's perspective.
        """
        # TODO
        pass

    def update_recursive(self, leaf_value):
        """
        Similar to update(), but applied recursively for all ancestors.
        """
        # If it is not root, this node's parent should be updated first.
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_unexpanded_actions(self):
        return list(set(self.all_actions) - set(self.children.keys()))


class MCTS(object):
    """A simple implementation of Monte Carlo Tree Search."""

    def __init__(self, start_state: State, c=1):
        """
        Parameters:
            start_state: the current state of the game to start the search from.
            c: the hyperparameter in the UCB value.
        """
        self.start_state = start_state
        self.root = TreeNode(None, start_state.get_all_actions())
        self.c = c

    def get_leaf_value(self, state: State):
        """
        Perform random playout until the end of the game, returning +1 if the current
        player wins, -1 if the opponent wins, and 0 if it is a tie.

        Note: the value should be under the perspective of state.get_current_player()
        """
        # TODO
        pass

    def sample(self, state: State):
        """
        Run a single sample loop, including:
        - Selection: select nodes according to UCB values among all expanded children.
        - Expansion: expand the tree by adding a new child node.
        - Simulation: run a simulation from the new child node by random playout.
        - Backpropagation: propagate the simulation result back to the root node.
        """
        node = self.root
        while not state.game_end()[0]:
            unexpanded_actions = node.get_unexpanded_actions()
            if len(unexpanded_actions) == 0:
                # Selection
                action, node = node.select(self.c)
                state = state.get_next_state(action)
            else:
                # Expansion
                action = random.choice(unexpanded_actions)
                state = state.get_next_state(action)
                node.expand(action, state.get_all_actions())
                node = node.children[action]
                break

        # Simulation
        leaf_value = self.get_leaf_value(state)

        # Backpropagation
        node.update_recursive(leaf_value)


class MCTSPlayer(Player):
    """AI player based on MCTS"""
    def __init__(self, c=1, n_sample=5000):
        super().__init__()
        self.c = c
        self.n_sample = n_sample
    
    def create_algorithm(self, state: State):
        return MCTS(state, self.c)

    def get_action(self, state: State):
        mcts = self.create_algorithm(state)
        # TODO
        pass
