#!/usr/bin/python
from __future__ import print_function
import sys
import commands

print(commands.getoutput('date'))
print("This is a test. I hope it passes!")

print("stderr!", file=sys.stderr)