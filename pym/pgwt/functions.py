###############################################################################
# GWT2 Plugin - Functions
#
# [gwt2:modules]
# 
# Set of tools
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import getopt, sys, os, inspect, string, subprocess

###############################################################################
# function: Display a list of exising modules - tested[2010-06-25]
###############################################################################
def listModules(args, showApp):
	app = args.get('app')
	modules = []
	
	print "~"
	print "~ GWT Modules list "
	print "~ ---------------- "
	print "~"
	
	if showApp == True:
		modules.append('app')
	
	path = os.path.join(app.path, args.get("modules_dir"))
	if os.path.exists(path):
		for dir in os.listdir(path):
			file = os.path.join(path, dir, dir.capitalize()+'.gwt.xml')
			if os.path.exists(file):
				modules.append(dir)
	
	if len(modules) > 0:
		for modul in modules:
			if modul == 'app':
				print "~ * " + modul + " (Application module)"
			else:
				print "~ * " + modul
	print "~"

###############################################################################
# function: has modules
###############################################################################
def hasModules(args, showApp):
	app = args.get('app')
	modules = []
	if showApp == True:
		modules.append('app')
	
	path = os.path.join(app.path, args.get("modules_dir"))
	if os.path.exists(path):
		for dir in os.listdir(path):
			file = os.path.join(path, dir, dir.capitalize()+'.gwt.xml')
			if os.path.exists(file):
				modules.append(dir)
	
	if len(modules) > 0:
		return True
	else:
		return False

###############################################################################
# function: Ask for a module name - tested[2010-06-25]
###############################################################################
def askForModule(args, actionText, showApp, abortIfEmpty):
	if hasModules(args, showApp):
		listModules(args, showApp)
	
		# ask for module to delete
		gwtmodule = raw_input('~ GWT Module to ' + actionText + ': ')
		gwtmodule = gwtmodule.strip()
		gwtmodule = string.replace(gwtmodule, ' ', '_')
	
		# if no module has been choose, stop	
		if abortIfEmpty:
			if gwtmodule == "" :
				print "~ aborted "
				print "~"
				sys.exit(0)
	else:
		if abortIfEmpty:
			print "~ no modules "
			print "~"
			sys.exit(0)
	
	return gwtmodule

###############################################################################
# function: Compile a gwt module - tested[X]
###############################################################################
def compile(args, modulename):
	app = args.get("app")
	env = args.get("env")
	application_path = args.get("app").path
	gwt2_module_dir = args.get("gwt2_module_dir")
	modules_dir = args.get("modules_dir")
	base_classpath = args.get("modules_base_classpath")
	public_dir = args.get("public_dir")
	gwt_path = args.get("gwt_path")
	
	modulepath = os.path.join(application_path, modules_dir, modulename)
	if modulename == "app":
		modulepath = os.path.join(application_path, "app")
	else:
		modulepath = os.path.join(application_path, modules_dir, modulename)

	# if module exists
	if os.path.exists(modulepath):
		# Compile GWT Modulemodulename
#		print "~ Compiling GWT Module " + modulename + " ..."
#		print "~"
#		print "----------------------------------------------"
		# prepare classpath and java
		#do_java()
		cp = []
		
		#Add Jpa Hibernate at first posision to fix compilation problem
		path = os.path.normpath(os.path.join(env["basedir"], "framework", "lib"))	
		for f in os.listdir(path):
			if f.startswith("hibernate-jpa"):
				cp.append(f)
		
		#Add GWT libs
		path = os.path.normpath(os.path.join(env["basedir"], "framework", "lib"))	
		for f in os.listdir(path):
			if f.startswith("gwt-user"):
				cp.append(f)
			if f.startswith("gwt-dev"):
				cp.append(f)
		
		#Add Play GWT2 plugin app & hack src
		cp.append(os.path.normpath(os.path.join(gwt2_module_dir, 'app')))
		cp.append(os.path.normpath(os.path.join(gwt2_module_dir, 'hack')))
		
		#Add Application path & libs
		cp.append(os.path.normpath(os.path.join(application_path, 'app')))
		for jar in os.listdir(os.path.join(application_path, 'lib')):
			if jar.endswith('.jar'):
				cp.append(os.path.normpath(os.path.join(application_path, 'lib/%s' % jar)))
		
		#Compute cp
		#windows		
		if os.name == 'nt':
			cps = ';'.join(cp)
			cps = cps + ';' + app.cp_args()
		#linux
		else:
			cps = ':'.join(cp)
			cps = cps + ':' + app.cp_args()
		
		java_path = app.java_path()
		
		modul = None
		if modulename == 'app':
			modul = 'App'
		else:
			modul = base_classpath + modulename+"."+modulename.capitalize()
		gwt_cmd = [java_path, '-Xmx256M', '-classpath', cps, 'com.google.gwt.dev.Compiler', '-style', 'OBF', '-war', os.path.normpath(os.path.join(application_path, public_dir)), modul]
		ret = subprocess.call(gwt_cmd, env=os.environ)
		if ret == 0:
			return True
		else:
			return False
	else:
		print "~"
		print "~ Error: GWT Module " + modulename + " not found."
		print "~"
