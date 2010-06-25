###############################################################################
# GWT2 Clean Command - tested[2010-06-25]
#
# [gwt2:clean]
# 
# Clean an existing GWT Module
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import sys, os, string
from gwt2 import *

def getCommands():
	return ["gwt2:clean"]

def execute(args):
	gwt2_modules_path = args.get("gwt2_modules_path")
	gwt2_public_path = args.get("gwt2_public_path")
	application_path = args.get("app").path
	
	# List all modules
	gwtmodule = functions.askForModule(args, 'clean', True)
	
	# delete the  app
	if not os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		print "~"
		print "~ Error: module " + gwtmodule + " not found."
		print "~"		
		sys.exit(1)
	
	# clean public dir
	if os.path.exists(os.path.join(application_path, gwt2_public_path, gwtmodule)):
		shutil.rmtree(os.path.join(application_path, gwt2_public_path, gwtmodule))
	
	print "~"
	print "~ GWT Module " + gwtmodule + " has been cleaned."
	print "~"
