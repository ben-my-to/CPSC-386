#!/usr/bin/env python3

import cProfile

def palindrome_test(s):
  return s == s[::-1]

def main():
  max_palindrome = -1
  for i in range(100, 1000):
    for j in range(100, 1000):
      n = i * j
      if palindrome_test(str(n)) and max_palindrome < n:
        max_palindrome = n
  print(max_palindrome)

if __name__ == '__main__':
  cProfile.run('main()')

main()
