#!/usr/bin/env python

from subprocess import *
from os import kill

def scl(*args, **kwargs):
	kwargs['shell'] = True
	return call(*args, **kwargs)

def rcl(*args, **kwargs):
	kwargs['shell'] = True
	kwargs['stdout'] = PIPE
	return Popen(*args, **kwargs).communicate()[0]
	
def attr(obj):
	try:
		d = obj.__dict__
	except:
		return
	if len(d) == 0:
		print "Empty __dict__"
		return
	for k in obj.__dict__:
		print "%10s: %s" % (str(k), str(d[k]))
		return

def getpids():
	output = rcl('ps -eo pid,cmd').strip().split('\n')
	lst = [i.strip().partition(' ') for i in output[1:]]
	d = dict([(i[-1],int(i[0])) for i in lst])
	return d

def pid(s):
	lst = []
	pids = getpids()
	for p in pids:
		if s in p:
			lst.append(pids[p])
	return tuple(lst)