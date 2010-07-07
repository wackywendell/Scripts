#!/usr/bin/python

import smtplib
import sys
import threading
fromaddr="Aporia <Aporia@dartmouth.edu>"
batchsize=40

# useful later
def batch(lst, size):
    b=[]
    loc=0
    while len(lst) > loc:
        b.append(lst[loc:loc+size])
        loc+=size
    return b

emailfile=open(sys.argv[1])
emails=[e.strip() for e in emailfile.readlines()]
print emails
msgfile=open(sys.argv[2])
msg="\n".join(msgfile.readlines())

def makemsg(em):
    return "To: "+em+"\n"+msg

class totalupdater:
    def __init__(self):
        self.num=0
        self.lock=threading.Lock()
    def update(self):
        self.lock.acquire()
        self.num+=1
        if self.num % 20 == 0:
            print "Emails sent:", self.num
        self.lock.release()

class sender(threading.Thread):
    def __init__(self, lock, emlst, num, totaler):
        threading.Thread.__init__(self, name="Thread "+str(num))
        self.lst=emlst
        self.num=num
        self.lock=lock
        self.totaler=totaler
    def run(self):
        server = smtplib.SMTP('mailhub.dartmouth.edu')
        for em in self.lst:
            try:
                server.sendmail(fromaddr, [em], makemsg(em))
            except smtplib.SMTPException, e:
                print ("-"*50)
                print "Error:", type(e)
                print e
                print em
                print "CONTINUING..."
                print ("-"*50)
            self.totaler.update()
        server.quit()
        self.totaler.lock.acquire()
        print "Thread " + str(self.num) + " Finished"
        self.totaler.lock.release()
    
def main():
    l=threading.Lock()
    emlst=enumerate(batch(emails, batchsize))
    t=totalupdater()
    threads=[sender(l, el, n+1, t) for (n, el) in emlst]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
