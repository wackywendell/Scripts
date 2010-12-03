#!/usr/bin/python3
import math
from itertools import count

def divisors(n):
    for i in range(2,int(math.sqrt(n))+1):
        if n % i == 0:
            yield i
            if i*i != n:
                yield n//i

def isperfect(n):
    return sum(divisors(n)) + 1 == n

def findperfs(start=1):
    for val in count(start):
        if isperfect(val):
            yield val

def pperfs(start=1):
    for val in count(start):
        if isperfect(val):
            print(val, sorted(divisors(val)))
            continue
        elif val < 10000:
            continue
        elif val == 10 ** int(math.log10(val)):
            print("        ",val)
        elif val == 2 * 10 ** int(math.log10(val)):
            print("        ",val)
        elif val == 5 * 10 ** int(math.log10(val)):
            print("        ",val)


def pdivs(start=1, end=0):
    for val in count(start):
        if end > start and val > end:
            return
        print(val, sorted(divisors(val)))

if __name__ == "__main__":
    pperfs()
