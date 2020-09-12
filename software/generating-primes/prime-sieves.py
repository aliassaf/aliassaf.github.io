#!/usr/bin/env python3

import itertools
import collections
import heapq

def limited_sieve_opt(limit):
  """ Standard limited sieve of Eratosthenes using an array. """
  yield 2
  composites = [False for i in range(limit)]
  for i in range(3, limit, 2):
    if not composites[i]:
      yield i
      for j in range(i ** 2, limit, 2 * i):
        composites[j] = True

def limited_sieve(limit):
  """ Standard limited sieve of Eratosthenes using a set. """
  composites = set()
  for i in range(2, limit):
    if i not in composites:
      yield i
      for j in range(2 * i, limit, i):
        composites.add(j)

def limited_sieve_square(limit):
  """ Limited sieve with the square optimisation. """
  composites = set()
  for i in range(2, limit):
    if i not in composites:
      yield i
      for j in range(i ** 2, limit, i):
        composites.add(j)

def limited_sieve_odd(limit):
  """ Limited sieve with the odd numbers optimisation. """
  yield 2
  composites = set()
  for i in range(3, limit, 2):
    if i not in composites:
      yield i
      for j in range(3 * i, limit, 2 * i):
        composites.add(j)

def limited_sieve_square_odd(limit):
  yield 2
  composites = set()
  for i in range(3, limit, 2):
    if i not in composites:
      yield i
      for j in range(i ** 2, limit, 2 * i):
        composites.add(j)

def bucket_sieve():
  composites = collections.defaultdict(set)
  for i in itertools.count(2):
    if i not in composites:
      yield i
      composites[2 * i].add(i)
    else:
      for p in composites.pop(i):
        composites[i + p].add(p)

def bucket_sieve_square():
  composites = collections.defaultdict(set)
  for i in itertools.count(2):
    if i not in composites:
      yield i
      composites[i ** 2].add(i)
    else:
      for p in composites.pop(i):
        composites[i + p].add(p)

def bucket_sieve_odd():
  yield 2
  composites = collections.defaultdict(set)
  for i in itertools.count(3, 2):
    if i not in composites:
      yield i
      composites[3 * i].add(i)
    else:
      for p in composites.pop(i):
        composites[i + 2 * p].add(p)

def bucket_sieve_square_odd():
  yield 2
  composites = collections.defaultdict(set)
  for i in itertools.count(3, 2):
    if i not in composites:
      yield i
      composites[i ** 2].add(i)
    else:
      for p in composites.pop(i):
        composites[i + 2 * p].add(p)

def insert(table, m, p):
  while m in table:
    m += p
  table[m] = p

def flat_sieve():
  composites = dict()
  for i in itertools.count(2):
    if i not in composites:
      yield i
      insert(composites, 2 * i, i)
    else:
      p = composites.pop(i)
      insert(composites, i + p, p)

def flat_sieve_square():
  composites = dict()
  for i in itertools.count(2):
    if i not in composites:
      yield i
      insert(composites, i ** 2, i)
    else:
      p = composites.pop(i)
      insert(composites, i + p, p)

def flat_sieve_odd():
  yield 2
  composites = dict()
  for i in itertools.count(3, 2):
    if i not in composites:
      yield i
      insert(composites, 3 * i, 2 * i)
    else:
      step = composites.pop(i)
      insert(composites, i + step, step)

def flat_sieve_square_odd():
  yield 2
  composites = dict()
  for i in itertools.count(3, 2):
    if i not in composites:
      yield i
      insert(composites, i * i, 2 * i)
    else:
      step = composites.pop(i)
      insert(composites, i + step, step)

def delayed_sieve():
  yield 2
  composites = dict()
  primes = delayed_sieve()
  delayed_prime = next(primes)
  for i in itertools.count(3):
    if i == 2 * delayed_prime:
      insert(composites, i, delayed_prime)
      delayed_prime = next(primes)
    if i not in composites:
      yield i
    else:
      p = composites[i]
      del composites[i]
      insert(composites, i + p, p)

def delayed_sieve_square():
  yield 2
  composites = dict()
  primes = delayed_sieve_square()
  delayed_prime = next(primes)
  for i in itertools.count(3):
    if i == delayed_prime ** 2:
      insert(composites, i, delayed_prime)
      delayed_prime = next(primes)
    if i not in composites:
      yield i
    else:
      p = composites.pop(i)
      insert(composites, i + p, p)

def delayed_sieve_odd():
  yield 2
  yield 3
  composites = dict()
  primes = delayed_sieve_odd()
  next(primes)
  delayed_prime = next(primes)
  for i in itertools.count(5, 2):
    if i == 3 * delayed_prime:
      insert(composites, i, 2 * delayed_prime)
      delayed_prime = next(primes)
    if i not in composites:
      yield i
    else:
      step = composites.pop(i)
      insert(composites, i + step, step)

def delayed_sieve_square_odd():
  yield 2
  yield 3
  composites = dict()
  primes = delayed_sieve_square_odd()
  next(primes)
  delayed_prime = next(primes)
  for i in itertools.count(5, 2):
    if i == delayed_prime ** 2:
      insert(composites, i, 2 * delayed_prime)
      delayed_prime = next(primes)
    if i not in composites:
      yield i
    else:
      step = composites.pop(i)
      insert(composites, i + step, step)

def delayed_sieve_opt():
  """ Based on Will Ness's algorithm:
      http://stackoverflow.com/a/10733621 """
  for p in 2, 3:
    yield p
  composites = dict()
  primes = delayed_sieve_opt()
  next(primes)
  delayed_prime = next(primes)
  delayed_square = delayed_prime ** 2
  for i in itertools.count(5, 2):
      step = composites.pop(i, None)
      if step is None and i % delayed_square == 0:
        step = 2 * delayed_prime
        delayed_prime = next(primes)
        delayed_square = delayed_prime ** 2
      if step is None:
        yield i
      else:
        i += step
        while i in composites:
            i += step
        composites[i] = step

def heap_sieve_opt():
  yield 2
  yield 3
  yield 5
  heap = [(9, 6)]
  m, step = heap[0]
  primes = heap_sieve_opt()
  next(primes)
  next(primes)
  delayed_prime = next(primes)
  delayed_square = delayed_prime ** 2
  delayed_step = 2 * delayed_prime
  for i in itertools.count(7, 2):
    if i < m:
      if i == delayed_square:
        heapq.heappush(heap, (delayed_square + delayed_step, delayed_step))
        delayed_prime = next(primes)
        delayed_square = delayed_prime ** 2
        delayed_step = 2 * delayed_prime
      else:
        yield i
    else:
      while i == m:
        heapq.heapreplace(heap, (m + step, step))
        m, step = heap[0]

def all_sieves(limit):
  return [
    ("limited_sieve_opt", limited_sieve_opt(limit)),
    ("limited_sieve", limited_sieve(limit)),
    ("limited_sieve_square", limited_sieve_square(limit)),
    ("limited_sieve_odd", limited_sieve_odd(limit)),
    ("limited_sieve_square_odd", limited_sieve_square_odd(limit)),
    ("bucket_sieve", bucket_sieve()),
    ("bucket_sieve_square", bucket_sieve_square()),
    ("bucket_sieve_odd", bucket_sieve_odd()),
    ("bucket_sieve_square_odd", bucket_sieve_square_odd()),
    ("flat_sieve", flat_sieve()),
    ("flat_sieve_square", flat_sieve_square()),
    ("flat_sieve_odd", flat_sieve_odd()),
    ("flat_sieve_square_odd", flat_sieve_square_odd()),
    ("delayed_sieve", delayed_sieve()),
    ("delayed_sieve_square", delayed_sieve_square()),
    ("delayed_sieve_odd", delayed_sieve_odd()),
    ("delayed_sieve_square_odd", delayed_sieve_square_odd()),
    ("delayed_sieve_opt", delayed_sieve_opt()),
    ("heap_sieve_opt", heap_sieve_opt()),
    ]

def test_primes_100(primes):
  primes_100 = list(itertools.takewhile(lambda p: p < 100, primes))
  correct_primes_100 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
  try:
    assert primes_100 == correct_primes_100
  except AssertionError as e:
    print(primes_100)
    raise e

def test():
  for sieve_name, primes in all_sieves(100):
    test_primes_100(primes)

def consume_primes(primes, limit):
  for p in itertools.takewhile(lambda p: p < limit, primes):
    pass

def profile():
  import timer
  limit = 1000000
  for sieve_name, primes in all_sieves(limit):
    with timer.timer:
      consume_primes(primes, limit)
    print("%-25s %.2f" % (sieve_name, timer.timer.total))

if __name__ == "__main__":
  test()
  profile()

