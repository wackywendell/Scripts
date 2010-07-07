#!/usr/bin/python
from dice2 import *

def myprint(f, ln):
    f.write(ln + '\n')
    print ln

if __name__ == "__main__":
    for i in range(8,11):
        thedice = getbest(i)
        f = open("diceans.txt", "a")
        myprint(f, "-"*80)
        myprint(f, str(i) + "-sided dice:")
        for x in thedice:
            myprint(f, str(x))
        f.close()
