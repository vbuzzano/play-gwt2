###############################################################################
# GWT2 Compile all Command - tested[2010-06-25]
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

def execute(args):
	application_path = args.get("app").path
	gwt2_modules_path = args.get("gwt2_modules_path")

	print "~"
	print "~ Compiling all modules ... "
	print "~"
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		functions.compile(args, dir)
