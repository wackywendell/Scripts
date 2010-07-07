#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Classes:
#  unitbase (e.g. 'distance')
#    with base unit defined (e.g. 1 meter)
#  unit     (e.g. 'kilometer')
#    with type(unit().base) == unitbase
#    unit().conv will be some unitval
#  unitval  (e.g. '1 meter')
#    with type (unitval().unit) == unit
#  converter

import collections

USE_UNICODE = True

class unit(object):
    __slots__ = ('name', '_bases', 'converter', 'abbr')
    
    def __init__(self, basis=None, name=None, abbr=None):
        assert name == None or isinstance(name, (str, unicode))
        self.name = name
        self.abbr = abbr or name
        
        if basis:
            self.basis = basis
        else:
            self.basis = self
    
    def isbasic(self):
        return self.basis == basis({self:1})
    
    @property
    def basis(self):
        return self._bases
    
    @basis.setter
    def basis(self, val):
        if val == self:
            self._bases = basis({self:1})
            return
        elif isinstance(val, unit):
            self._bases = basislist({self:1})
            return
        elif self in val:
            self._bases = basis({self:1})
        else:
            self._bases = basis(val)
            
    def __mul__(self, other):
        return self.__class__(self.basis * other.basis)
    
    def __rmul__(self, other):
        return self.__class__(self.basis * other.basis)
    
    def __pow__(self
    
    def __str__(self):
        if self.abbr:
            return self.abbr
        elif self.name:
            return '|' + self.name + '|'
        else:
            return str(self.basis)
    
    def __repr__(self):
        return str(self)

class basis(dict):
    """This defines a dictionary of unit keys and exponent values that define the unit.
    
    Warning: It is not designed to handle recursion."""
    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)
    
    @classmethod
    def combine(basis1, basis2):
        pass
    
    def simplify(self):
        runagain = True
        while runagain:
            runagain = False
            for k in list(self.keys()):
                if not k.isbasic():
                    #print k
                    
                    exp1 = self[k]
                    for newk,v in k.basis.items():
                        self[newk] = self.get(newk, 0) + v*exp1
                        #print "adding", newk, "^", v*exp1
                    #print "removing", k
                    
                    del self[k]
                    runagain = True
    
    def _makestr(self, unicode=False):
        #print "basislist str"
        numerator = []
        denom = []
        for k,v in self.items():
            vstr = '^' + str(abs(v))
            if unicode:
                vstr = inttosuper(abs(v))
            
            if v == 1:
                numerator.append(str(k))
            elif v == -1:
                denom.append(str(k))
            elif v > 1:
                numerator.append(str(k) + vstr)
            elif v < -1:
                denom.append(str(k) + vstr)
        numerator = " ".join(numerator)
        denom = " ".join(denom)
        return '[' + numerator + '/' + denom + ']'
    
    def __unicode__(self):
        return self._makestr(True)
    
    def __str__(self):
        return self._makestr(USE_UNICODE).encode('utf-8')
    
    def __repr__(self):
        return str(self)
        #return self._makestr(False)
    
    def __mul__(self, other):
        c = self.__class__(self.copy())
        #print type(self), type(other)
        for k, v in other.items():
            c[k] = c.get(k,0) + v
        c.simplify()
        return c
    
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __pow__(self, other):
        return self.__mul__(self)

def inttosuper(n):
    d={'1':u'¹',
       '2':u'\xb2',
       '3':u'\xb3',
       '4':u'\u2074',
       '5':u'\u2075',
       '6':u'\u2076',
       '7':u'\u2077',
       '8':u'\u2078',
       '9':u'\u2079',
       '0':u'\u2070'}
    return "".join(d[x] for x in str(int(n)))

d = unitbase(None, 'Meter')
t = unitbase(None, 'Second')
v = unitbase({d:1, t:-1}, 'Velocity')
a = unitbase({v:1, t:-1}, 'Acceleration')
l = unitbase({a:1, t:-1}, 'Lurch')

print unicode(l.basis)
l.basis.simplify()
print unicode(l.basis)
