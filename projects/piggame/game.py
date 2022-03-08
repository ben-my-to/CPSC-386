# Jason Duong
# CPSC 386-03
# 2022-03-06
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 02-00
#
# Game Simulation
#


"""A Game Class"""


import sys
from textwrap import wrap
from .util import Writer
from .player import Player
from .player import AI
from .die import Die


OUT = Writer()


class PigGame:
    """Game Class"""

    def __init__(self):
        self._player = []  # list of player objects
        self._state = None  # the current's player input/decision
        self._turn = 0  # signifies the current player as an index
        self._goal = 30  # the number of points to win

    def __repr__(self):
        """outputs the utility"""
        player = self._player[self._turn]
        return "\t[ Roll: {} | Current: {} | Total: {} | Times: {} ]\n".format(
            player.eval, player.stack, player.score, player.times
        )

    @property
    def state(self):
        """returns a player's state"""
        return self._state

    @property
    def goal(self):
        """returns the goal value"""
        return self._goal

    def terminal(self):
        """determines if the current state is a goal state"""
        return self._player[self._turn].score >= self._goal

    def get_stats(self):
        """returns the game statistics"""
        stat = self._player.copy()
        # sorts players by their score
        stat.sort(key=lambda p: p.score + p.stack, reverse=True)

        OUT << "\nStatisics\n---------\n"
        for place, player in enumerate(stat):
            item = [player.name, player.score, player.stack]
            row = f"{place + 1}. {item[0]} ({item[1] + item[2]})\n"

            if player == self._player[self._turn]:
                row = "▷ " + row  # marker to indicate the current player
            OUT << row

        OUT << "\n"

    def lookup(self, current):
        """returns the opponent's score"""
        if self._player[self._turn] == current:
            lookup = (self._turn + 1) % len(self._player)

        return self._player[lookup]

    def fsm(self, player, action):
        """finite state machine implementation"""

        if action == "r":  # player has decided to roll
            player.eval = Die().roll()

            if player.eval == 1:  # player just lost their turn
                self._state = "<SKIP>"
                player.stack, player.times = 0, 0
            else:
                self._state = "<ROLL>"
                player.stack += player.eval
                player.times += 1
        elif action == "h":  # player has decided to hold
            if player.times == 0:
                sys.exit(OUT << "[ ERROR ]: expected at least one roll\n")

            self._state = "<HOLD>"
            player.eval = None
            player.score += player.stack
            player.stack, player.times = 0, 0
        elif action == "s":  # player decided to see the scoreboard
            self._state = "<STAT>"
            self.get_stats()
        else:
            sys.exit(OUT << "[ ERROR ]: expected r/h\n")

    def setup(self):
        """initializes the player queue"""

        OUT << "How many players? [1-4] "
        num = int(input())

        if num not in range(1, 5):
            sys.exit(OUT << "[ ERROR ]: expected 1-4 players\n")

        OUT << "Do you want to view the instructions (y/n)? "
        answer = input()

        if answer not in ("y", "n"):
            sys.exit(OUT << "[ ERROR ]: expected y/n\n")

        if answer == "y":
            OUT << "\n"
            OUT << "\n".join(
                wrap(
                    "Here are the rules. Each player rolls his/her"
                    + " die once to determine their turn order. Within"
                    + " a player's turn, no other players are allowed"
                    + " to play, turn-based. The current player will"
                    + " roll until his/her turn is over. The player turn's end"
                    + " by either a non-preemptively hold or if he/she"
                    + " rolls a one. if the current player decides to"
                    + " hold, his/her temporary score is accumulated to their"
                    + " total score. Otherwise, if the current player rolls"
                    + " a one, their temporary score is dropped; meaning,"
                    + " the current player's total score was not affected"
                    + " for his/her turn. The winner is the first player"
                    + " to receive a total score of at least 30."
                    + " To roll, enter 'r' on the keyboard."
                    + " To hold, enter 'h' on the keyboard."
                    + " To display the game statistics,"
                    + " enter 's' on the keyboard."
                )
            )
            OUT << "\n"

        for player in range(num):
            OUT << f"\nEnter Player #{player + 1}'s Name: "
            name = input()
            OUT << "Press enter to roll."
            input()
            order = Die().roll()
            OUT << f"\n{name} rolled a {order}\n"
            self._player.append(Player(name, order, self))

        if num == 1:
            order = Die().roll()
            self._player.append(AI(order, self))
            OUT << f"{self._player[num].name} rolled a {order}\n"

        # sorts the players according to what they rolled in decending order
        self._player.sort(key=lambda p: p.order, reverse=True)

        OUT << "\nORDER\n-----\n"
        for counter, player in enumerate(self._player):
            OUT << f"{counter + 1}. {player.name} ({player.order})\n"
        OUT << "\n"

    def run(self):
        """Starts the Game"""

        while True:
            player = self._player[self._turn]
            player.move()

            if self.terminal():  # goal state is reached
                break

            if self._state != "<STAT>":  # do not output if no roll made
                OUT << self

            if self._state in ("<SKIP>", "<HOLD>"):  # either hold or lost turn
                self._turn = (self._turn + 1) % len(self._player)

        OUT << f"\n[ WINNER ]: {self._player[self._turn].name}\n"
