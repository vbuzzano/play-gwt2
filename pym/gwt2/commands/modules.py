###############################################################################
# GWT2 Modules Command - tested[2010-10-07]
#
# [gwt2:modules]
# 
# List all modules in an application
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
from gwt2 import *

def getCommands():
	return ["gwt2:modules", "gwt2:list"]

def getHelp():
	return "List all GWT Modules"

def execute(args):
	functions.listModules(args)
