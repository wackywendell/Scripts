
import sys
import terminal

class ProgressPrinter:
	def __init__(self, beginmsg):
		self.lines = 0
		beginmsg = '\r'.join(beginmsg.split('\n'))
		sys.stdout.write("\r"+beginmsg)
		self.lines = len(beginmsg/split("\r"))
	
	def clear(self):
		if self.lines == 0:
			return
		sys.stdout.write(
			self.lines * (terminal.UP + terminal.BOL + terminal.CLEAR_EOL)
			)
		
	
	def writemsg(self, msg):
		self.clear()
		beginmsg = '\r'.join(beginmsg.split('\n'))
		sys.stdout.write("\r"+beginmsg)
		self.lines = len(beginmsg/split("\r"))
	
if __name__ == "__main__":
	import time
	p = ProgressPrinter("TEST 0")
	for i in range(3):
		sleep(.3)
		p.writemsg("TEST " + str(i))
		
