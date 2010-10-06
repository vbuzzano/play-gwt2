###############################################################################
# GWT2 Compile Command - tested[2010-06-25]
#
# [gwt2:compile]
# 
# Compile an existing GWT Module
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import string
from gwt2 import *

def getCommands():
	return ["gwt2:compile"]

def getHelp():
	return "Compile a GWT Module"

def execute(args):
	
	# List all modules
	gwtmodule = functions.askForModule(args, 'compile', True)
		
	# Compile selected module
	functions.compile(args, gwtmodule)
