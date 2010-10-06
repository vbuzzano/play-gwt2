###############################################################################
# GWT2 Clean All Command - tested[2010-06-25]
#
# [gwt2:cleanall]
# 
# Clean all existing GWT Modules
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import os, shutil

def getCommands():
	return ["gwt2:cleanall"]

def getHelp():
	return "Clean all compiled GWT Modules"

def execute(args):
	
	application_path = args.get("app").path
	gwt2_modules_path = args.get("gwt2_modules_path")
	gwt2_public_path =  args.get("gwt2_public_path")
	
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		pathmodule = os.path.join(application_path, gwt2_public_path, dir) 
		if os.path.exists(pathmodule):		
			shutil.rmtree(pathmodule)
		print "~ " + dir + " has been cleaned."
	
	print "~"
