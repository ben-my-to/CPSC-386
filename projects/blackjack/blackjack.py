#!/usr/bin/env python3
# Jason Duong
# CPSC 386-03
# 2022-04-11
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 03-00
#
# Main Application File
#


'''Application Startup File'''


from blackjackgame import *


if __name__ == '__main__':
    APP = game.BlackJack()
    APP.run()
