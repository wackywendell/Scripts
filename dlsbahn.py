#!/usr/bin/python
# encoding:UTF-8

#from __future__ import (absolute_import, print_function,
#                        division, unicode_literals)
from __future__ import (absolute_import, print_function, division)
from future_builtins import filter, map, zip

import httplib2, os, logging, logging.handlers
from fpath import *
from datetime import datetime
import subprocess, zipfile, StringIO

mydir=Path("/home/wendell/Dropbox/Us/Germany Documents/berlin transportation")

LOG_FILENAME = str("/home/wendell/.config/sbahn.log")
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=2*1000*1000, backupCount=5)
my_logger.addHandler(handler)

my_logger.debug('----------------' + logging.time.ctime())

fbase = "http://www.s-bahn-berlin.de/fahrplanundnetz/pdf/"
fbase2 = "http://www.s-bahn-berlin.de/pdf/"
fpaths = [
    fbase + "MoFr_BGWD_Richtung_BWKR.pdf",
    fbase + "MoFr_BGWD_Richtung_BNIS.pdf",
    fbase + "SaSo_BGWD_Richtung_BWKR.pdf",
    fbase + "SaSo_BGWD_Richtung_BNIS.pdf",
    fbase2 + "S+U-Liniennetz.pdf",
    fbase2 + "VBB-Liniennetz.pdf"]
#fpaths = fpaths[4:5]
fnames = [
    'S7-Weekday-Inbound.pdf',
    'S7-Weekday-Outbound.pdf',
    'S7-Weekend-Inbound.pdf',
    'S7-Weekend-Outbound.pdf',
    'map-S-U-bahn.pdf',
    'map-VBB.pdf']

fnames = [File(mydir + f) for f in fnames]

zipf='http://www.vbbonline.de/software/WINKOMP526.ZIP'
zipdir = Path('/home/wendell/Dropbox/Us/Germany Documents/vbb update')

h = httplib2.Http(os.path.expanduser('~/.cache/sbahn'))

def getfile(hname):
    my_logger.debug('Getting ' + str(hname))
    
    try:
        resp, txt = h.request(str(hname))
    except Exception as e:
        my_logger.exception('ERROR DOWNLOADING FILE ' + hname)
        #my_logger.debug('Full Response: ' + str(resp))
        return None, False
    
    if resp['status'] == '404':
        my_logger.debug('File not found. Response: ' + str(resp['status']))
        return None, False
    if resp['status'] != '304':
        my_logger.debug('File Retrieved with Response: ' + str(resp['status']))
        return txt, resp['status']
    else:
        my_logger.debug('File not new. Response: ' + str(resp['status']))
        return txt, False

def getsavefile(hname, fname):
    fname = Path(fname)
    txt, new = getfile(hname)
    if txt == None:
        return False
    if fname.stat().isfile and not new:
        #fname.touch()
        return new
    
    my_logger.debug('Writing file: ' + str(fname))
    with open(str(fname), 'w') as f:
        f.write(txt)
    return new

def dlzipfile(hpath, dir):
    txt,new = getfile(hpath)
    if not new:
        my_logger.debug('File not new: ' + str(hpath))
        return False
    try:
        my_logger.debug('Extracting Zipfile to ' + str(dir))
        sioobj = StringIO.StringIO(txt)
        zipobj = zipfile.ZipFile(sioobj)
        zipobj.extractall(str(zipdir))
    except Exception:
        my_logger.exception('ERROR EXTRACTING FILE')
        return False
    return True

if __name__ == '__main__':
    for fp, fn in zip(fpaths, fnames):
        new = getsavefile(fp,fn)
        if new:
            #print('NEW:', fn)
            subprocess.Popen(('evince',str(fn)))
    
    new = dlzipfile(zipf, zipdir)
    if new:
        try:
            setuppath = zipdir + 'SETUP.EXE'
            if not setuppath.isfile():
                my_logger.exception('FILE DOES NOT EXIST: ' + str(setuppath))
            subprocess.Popen(('wine',str(setuppath)))
        except Exception:
            raise
            