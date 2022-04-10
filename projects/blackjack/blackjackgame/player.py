# Jason Duong
# CPSC 386-03
# 2022-04-11
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 03-00
#
# Player Class Implementation
#


"""A Player Class"""


from enum import Flag, auto
from collections import namedtuple
from .util import Writer, BankruptExecution


Hand = namedtuple("Hand", ["card", "bet", "state", "times"])


class HandState(Flag):
    """Hand State Configuration"""

    __order__ = "WIN BUST PUSH DOUBLE DEFAULT"
    WIN = auto()
    BUST = auto()
    PUSH = auto()
    DOUBLE = auto()
    DEFAULT = auto()


class PlayerState(Flag):
    """Player State Configuration"""

    __order__ = "INSURANCE SPLIT DEFAULT"
    INSURANCE = auto()
    SPLIT = auto()
    DEFAULT = auto()


class Player:
    """A Player Class"""

    write = Writer().slow

    def __init__(self, name, game=None, bank=10000.0):
        self._name = name
        self._game = game
        self._balance = [bank, 0]
        self._state = PlayerState.DEFAULT

        self._active = 0
        self._hand = [Hand([], bet=None, state=HandState.DEFAULT, times=0)]

    def __str__(self):
        """returns a list of the player's hand"""
        return "  ".join([str(card) for card in self.curr.card])

    def __len__(self):
        """returns the player hand's length"""
        return len(self._hand)

    @property
    def name(self):
        """returns a reference of the player's name"""
        return self._name

    @property
    def bank(self):
        """returns a reference of the player's balance"""
        return self._balance[0]

    @bank.setter
    def bank(self, value=0.0):
        """sets the value of the player's bank"""
        if value < 0:
            raise ValueError("Expected Positive Number")
        self._balance[0] = value

    @property
    def active(self):
        """returns the player active hand"""
        return self._active

    @active.setter
    def active(self, value=0):
        """sets the value of the active variable"""
        if not isinstance(value, int):
            raise TypeError("Expected Whole Number")
        if value < 0:
            raise IndexError("Expected Positive Number")
        self._active = value

    @property
    def hand(self):
        """returns a reference of the player's current hand"""
        return self._hand

    @property
    def curr(self):
        """returns a reference of the player's current hand"""
        return self._hand[self._active]

    @property
    def pstate(self):
        """returns a reference of the player's hand state"""
        return self._state

    @pstate.setter
    def pstate(self, value=PlayerState.DEFAULT):
        """sets the value of the player's state"""
        self._state = value

    @property
    def hstate(self):
        """returns a reference of the player's hand state"""
        return self.curr.state

    @hstate.setter
    def hstate(self, value=HandState.DEFAULT):
        """sets the value of the player's hand state"""
        self._hand[self._active] = self.curr._replace(state=value)

    @property
    def times(self):
        """returns a reference to the number of times a player bet"""
        return self.curr.times

    @times.setter
    def times(self, value=0):
        """sets the value of the number of time sa player bet"""
        if value < 0:
            raise ValueError("Expected Positive Number")
        self._hand[self._active] = self.curr._replace(times=value)

    @property
    def bet(self):
        """returns a reference of the player's wager"""
        return self.curr.bet

    @bet.setter
    def bet(self, value=None):
        """modifies the player's wager"""
        if value is not None and value < 0:
            raise ValueError("Expected Positive Number")
        self._hand[self._active] = self.curr._replace(bet=value)

    @property
    def insurance(self):
        """returns a reference of the player's wager"""
        return self._balance[1]

    @insurance.setter
    def insurance(self, value=0):
        """adds an additional bet as insurance"""
        if value < 0:
            raise ValueError("Expected Positive Number")
        self._balance[1] = value

    def empty_hand(self):
        """resets a player's state"""
        self._active, self._balance[1] = 0, 0
        self._state = PlayerState.DEFAULT
        self._hand = [Hand([], bet=None, state=HandState.DEFAULT, times=0)]

    def sum_hand(self):
        """returns the player's hand cost"""
        total = sum(list(map(int, self.curr.card)))
        num_of_aces = sum(
            card.rank == "Ace" and card.status for card in self.curr.card
        )

        if num_of_aces:
            total -= 10 * (num_of_aces - 1)
            if total > 21:
                total -= 10

        return total

    def has_blackjack(self):
        """returns true of the player has 21 given an Ace and a rank 10"""
        return len(self.curr.card) == 2 and set(map(int, self.curr.card)) == {
            11,
            10,
        }

    def has_equal_hand(self):
        """returns true if the player's hand is of equal ranks"""
        return all(
            card.rank == self.curr.card[0].rank for card in self.curr.card
        )

    def has_insurance(self):
        """returns true if the player took insurance"""
        return PlayerState.INSURANCE in self._state

    def has_doubled_down(self):
        """returns true if the player doubled-down"""
        return HandState.DOUBLE in self.hstate

    def has_split(self):
        """returns true if the player splitted"""
        return PlayerState.SPLIT in self._state

    def is_busted(self):
        """returns if the player's hand is over 21"""
        return self.sum_hand() > 21

    def will_hit(self, value=0):
        """adds a new card to the player's hand"""
        self.write(f"{self._name} was dealt a {str(value)}")
        self.curr.card.append(value)
        if self.is_busted():
            self.write(f"{self._name} got busted")
        return self.is_busted()

    def will_double_down(self):
        """doubles the player's bet and the player hits once"""
        self.bet *= 2
        self.will_hit(self._game.deck.deal()[0])
        return True

    def will_split(self):
        """splits the player's hand"""
        item = [self.curr.card.pop()]
        value = self._game.deck.deal(3)
        self._hand.append(
            Hand(item, bet=self.bet, state=HandState.DEFAULT, times=0)
        )

        for num in range(len(self)):
            self.active = num
            self.write(f"Hand #{num + 1} - ", key="")
            self.will_hit(value[num])
        self.active = 0


class Dealer(Player):
    """A Dealer Class"""

    def __init__(self, game=None):
        super().__init__("House", game, float("inf"))

    def all_busted(self):
        """returns if all players lost"""
        return all(player.is_busted() for player in self._game.players[:-1])

    def shuffle(self, num=1):
        """randomly reorders the decks"""
        self._game.deck.shuffle(num)

    def cut(self):
        """approximately slices the deck from the middle"""
        self._game.deck.cut()

    def will_deal(self):
        """deals two cards to each player"""
        for cycle in range(2):
            for player in self._game.players:
                value = self._game.deck.deal()[0]

                if player == self and cycle == 1:
                    value = self._game.deck.flip_card(value)

                self.write(f"{player.name} was dealt a {value!s}")
                player.curr.card.append(value)

    def will_hit(self, value=0):
        """adds a new card to the dealer's hand"""
        if not self.all_busted():
            while self.sum_hand() < 17:
                super(Dealer, self).will_hit(self._game.deck.deal()[0])
                self.write(str(self._game) + "\n")

    def evaluate(self):
        """dealer decides whether players won/lost/push"""
        for player in self._game.players[:-1]:
            player.active = 0
            for key in range(len(player.hand)):
                player.active = key

                if player.is_busted():
                    player.hstate |= HandState.BUST
                elif self.is_busted():
                    player.hstate |= HandState.WIN
                elif player.sum_hand() < self.sum_hand():
                    player.hstate |= HandState.BUST
                elif player.sum_hand() > self.sum_hand():
                    player.hstate |= HandState.WIN
                else:
                    player.hstate |= HandState.PUSH

                if HandState.WIN in player.hstate:
                    self.make_pay(player)
                elif HandState.BUST in player.hstate:
                    self.make_charge(player)
                elif HandState.PUSH in player.hstate:
                    self.write(f"{player.name} got pushed on hand #{key + 1}")

                if player.insurance != 0:
                    if self.has_blackjack():
                        self.make_pay(player, key="side")
                    else:
                        self.make_charge(player, key="side")

                if player.bank <= 0:
                    player.bank = 10000.0

            player.empty_hand()
        self.empty_hand()
        self.write()

    def offer_insurance(self, player):
        """asks the player if they want insurance"""
        answer = input(self.write("Buy Insurance? (Y/N): ", key="")).upper()
        if answer not in ["Y", "N"]:
            raise AttributeError("Invalid Input")
        if answer == "Y":
            limit = player.bank - player.bet
            side_bet = self._game.ask_bet(player, limit)
            try:
                if side_bet < 1 or side_bet > limit:
                    raise BankruptExecution(player.name)
                player.insurance = side_bet
                return True
            except BankruptExecution as inst:
                self.write(str(inst))
        return False

    def make_pay(self, player, key="initial"):
        """pays the winning player 2-to-1 for wager"""
        money = player.insurance if key == "side" else player.bet
        self.write(
            f"{player.name} earned ${money} on their "
            f"{key}-bet on hand #{player.active + 1}"
        )
        player.bank += money

    def make_charge(self, player, key="initial"):
        """subtracts the lossing player's wager"""
        money = player.insurance if key == "side" else player.bet
        self.write(
            f"{player.name} lost ${money} on their "
            f"{key}-bet on hand #{player.active + 1}"
        )
        player.bank -= money
