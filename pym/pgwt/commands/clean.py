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
from pgwt import *

def getCommands():
	return ["gwt2:clean"]

def getHelp():
	return "Clean a compiled GWT Module"


def execute(args):
	application_path = args.get("app").path
	public_dir = args.get("public_dir")
	modules_dir = args.get("modules_dir")
	gwt_path = args.get("gwt_path")
	
	# List all modules
	modulename = functions.askForModule(args, 'clean', True, True)
		
	# delete the  app
	modulepath = None
	if modulename != 'app':
		modulepath = os.path.join(application_path, modules_dir, modulename)	
		if not os.path.exists(modulepath):
			print "~"
			print "~ Error: module " + modulename + " not found."
			print "~"		
			sys.exit(1)
	
	# clean public dir
	modulepath = None
	if os.path.exists(os.path.join(application_path, public_dir, modulename)):
		shutil.rmtree(os.path.join(application_path, public_dir, modulename))
	if os.path.exists(os.path.join(application_path, public_dir, 'WEB-INF','deploy',modulename)):
		shutil.rmtree(os.path.join(application_path, public_dir, 'WEB-INF','deploy',modulename))
	
	print "~"
	print "~ done"
	print "~"

