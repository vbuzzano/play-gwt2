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
def listModules(args):
	print "~"
	print "~ GWT Modules list "
	print "~ ---------------- "
	print "~"
	count = 1
	for dir in os.listdir(os.path.join(args.get("app").path, args.get("gwt2_modules_path"))):
		print "~ * " + dir
		count = count + 1
	print "~"

###############################################################################
# function: Ask for a module name - tested[2010-06-25]
###############################################################################
def askForModule(args, actionText, abortIfEmpty):
	listModules(args)
	
	# ask for module to delete
	gwtmodule = raw_input('~ GWT Module to ' + actionText + ' : ')
	gwtmodule = gwtmodule.strip()
	gwtmodule = string.replace(gwtmodule, ' ', '_')
	
	# if no module has been choose, stop	
	if abortIfEmpty:
		if gwtmodule == "" :
			print "~ aborted "
			print "~"
			sys.exit(0)
	
	return gwtmodule

###############################################################################
# function: Compile a gwt module - tested[X]
###############################################################################
def compile(args, gwtmodule):
	app = args.get("app")
	application_path = args.get("app").path
	gwt2_modules_path = args.get("gwt2_modules_path")
	gwt2_public_path = args.get("gwt2_public_path")
	gwt_path = args.get("gwt_path")
	
	# if module exists
	if os.path.exists(os.path.join(application_path, gwt2_modules_path, gwtmodule)):
		# Compile GWT Module
		print "~ Compiling GWT Module " + gwtmodule + " ..."
		print "~"
		print "----------------------------------------------"
		# prepare classpath and java
		#do_java()
		cp = []
		cp.append(os.path.normpath(os.path.join(application_path, 'app')))
		cp.append(os.path.normpath(os.path.join(application_path, 'lib/gwt-user.jar')))
		cp.append(os.path.normpath(os.path.join(gwt_path, 'gwt-dev.jar')))
		for jar in os.listdir(os.path.join(application_path, 'lib')):
			if jar.endswith('.jar'):
				cp.append(os.path.normpath(os.path.join(application_path, 'lib/%s' % jar)))
		cps = ':'.join(cp)
		cps = cps + ':' + app.cp_args()
		if os.name == 'nt':
			cps = ';'.join(cp)
		java_path = app.java_path()
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