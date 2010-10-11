###############################################################################
# GWT2 Clean All Command - tested[2010-10-07]
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
	public_path = args.get("public_path")
	modules_path = args.get("modules_path")
	gwt_path = args.get("gwt_path")
	
	path = os.path.join(application_path, modules_path)
	for dir in os.listdir(path):
		file = os.path.join(path, dir, dir.capitalize()+'.gwt.xml')
		if os.path.exists(file):
			pathmodule = os.path.join(application_path, public_path, dir) 
			if os.path.exists(pathmodule):		
				shutil.rmtree(pathmodule)
			print "~ " + dir + " has been cleaned."
	
	print "~"
