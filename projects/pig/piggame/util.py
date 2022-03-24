# Jason Duong
# CPSC 386-03
# 2022-03-06
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 02-00
#
# Utilities Files
#


"""Utilities for Pig Game"""


from time import sleep


class Writer:
    """Writer Class"""

    def __init__(self, speed=0.075):
        self._speed = speed

    def __lshift__(self, stream):
        """simulates a typewriter effect"""
        for text in str(stream):
            sleep(self._speed)
            print(text, end="", flush=True)
