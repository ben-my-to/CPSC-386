#!/usr/bin/env python3

import time

def main():
    start = time.perf_counter()
    max = 1000
    three = set(range(3, max, 3))
    five = set(range(5, max, 5))
    union = five | three
    answer = sum(list(union))
    end = time.perf_counter()
    print(
        "The sum of all the multiples of 3 or 5 below {} is {}".format(
            max, answer
        )
    )
    print('Elapsed time: {} seconds'.format(end - start))

if __name__ == '__main__':
    main()
