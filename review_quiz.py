#!/usr/bin/env python3

# Quiz 6 - #2

def prime_number_product():
    l = [2, 3, 5, 7, 11, 13, 17, 19]
    p = 1
    for i in l:
        p *= i
    return p

def divisible_test(n):
    for i in range(1, 21):
        if n % i:
            return False
    return True

def divisible_testx(n):
    return sum([n % i for i in range(1, 21)]) == 0

def main():
    n = prime_number_product()
    counter = n
    while True:
        if divisible_test(counter):
            break
        counter += n
    print(counter)

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


def collatz_iterative(n, l):
    while n != 1:
        if n & 1:
            # odd
            n = 3 * n + 1
        else:
            # even
            n //= 2
        l.append(n)


if __name__ == '__main__':
    d = {}
    for i in range(1, 101):
        val = i
        val = 8
        m = []
        m.append(val)
        collatz(val, m)
        d[val] = len(m)

    print(d)
    # main()

