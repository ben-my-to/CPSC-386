#!/usr/bin/env python3

'''
2520 is the smallest number that can be divided by each of the numbers from 1 to 10 without any remainder.
What is the smallest positive number that is evenly divisible by all of the numbers from 1 to 20?
'''

def prime_number_product():
    l = [2, 3, 5, 7, 11, 13, 17, 19]
    p = 1
    for i in l:
        p *= i
    return p

def divisible_test(n):
    return sum([n % i for i in range(1, 21)]) == 0

def main():
    n = prime_number_product()
    counter = n
    while True:
        if divisible_test(counter):
            break
        counter += n
    print(counter)

if __name__ == '__main__':
    main()
