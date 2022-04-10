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
from .player import Player, Dealer, PlayerState, HandState
from .util import Writer, BankruptExecution


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
            return "\n".join([f"{p.sum_hand()}: {p!s}" for p in [dealer]])
        return "\n".join([f"{p.sum_hand()}: {p!s}" for p in [dealer, player]])

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
        player_list = self._players
        with open("saved_game.bj", "wb") as file_handle:
            pickle.dump(player_list, file_handle, pickle.HIGHEST_PROTOCOL)

    def load_game(self):
        """read the contents of save.db, decode it, and return it as players"""
        try:
            with open("saved_game.bj", "rb") as file_handle:
                self._players = pickle.load(file_handle)
        except FileNotFoundError:
            self.write("No Saved-Game File Detected\n")
            return False
        return True

    def display(self, player):
        """outputs all necessary information on a player's turn"""
        self.write(f"\n----------{player.name}'s Turn----------")
        self.write(str(self))

    def start_game(self):
        """establishes all player's initial bets prior to any action"""
        self._players[-1].shuffle()
        self._players[-1].cut()
        if not self.load_game():
            self.acquire_players()

    def acquire_players(self):
        """retreives a list of players for the game"""
        num = int(input(self.write("How many players? [1-4]: ", key="")))
        if num not in range(1, 5):
            raise ValueError("Invalid Number of Players")

        for player in range(num):
            name = self.request_name(player)
            self._players.insert(len(self) - 1, Player(name, self))

    def request_name(self, player):
        """prompts players for unique names"""
        name = f"Enter Player #{player + 1}'s Name: "
        error = "The name already exists, please choose a different name"
        while True:
            try:
                if (pid := input(self.write(name, key=""))) in self:
                    raise NameError
                return pid
            except NameError:
                self.write(error, key="\n")

    def ask_bet(self, player, arg=None):
        """prompts the player for their wager"""
        if arg is None:
            arg = round(player.bank, 2)
        cash = float(
            input(
                self.write(
                    f"{player.name}, how much do you want to bet [${arg}]: ",
                    key="",
                )
            )
        )

        if cash < 1 or cash > player.bank:
            raise ValueError("Invalid Bet")
        return cash

    def check_balance(self, player, valid=False):
        """checks if there is sufficient funds to double a player's wager"""
        try:
            if player.bank < player.bet * 2:
                raise BankruptExecution(player.name)
            valid = True
        except BankruptExecution as inst:
            self.write(str(inst))
        return valid

    def offer_double_down(self, player):
        """prompts the player if they want to double-down"""
        self.write(f"Hand #{player.active + 1} - ", key="")
        answer = input(self.write("Double-Down? (Y/N): ", key="")).upper()
        if answer not in ["Y", "N"]:
            raise AttributeError("Invalid Input")
        if answer == "Y":
            if self.check_balance(player):
                return player.will_double_down()
        return False

    def ask_split(self, player):
        """prompts the player if they want to split their hand"""

        answer = input(self.write("Split-Hand? (Y/N): ", key="")).upper()
        if answer not in ["Y", "N"]:
            raise AttributeError("Invalid Input")
        if answer == "Y":
            if self.check_balance(player):
                player.will_split()
                return True
        return False

    def ask_choice(self, player, dealer):
        """prompts the player for their legal moves"""
        self.display(player)
        player.times += 1

        if player.has_blackjack():
            self.write(f"\n{player.name} got BlackJack!")

        if int(dealer.curr.card[0]) >= 10 and not player.has_insurance():
            player.pstate |= PlayerState.INSURANCE
            dealer.offer_insurance(player)

        if player.times == 1 and player.has_equal_hand():
            if self.ask_split(player):
                player.pstate |= PlayerState.SPLIT

        if player.times == 1:
            if self.offer_double_down(player):
                player.hstate |= HandState.DOUBLE
                return True
            return False

        if not player.has_blackjack():
            self.write(f"Hand #{player.active + 1} - ", key="")
            choice = input(self.write("(H)it or (S)tand: ", key="")).upper()

            if choice not in ["H", "S"]:
                raise AttributeError("Invalid Move")
            if choice == "H":
                return player.will_hit(self._deck.deal()[0])
        return True

    def ask_multiple_choices(self, player, dealer, start):
        """prompts the player for their legal moves given they splitted"""
        for key in range(start, len(player.hand)):
            player.active = key
            while True:
                advance = self.ask_choice(player, dealer)
                if advance:
                    break
        return advance

    def end_game(self):
        """determines which player want to keep playing"""
        self.save_game()
        self._deck = Deck() * 8
        self._players[-1].shuffle()
        self._players[-1].cut()

        first_player = self._players[0]
        hold = [self._players[-1]]

        for player in self._players[:-1]:
            answer = input(
                self.write(f"{player.name}, continue playing? (y/n) ", key="")
            ).upper()

            if answer not in ["Y", "N"]:
                raise AttributeError("Invalid Input")
            if answer == "Y":
                hold.append(player)

        self._players = [player for player in self._players if player in hold]
        return first_player not in self._players

    def run(self):
        """starts the game"""
        self.start_game()

        player, dealer = self._players[0], self._players[-1]
        while True:
            if self._deck.needs_shuffling():
                if self.end_game():
                    break

            for current in self._players[:-1]:
                current.bet = self.ask_bet(current)

            self.write()
            dealer.will_deal()

            while player is not dealer:
                advance = self.ask_choice(player, dealer)

                if player.has_split():
                    start = 1 if player.has_doubled_down() else 0
                    advance = self.ask_multiple_choices(player, dealer, start)

                if advance:
                    player = self.__next__()

            self.write(f"\n----------{player.name}'s Turn----------")
            player.curr.card[1] = self._deck.flip_card(player.curr.card[1])
            self.write(f"{player.name} flipped over a {player.curr.card[1]}")

            player.will_hit()
            player.evaluate()
            player = self.__next__()
