###############################################################################
# GWT2 Create Command - tested[2010-06-25]
#
# [gwt2:create]
# 
# Create a new GWT Module
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import sys, os, string, shutil

from play.utils import *

def getCommands():
	return ["gwt2:create"]

def execute(args):
	
	# init variable
	env = args.get("env")
	application_path = args.get("app").path
	gwt2_modules_path = args.get("gwt2_modules_path")
	module_path = args.get("module_path")
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
	shutil.copyfile(os.path.join(env["basedir"], module_path, 'resources','index.html'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'public','index.html'))
	indexFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'public', 'index.html')
	replaceAll(indexFile, r'gwtmodule', gwtmodule)
	
	# copy entry point	
	shutil.copyfile(os.path.join(env["basedir"], module_path, 'resources', 'Main.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', gwtmodule.capitalize()+'.java'))
	mainFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', gwtmodule.capitalize()+'.java')
	replaceAll(mainFile, r'gwtmodule', gwtmodule)
	replaceAll(mainFile, r'classmodule', gwtmodule.capitalize())	
	
	# copy app def
	shutil.copyfile(os.path.join(env["basedir"], module_path, 'resources', 'Main.gwt.xml'), os.path.join(application_path, gwt2_modules_path, gwtmodule, gwtmodule.capitalize()+'.gwt.xml'))
	mainFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, gwtmodule.capitalize()+'.gwt.xml')
	replaceAll(mainFile, r'gwtmodule', gwtmodule)
	replaceAll(mainFile, r'classmodule', gwtmodule.capitalize())	
	
	# copy service class	
	shutil.copyfile(os.path.join(env["basedir"], module_path, 'resources', 'GreetingService.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingService.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingService.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)
	shutil.copyfile(os.path.join(env["basedir"], module_path, 'resources', 'GreetingServiceAsync.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingServiceAsync.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingServiceAsync.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)
	shutil.copyfile(os.path.join(env["basedir"], module_path, 'resources', 'GreetingServiceImpl.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'server', 'GreetingServiceImpl.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule,'server', 'GreetingServiceImpl.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)	
	shutil.copyfile(os.path.join(env["basedir"], module_path, 'resources', 'FieldVerifier.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'shared', 'FieldVerifier.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'shared', 'FieldVerifier.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)	
	
	print "~"
	print "~ GWT Module " + gwtmodule + " has been created" 
	print "~"
