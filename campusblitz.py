#!/usr/bin/python

import os
import smtplib
import sys
import threading
from getopt import getopt
import mimetypes
from email import encoders
from email.message import Message
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from copy import copy, deepcopy

fromaddr="Aporia <Aporia@dartmouth.edu>"
attachmentfnames=[]
tofilename=""
msgfilename=""
subject=""
batchsize=40

usgtxt="""\
blitzcampus.py [-h] [-f addr] [-a attach1 [-a attach2 ...]] -t file -m file

Blitz out to a list.

From defaults to "Aporia <Aporia@dartmouth.edu>"

Options:
-h      
-f addr     Change from address to addr
-t file     Text file from which to get to addresses
-a file     attach file to emails
"""

def checksubj():
    if subject == "":
        print "No subject specified. Continue?"
        print "Y to continue, anything else to exit"
        a=raw_input()
        if a not in ("Y", "y"):
            print "Exiting"
            exit()
        else:
            print "Continuing with blank subject..."

def usage():
    print usgtxt
    exit()

# useful later
def batch(lst, size):
    b=[]
    loc=0
    while len(lst) > loc:
        b.append(lst[loc:loc+size])
        loc+=size
    return b



#~ emailfile=open(sys.argv[1])
#~ emails=[e.strip() for e in emailfile.readlines()]
#~ print ", ".join(emails)
#~ msgfile=open(sys.argv[2])
#~ msg="\n".join(msgfile.readlines())

def makemsg(em):
    return "To: "+em+"\n"+msg

class totalupdater:
    def __init__(self, total):
        self.num = total
        self.total = total
        self.lock=threading.Lock()
    def update(self):
        self.lock.acquire()
        self.num -= 1
        if self.num % 20 == 0:
            print "Emails left:", self.num, "out of", self.total
        self.lock.release()

copylock = threading.Lock()
def createmsg(toaddr):
    copylock.acquire()
    m = copy(mainmsg)
    copylock.release()
    m["To"] = toaddr
    return m
    

def smtptry(func, *args, **kwargs):
            try:
                func(*args, **kwargs)
            except smtplib.SMTPException, e:
                print ("-"*50)
                print "Error:", type(e)
                print e
                print em
                print "CONTINUING..."
                print ("-"*50)

class sender(threading.Thread):
    def __init__(self, lock, emlst, num, totaler):
        threading.Thread.__init__(self, name="Thread "+str(num))
        self.lst=emlst
        self.num=num
        self.lock=lock
        self.totaler=totaler
        self.numleft=len(emlst)
    def run(self):
        server = smtplib.SMTP('mailhub.dartmouth.edu')
        for em in self.lst:
            m = createmsg(em)
            try:
                server.sendmail(fromaddr, [em], str(m))
            except smtplib.SMTPServerDisconnected:
                server.connect()
                server.sendmail(fromaddr, [em], str(m))
            except smtplib.SMTPException, e:
                print ("-"*50)
                print "Error:", type(e)
                print e
                print em
                print "CONTINUING..."
                print ("-"*50)
            print "updating..."
            self.totaler.update()
            server.quit()
        self.totaler.lock.acquire()
        print "Thread " + str(self.num) + " Finished"
        self.totaler.lock.release()

tofilename=""
msgfilename=""
def parseargs():
    (opts, args)=getopt(sys.argv[1:],"hf:t:m:a:s:")
    global fromaddr, msgfilename, tofilename, attachmentfnames, subject
    lastopt = ""
    for (o,val) in opts:
        lastopt = o
        if o == '-h':
            usage()
        elif o == '-f':
            fromaddr = val
            print "from:", fromaddr
        elif o == '-m':
            msgfilename = val
            print "msgfile:", msgfilename
        elif o == '-t':
            tofilename = val
            print "tofile:", tofilename
        elif o == '-a':
            attachmentfnames.append(val)
        elif o == '-s':
            subject = val
            print "subject:", subject
    
    # after parsing named arguments, deal with leftovers
    # if the last option was "-a", add it to the filenames
    
    for a in args:
        if lastopt == '-a':
            attachmentfnames.append(val)
        else:
            print "Ignoring argument", a
            
    # print number of files
    print "Total attachments:", len(attachmentfnames)
    
    if tofilename == '':
        print "ERROR: No file specified for sending addresses, exiting"
        exit()
    if msgfilename == '':
        print "ERROR: No message file specified, exiting"
        exit()
    
    # make sure there is a subject, and if not, question whether to continue
    checksubj()

mainmsg = Message()
def createmainmsg():
    msgf=file(msgfilename,'rb')
    msgtxt=msgf.read()
    msgf.close()
    if attachmentfnames:
        m = MIMEMultipart()
        m.preamble = 'This is a multipart MIME message.\n'
        m.attach(MIMEText(msgtxt))
        parts = [msgf] + attachmentfnames
        for path in attachmentfnames:
            if not os.path.isfile(path):
                print "ERROR: Could not find file", path
                print "EXITING"
                exit()
            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, encoding = mimetypes.guess_type(path)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            maintype, subtype = ctype.split('/', 1)
            if maintype == 'text':
                fp = open(path)
                # Note: we should handle calculating the charset
                msg = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'image':
                fp = open(path, 'rb')
                msg = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == 'audio':
                fp = open(path, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(path, 'rb')
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                fp.close()
                # Encode the payload using Base64
                encoders.encode_base64(msg)
            # Set the filename parameter
            filenm = os.path.split(path)[1]
            msg.add_header('Content-Disposition', 'attachment', filename=filenm)
            m.attach(msg)
    else:
        m = MIMEText(msgtxt)
    m["From"] = fromaddr
    m["Subject"] = subject
    global mainmsg
    mainmsg = m

def main():
    emailfile=open(tofilename)
    emails=[e.strip() for e in emailfile.readlines()]
    emailfile.close()
    
    createmainmsg()
    
    emlst=enumerate(batch(emails, batchsize))
    
    t=totalupdater(len(emails))
    
    l=threading.Lock()
    threads=[sender(l, el, n+1, t) for (n, el) in emlst]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()

if __name__ == "__main__":
    parseargs()
    main()
