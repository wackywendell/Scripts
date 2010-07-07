import ldap
from string import digits, printable, whitespace

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

q1 = query(q='123')
q2 = query(j='abc')
qo = orquery(q1,q2)
qa = andquery(q1,q2)

nums=digits

def testcls(s):
    'Tests whether a string matches that for a class, e.g. "\'09"'
    try:
        return s[0]=="'" and s[1] in nums and s[2] in nums
    except IndexError:
        return False

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

ldinternal = None
ldinthost = "ldap://ldap.dartmouth.edu"
ldintbn = "dc=dartmouth,dc=edu"

def getld(host="ldap://ldap.dartmouth.edu",bn="dc=dartmouth,dc=edu"):
    "Gets the current ldap server object, creating one if necessary"
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
    ldinternal.simple_bind_s(bn,"")
    return ldinternal

yalehost = "ldap://directory.yale.edu"
yalebn = "o=yale.edu"

def yaleld():
    return getld(yalehost,yalebn)

def myquery(ld=None, **kwargs):
    """Searches for a filter, with kwargs being used to generate the filter.

Examples:
myquery(CN='*wendell*',dnddeptClass="'09")"""
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
        self.nicks = d.get('nickname',[""])[0]
        self.given = d.get('givenName',[""])[0]
        self.sn    = d.get('sn',[""])[0]
        self.email = d.get('mail',[""])[0]
        self.year  = d.get('dndDeptclass',[""])[0]
        self.addr  = d.get('dndHinmanaddr',[""])[0]
        self.tel   = d.get('telephoneNumber',[""])[0]
        self.affil = d.get('eduPersonAffiliation',[""])[0]
        self.data  = d
    
    tablestr = " ".join([
            fixedstring("Name",25),
            fixedstring("Class/Year",12),
            fixedstring("Address",12),
            fixedstring("Telephone",15),
            #fixedstring("Affiliation",12),
            #fixedstring("Email", 40)
            fixedstring("Nicknames", 50)
            ])
        
    def __cmp__(self, y):
        "Compares 'person' objects by year, last name, firstname, other"
        if isinstance(y, person):
            if y.year != self.year:
                return cmp(self.year, y.year)
            elif y.sn != self.sn:
                return cmp(self.sn, y.sn)
            elif y.name != self.name:
                return cmp(self.name, y.name)
            else:
                return cmp(self.data, y.data)
        else:
            return cmp(self.data, y)
    def __str__(self):
        return " ".join([
            fixedstring(self.name,25),
            fixedstring(self.year,12),
            fixedstring(self.addr,12),
            fixedstring(self.tel,15),
            #fixedstring(self.affil,12),
            #fixedstring(self.email, 40)
            fixedstring(self.nicks, 100)
            ]).strip()
    def __repr__(self):
        return ("<person '%s'>" % self.name)
    
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
