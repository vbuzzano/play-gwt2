###############################################################################
# GWT2 Plugin for Play! 1.1
# by Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import getopt, sys, os, inspect

script_path = inspect.getfile(inspect.currentframe()).replace("commands.py","")
sys.path.append(os.path.join(script_path, "pym"))

from gwt2 import *
from gwt2.commands import *
from play.utils import *

play_app = None
play_env = None
play_command = None
play_remaining_args = None


COMMANDS = ["gwt2:", 
			"gwt2:help", 
			"gwt2:init", 
			"gwt2:modules", 
			"gwt2:list",			
			"gwt2:remove", 
			"gwt2:clean", 
			"gwt2:cleanall", 
			"gwt2:compile", 
			"gwt2:compileall", 
			"gwt2:create", 
			"gwt2:devmode" 
		   ]

###############################################################################
# Module Execute 
###############################################################################
def execute(**kargs):
	# get application
	app = kargs.get("app")
	
	# get env
	env = kargs.get("env")
	
	# get command
	command = kargs.get("command")
	
	# get args
	play_remaining_args = kargs.get("args")
		
	# gwt plublic path	
	kargs['gwt2_public_path'] = "gwt-public"
	
	# gwt modules path
	kargs['gwt2_modules_path'] = os.path.join("app","gwt")
	
	# Module path (this_path) 
	kargs['module_path'] = inspect.getfile(inspect.currentframe()).replace("commands.py","")

	# Check options
	gwt_path = None
	try:
		optlist, args = getopt.getopt(play_remaining_args, '', ['gwt='])
		for o, a in optlist:
			if o == '--gwt':
				gwt_path = os.path.normpath(os.path.abspath(a))
	except getopt.GetoptError, err:
		print "~ %s" % str(err)
		print "~ "
		sys.exit(-1)
	
	# if path has not been set via arguments, we check for OS variable
	if not gwt_path and os.environ.has_key('GWT_PATH'):
		gwt_path = os.path.normpath(os.path.abspath(os.environ['GWT_PATH']))
	
	# if nothing has been found. stop
	if not gwt_path:
		print "~ Error: You need to specify the path of you GWT installation, "
		print "~ either using the $GWT_PATH environment variable or with the --gwt option" 
		print "~ "
		sys.exit(-1)
	
	# check for minimum library
	if not os.path.exists(os.path.join(gwt_path, 'gwt-user.jar')) or not os.path.exists(os.path.join(gwt_path, 'gwt-dev.jar')):
		print "~ Error: %s is not a valid GWT installation (checked for gwt-user.jar and gwt-dev.jar)" % gwt_path
		print "~ This module has been tested with GWT 2.0.3"
		print "~ "
		sys.exit(-1)
	
	kargs['gwt_path'] = gwt_path
	
	# execute to comand
	if command == 'gwt2:help':
		help.execute(kargs)
	elif command == 'gwt2:init':
		init.execute(kargs)
	elif command == 'gwt2:modules':
		modules.execute(kargs)
	elif command == 'gwt2:list':
		modules.execute(kargs)
	elif command == 'gwt2:remove':
		remove.execute(kargs)
	elif command == 'gwt2:clean':
		clean.execute(kargs)
	elif command == 'gwt2:cleanall':
		cleanall.execute(kargs)
	elif command == 'gwt2:compile':
		compile.execute(kargs)
	elif command == 'gwt2:compileall':
		compileall.execute(kargs)
	elif command == 'gwt2:create':
		create.execute(kargs)
	elif command == 'gwt2:devmode':
		devmode.execute(kargs)

	