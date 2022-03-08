![Header](../../actions/workflows/py-header.yml/badge.svg)
![Lint](../../actions/workflows/py-lint.yml/badge.svg)
![Format](../../actions/workflows/py-format.yml/badge.svg)

# Pig - A Die Game

The objectives of this exercise are:

* Verify that a student's development environment is set up
* Refresh our memory on how to write a program to a specification
* Improving our programming practices
* Learn about the Python programming language and it's standard library

We shall all write the dice game named [Pig](https://en.wikipedia.org/wiki/Pig_(dice_game)). Pig is a game that is probably quite old and was first described in print by [John Scarne](https://en.wikipedia.org/wiki/John_Scarne) (famous for [Scarne's four aces trick](https://youtu.be/0Zmy2WlbSpg)).

The game uses only one six sided die and is played with 2 or more players. Players take turns rolling the die and tabulating a score according to the rules. The first player to score 100 or more points wins.

In our version of the game, we shall make a few changes to the rules. Since it is a computer based game, the six-sided die is simulated by the computer. Additionally, the game can be played against the computer should there only be one player. If there is more than one player, the game is played as a [hotseat](https://en.wikipedia.org/wiki/Hotseat_(multiplayer_mode)) multiplayer game. And to win the game, a player must score 30 points.

## Rules

* There is at least two players playing the game and at most four.
* To start the game, a player can enter the number 1 through 4 to establish how many players there are. If a player enters 1, then the other player is a _computer AI_.
* When the player enteres 2 or more players, then the _computer AI_ is not used as a player.
* There is one six-sided die (simulated by the game using a psuedo-random number generator); the faces of the die are numbered 1, 2, 3, 4, 5, and 6.
* The game is turn based.
* All players have a name, including the _computer AI_.
* The player who goes first is selected by each player rolling the die once. The players are ordered in ascending order given the number they rolled. If there is a tie between two or more players, the computer can break the tie by arbitrarily assigning that player to a position not less than the position the player rolled.
* Once each player has had a turn in ascending order, the turn returns to the first player. (The process is a circular queue.)
* Each turn, a player rolls the die.
    * The current player rolls the die until their turn ends. All other players wait their turn. A turn ends when a player rolls a 1 or chooses to hold.
    * If the player rolls a 1, the player scores nothing that turn and it becomes the next player's turn. The player's overall score does not change because the player has lost the points accrued during their turn.
    * If the player rolls any other number, the value of the die is added to their turn's score as points and the player's turn may continue. The player's overall score does not change until their turn ends.
    * If a player chooses to hold, their turn score total is added to their score, and it becomes the next player's turn.
* The player may not choose to hold until after the die has been rolled at least once.
* The game ends when a player ends their turn with a score of 30 points or greater.
* At the beginning of every die roll, the game displays the current player's total score, current turn score, and how many times the player has rolled. Once the die is rolled, the computer displays the value of the die. If it is a 1, the computer ends the current player's turn and moves on to the next player.

## Requirements

The requirements of the program are that the game must play according to the rules given above. If there is any ambiguity of the rules, the the student should discuss the rules with the instructor to clarify the rules.

The game must be written in Python 3. Limit your game to use only what is available in the Python Standard Library. Do not use additional Python modules that are outside of the Python Standard Library.

To run the game, the command must be `./pig.py`. This means that the file `pig.py` must have a shebang and call the main game loop. This file contains only a call to the game's main loop which is defined in the `piggame` package.

The game's logic must be defined in a package named `piggame`. This means there must be a directory named `piggame` which contains all the Python source code for the project. At a minnimum, the following files must be included in the `piggame` package:
* `__init__.py`
* `die.py`
* `game.py`
* `player.py`

The file `__init__.py` can be a very simple file which defines an `__all__` variable for the package. See the documentation about [Python modules](https://docs.python.org/3/tutorial/modules.html), specifically [Section 6.4.1. Importing * From a Package](https://docs.python.org/3/tutorial/modules.html#importing-from-a-package).

The file `die.py` defines a six sided die class and any other supporting classes and functions.

The file `game.py` defines the game loop and any other supporting classes and functions needed to realize the game. The game loop may be defined as a funciton or as a class.

The file `player.py` defines the human player class, the _computer AI_, and the circular player queue class. Additional classes and functions related to the players may be included as well.

The source file that is the executable file shall be named `pig.py`, and it shall be executable with a shebang at the top of the file.

The user interface of the game is text. There are no graphics (2D, 3D, sprites, etc.) in this game.

If you would like to use audio effects or a soundtrack, you may however the program may only use what's available in the Python Standard Library.

The _computer AI_ player does not need to be a sophisticated machine. You may make the _computer AI_ as simple or as sophisticated as you like. However, the _computer AI_ should not appear to be unpredictable. The _computer AI_ may be defined as a separate class, a sub-class of the player class, or a special case of the player class. Since all players have a name, the _computer AI_ must be named as well.

Since this game is a terminal based game, use [sleep](https://docs.python.org/3/library/time.html?highlight=sleep#time.sleep) or other similar mechanism to slow down the game to make the text appear on the screen slowly. Give the player an opportunity to read the text. A typewriter effect can be achieved with some creative use `time.sleep` with values less than 1 second.

## Don't Forget

Please remember that:

* You need to put a header in every file per the [instructions](https://docs.google.com/document/d/1OgC3_82oZHpTvoemGXu84FAdnshve4BCvtwaXZEJ9FY/edit?usp=sharing) shared in Canvas.
* You need to follow [PEP-8](https://www.python.org/dev/peps/pep-0008/); use linters and style checkers such as `pycodestyle`, `pylint`, and `black`.
* You need to test your program. If it does not run correctly or if it unplayable then your project will receive poor marks.

# Rubric

This exercise is worth 10 points. There is a total of 10 points possible. Your program must not have any syntax errors before it is graded. Submissions that have a syntax error or throw an uncaught exception will be assigned a score of 0.
* Functionality (6 points): Your submission shall be assessed for the appropriate constructs and strategies to address the exercise. A program the passes the instructor's tests completely receives full marks. A program that partially passes the instructors tests receives partial-marks. A program that fails the majority or all the tests receives no marks.
    * A game that does not have a _computer AI_ player forfeits all marks.
    * A game that is not multiplayer looses 3 points
    * A game that is not defined in separate files using a Python package per the requirements looses 5 points.
    * A game that does not execute with the command `./pig.py` looses 3 points.
    * A project that does not have the required individual files looses 4 points.
    * Partial implementation of the rules shall loose 1-5 points depending on the number of requirements not met.
* Format & Readability (4 point): Your submission shall be assessed by checking whether your code passess the style and format check, as well as how well it follows the proper naming conventions, and internal documentation guidelines. Git log messages are an integral part of how readable your project is. Failure to include a header forfeits all marks. Not conforming to PEP-8 forfeits all marks.

