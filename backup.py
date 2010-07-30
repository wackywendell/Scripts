#!/usr/bin/env python
from __future__ import print_function, unicode_literals
from myspath import path
from subprocess import Popen
#import commands
#from dateutil.parser import parse as parser
from datetime import datetime

now = datetime.today()


#variables
diskpath = path('/media/backup/rsynced')
foldername = '%Y%m%d-%H%M%S'
numbackups=10

rsyncdirs = ['/home','/bin','/boot','/data','/etc','/var','/usr',
             '/lib','/root']
# minimal
rsyncdirs = ['/home','/boot','/data']
rsyncopts = ['--archive', '--backup', 
             '--verbose', '--progress', '--itemize-changes',
             '--delete', # in case there's somehow already junk in that folder
                         # from a failed backup
             '--delete-excluded'
             ]

#code
# mount
if not diskpath.exists():
    print('Mounting...')
    backupdev=(
        '/dev/disk/by-id/usb-WD_2500BMV_' + 
        'External_57442D575845583038414638363538-0:0-part1')
    mntargs = ['sudo','mount','-text4',backupdev, '/media/backup']
    mntproc = Popen(mntargs)
    mntproc.wait()

if not diskpath.exists():
    raise IOError("Backup directory {0} does not exist".format(diskpath))

destdir = diskpath + 'tmp'

backedup = sorted([d for d in diskpath.getdirs() if d != destdir])
if len(backedup) > 0:
    lastbackup = backedup[-1]
    rsyncopts.append(r'--link-dest={0}'.format(str(lastbackup)))
    print('Using hard links from',lastbackup)

nowbackup = diskpath + now.strftime(foldername)
# we backup to 'tmp', and then rename it when it completes. This means that
# unfinished backups get written over and completed, and only complete
# backups are given numbers. This is also especially useful for conserving disk 
# space - only completed backups are available for hard-linking.
if not destdir.exists():
    destdir.mkdir()
# run rsync
dirsasargs = [str(d) for d in rsyncdirs]


opts = rsyncopts + dirsasargs + [str(destdir)]
cmd = ['sudo','rsync'] + opts
try:
    process = Popen(cmd)
    process.wait()
except KeyboardInterrupt:
    print('KeyboardInterrupt, breaking.')
    Popen(['sudo','kill','-INT',str(process.pid)]).wait()
    try:
        process.wait()
    except KeyboardInterrupt:
        print('KeyboardInterrupt. Terminating!')
        Popen(['sudo','kill','-TERM',str(process.pid)]).wait()
        try:
            process.wait()
        except KeyboardInterrupt:
            print('KeyboardInterrupt. KILLING!')
            Popen(['sudo','kill','-KILL',str(process.pid)]).wait()
    process.wait()
    print('Unfinished backup in ' + str(destdir))
    exit()
if process.returncode != 0:
    Popen(['notify-send', '--icon=computer','Backup failed', 
        'Backup failed with return value {0}.'.format(process.returncode)]).wait()
    exit()

destdir.move(nowbackup)
Popen(['notify-send', '--icon=computer','Backup finished', 
        'Finished backing up to {0}.'.format(str(nowbackup))]).wait()