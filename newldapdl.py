import ldap

alpha="abcdefghijklmnopqrstuvwxyz"
nums="1234567890"

ld = ldap.initialize("ldap://ldap.dartmouth.edu")
ld.simple_bind_s("dc=dartmouth,dc=edu","")

def testcls(s):
    try:
        return s[0]=="'" and s[1] in nums and s[2] in nums
    except IndexError:
        return False

def query(**kwargs):
    q="(&"
    for (k,v) in kwargs.iteritems():
        q += "(" + str(k) + "=" + str(v) + ")"
    q += ")"
    return ld.search("dc=dartmouth,dc=edu",2,q)

def queries():
    for a in alpha:
        for b in alpha:
            yield query(CN=a+'*', SN=b+'*', eduPersonAffiliation='student')

class person:
    def __init__(self, obj):
        d=obj[1]
        self.name  = d.get('cn',[""])[0]
        self.nicks = d.get('nickname',[""])[0]
        self.given = d.get('givenName',[""])[0]
        self.email = d.get('mail',[""])[0]
        self.cls   = d.get('dndDeptclass',[""])[0]
        self.affil = d.get('eduPersonAffiliation',[""])[0]

def main():
    print "submitting queries..."
    ids=list(queries())
    print len(ids)
    people=[]
    print "getting results..."
    for (q, id) in ids:
        rslt = ld.result(id)
        for r in rslt[1]:
            #~ print r
            p = person(r)
            if testcls(p.cls):
                people.append(p)
                print "%4d: %s, %s" % (len(people), p.name, p.cls)

def main2():
    print "submitting queries..."
    ids=list(queries())
    print len(ids)
    people=[]
    print "getting results..."
    while len(ids) > 0:
        rslt = ld.result2()
        ids.remove(rslt[2])
        for r in rslt[1]:
            #~ print r
            p = person(r)
            if testcls(p.cls):
                people.append(p)
                print "%4d: %s, %s" % (len(people), p.name, p.cls)

#~ if __name__ == "__main__":
    #~ main()
