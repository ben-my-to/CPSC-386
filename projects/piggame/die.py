# Jason Duong
# CPSC 386-03
# 2022-03-06
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 02-00
#
# Die Simulation
#


"""A Die Class"""


from random import randrange


class Die:
    """Die Class"""

    def __init__(self, lower=1, upper=7):
        self._lower, self._upper = lower, upper  # die-value range

    def roll(self):
        """simulates the rolling of a die"""
        return randrange(self._lower, self._upper)
