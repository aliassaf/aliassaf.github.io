---
---

While playing around with prime number generation in Python, I stumbled upon this [post](http://stackoverflow.com/a/10733621) by Will Ness. In his comment, Will makes an interesting observation that leads to a huge optimization. His algorithm is difficult to understand at first glance, so I took the time to break it down and find out exactly where his trick comes into play. Here are the results.

## The sieve of Eratosthenes

At $i = 2$, the cells look like this:

    |   |   | x |   | x |   | x |   | x |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

At $i = 3$, the cells look like this:

    |   |   | x |   | x |   | x | x | x |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

We use a set instead of an array to keep track of the composites. A number is in the set if its cell is crossed out (it is composite) and it is not in the set otherwise.

``` python
def limited_sieve(limit):
  composites = set()
  for i in range(2, limit):
    if i not in composites:
      yield i
      for j in range(2 * i, limit, i):
        composites.add(j)
```

We can print the prime numbers by iterating over the generator:

``` python
primes = limited_sieve(100)
for p in primes:
  print(p)
```

Notice that when crossing out multiples of a prime number $p > 2$, we don't need to worry about crossing out $2 \times p$ since that number has already been crossed out by 2. The same goes for $p > 3$ and $3 \times p$. In fact, the first multiple that has not been crossed out yet is $p \times p$, so we can start our iteration from there:

``` python
def limited_sieve(limit):
  ...
      for j in range(i * i, limit, i):
        composites.add(j)
```

## Removing the limit

Instead of iterating over all the multiples of each prime number, we lazily remember the last multiple that we have crossed out for each prime number. Each number has a bucket containing its prime divisors. When we process a number, if the bucket is empty, it is a prime number. Otherwise, we take each prime divisor and move it to the next number that it divides. For example, at $i = 6$, the buckets look like this:

                      2
    |   |   |   |   | 3 |   |   |   | 5 |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

At $i = 7$, the buckets look like this:

    |   |   |   |   |   |   | 2 | 3 | 5 |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

We use the `count` function from the `itertools` library to generate all the numbers starting from 3, and the `defaultdict` data structure from the `collections` library to have dictionaries with default values.

``` python
import itertools
import collections

def bucket_sieve():
  yield 2
  factors = collections.defaultdict(set)
  for i in itertools.count(3):
    if i not in factors:
      yield i
      factors[2 * i].add(i)
    else:
      for p in factors[i]:
        factors[i + p].add(p)
      del factors[i]
```

Empty buckets don't actually exist in the `factors` dictionary and don't take up memory. We delete the factors of $i$ at the end of the loop because we don't need them anymore. As a result, each prime number generated so far appears exactly once in one of the buckets of the factors table. The space complexity is therefore $O(P)$, where $P$ is the number of prime numbers generated so far.

Again, we can optimize this algorithm by jumping to the square multiple instead of the double:

``` python
def bucket_sieve(limit):
  ...
    if i not in factors:
      yield i
      factors[i * i].add(i)
```

## Removing the buckets

Bucket manipulation slows the algorithm down. We only need to know one prime divisor in order to conclude that a number is composite. With this observation, we can get rid of the buckets and put only one prime divisor in each cell. While moving a prime number, if the new cell is occupied, we keep searching until we find a multiple that has an empty cell.

At $i = 4$, the cells look like this:

    |   |   | 2 |   | 3 |   |   |   |   |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

At $i = 5$, the cells look like this:

    |   |   |   |   | 3 |   | 2 |   |   |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

Again, we can optimize this algorithm by jumping to the square multiple instead of the double.

``` python
def flat_sieve():
  yield 2
  factor = dict()
  for i in itertools.count(3):
    if i not in factor:
      yield i
      insert(factor, 2 * i, i)
    else:
      p = factor[i]
      del factor[i]
      insert(factor, i + p, p)

def insert(table, m, p):
  while m in table:
    m += p
  table[m] = p
```

This version of the algorithm has exactly the same time complexity as `limited_sieve` but is not limited.

Again, we can optimize this algorithm by jumping to the square multiple instead of the double:

``` python
def flat_sieve(limit):
  ...
    if i not in factors:
      yield i
      insert(factor, i * i, i)
```

## Delaying insertions (Will Ness's trick)

In the previous version, we immediately insert the square of each prime number we encounter. This introduces a lot of useless information that we won't need until much later. For example, at $i = 6$, the cells look like this:

    |   |   |   |   | 3 |   | 2 |   | 5 |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

At $i = 8$, the cells look like this:

    |   |   |   |   |   |   | 2 | 3 | 5 |   | 7 |
    -------------------------------------   -----
      2   3   4   5   6   7   8   9  10  ... 14

We can avoid these insertions and save up some memory by delaying an insertion until we encounter the multiple. How do we know when we encounter a multiple? We need to "remember" primes that occured previously, but if we store all the primes that we generate, we are back to square one. The key insight of Will Ness is that we can use a separate stream of prime numbers, that we exhaust at a slower rate to generate the prime multiples that we need to insert at the current position. This time, before looking at the cell of a number is empty, we first check if the number is a multiple of the first prime number of the delayed stream.

How do we get access to a separate stream of prime numbers? By calling our generator, recursively!

``` python
def delayed_sieve():
  yield 2
  factor = dict()
  primes = delayed_sieve()
  delayed_prime = next(primes)
  for i in itertools.count(3):
    if i == 2 * delayed_prime:
      insert(factor, i, delayed_prime)
      delayed_prime = next(primes)
    if i not in factor:
      yield i
    else:
      p = factor[i]
      del factor[i]
      insert(factor, i + p, p)
```

At $i = 8$, the secondary stream is still at 5, and the cells look like this:

    |   |   |   |   |   |   | 2 | 3 |   |
    -------------------------------------
      2   3   4   5   6   7   8   9  10

We can already guess that this algorithm uses less memory. How far can we delay this secondary stream? As pointed out previously, the first multiple of $p$ that has no other prime divisor is $p \times p$. We cannot delay more than that.

``` python
def delayed_sieve():
  ...
    if i == delayed_prime * delayed_prime:
      insert(factor, i, delayed_prime)
      delayed_prime = next(primes)
  ...
```

What impact does this have on memory? As before, each prime number generated so far is in at most one cell. This time however, prime numbers larger than $\sqrt{i}$ are delayed and are not inserted. The memory complexity is therefore $O(\sqrt{P})$, a huge improvement! This optimization reduces the memory consumption drastically. With it, I could easily generate all the prime numbers below 1,000,000,000 without running out of memory.

You might be wondering about the number of recursive calls that are being made here. Surely the delayed stream is calling another, even more delayed stream, and so on. Don't these streams consume memory too? First, note that the recursive call returns immediately because a generator does not compute anything until we consume its elements, so there is no risk of exploding the stack. Second, each delayed stream is at the square root of the position of the previous one. This number falls down very rapidly and eventually reaches 2. To give you an idea, at $i = 2^{2^{10}}$ (a number with 308 digits), we are only using around 10 streams in total.


