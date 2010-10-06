###############################################################################
# GWT2 Remove - tested[2010-06-25]
#
# [gwt2:remove]
# 
# Remove a GWT Module
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import sys, os, string, shutil

from gwt2 import *

def getCommands():
	return ["gwt2:remove"]

def getHelp():
	return "Remove a GWT Module"

def execute(args):
	application_path = args.get("app").path
	gwt2_modules_path = args.get("gwt2_modules_path")
	gwt2_public_path = args.get("gwt2_public_path")
	
	# List all modules
	gwtmodule = functions.askForModule(args, 'remove', True)
	
	# delete the  app
	if not os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		print "~"
		print "~ Error: module " + gwtmodule + " not found."
		print "~"		
		sys.exit(1)
	
	if os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		shutil.rmtree(os.path.join(application_path, gwt2_modules_path, gwtmodule))
	
	if os.path.exists(os.path.join(application_path, gwt2_public_path, gwtmodule)):
		shutil.rmtree(os.path.join(application_path, gwt2_public_path, gwtmodule))
	
	print "~"
	print "~ Ok. Your GWT module has been deleted "
	print "~"
