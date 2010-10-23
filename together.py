from datetime import datetime

now = datetime.now()
w = datetime(1986,12,17)
j = datetime(1987,7,26)
wj = datetime(2006,2,19)

def datesub(d1, d2):
    ys = d1.year - d2.year
    ms = d1.month - d2.month
    ds = d1.day - d2.day

    if ds < 0:
        ds += 30
        ms -= 1
    if ms < 0:
        ms += 12
        ys -= 1
    return (ys, ms, ds)


wpercent = float((now - wj).days) / (now - w).days * 100
jpercent = float((now - wj).days) / (now - j).days * 100

print "Percent of Wendell's life: {0:2f}".format(wpercent)
print "Percent of Jenny's life: {0:2f}".format(jpercent)

wfifth = (wj-w)/4 + wj
wfifthleft = datesub(wfifth, now)
jfifth = (wj-j)/4 + wj
jfifthleft = datesub(jfifth, now)

print "W 20%: {0}; {1}y {2}m {3}d".format(wfifth.date(), *wfifthleft)
print "J 20%: {0}; {1}y {2}m {3}d".format(jfifth.date(), *jfifthleft)
