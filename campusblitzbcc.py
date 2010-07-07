#!/usr/bin/python

import os
import smtplib
import sys
import getpass

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
toaddr="Aporia <Aporia@dartmouth.edu>"
#fromaddr="Wendell <wendell.smith@dartmouth.edu>"
#toaddr="Wendell Smith <wendell.smith@dartmouth.edu>"
loginname="W. Wendell Smith"
#~ loginname="wackywendell@gmail.com"
attachmentfnames=[]
tofilename=""
msgfilename=""
subject=""
batchsize=40

usgtxt="""\
blitzcampus.py [-h] [-f addr]  -t file -m file [-a attach1 [attach2 ...]]

Blitz out to a list.

From defaults to "Aporia <Aporia@dartmouth.edu>"

Options:
-h      
-f addr     Change from address to addr
-t file     Text file from which to get to addresses
-a file     attach file to emails
-m file     text for body of message
-x addr     change to address to addr
-l id       Change login (defaults to "W. Wendell Smith")
-s subj     specify subject
-S          use first line of file as subject
"""

def checksubj():
    global subject
    if subject == "" and not usefsubject:
        print "No subject specified. Continue?"
        print "Y to continue, S to enter a subject, anything else to exit"
        a=raw_input()
        if "s" in a.lower():
            isok = False
            while not isok:
                subject = raw_input("Subject: ")
                print "New Subject:"
                print subject
                newok = raw_input("Continue? (Y/N): ")
                if "y" in newok.lower(): isok=True
        elif "y" in a.lower():
            print "Continuing with blank subject..."
        else:
            print "Exiting"
            exit()

def usage():
    print usgtxt
    exit()

def msggen(ems, n):
    curcount=0
    m = copy(mainmsg)
    bcclst=[]
    for em in ems:
        if curcount >= n:
            del m["Bcc"]
            m["Bcc"]=",".join(bcclst)
            yield (m,bcclst)
            m = copy(mainmsg)
            curcount=0
            bcclst=[]
        bcclst.append(em)
        curcount += 1
    del m["Bcc"]
    m["Bcc"]=",".join(bcclst)
    yield (m,bcclst)

def sendblitzes(emlst, n=100):
    numleft=len(emlst)
    numsent=0
    
    #get password to log in
    print "Password for",loginname
    pw=getpass.getpass(":")
    
    print "Connecting..."
    #server = smtplib.SMTP_SSL()
    server = smtplib.SMTP_SSL('mailhub.dartmouth.edu', 465)
    print server.connect('mailhub.dartmouth.edu', 465)
    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.set_debuglevel(True)
    print "Logging in..."
    
    print server.login(loginname,pw)
    for (m, addrs) in msggen(emlst, n):
        ems = addrs + [toaddr]
        print "Sending message", (numsent+1)
        try:
            print server.sendmail(fromaddr, ems, str(m))
        except smtplib.SMTPServerDisconnected:
            print "Disconnected, Retrying..."
            server.connect()
            print server.sendmail(fromaddr, ems, str(m))
        except smtplib.SMTPException, e:
            print ("-"*50)
            print "Error:", type(e)
            print e
            print em
            print "CONTINUING..."
            print ("-"*50)
        numsent += 1
        numleft -= n
    print "Finished sending"

tofilename=""
msgfilename=""
def parseargs():
    (opts, args)=getopt(sys.argv[1:],"hf:t:m:a:s:Sx:l:")
    global fromaddr, toaddr, loginname, msgfilename, tofilename
    global attachmentfnames, subject, usefsubject
    lastopt = ""
    usefsubject = False
    for (o,val) in opts:
        lastopt = o
        if o == '-h':
            usage()
        elif o == '-f':
            fromaddr = val
            print "from:", fromaddr
        elif o == '-x':
            toaddr = val
            print "to:", toaddr
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
        elif o == '-S':
            usefsubject = True
        elif o == '-l':
            loginname = val
            print "login:", loginname
    
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
    global subject
    msgf = file(msgfilename,'rb')
    msgtxt = msgf.read()
    msgf.close()
    
    if usefsubject:
        (subj, sep, rest) = msgtxt.partition(os.linesep)
        subject = subj
        msgtxt = rest
    
    msgtxt = msgtxt.strip()
    
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
    m["To"] = toaddr
    m["Subject"] = subject
    global mainmsg
    mainmsg = m

def main():
    emailfile=open(tofilename)
    emails=[e.strip() for e in emailfile.readlines()]
    emailfile.close()
    
    createmainmsg()
    if usefsubject:
        print "Subject:", subject
    
    sendblitzes(emails)

if __name__ == "__main__":
    parseargs()
    main()
