###############################################################################
# GWT2 Compile all Command - tested[2011-01-10]
#
# [gwt2:compileall]
# 
# Compile all existing GWT Modules
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import os
from pgwt import *

def getCommands():
	return ["gwt2:compileall"]

def getHelp():
	return "Compile all GWT Modules"

def execute(args):
	application_path = args.get("app").path
	modules_dir = args.get("modules_dir")
	
	print "~"
	print "~ Compiling application ... "
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	success = True
	
	# compile application module
	if not functions.compile(args, 'app'):
		success = False
	
	if success:	
		# compile modules
		modules = []
		path = os.path.join(application_path, modules_dir)
		for dir in os.listdir(path):
			if (dir[0] != '.'):
				file = os.path.join(path, dir, dir.capitalize()+'.gwt.xml')
				if os.path.exists(file):
					modules.append(dir)
		if len(modules) > 0:
			print "~"
			print "~ Compiling all modules ... "
			for modul in modules:
				if success:
					print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
					if not functions.compile(args, modul):
						sucess = False
	
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print "~"
	if success:
		print "~ done"
	else:
		print "~ failed"
	print "~"

