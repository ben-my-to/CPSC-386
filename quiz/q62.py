#!/usr/bin/env python3

from math import prod
import time


def eratosthenes(n):
    '''yields the sequence of prime numbers via the Sieve of Eratosthenes up to n'''
    yield 2
    D = {}  # map composite integers to primes witnessing their compositeness
    q = 3  # first integer to test for primality
    while q < n:
        p = D.pop(q, None)
        if p:
            x = p + q
            while x in D:
                x += p
            D[x] = p
        else:
            yield q
            D[q * q] = 2 * q
        q += 2


class NGenerator:
    def __init__(self, n):
        self.a = 0
        self.n = n

    def __iter__(self):
        while True:
            self.a += self.n
            yield self.a


def test(x):
    rv = True
    for i in range(3, 21):
        if x % i != 0:
            rv = False
            break
    return rv


def main():
    start = time.perf_counter()
    l = [x for x in eratosthenes(20)]
    p = prod(l)
    for i in NGenerator(p):
        if test(i):
            break
    end = time.perf_counter()
    print(
        f'{i} is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20'
    )
    print('Elapsed time: {} seconds'.format(end - start))


if __name__ == '__main__':
  main()
