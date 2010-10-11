###############################################################################
# GWT2 Plugin for Play! 1.1
# by Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import getopt, sys, os, inspect
global module_path, command_path
module_path = inspect.getfile(inspect.currentframe()).replace("commands.py","")
command_path = os.path.join(module_path, "pym", "gwt2", "commands")

sys.path.append(os.path.join(module_path, "pym"))
from gwt2 import *
from gwt2.commands import *
from play.utils import *

###############################################################################
# Call a module command 
###############################################################################
def callModuleCommand(args):
	global command_path
	module = None
	command = args.get("command")
	
	for file in os.listdir(command_path):
		if file[-3:] == '.py' and file[0:2] != '__':
			m = file[0:-3]+".getCommands()"
			cmd = eval(m)
			for item in cmd :
				if item == command :
					module = file[0:-3]
	
	if command != "" and module != None:
		eval(module+'.execute(args)')

###############################################################################
# Module Execute 
###############################################################################
def execute(**kargs):
	global args
	args = kargs
	
	# get application
	app = kargs.get("app")
	
	# get env
	env = kargs.get("env")
	
	# get args
	play_remaining_args = kargs.get("args")
	
	# gwt plublic path	
	kargs['public_path'] = "gwt-public"
	
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
	
	# get module path
	modules_path = app.readConf('gwt2.modulespath')
	if modules_path != "":
		kargs['modules_path'] = os.path.join('app', modules_path)
	else:
		kargs['modules_path'] = os.path.join('app', 'gwt')
	
	# Module path (this_path)
	kargs['gwt2_module_path'] = module_path
	
	# if path has not been set via arguments, we check for OS variable
	if not gwt_path and os.environ.has_key('GWT_PATH'):
		gwt_path = os.path.normpath(os.path.abspath(os.environ['GWT_PATH']))
	
	if not gwt_path and os.environ.has_key('GWT_HOME'):
		gwt_path = os.path.normpath(os.path.abspath(os.environ['GWT_HOME']))
	
	# if nothing has been found. stop
	if not gwt_path:
		print "~ Error: You need to specify the path of you GWT installation, "
		print "~ either using the $GWT_PATH or $GWT_HOME environment variable or with the --gwt option" 
		print "~ "
		sys.exit(-1)
	
	# check for minimum library
	if not os.path.exists(os.path.join(gwt_path, 'gwt-user.jar')) or not os.path.exists(os.path.join(gwt_path, 'gwt-dev.jar')):
		print "~ Error: %s is not a valid GWT installation (checked for gwt-user.jar and gwt-dev.jar)" % gwt_path
		print "~ This module has been tested with GWT 2.0.3"
		print "~ "
		sys.exit(-1)
	
	kargs['gwt_path'] = gwt_path
	
	# execute command
	callModuleCommand(kargs)

###############################################################################
# Init Modules Commands 
###############################################################################
###############################################################################
# Get Dynamic commands and Help List 
###############################################################################
# commands list
clist = []
hlist = {}
#clist.append('eclipsify')
for file in os.listdir(command_path):
	if file[-3:] == '.py' and file[0:2] != '__':
		m = file[0:-3]+".getCommands()"
		cmd = eval(m)
		for item in cmd :
			# append command
			clist.append(item)
			# create command help 
			h = file[0:-3]+".getHelp()"
			try:
				h = eval(h)
			except:
				h = "No help found"
			hlist[item] = h
COMMANDS = clist
HELP = hlist
