#!/usr/bin/env python3

from collections import namedtuple
from random import shuffle

Card = namedtuple('Card', ['rank', 'suit'])

def stringify_card(c):
    return '{} of {}'.format(c.rank, c.suit)

Card.__str__ = stringify_card

class Deck:
    ranks = ['Ace'] + list(map(str, range(2, 11))) + \
        'Jack Queen King'.split()

    suits = 'Clubs Hearts Spades Diamonds'.split()

    values = list(range(1, 11)) + [10, 10, 10]


    def __init__(self):
        self._cards = [Card(rank, suit)      \
            for suit in Deck.suits           \
            for rank in Deck.ranks]

    def __str__(self):
        return '\n'.join(['{} {}'.format(i, j) \
            for i , j in enumerate(self._cards)])

    def __len__(self):
        return len(self._cards)

    def shuffle(self, n=1):
        for i in range(n):
            shuffle(self._cards)

    def deal(self, n=1):
        return [self._cards.pop() for i in range(n)]


if __name__ == '__main__':
    c = Card('3', 'Diamonds')


    """
    print(ranks)
    print(suits)
    print(c)
    print(str(c))
    print('\n'.join(map(str, cards)))
    """

    d = Deck()
    d.shuffle(3)

    print(d)

    value_dict = dict(zip(Deck.ranks, Deck.values))
    print(value_dict['Queen'])

    hand = d.deal(7)
    print(hand)
    print(d)
