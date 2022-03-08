#!/usr/bin/env python3
# Jason Duong
# CPSC 386-03
# 2022-03-06
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 02-00
#
# Main Application File
#


"""Pig - A Die Game"""


from piggame import *


if __name__ == "__main__":
    PIG = game.PigGame()
    PIG.setup()
    PIG.run()
