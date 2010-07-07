"""
  Generator for getting factors for a number
"""
def factor(n):
    while n % 2 == 0:
        yield 2
        n /= 2
    
    i = 3
    limit = int(n**0.5) + 1
    while i <= limit:
        if n % i == 0:
            yield i
            n = n / i
            limit = int(n**0.5 ) + 1
            continue
        i += 2
    if n > 1:
        yield n

if __name__ == "__main__":
  import sys
  for index in xrange(1,len(sys.argv)):
    print "Factors for %s : %s" %(sys.argv[index], [i for i in factor(int(sys.argv[index]))])
