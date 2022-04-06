#!/usr/bin/env python3

def collatz(n, l):
    if n & 1:
        # odd
        n = 3 * n + 1
    else:
        # even
        n //= 2
    l.append(n)
    if n != 1:
        collatz(n,l)

def problem14():
    d = {}
    for i in range(1, (10**6)+1):
        val = i
        m = []
        m.append(val)
        collatz(val, m)
        d[val] = len(m)

    print(d)

if __name__ == '__main__':
    problem14()
