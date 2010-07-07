#!/usr/bin/env python

import os
import os.path as path
import time
import getpass
import ssmtplib
import glob
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

topdirs = [r'/data/wendell/college',r'/data/wendell/grad school']

def testf(f):
    return f[-4:] == '.pdf' and time.time() - os.stat(f)[8] < (timedif)

def shorten(f):
    return os.sep.join(f[:-4].split(os.sep)[-2:])

timedif = 60*60*16 # 16 hours
fromaddr = '"Wendell Smith" <wws@dartmouth.edu>'
toaddrs = ["wws@dartmouth.edu"]
username = "W. Wendell Smith"
def subj(fs):
    """subj(filename iterator) -> str

Returns a nicely formatted subject line for the message to be sent"""
    s = "print: "
    s += ", ".join(shorten(f) for f in fs)
    return s

fs = []

for t in topdirs:
    for dir, subdirs, files in os.walk(t):
        for f in files:
            fullf = '%s%s%s' % (dir, os.sep, f)
            if testf(fullf):
                fs.append(fullf)

#~ for f in fs: print shorten(f)
def println():
    if fs: 
        print "Subject:", subj(fs)
    else: print "No files to send"

#------------------------------------------------------------------------------


def send_mail(send_from, send_to, subject, text, files, smtp):
    assert type(send_to)==list
    assert type(files)==list
  
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )
    
    print "attaching files:"
    for f in files:
        part = MIMEBase('application', "octet-stream")
        print f
        load = open(f,"rb").read()
        part.set_payload( load )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
           'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
  
    smtp.sendmail(send_from, send_to, msg.as_string())


#------------------------------------------------------------------------------
def main():
    if fs:
        println()
        msg = '\n'.join(fs)
        pw = getpass.getpass("password: ")
        print 'creating connection...'
        smtpserverin = ssmtplib.SMTP_SSL('mailhub.dartmouth.edu', 465)
        print 'logging in...' 
        smtpserverin.login(username, pw)
        print 'sending mail...'
        send_mail(fromaddr, toaddrs, subj(fs), msg, fs, smtpserverin)
        print 'closing connection...'
        smtpserverin.close()

if __name__ == '__main__':
    for f in fs:
        print f
    main()
