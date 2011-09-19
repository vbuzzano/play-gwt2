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
	
	# Create client dir
	if not os.path.exists(os.path.join(app.path, "app", "client")):
		os.mkdir(os.path.join(app.path, "app", "client"))

	if not os.path.exists(os.path.join(app.path, "app", "client", "services")):
		os.mkdir(os.path.join(app.path, "app", "client", "services"))

	if not os.path.exists(os.path.join(app.path, "app", "client", "ui")):
		os.mkdir(os.path.join(app.path, "app", "client", "ui"))

	# Create services dir
	if not os.path.exists(os.path.join(app.path, "app", "services")):
		os.mkdir(os.path.join(app.path, "app", "services"))
	
	# Create shared dir
	if not os.path.exists(os.path.join(app.path, "app", "shared")):
		os.mkdir(os.path.join(app.path, "app", "shared"))
			
	# find if gwt lib is present
	gwtuserok = 0
	gwtdevok = 0
	for file in os.listdir(os.path.join(app.path, "lib")):
		if file.startswith("gwt-user"):
			gwtuserok = 1
		if file.startswith("gwt-dev"):
			gwtdevok = 1
	if gwtuserok == 0 or gwtdevok == 0:
		# if nothing has been found. stop
		if not gwt_path:
			print "~ "
			print "~ Error: You need to specify the path of you GWT installation, "
			print "~ either using the $GWT_PATH or $GWT_HOME environment variable or with the --gwt option" 
			print "~ OR add \n~    - com.google -> gwt-user 2.3.0\n~    - com.google -> gwt-dev 2.3.0\n to you dependencies.yml file and execute 'play deps' before runing gwt2:init again\n"
			sys.exit(-1)
		
		# check for minimum library
		if not os.path.exists(os.path.join(gwt_path, 'gwt-user.jar')) or not os.path.exists(os.path.join(gwt_path, 'gwt-dev.jar')):
			print "~ "
			print "~ Error: %s is not a valid GWT installation (checked for gwt-user.jar and gwt-dev.jar)" % gwt_path
			print "~ This module has been tested with GWT 2.3.0"
			print "~ "
			sys.exit(-1)
	
	# init main module
	isAlreadyInit(app)
	initApplication(app, args.get("env"), args.get("gwt2_module_dir"), modules_dir)
	
	print "~ Application ready..."
	print "~"

# Initialize Application
def initApplication(app, env, gwt2_module_dir, modules_dir):
	modulename = "app"
	
	# replace favicon
	os.remove(os.path.join(app.path, 'public', 'images', 'favicon.png'))
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'favicon.png'), os.path.join(app.path, 'public', 'images', 'favicon.png'))
	
	# replace view/main.html
	os.remove(os.path.join(app.path, 'app', 'views', 'main.html'))
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'main.html'), os.path.join(app.path, 'app', 'views', 'main.html'))
	
	# replace css
	os.remove(os.path.join(app.path, 'public', 'stylesheets', 'main.css'))
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'main.css'), os.path.join(app.path, 'public', 'stylesheets', 'main.css'))


	# create app xml def
	file = os.path.join(app.path, 'app', modulename.capitalize()+'.gwt.xml')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'Main.gwt.xml'), file)
	replaceAll(file, r'\[modulename\]', modulename)
	replaceAll(file, r'\[othermodule\]', "<inherits name='play.modules.gwt2.PlayGWT2'/>")
	replaceAll(file, r'\[entrypointclass\]', "client.Application")
	replaceAll(file, r'\[sourcepath\]', "<source path='client'/>\n    <source path='shared'/>\n    <source path='models'/>")
	
	# replace views/Application/index.html
	os.remove(os.path.join(app.path, 'app', 'views', 'Application', 'index.html'))
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'index.html'), os.path.join(app.path, 'app', 'views', 'Application', 'index.html'))

	# copy entry point
	file = os.path.join(app.path, 'app', 'client', 'Application.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'appApplication.java'), file)
	
	# copy service class	
	tmpfile = os.path.join(app.path, 'app', 'client', 'services', 'GreetingService.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'appGreetingService.java'), tmpfile)
	
	tmpfile = os.path.join(app.path, 'app', 'client', 'services', 'GreetingServiceAsync.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'appGreetingServiceAsync.java'), tmpfile)
	
	tmpfile = os.path.join(app.path, 'app', 'services', 'Greeting.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'appGreeting.java'), tmpfile)
	
	tmpfile = os.path.join(app.path, 'app', 'shared', 'FieldVerifier.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'appFieldVerifier.java'), tmpfile)


# Check if the application has already been initialized. if yes, we stop the command
def isAlreadyInit(app):
	modulename = "app"
	file = os.path.join(app.path, 'app', modulename.capitalize()+'.gwt.xml')
	if os.path.exists(file):
		print "~ "
		print "~ this application has already been initialized with play-gwt2"
		print "~ "
		sys.exit(-1)

	
