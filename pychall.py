#!/usr/bin/python3

dir='/home/wendell/scripts/pychall'

import string
def trans(s):
    new = ""
    let = string.ascii_lowercase.encode()
    tran = string.maketrans(let,let[2:] + let[:2])
    print("""g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj. """.translate(tran))
    return tran
    
# 3

import collections
def do3():
    d = collections.defaultdict(lambda:0)
    a=""
    
    with open(dir + '/3.txt') as f:
        for char in f.read():
            d[char] += 1
            if char in string.letters:
                a+=char
    return a

import re
def do4():
    expr = re.compile('[a-z][A-Z]{3}[a-z][A-Z]{3}[a-z]')
    #return expr
    with open(dir + '/4.txt') as f:
        strs = expr.findall(f.read())
        return "".join(c[4] for c in strs)

import urllib.req
def do5()