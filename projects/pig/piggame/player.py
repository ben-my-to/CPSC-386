# Jason Duong
# CPSC 386-03
# 2022-03-06
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 02-00
#
# Player Class Implementation
#


"""A Player Class"""


from .util import Writer


OUT = Writer()


class State:
    """current Player configuration"""

    def __init__(self, name, order):
        self._name, self._order = name, order
        self._score = {"total": 0, "current": 0}
        self._eval = None
        self._times = 0

    @property
    def name(self):
        """returns the name of a player"""
        return self._name

    @property
    def order(self):
        """returns the order of a player"""
        return self._order

    @property
    def stack(self):
        """returns the current score of a player"""
        return self._score["current"]

    @stack.setter
    def stack(self, new_stack):
        """current score setter method"""
        self._score["current"] = new_stack

    @property
    def score(self):
        """returns the total score of a player"""
        return self._score["total"]

    @score.setter
    def score(self, new_total):
        """score setter method"""
        self._score["total"] = new_total

    @property
    def eval(self):
        """returns the eval score of a player"""
        return self._eval

    @eval.setter
    def eval(self, new_eval):
        """eval score setter method"""
        self._eval = new_eval

    @property
    def times(self):
        """returns the number of rolls of a player's turn"""
        return self._times

    @times.setter
    def times(self, new_time):
        """time setter method"""
        self._times = new_time


class Player(State):
    """Player Class"""

    def __init__(self, name, order, game):
        super().__init__(name, order)
        self._game = game  # game object pointer

    def move(self):
        """simulates player moves"""
        OUT << f"{self._name}'s Turn: "
        self._game.fsm(self, input())


class AI(Player):
    """Artificial Intelligence Player Class"""

    def __init__(self, order, game):
        super().__init__("Challenger", order, game)

    def move(self):
        """Simulates AI Move"""
        OUT << f"{self._name}'s Turn: \n"

        # AI wil find the his/her opponent
        opponent = self._game.lookup(self)
        # AI is considered losing if its score is less then its opponent's
        losing = opponent.score >= sum(self._score.values())
        # AI will roll if it has not rolled, won, or currently losing
        choice = losing or self._game.terminal() or self._times == 0

        action = "r" if choice else "h"
        self._game.fsm(self, action)
