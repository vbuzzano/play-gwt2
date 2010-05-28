# GWT2 Plugin for Play!
# by Vincent Buzzano <vincent.buzzano@gmail.com>

import sys,os,inspect

###############################################################################
# Check for GWT_PATH environment variable
###############################################################################
if play_command.startswith('gwt2:'):
	global gwt2_public_path
	global gwt2_modules_path
	global this_path
	this_path = inspect.getfile(inspect.currentframe()).replace("commands.py","")
	gwt2_public_path = "gwt-public"
	gwt2_modules_path = os.path.join("app","gwt")
	gwt_path = None
	try:
		optlist, args = getopt.getopt(remaining_args, '', ['gwt='])
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
		print "~ You need to specify the path of you GWT installation, "
		print "~ either using the $GWT_PATH environment variable or with the --gwt option" 
		print "~ "
		sys.exit(-1)
	# check for minimum library
	if not os.path.exists(os.path.join(gwt_path, 'gwt-user.jar')) or not os.path.exists(os.path.join(gwt_path, 'gwt-dev.jar')):
		print "~ %s seems not to be a valid GWT installation (checked for gwt-user.jar and gwt-dev.jar)" % gwt_path
		print "~ This module has been tested with GWT 2.0.3"
		print "~ "
		sys.exit(-1)

###############################################################################
# function: Display a list of exising modules - tested[24.05.2010]
###############################################################################
def displayModule():
	print "~"
	print "~ GWT Modules list "
	print "~ ---------------- "
	print "~"
	count = 1
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		print "~ * " + dir
		count = count + 1
	print "~"

###############################################################################
# function: Compile a gwt module - tested[24.05.2010]
###############################################################################
def compileModule(gwtmodule):
	# if module exists
	if os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		# Compile GWT Module
		print "~ Compiling GWT Module " + gwtmodule + " ..."
		print "~"
		print "----------------------------------------------"
		# prepare classpath and java
		do_classpath()
		do_java()
		cp = []
		cp.append(os.path.normpath(os.path.join(application_path, 'app')))
		cp.append(os.path.normpath(os.path.join(application_path, 'lib/gwt-user.jar')))
		cp.append(os.path.normpath(os.path.join(gwt_path, 'gwt-dev.jar')))
		for jar in os.listdir(os.path.join(application_path, 'lib')):
			if jar.endswith('.jar'):
				cp.append(os.path.normpath(os.path.join(application_path, 'lib/%s' % jar)))
		cps = ':'.join(cp)
		if os.name == 'nt':
			cps = ';'.join(cp)
		gwt_cmd = [java_path, '-Xmx256M', '-classpath', cps, 'com.google.gwt.dev.Compiler', '-style', 'OBF', '-war', os.path.normpath(os.path.join(application_path, gwt2_public_path)), 'gwt.'+gwtmodule+"."+gwtmodule.capitalize()]
		subprocess.call(gwt_cmd, env=os.environ)
		print "----------------------------------------------"
		print "~"
		print "~ GWT Module " + gwtmodule + " compiled."
		print "~"		
	else:
		print "~"
		print "~ Error: GWT Module " + gwtmodule + " not found."
		print "~"		

###############################################################################
# [gwt2:help] Display Help 
###############################################################################
if play_command == 'gwt2:help':
	print "~"
	print "~ GWT2 Plugin for Play! Help"
	print "~ --------------------------"
	print "~"
	print "~ Usage: play gwt2:cmd [app_path] [--options]"
	print "~ "
	print "~ cmd:"  
	print "~        init       Initialize the application"
	print "~        modules    List all GWT Modules"
	print "~        create     Create a new GWT Module"
	print "~        remove     Remove a GWT Module"
	print "~        clean      Clean a compiled GWT Module"
	print "~        cleanall   Clean all compiled GWT Modules"
	print "~        compile    Compile a GWT Module"
	print "~        compileall Compile all GWT Modules"
	print "~        devmode    Start GWT2 DevMode"
	print "~        help       Show this help"
	print "~"
	print "~ options: "
	print "~        --gwt      path to gwt sdk"
	print "~"
	sys.exit(0)

###############################################################################
# [gwt2:init] Init GWT project - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:init':
	# Create gwt2_public_path
	if not os.path.exists(os.path.join(application_path, gwt2_public_path)):
		os.mkdir(os.path.join(application_path, gwt2_public_path))
	# Create gwt2_modules_path
	if not os.path.exists(os.path.join(application_path, gwt2_modules_path)):
		os.mkdir(os.path.join(application_path, gwt2_modules_path))
	# Copy libs
	shutil.copyfile(os.path.join(gwt_path, 'gwt-user.jar'), os.path.join(application_path, 'lib/gwt-user.jar'))
	print "~ Application ready..."
	print "~"	
	sys.exit(0)

###############################################################################
# [gwt2:modules] List GWT modules - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:modules':
	displayModule()
	sys.exit(0)

###############################################################################
# [gwt2:remove] Remove a GWT module - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:remove':
	displayModule()
	gwtmodule = raw_input('~ GWT Module to remove : ')
	gwtmodule = gwtmodule.strip()
	gwtmodule = string.replace(gwtmodule, ' ', '_')
	# delete the  app
	if not os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		print "~ Error: module " + gwtmodule + " not found."
		print "~"		
		sys.exit(1)
	if os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		shutil.rmtree(os.path.join(application_path, gwt2_modules_path, gwtmodule))
	if os.path.exists(os.path.join(application_path, gwt2_public_path, gwtmodule)):
		shutil.rmtree(os.path.join(application_path, gwt2_public_path, gwtmodule))
	print "~"
	print "~ Ok. Your GWT module has been deleted "
	print "~"
	sys.exit(0)

###############################################################################
# [gwt2:clean] Clean a GWT module - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:clean':
	displayModule()
	gwtmodule = raw_input('~ gwt module to clean : ')
	gwtmodule = gwtmodule.strip()
	gwtmodule = string.replace(gwtmodule, ' ', '_')
	# clean public dir
	if os.path.exists(os.path.join(application_path, gwt2_public_path, gwtmodule)):
		shutil.rmtree(os.path.join(application_path, gwt2_public_path, gwtmodule))
	print "~"
	print "~ GWT Module " + gwtmodule + " has been cleaned."
	print "~"
	sys.exit(0);

###############################################################################
# [gwt2:cleanall] Clean all GWT modules
###############################################################################
if play_command == 'gwt2:cleanall':
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		pathmodule = os.path.join(application_path, gwt2_public_path, dir) 
		if os.path.exists(pathmodule):		
			shutil.rmtree(pathmodule)
		print "~ " + dir + " has been cleaned."
	print "~"
	sys.exit(0);

###############################################################################
# [gwt2:compile] Compile a module - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:compile':
	displayModule()
	gwtmodule = raw_input('~ gwt module to compile : ')
	gwtmodule = gwtmodule.strip()
	gwtmodule = string.replace(gwtmodule, ' ', '_')
	print "~"
	compileModule(gwtmodule)
	sys.exit(0)

###############################################################################
# [gwt2:compileall] Compile a all modules - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:compileall':
	print "~"
	print "~ Compiling all modules ... "
	print "~"
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		compileModule(dir)
	sys.exit(0);
	
###############################################################################
# [gwt2:create] Create a GWT module - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:create':
	gwtmodule = raw_input('~ Enter a gwt module name : ')
	gwtmodule = gwtmodule.strip()
	gwtmodule = string.replace(gwtmodule, ' ', '_')
	# create the new app
	if os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		print "~ Error: GWT Module " + gwtmodule + " already exists"
		print "~"		
		sys.exit(1)
	# make structure
	os.mkdir(os.path.join(application_path, gwt2_modules_path, gwtmodule))
	os.mkdir(os.path.join(application_path, gwt2_modules_path, gwtmodule, 'public'))
	os.mkdir(os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client'))
	os.mkdir(os.path.join(application_path, gwt2_modules_path, gwtmodule, 'shared'))
	os.mkdir(os.path.join(application_path, gwt2_modules_path, gwtmodule, 'server'))
	# copy index.html
	shutil.copyfile(os.path.join(play_base, this_path, 'resources','index.html'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'public','index.html'))
	indexFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'public', 'index.html')
	replaceAll(indexFile, r'gwtmodule', gwtmodule)
	# copy entry point	
	shutil.copyfile(os.path.join(play_base, this_path, 'resources', 'Main.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', gwtmodule.capitalize()+'.java'))
	mainFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', gwtmodule.capitalize()+'.java')
	replaceAll(mainFile, r'gwtmodule', gwtmodule)
	replaceAll(mainFile, r'classmodule', gwtmodule.capitalize())	
	# copy app def
	shutil.copyfile(os.path.join(play_base, this_path, 'resources', 'Main.gwt.xml'), os.path.join(application_path, gwt2_modules_path, gwtmodule, gwtmodule.capitalize()+'.gwt.xml'))
	mainFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, gwtmodule.capitalize()+'.gwt.xml')
	replaceAll(mainFile, r'gwtmodule', gwtmodule)
	replaceAll(mainFile, r'classmodule', gwtmodule.capitalize())	
	# copy service class	
	shutil.copyfile(os.path.join(play_base, this_path, 'resources', 'GreetingService.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingService.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingService.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)
	shutil.copyfile(os.path.join(play_base, this_path, 'resources', 'GreetingServiceAsync.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingServiceAsync.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingServiceAsync.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)
	shutil.copyfile(os.path.join(play_base, this_path, 'resources', 'GreetingServiceImpl.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'server', 'GreetingServiceImpl.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule,'server', 'GreetingServiceImpl.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)	
	shutil.copyfile(os.path.join(play_base, this_path, 'resources', 'FieldVerifier.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'shared', 'FieldVerifier.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'shared', 'FieldVerifier.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)	
	print "~"
	print "~ GWT Module " + gwtmodule + " has been created" 
	print "~"
	sys.exit(0)

###############################################################################
# [gwt2:devmode] Run the gwt DevMode - tested[24.05.2010]
###############################################################################
if play_command == 'gwt2:devmode':
	# Run dev mode
	print "~"
	print "~ Running com.google.gwt.dev.DevMode ..."
	do_classpath()
	do_java()
	cp = []
	cp.append(os.path.normpath(os.path.join(application_path, 'app')))
	cp.append(os.path.normpath(os.path.join(application_path, 'lib/gwt-user.jar')))
	cp.append(os.path.normpath(os.path.join(gwt_path, 'gwt-dev.jar')))
	# get gwt module
	modulename = []
	print "~ Loading modules : "
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		modulename.append(dir)
		print " - " + dir
	print "~"
	# append classpath
	for jar in os.listdir(os.path.join(application_path, 'lib')):
		if jar.endswith('.jar'):
			cp.append(os.path.normpath(os.path.join(application_path, 'lib/%s' % jar)))
	cps = ':'.join(cp)
	# if windows
	if os.name == 'nt':
		cps = ';'.join(cp)
	# '-logLevel', 'DEBUG',
	gwt_cmd = [java_path, '-Xmx256M', '-classpath', cps, 'com.google.gwt.dev.DevMode', '-noserver', '-war', os.path.normpath(os.path.join(application_path, gwt2_public_path))]
	gwt_cmd.insert(2, '-Xdebug')
	gwt_cmd.insert(2, '-Xrunjdwp:transport=dt_socket,address=%s,server=y,suspend=n' % '3408')
	# append modules
	for modul in modulename:
		gwt_cmd.append('gwt.'+modul+'.'+modul.capitalize())
	for modul in modulename:
		gwt_cmd.append('-startupUrl')
		gwt_cmd.append('http://localhost:' + readConf('http.port') + '/app/'+modul+'/index.html')
	subprocess.call(gwt_cmd, env=os.environ)
	print "~"
	sys.exit(0)

###############################################################################
# [eclipsify] make small modification to get access to source
###############################################################################
#if play_command == 'ec' or play_command == 'eclipsify':
#	dotProject = os.path.join(application_path, '.project')
#	replaceAll(dotProject, r'/gwt2/app</location>', "/gwt2/src</location>")
	