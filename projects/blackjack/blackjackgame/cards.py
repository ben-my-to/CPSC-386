# Jason Duong
# CPSC 386-03
# 2022-04-11
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 03-00
#
# Card Class Implementation
#


"""A Card Class"""


from collections import namedtuple
from random import shuffle, randrange
from math import ceil
from .util import Writer


Card = namedtuple("Card", ["rank", "suit", "status"])


class Deck:
    """A Deck Class holding 52 French-Suited Playing Cards"""

    write = Writer().slow
    suit = "♠ ♥ ♦ ♣".split()
    faceless = [str(x) for x in range(2, 11)]
    rank = ["Ace"] + faceless + "Jack Queen King".split()

    values = [11] + list(range(2, 11)) + [10] * 3
    lookup = dict(zip(rank, values))

    def __init__(self):
        """creates a single deck of 52 playing cards"""
        self._cards = [
            Card(rank, suit, True) for suit in self.suit for rank in self.rank
        ]
        self.place_cut_card()

    def __str__(self):
        """converts the deck into a string format"""
        return ", ".join(map(str, self._cards))

    def __mul__(self, count=1):
        """merges a variable number of decks"""
        if count < 1:
            raise ValueError("Expected Positive Number")

        for _ in range(count - 1):
            self.merge(Deck())
        return self

    def __len__(self):
        """returns the number of cards in the deck"""
        return len(self._cards)

    def __getitem__(self, pos=0):
        """returns the card at a given position"""
        if pos not in range(0, len(self)):
            raise IndexError("Invalid Index")
        return self._cards[pos]

    @property
    def cards(self):
        """returns a reference of the deck object"""
        return self._cards

    def place_cut_card(self):
        """places a cut card between the 60-80 percentile from the bottom"""
        bound = list(map(lambda x: ceil(len(self._cards) * x), [0.6, 0.8]))
        self._marker = randrange(*bound)

    def flip_card(self, card):
        """flip a card to face-up or face-down"""
        return card._replace(status=not card.status)

    def needs_shuffling(self):
        """determines whether the deck needs shuffling"""
        return len(self._cards) <= self._marker

    def merge(self, other_deck):
        """merges the current deck with the new deck set"""
        self._cards = self._cards + other_deck.deal(len(other_deck))
        self.place_cut_card()

    def shuffle(self, count=1):
        """shuffles the deck by a given number of times"""
        self.write("\nShuffling...")
        for _ in range(count):
            shuffle(self._cards)

    def cut(self):
        """cuts the deck at the half-way point with a 20% margin of error"""
        self.write("Cutting...\n")
        margin = ceil(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + randrange(-margin, margin)
        top, bottom = self._cards[:half], self._cards[half:]
        self._cards = bottom + top

    def deal(self, count=1):
        """returns a list of a given number of cards from the top"""
        if count < 0:
            raise ValueError("Expected Positive Number")
        return [self._cards.pop(0) for x in range(count)]


def cardify(card):
    """returns a formated string of a card"""
    return (card.rank + card.suit) if card.status else "🂠"


def card_value(card):
    """returns the numerical value of the given card's rank"""
    if card.status:
        return Deck.lookup[card.rank]
    return 0


def verify(card):
    """returns whether a card is faced up"""
    return card.status


Card.__str__ = cardify
Card.__int__ = card_value
Card.__bool__ = verify
