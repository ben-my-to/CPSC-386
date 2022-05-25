#!/usr/bin/env python3
# Jason Duong
# CPSC 386-03
# 2022-05-09
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 05-00
#
# Main Application File.
#


"""Imports the Bounce demo and executes the main function."""


import sys
from random import randint
from game import game


if __name__ == "__main__":
    min_val, max_val = 3, 49

    if len(sys.argv) == 1:
        NUM_BALLS = randint(min_val, max_val)
    elif len(sys.argv) == 2:
        NUM_BALLS = max(min_val, min(int(sys.argv[1]), max_val))
    else:
        sys.exit("Too many arguments.")

    video_game = game.BounceDemo(NUM_BALLS)
    video_game.build_scene_graph()
    video_game.run()
