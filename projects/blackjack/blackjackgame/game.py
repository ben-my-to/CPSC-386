# Jason Duong
# CPSC 386-03
# 2022-04-11
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 03-00
#
# Game Process
#


"""Game Class"""


import pickle
from .cards import Deck
from .player import Player, Dealer, PlayerState
from .util import Writer


class BlackJack:
    """BlackJack Game Class"""

    write = Writer().slow

    def __init__(self):
        self._players = [Dealer(self)]
        self._deck = Deck() * 8
        self._turn = 0

    def __contains__(self, name):
        """check if name already exists in player list"""
        return name in [p.name for p in self._players]

    def __next__(self):
        """returns the next player's turn"""
        self._turn = (self._turn + 1) % len(self._players)
        return self._players[self._turn]

    def __len__(self):
        """returns the number of players"""
        return len(self._players)

    def __str__(self):
        """returns a players hand"""
        player, dealer = self._players[self._turn], self._players[-1]

        if player == dealer:
            return "\n".join(
                [f"{p.sum_hand():2}: {p!s}" for p in [dealer]]
            )

        return "\n".join(
            [f"{p.sum_hand():2}: {p!s}" for p in [dealer, player]]
        )

    @property
    def deck(self):
        """returns a reference to the deck"""
        return self._deck

    @property
    def players(self):
        """returns a referene to a list of players"""
        return self._players

    def save_game(self):
        """self.write the list players to the file"""
        player_list = [Player(i.name, i.bank) for i in self._players]
        with open("save.db", "wb") as file_handle:
            pickle.dump(player_list, file_handle, pickle.HIGHEST_PROTOCOL)

    def load_game(self):
        """read the contents of save.db, decode it, and return it as players"""
        with open("save.db", "rb") as file_handle:
            self._players = pickle.load(file_handle)

    def display(self, player):
        """outputs all necessary information on a player's turn"""
        self.write(f"\n----------{player.name}'s Turn----------")
        self.write(str(self))

    def acquire_players(self):
        """retreives a list of players for the game"""
        num = int(input(self.write("How many players? [1-4]: ", key="")))
        if num not in range(1, 5):
            raise ValueError("Invalid Number of Players")

        for player in range(num):
            pid = input(self.write(f"Enter Player #{player + 1}'s Name: ", key=""))
            while pid in self:
                pid = input(
                    self.write(
                        f"The name '{pid}' already exists, "
                        "please choose a different name: ", key=""
                    )
                )
            self._players.insert(len(self)-1, Player(pid, self))

    def ask_bet(self, player):
        """prompts the player for their wager"""
        cash = float(
            input(
                self.write(
                    f"{player.name}, how much do you "
                    f"want to bet [${round(player.bank, 2)}]: ", key=""
                )
            )
        )

        if cash < 1 or cash > player.bank:
            raise ValueError("Invalid Bet")
        return cash

    def check_balance(self, player):
        """checks if there is sufficient funds to double a player's wager"""
        return player.bank > player.bet * 2

    def ask_split(self, player):
        """prompts the player if they want to split their hand"""
        if check_balance:
            choice = input(self.write('Split Hand? (Y/N): ', key="")).upper()
            if choice == "Y":
                bet = self.ask_bet(player)
                player.will_split(bet)
        else:
            self.write(f"{player.name} has insufficient funds")

    def ask_double_down(self, player):
        """prompts the player if they want to double-down"""
        if check_balance:
            choice = input(self.write('Double-Down? (Y/N): ', key="")).upper()
            if choice == "Y":
                player.will_double_down()
        else:
            self.write(f"{player.name} has insufficient funds")
        return choice == "Y"

    def ask_choice(self, player, dealer):
        """prompts the player for their legal moves"""
        if int(dealer.curr.card[0]) >= 10 and not player.has_insurance():
            player.pstate |= PlayerState.INSURANCE
            dealer.offer_insurance(player)
            
        # did_double = False
        # if len(player.curr.card) == 2:
        #    did_double = self.ask_double_down(player)
        #    if player.equal_hand():
        #        self.ask_split(player)
        #
        # if did_double:
        #     return "D"

        if player.has_blackjack():
            self.write(f"\n{player.name} got BlackJack!")
            choice = "S"
        else:
            choice = input(self.write("\n(H)it or (S)tand: ", key="")).upper()

        if choice not in ["H", "S"]:
            raise AttributeError("Invalid Move")
        return choice

    def action(self, player, state):
        """lists the possible actions taken by a player"""
        forward = False

        if state == "H":
            player.will_hit(self._deck.deal()[0])
            if player.is_busted():
                forward = True
        else:
            forward = True

        return forward

    def start_game(self):
        """establishes all player's initial bets prior to any action"""
        if self._deck.needs_shuffling():
            self._deck = Deck() * 8
        self._players[0].shuffle()
        self._players[0].cut()

    def end_game(self):
        """determines which player want to keep playing"""
        hold = [self._players[-1]]
        for player in self._players[:-1]:
            answer = input(
                self.write(f"{player.name}, continue playing? (y/n) ", key="")
            ).upper()

            if answer not in ["Y", "N"]:
                raise AttributeError("Invalid Input")
            if answer == "Y":
                hold.append(player)

        self._turn = 0
        self._players = [player for player in self._players if player in hold]

    def run(self):
        """starts the game"""
        self.start_game()
        self.acquire_players()

        while len(self._players) > 1:
            player, dealer = self._players[0], self._players[-1]

            for current in self._players[:-1]:
                current.bet = self.ask_bet(current)
            self.write()
            dealer.will_deal()

            while player is not dealer:
                self.display(player)

                signal = False
                num_of_hands = len(player.hand)
                for key in range(0, num_of_hands):
                    player.active = key
                    choice = self.ask_choice(player, dealer)
                    signal = self.action(player, choice)
                    num_of_hands = len(player.hand)
                if signal:
                    player = self.__next__()

            self.write(f"\n----------{player.name}'s Turn----------")
            player.curr.card[1] = self._deck.flip_card(player.curr.card[1])
            self.write(
                f"{player.name} flipped over a {player.curr.card[1]}"
            )

            player.will_hit()
            player.evaluate()

            self.save_game()
            self.end_game()
