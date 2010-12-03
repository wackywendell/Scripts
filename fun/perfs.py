import math, itertools, functools, operator

def product(seq):
    """Product of a sequence."""
    return functools.reduce(operator.mul, seq, 1)

def primes(n=0):
    """ Returns  an iterable of primes < n, or an infinite list """
    primes = []
    for val in itertools.count(2):
        for p in primes:
            if val % p == 0:
                break
        else:
            yield val
            primes += [val]
            if n>0 and len(primes) >= n:
                return
        continue

def allcombos(lst):
    s = list(lst)
    return set(
        itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s)+1))
        )

def allcombos_repeats(lst, n=0):
    if n == 0:
        n = len(lst)
    def single(i):
        return itertools.combinations_with_replacement(lst, i)
    return itertools.chain.from_iterable(map(single, range(n+1)))

def makesperfect(*factors):
    #print(sorted(factors))
    #print(allcombos(factors))
    divs = map(product, allcombos(factors))
    #print(list(divs))
    #print(sum(divs), '==', 2*product(factors))
    return sum(divs) == 2*product(factors)

def find_perfs(n):
    myprimes = sorted(primes(n))
    factorgroups = allcombos_repeats(myprimes,n)
    for (nth,factors) in enumerate(factorgroups):
        if nth % 20000 == 0:
            print("Checked", nth, "| Now on", product(factors),
                    "| with factors", sorted(factors))
            #print("Checking",product(factors),nth,"group",sorted(factors))
        if makesperfect(*factors):
            print("FOUND:", product(factors), sorted(factors))
        