#!/usr/bin/python
from myemaillib import mysmtp
from myspath import path
from dateutil.tz import tzlocal
from dateutil.parser import parse as dateparser
from datetime import datetime
import commands
import logging


LOG_FILENAME = '/home/wendell/jennyemails/log.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

frm='wackywendell@gmail.com'
uname=frm
to=[frm,'jenny.strakovsky@gmail.com']
#to=[frm,'wendell.smith@yale.edu']
pword='66969072'
defaultdate = datetime(2009,7,26,tzinfo=tzlocal())
now = dateparser(commands.getoutput('date'))

logging.debug('RUNNNING: ' + str(now))

dir = path('/home/wendell/jennyemails')

fs = [(dateparser(f[-1], default = defaultdate), f) for f in dir.getfiles()
        if 'log' not in str(f)]
fstogo = sorted((d,f) for (d,f) in fs if d <= now)

if list(fstogo):
    with mysmtp(uname,pword) as smtp:
        for d,fname in fstogo:
            logging.debug(str(d) + ' ' + repr(d))
            logging.debug(str(fname))
            with open(str(fname)) as f:
                txt = f.read()
                smtp.sendmail(frm, to, txt)
            logging.debug('SENT')
            dst = fname[:-1] + 'old' + fname[-1]
            fname.move(dst)
            logging.debug('MOVED')
else:
    logging.debug('No files to send found.')
