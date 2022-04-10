# Jason Duong
# CPSC 386-03
# 2022-04-11
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 03-00
#
# Utilities Files
#


"""Function Utilites to support BlackJack"""


from time import sleep


class BankruptExecution(Exception):
    """Player does not have sufficient funds"""

    def __init__(self, target, message=" has insufficient funds"):
        super().__init__(message)
        self._target = target
        self._message = message

    def __str__(self):
        """returns the error message to the player"""
        return self._target + self._message


class Writer:
    """Writer Class"""

    def __init__(self, speed=0.15):
        self._speed = speed

    def slow(self, stream="", key="\n"):
        """simulates a typewriter effect"""
        for text in str(stream):
            sleep(self._speed)
            print(text, end="", flush=True)
        print(end=key)
        return ""
