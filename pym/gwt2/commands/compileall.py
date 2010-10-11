###############################################################################
# GWT2 Compile all Command - tested[2010-10-07]
#
# [gwt2:compileall]
# 
# Compile all existing GWT Modules
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import os
from gwt2 import *

def getCommands():
	return ["gwt2:compileall"]

def getHelp():
	return "Compile all GWT Modules"

def execute(args):
	application_path = args.get("app").path
	modules_path = args.get("modules_path")

	print "~"
	print "~ Compiling all modules ... "
	print "~"
	path = os.path.join(application_path, modules_path)
	for dir in os.listdir(path):
		file = os.path.join(path, dir, dir.capitalize()+'.gwt.xml')
		if os.path.exists(file):
			functions.compile(args, dir)
