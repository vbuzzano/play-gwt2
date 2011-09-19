###############################################################################
# GWT2 Compile Command - tested[2010-10-07]
#
# [gwt2:compile]
# 
# Compile an existing GWT Module
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import string
from pgwt import *

def getCommands():
	return ["gwt2:compile"]

def getHelp():
	return "Compile a GWT Module"

def execute(args):
	
	# List all modules
	modulename = functions.askForModule(args, 'compile', True, True)
	
	# Compile selected module
	print "~ ---------------------- "
	ret = functions.compile(args, modulename)
	print "~ ---------------------- "
	
	print "~"
	if ret:
		print "~ done"
	else:
		print "~ failed"
	print "~"

