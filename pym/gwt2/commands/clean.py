###############################################################################
# GWT2 Clean Command - tested[2010-10-07]
#
# [gwt2:clean]
# 
# Clean an existing GWT Module
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import sys, os, string, shutil
from gwt2 import *

def getCommands():
	return ["gwt2:clean"]

def getHelp():
	return "Clean a compiled GWT Module"


def execute(args):
	application_path = args.get("app").path
	public_path = args.get("public_path")
	modules_path = args.get("modules_path")
	gwt_path = args.get("gwt_path")
	
	# List all modules
	modulename = functions.askForModule(args, 'clean', True)
	
	# delete the  app
	if not os.path.exists(os.path.join(application_path, modules_path, modulename)):
		print "~"
		print "~ Error: module " + modulename + " not found."
		print "~"		
		sys.exit(1)
	
	# clean public dir
	if os.path.exists(os.path.join(application_path, public_path, modulename)):
		shutil.rmtree(os.path.join(application_path, public_path, modulename))
	
	print "~"
	print "~ GWT Module " + modulename + " has been cleaned."
	print "~"
