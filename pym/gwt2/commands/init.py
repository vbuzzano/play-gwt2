###############################################################################
# GWT2 Init command - tested[2010-10-07]
#
# [gwt2:init] 
#
# Init GWT project. Create needed folder and copy gwt-user.jar 
# to the targeted application
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import getopt, sys, os, inspect, shutil, string

from play.utils import *

import create

def getCommands():
	return ["gwt2:init"]

def getHelp():
	return "Initialize the application"

def execute(args):
	app = args.get("app")
	public_dir = args.get("public_dir")
	modules_dir = args.get("modules_dir")
	gwt_path = args.get("gwt_path")
	
	# Create gwt2_public_dir
	if not os.path.exists(os.path.join(app.path, public_dir)):
		os.mkdir(os.path.join(app.path, public_dir))
	
	# Create gwt2_modules_dir
	if not os.path.exists(os.path.join(app.path, modules_dir)):
		os.mkdir(os.path.join(app.path, modules_dir))
	
	# Create folder lib if not exists
	if not os.path.exists(os.path.join(app.path, "lib")):
		os.mkdir(os.path.join(app.path, "lib"))
	
	# Create base module
	#create.createModule(app, args.get("env"), args.get("gwt2_module_dir"), modules_dir, "")
	
	# Copy libs
	shutil.copyfile(os.path.join(gwt_path, 'gwt-user.jar'), os.path.join(app.path, 'lib/gwt-user.jar'))
	
	# init main module
	isAlreadyInit(app)
	initMainModule(app, args.get("env"), args.get("gwt2_module_dir"))
	
	print "~ Application ready..."
	print "~"

# Initialize Application
def initMainModule(app, env, gwt2_module_dir):
	modulename = "app"
	
	# create app xml def
	file = os.path.join(app.path, 'app', modulename.capitalize()+'.gwt.xml')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'Main.gwt.xml'), file)
	replaceAll(file, r'\[modulename\]', modulename)
	replaceAll(file, r'\[othermodule\]', "<inherits name='play.modules.gwt2.PlayGWT2'/>")
	replaceAll(file, r'\[entrypointclass\]', "")
	replaceAll(file, r'\[sourcepath\]', "<source path='models'/>")

# Check if the application has already been initialized. if yes, we stop the command
def isAlreadyInit(app):
	modulename = "app"
	file = os.path.join(app.path, 'app', modulename.capitalize()+'.gwt.xml')
	if os.path.exists(file):
		print "this application has already been initialized with play-gwt2"
		sys.exit(-1)

	