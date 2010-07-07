teststr = "Adam A. Allen, Beth B. Bridget\n\n\nbanana"

def linestocommas(s):
    s=s.strip()
    while "\n\n" in s:
        s = s.replace("\n\n","\n")
    return s.replace("\n",",")
    
def namestoemails(s):
    names = [n.strip().split(" ") for n in linestocommas(s).split(',')]
    def toemail(n):
        name = ".".join(w for w in n if w != "")
        while ".." in name:
            name = name.replace("..",".")
        return name + "@dartmouth.edu"
    newnames = [toemail(n) for n in names]
    emails = []
    return newnames

def splitintogroups(s,length):
    s=s.split(",")
    news = []
    while(len(s)>0):
        news.append(",".join(s[:length]))
        s=s[length:]
    return news

def namestoemailstr(s):
    names = namestoemails(s)
    return ",".join(names)

print namestoemailstr(teststr)

fin = open('allcampuslist.txt')
instring = fin.read()
fin.close()

names=namestoemailstr(instring)
outstring="\n\n".join(splitintogroups(names,1100))

fout = open('allcampuslistemails.txt','w')
fout.write(outstring)
fout.close()
