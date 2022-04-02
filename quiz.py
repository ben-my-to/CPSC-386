#!/usr/bin/env python3


def action(n):
    if n&1:
        return 3*n+1
    else:
        return n/2

if __name__ == '__main__':
    goal = 0
    b = 0

    for state in range(1, 1000000):
        chain = ['e']

        n = state
        while n != 1:
            n = int(action(n))
            chain.append(n)

        if len(chain) > b:
            goal = state
            b = len(chain)

        state -= 1

    print(goal)

