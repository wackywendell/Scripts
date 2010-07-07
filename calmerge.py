#!/usr/bin/env python

import icalendar, shelve

dbfname = '~/.config/calmerge'
db=shelve.open(dbfname)
db.close()

