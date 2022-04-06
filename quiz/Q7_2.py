#!/usr/bin/env python3

import cProfile

def collatz(n, d):
  og_n = n
  counter = 1
  if d.get(n, False):
    return d[n]
  else:
    while n != 1:
      counter += 1
      if n % 2 == 0:
        # even
        n = n // 2
      else:
        # odd
        n = (3 * n) + 1
      if d.get(n, False):
        d[og_n] = d[n] + counter
        return d[og_n]
  d[og_n] = counter
  return counter



def main():
  max_count = -1
  special_n = -1
  d = {}
  for x in range(1, 1000000):
    count = collatz(x, d)
    if count > max_count:
      special_n = x
      max_count = count
  print(f'{special_n} {max_count}')

cProfile.run('main()')
main()
