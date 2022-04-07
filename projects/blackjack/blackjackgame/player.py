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


from collections import namedtuple
from enum import Enum, Flag, auto
from .util import Writer


Hand = namedtuple("Hand", ["card", "bet", "state"])


class HandState(Enum):
    """Hand State Configuration"""

    WIN = auto()
    BUST = auto()
    PUSH = auto()


class PlayerState(Flag):
    """Player State Configuration"""

    NULL = auto()
    INSURANCE = auto()
    SPLIT = auto()
    DOUBLE = auto()


class Player():
    """A Player Class"""

    write = Writer().slow

    def __init__(self, name, game=None, bank=10000.0):
        self._name = name
        self._game = game
        self._bank = [bank, None]
        self._state = PlayerState.NULL

        self._active = 0
        self._hand = [Hand([], bet=None, state=None)]

    def __str__(self):
        """returns a list of the player's hand"""
        return "  ".join([str(card) for card in self.curr.card])

    @property
    def name(self):
        """returns a reference of the player's name"""
        return self._name

    @property
    def bank(self):
        """returns a reference of the player's balance"""
        return self._bank[0]

    @bank.setter
    def bank(self, value=0.0):
        """sets the value of the player's bank"""
        self._bank[0] = value

    @property
    def active(self):
        """returns the player active hand"""
        return self._active

    @active.setter
    def active(self, value=0):
        """sets the value of the active variable"""
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
    def pstate(self, value=None):
        """sets the value of the player's state"""
        self._state = value

    @property
    def hstate(self):
        """returns a reference of the player's hand state"""
        return self.curr.state

    @hstate.setter
    def hstate(self, value=None):
        """sets the value of the player's hand state"""
        self._hand[self._active] = self.curr._replace(state=value)

    @property
    def bet(self):
        """returns a reference of the player's wager"""
        return self.curr.bet

    @bet.setter
    def bet(self, value=None):
        """modifies the player's wager"""
        self._hand[self._active] = self.curr._replace(bet=value)

    @property
    def insurance(self):
        """returns a reference of the player's wager"""
        return self._bank[1]

    @insurance.setter
    def buy_insurance(self, value=None):
        """adds an additional bet as insurance"""
        self._bank[1] = value

    def empty_hand(self):
        """resets a player's state"""
        self._active = 0
        self._bank[1] = None
        self._state = PlayerState.NULL
        self._hand = [Hand([], bet=None, state=None)]

    def sum_hand(self):
        """returns the player's hand cost"""
        total = sum(list(map(int, self.curr.card)))
        num_of_aces = sum(
            list(
                map(
                    lambda card: card.rank == "Ace" and card.status,
                    self.curr.card,
                )
            )
        )

        if total > 21 and num_of_aces > 0:
            total -= 10
        if num_of_aces > 1:
            total -= 10 * (num_of_aces - 1)

        return total

    def equal_hand(self):
        """returns true if the player's hand is of equal ranks"""
        return all(
            card.rank == self.curr.card[0].rank for card in self.curr.card
        )

    def has_blackjack(self):
        """returns true of the player has 21 given an Ace and a rank 10"""
        return len(self.curr.card) == 2 and \
            set(map(int, self.curr.card)) == {11, 10}

    def has_insurance(self):
        """returns true if the player took insurance"""
        return PlayerState.INSURANCE in self._state

    def is_busted(self):
        """returns if the player's hand is over 21"""
        return self.sum_hand() > 21

    def will_hit(self, value=0):
        """adds a new card to the player's hand"""
        self.write(f"{self._name} was dealt a {str(value)}")
        self.curr.card.append(value)
        if self.is_busted():
            self.write(f"{self._name} got busted")

    def will_double_down(self):
        """doubles the player's bet and the player hits once"""
        self.bet *= 2
        self.will_hit(self._game.deck.deal()[0])

    def will_split(self, value=1):
        """splits the player's hand"""
        item = [self.curr.card.pop()]
        self._hand.append(Hand(item, bet=value, state=None))


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
        deck = self._game.deck
        for cycle in range(2):
            for player in self._game.players:
                value = deck.deal()[0]

                if player == self and cycle == 1:
                    value = deck.flip_card(value)

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
            for key in range(0, len(player.hand)):
                player.active = key

                if player.is_busted():
                    player.hstate = HandState.BUST
                elif self.is_busted():
                    player.hstate = HandState.WIN
                elif player.sum_hand() < self.sum_hand():
                    player.hstate = HandState.BUST
                elif player.sum_hand() > self.sum_hand():
                    player.hstate = HandState.WIN
                else:
                    player.hstate = HandState.PUSH

                if player.hstate == HandState.WIN:
                    self.write("[INITIAL BET]")
                    self.make_pay(player)
                elif player.hstate == HandState.BUST:
                    self.write("[INITIAL BET]")
                    self.make_charge(player)
                elif player.hstate == HandState.PUSH:
                    self.write(f"{player.name} got pushed")

                if PlayerState.INSURANCE in player.pstate:
                    self.write("[INSURANCE]")
                    if self.has_blackjack():
                        self.make_pay(player)
                    else:
                        self.make_charge(player)

                if player.bank <= 0:
                    player.bank = 10000.0

                player.empty_hand()
        self.empty_hand()
        self.write()

    def make_pay(self, player):
        """pays the winning player double their wager"""
        self.write(f"{player.name} earned ${player.bet * 2.0}")
        player.bank += player.bet * 2.0

    def make_charge(self, player):
        """subtracts the lossing player's wager"""
        self.write(f"{player.name} lost ${player.bet}")
        player.bank -= player.bet

    def offer_insurance(self, player):
        """asks the player if they want insurance"""
        answer = input(self.write("Buy Insurance? (Y/N): ", key="")).upper()
        if answer not in ["Y", "N"]:
            raise AttributeError("Invalid Input")
        if answer == "Y":
            side_bet = self._game.ask_bet(player)
            if side_bet < 1 or side_bet > player.bank - player.bet:
                self.write(f"{player.name} has insufficient funds")
            else:
                player.buy_insurance = side_bet
