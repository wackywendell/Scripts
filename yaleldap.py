import ldap
from string import digits, printable, whitespace
from string import ascii_lowercase as letters
from collections import defaultdict

yalehost = "ldap://directory.yale.edu"
yalebn = "o=yale.edu"

ldinternal = None
ldinthost = yalehost
ldintbn = yalebn

def getld(host=yalehost,bn=yalebn):
    "Gets the current ldap server object, creating one if necessary"
    global ldinternal
    try:
        if ldinternal:
            return ldinternal
        else:
            ldinternal = None
            ldinthost = host
            ldintbn = bn
    except:
        pass
    ldinternal = ldap.initialize(host)
    #ldinternal.simple_bind_s(bn,"")
    return ldinternal


class query:
    """Defines a simple query to be sent to an LDAP server."""
    def __init__(self, **kwargs):
        if len(kwargs)>1 or len(kwargs) < 1:
            raise TypeError("query() takes exactly 1 keyword argument.")
        (self.k,self.v) = kwargs.items()[0]
    
    def __str__(self):
        return '(' + str(self.k) + '=' + str(self.v) + ')'
    
    def __repr__(self):
        return str(self)
        
    def __and__(self, q):
        return andquery(q, self)
        
    def __or__(self, q):
        return orquery(q, self)

    def run(self, ld=None):
        return [person(p) for p in queryqueries(str(self),ld=ld)]

class orquery(query, list):
    "Takes a list of queries and combines them with 'or'."
    def __init__(self, *qs, **kwargs):
        for q in qs:
            if isinstance(q, orquery):
                self.extend(q)
            else:
                self.append(q)
        for k,v in kwargs.items():
            kw = {k:v}
            self.append(query(**kw))
        
    def __str__(self):
        s = '(|'
        for q in self:
            s += str(q)
        s += ')'
        return s

class andquery(query, list):
    """Takes a list of queries and combines them with 'and'.
    
    Can also take a list of keyword arguments to make an 'and' query."""
    def __init__(self, *qs, **kwargs):
        for q in qs:
            if isinstance(q, andquery):
                self.extend(q)
            else:
                self.append(q)
        for k,v in kwargs.items():
            kw = {k:v}
            self.append(query(**kw))
        
    def __str__(self):
        s = '(&'
        for q in self:
            s += str(q)
        s += ')'
        return s

nums=digits

def queryname(strng, ld):
    "Searches using a string for the filter"
    q=ld.search_s(ldintbn,2,str(strng))
    return [person(p) for p in q]
    # return q

def searchstu(strng,yr):
    "Searches for students, with name matching 'strng' and year matching 'yr'"
    return queryname("(&(CN="+strng+"*)(dndDeptclass="+yr+
                            ")(eduPersonAffiliation=student))")

def fixedstring(strng, n):
    "Takes a string and returns one of fixed length 'n', cutting or extending as necessary"
    return strng[:n].ljust(n)

def makeprintable(strng):
    "Takes a string and makes it printable"
    lst=[]
    for l in strng:
        if l not in printable:
            lst.append('_')
        elif l in whitespace:
            lst.append(' ')
        else:
            lst.append(l)
    return "".join(lst)
    #~ return repr(strng)

def myquery(ld=None, **kwargs):
    """Searches for a filter, with kwargs being used to generate the filter.

Examples:
myquery(CN='*wendell*',class="2015")"""
    if not ld:
        ld = getld()
    q="(&"
    for (k,v) in kwargs.iteritems():
        q += "(" + str(k) + "=" + str(v) + ")"
    q += ")"
    # print q
    return ld.search_s(ldintbn,2,q)

def queryqueries(q, ld=None):
    """Searches for a query of type 'query'"""
    if not ld:
        ld = getld()
    # print q
    return ld.search_s(ldintbn,2,str(q))
    
def queryppl(*args, **kwargs):
    "Same as 'myquery', but returns a list of type 'person'"
    return [person(p) for p in myquery(*args, **kwargs)]

class person:
    "A class for making the ldap readout more pythonic and readable."
    def __init__(self, obj):
        "Initialize with output from a search"
        d=obj[1]
        self.name  = d.get('cn',[""])[0]
        self.alias = d.get('alias',[""])[0]
        self.year  = d.get('class',[""])[0]
        self.given = d.get('givenName',[""])[0]
        self.sn    = d.get('sn',[""])[0]
        self.email = d.get('mail',[""])[0]
        self.hmail = d.get('emailHome',[""])[0]
        self.org   = d.get('o',[""])[0]
        self.dept  = d.get('ou',[""])[0]
        self.netid = d.get('uid',[""])[0]
        self.major = d.get('major',[""])[0]
        self.curric= d.get('curriculumShortName',[""])[0]
        self.data  = d
    
    tablestr = " ".join([
            fixedstring("Name",25),
            fixedstring("Class/Year",12),
            fixedstring("Net ID",8),
            fixedstring("Major",18),
            fixedstring("Curriculum", 10),
            fixedstring("Alias", 15)
            ])
    
    def __str__(self):
        return " ".join([
            fixedstring(self.name,25),
            fixedstring(self.year,12),
            fixedstring(self.netid,8),
            fixedstring(self.major,18),
            fixedstring(self.curric, 10),
            fixedstring(self.alias, 15)
            
            ]).strip()
    def __repr__(self):
        return ("<person '%s'>" % self.name)
        
    def __cmp__(self, y):
        "Compares 'person' objects by year, last name, firstname, other"
        if isinstance(y, person):
            if y.year != self.year:
                return cmp(self.year, y.year)
            elif y.sn != self.sn:
                return cmp(self.sn, y.sn)
            elif y.name != self.name:
                return cmp(self.name, y.name)
            return cmp(self.data, y.data)
        return cmp(self.data, y)
    
    @classmethod
    def tableprint(cls, iter=[]):
        "Class method. Takes a list of 'person' objects, and prints in a table form"
        print(cls.tablestr.strip())
        for p in iter:
            print(makeprintable(str(p)).strip())

    def longprint(self, f=None):
        "Prints all data for the person, cutting each field at 80 chars"
        for (k,v) in self.data.items():
            strng = (k.ljust(20)+ ": " + makeprintable(";".join(v)))[:100]
            if f:
                f(strng)
            else:
                print(strng)

    def longlongprint(self, f=None):
        "Prints ALL data for the person; can be very long"
        for (k,v) in self.data.items():
            strng = (k.ljust(20)+ ": " + makeprintable(";".join(v)))
            if f:
                f(strng)
            else:
                print(strng)
    
    def smalldat(self):
        "returns the dictionary with values converted to short strings."
        newdict = {}
        for (k,v) in self.data.items():
            rep = repr(v)[1:-1][:40]
            newdict[k] = rep
        return newdict

pgrads16 = andquery(major='Physics',Class='2016')

import time
def pgrads():
    l=[]
    for d in digits:
        q=andquery(major='Physics',curriculumShortName='GS',uid=('*'+d))
        l.extend(q.run())
        print d, len(l)
        if d != digits[-1]:
            time.sleep(1)
    return l

def cgrads():
    l=[]
    for c in letters:
        q=andquery(major='Chemistry',curriculumShortName='GS',uid=(c+'*'))
        l.extend(q.run())
        print c, len(l)
        if c != letters[-1]:
            time.sleep(.4)
    return l