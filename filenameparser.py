import pyparsing as pars
from pyparsing import alphas, nums, alphanums
from pyparsing import Word, Suppress, Literal, Optional

parseint = Word(nums)
parseint.setParseAction(lambda x: int(x[0]))

tracknum = parseint('tracknum')
discnum = parseint('discnum')
sep = (Word("-") | ":")('sep')
title = Word(alphas + " ")('title')
extension = Word(alphanums)('extension')

smallfilename = (title + Suppress(".") + extension)
medfilename = tracknum +  Suppress(sep) + smallfilename
largefilename = discnum + Suppress(sep) + medfilename

ending = pars.StringEnd()

full = largefilename ^ medfilename ^ smallfilename + ending