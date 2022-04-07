#!/usr/bin/env python3
# Jason Duong
# CPSC 386-03
# 2022-03-17
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 03-00
#
# I will delete after submitting.
#


'''Just making life easier'''


from os import system
from path import Path


PATH = Path.getcwd() / 'blackjackgame/'
CHECK = ['pycodestyle', 'flake8', 'pylint', 'black --diff']


def sanitize():
    '''lints every file in directory'''

    def color(text):
        print('\n\033[93m{}\033[0m'.format(text), f'{run} {file.relpath()}\n')

    for file in PATH.files('*.py'):
        for run in CHECK[:-1]:
            color('[DEBUG]: ')
            system(f'{run} {file}')

    system(f'wc -l {PATH}*.py')


sanitize()
