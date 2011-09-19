###############################################################################
# GWT2 Plugin for Play! 1.2.2
# by Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import getopt, sys, os, inspect
global gwt2_module_dir, command_dir
gwt2_module_dir = inspect.getfile(inspect.currentframe()).replace("commands.py","")
command_dir = os.path.join(gwt2_module_dir, "pym", "pgwt", "commands")
sys.path.append(os.path.join(gwt2_module_dir, "pym"))

from pgwt import *
from pgwt.commands import *
from play.utils import *
from play.commands import deps

###############################################################################
# Call a module command 
###############################################################################
def callModuleCommand(args):
	global command_dir
	module = None
	command = args.get("command")
	
	for file in os.listdir(command_dir):
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
	kargs['public_path'] = app.readConf('gwt2.publicpath')
	if kargs['public_path'] == None or kargs['public_path'] == '':
		kargs['public_path'] = '/app'

	# gwt plublic dir
	kargs['public_dir'] = app.readConf('gwt2.publicdir')
	if kargs['public_dir'] == None or kargs['public_dir'] == '':
		kargs['public_dir'] = 'gwt-public'

	# get modules dir
	modules_dir = kargs.get("modules_dir")
	if not modules_dir:
		modules_dir = app.readConf('gwt2.modulesdir')
		if modules_dir == "":
			modules_dir = 'gwt'
	
	kargs['modules_base_classpath'] = modules_dir.replace(os.sep,".") + "."
	
	kargs['modules_dir'] = os.path.join('app', modules_dir)
	
	# Module path (this_path)
	kargs['gwt2_module_dir'] = gwt2_module_dir
	
	# Check options
	gwt_path = "notset"
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
	
	if not gwt_path and os.environ.has_key('GWT_HOME'):
		gwt_path = os.path.normpath(os.path.abspath(os.environ['GWT_HOME']))
	
	if gwt_path != "notset":
		kargs['gwt_path'] = gwt_path
	
	# execute command
	callModuleCommand(kargs)

###############################################################################
# After Commands 
###############################################################################
def after(**kargs):
	command = kargs.get("command")
	app = kargs.get("app")
	args = kargs.get("args")
	env = kargs.get("env")
	modules_dir = "modules"
	
	# ~~~~~~~~~~~~~~~~~~~~~~ new
	if command == 'new':
		# add google dependencies		
		depspath = os.path.join(app.path, 'conf/dependencies.yml')
		depsfile = open(depspath,"a")
		depsfile.write('\n    - com.google.gwt -> gwt-user 2.3.0\n')
		depsfile.write('    - com.google.gwt -> gwt-dev 2.3.0\n')
		depsfile.close()
		
		# Add gwt2 configuration
		confpath = os.path.join(app.path, 'conf/application.conf')
		conffile = open(confpath,"a")
		conffile.write('\n# GWT module dir\n# ~~~~~\n# use to define the directory where modules will be store\ngwt2.modulesdir=' + modules_dir + '\n')
		conffile.write('\n# GWT public dir\n# ~~~~~\n# use to define where gwt will compile and expose modules\ngwt2.publicdir=gwt-public/modules\n')
		conffile.write('\n# GWT public path\n# ~~~~~\n# base name for route.\n# gwt2.publicpath=/app\n')
		conffile.write('\n# GWT devmode startupUrls\n# gwt2.devmode.url.auto=true\ngwt2.devmode.url.1=/\n')

		conffile.close()
				
		# execute play dependencies
	        deps.execute(command='dependencies', app=app, args=['--sync'], env=env, cmdloader=None)
		
		# init
		execute(command="gwt2:init", app=app, modules_dir=modules_dir, args=[], env=env)
		
		# add module to application routes
		file = os.path.join(app.path, 'conf', "routes")
		replaceAll(file, '# Ignore favicon requests', '# Play! GWT2 Modules\n*       /                                       module:gwt2\n\n# Ignore favicon requests')
		
		# update gwt application xml
		file = os.path.join(app.path, 'app', 'App.gwt.xml')
		replaceAll(file, '    <!-- Specify the app entry point class.                         -->', '    <!-- Specify the app entry point class.                         -->\n    <entry-point class="client.Application"/>')
		replaceAll(file, "<source path='shared'/>", "<source path='client'/>\n    <source path='shared'/>")
		
		# remove javascripts
		if os.path.exists(os.path.join(app.path, 'public', 'javascripts')):
			shutil.rmtree(os.path.join(app.path, 'public', 'javascripts'))               
                


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
for file in os.listdir(command_dir):
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
MODULE = 'gwt2' 

