#!usr/bin/env python3


from collections import namedtuple
from random import shuffle, randrange


Card = namedtuple('Card', ['rank', 'suit'])


def stringify_card(c):
    return '{} of {}'.format(c.rank, c.suit)


Card.__str__ = stringify_card


class Deck:
    ranks = ['Ace'] + [str(x) for x in range(2, 11)] + \
        'Jack Queen King'.split()
    suits = 'Clubs Hearts Spades Diamonds'.split()
    values = dict(zip(ranks, range(1, 14)))

    def __init__(self):
        self._cards = [Card(rank, suit) \
            for suit in self.suits for rank in self.ranks]

    def __str__(self):
        return ', '.join(map(str, self._cards))

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)

    def merge(self, the_other_deck):
        self._cards = self._cards + the_other_deck._cards

    def shuffle(self, n=1):
        for _ in range(n):
            shuffle(self._cards)

    def cut(self):
        half_way_point = (len(self._cards) // 2) + randrange(-10, 11)
        tophalf = self._cards[:half_way_point]
        bottomhalf = self._cards[half_way_point:]
        self._cards = bottomhalf + tophalf

    def deal(self, n=1):
        return [self._cards.pop() for _ in range(n)]


def card_value(c):
    return Deck.values[c.rank]


Card.__int__ = card_value


def demo():
    """
    c = Card('7', 'Spades')
    print(c)
    s = str(c)
    print(s)
    """

    d = Deck()

    for _ in range(3):
        d.merge(Deck())

    print(len(d))

    d.shuffle(5)

    hand=d.deal(104)
    print(len(hand))
    print(len(d))

    d.deal(100)

    d = Deck()
    print(d)
    #d.shuffle()
    #d.cut()
    print(d)


    for index in range(len(d)):
        print(int(d[index]))

if __name__ == '__main__':
    demo()
