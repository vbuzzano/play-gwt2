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
	public_dir = args.get("public_dir")
	modules_dir = args.get("modules_dir")
	gwt_path = args.get("gwt_path")

	# app clean
	pathmodule = os.path.join(application_path, public_dir, 'app') 
	if os.path.exists(pathmodule):		
		shutil.rmtree(pathmodule)
		print "~ app (Application module) has been cleaned."
	
	# modules cleans	
	path = os.path.join(application_path, modules_dir)
	for dir in os.listdir(path):
		file = os.path.join(path, dir, dir.capitalize()+'.gwt.xml')
		if os.path.exists(file):
			pathmodule = os.path.join(application_path, public_dir, dir) 
			if os.path.exists(pathmodule):		
				shutil.rmtree(pathmodule)
			print "~ " + dir + " has been cleaned."
	
	print "~"
	print "~ done"
	print "~"

