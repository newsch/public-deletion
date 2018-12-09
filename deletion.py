import os
import random
import dircache
import serial
import time
import win32api
import win32print
import tempfile

rootdir = 'C:\Users\iharrison\publicprint'

def readSignal():
	ser = serial.Serial('COM11', 9600)
	while True:
		value = ser.readline()
		print value
		if value:
			print 'inside'
			print chooseFile(rootdir)
			time.sleep(1)
			

def chooseFile(dir):
  	dircache.reset()
  	list = dircache.listdir(dir)
  	dircache.annotate(dir, list )
 	if list == []:
		print 'restarting'
		return chooseFile('C:\Users\iharrison\publicprint')
 	else: 
 		filename = random.choice(list)
 		path = os.path.join(dir, filename)
	if path[-1] == '/':	
		path = path[:-1]
		return chooseFile(path)
	else:
 		return path


def printFile(path):	
	# open (path, "w").write ("This is a test")
	# http://timgolden.me.uk/pywin32-docs/win32api__ShellExecute_meth.html
	win32api.ShellExecute (
	  0,
	  "print",
	  path,
	  #
	  # If this is None, the default printer will
	  # be used anyway.
	  #
	  '/d:"\\17NHT32\%s"' % "HP ENVY 5660 series (copy 1)",
	  ".",
	  0
	)