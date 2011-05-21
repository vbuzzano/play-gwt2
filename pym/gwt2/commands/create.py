###############################################################################
# GWT2 Create Command - tested[2010-10-07]
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

def getHelp():
	return "Create a new GWT Module"

def execute(args):	
	# init variable
	env = args.get("env")
	app = args.get("app")
	
	# gwt modules dir
	modules_dir = args.get("modules_dir")
	
	# play-gwt2 module dir
	gwt2_module_dir = args.get("gwt2_module_dir")

	# base classpath
	base_classpath = args.get("modules_base_classpath")
	
	# get a name for the module
	modulename = raw_input('~ Enter a gwt module name : ')
	modulename = modulename.strip()
	modulename = string.replace(modulename, ' ', '_')
	
	# create the new module
	if os.path.exists(os.path.join(app.path, modules_dir, modulename)):
		print "~ Error: GWT Module " + modulename + " already exists"
		print "~"		
		sys.exit(1)
	
	createModule(app, env, gwt2_module_dir, modules_dir, modulename, base_classpath)

# Create Module
def createModule(app, env, gwt2_module_dir, modules_dir, modulename, base_classpath):
	modpackage = base_classpath;

	# make structure
	modulesdir = os.path.join(app.path, modules_dir)
	if not os.path.exists(modulesdir): 
		os.mkdir(modulesdir)
	os.mkdir(os.path.join(modulesdir, modulename))
	os.mkdir(os.path.join(modulesdir, modulename, 'public'))
	os.mkdir(os.path.join(modulesdir, modulename, 'client'))
	os.mkdir(os.path.join(modulesdir, modulename, 'shared'))
	os.mkdir(os.path.join(modulesdir, modulename, 'services'))

	# copy index.html
	file = os.path.join(modulesdir, modulename, 'public', 'index.html')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources','index.html'), file)
	replaceAll(file, r'\[modulename\]', modulename)
	
	# copy entry point
	file = os.path.join(modulesdir, modulename, 'client', modulename.capitalize()+'.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'Main.java'), file)
	replaceAll(file, r'\[modulename\]', modulename)
	replaceAll(file, r'\[classmodule\]', modulename.capitalize())	
	replaceAll(file, r'\[modpackage\]', modpackage)
	
	# copy app def
	file = os.path.join(modulesdir, modulename, modulename.capitalize()+'.gwt.xml')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'Main.gwt.xml'), file)
	replaceAll(file, r'\[modulename\]', modulename)
	replaceAll(file, r'\[entrypointclass\]', '<entry-point class="' + modpackage + modulename+'.client.'+ modulename.capitalize() +'"/>')
	replaceAll(file, r'\[sourcepath\]', "<source path='client'/>\n	<source path='shared'/>")
	replaceAll(file, r'\[othermodule\]', "<inherits name='App' />")
	
	# copy service class	
	tmpfile = os.path.join(app.path, modules_dir, modulename, 'client', 'GreetingService.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'GreetingService.java'), tmpfile)
	replaceAll(tmpfile, r'\[modulename\]', modulename)
	replaceAll(tmpfile, r'\[modpackage\]', modpackage)
	
	tmpfile = os.path.join(app.path, modules_dir, modulename, 'client', 'GreetingServiceAsync.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'GreetingServiceAsync.java'), tmpfile)
	replaceAll(tmpfile, r'\[modulename\]', modulename)
	replaceAll(tmpfile, r'\[modpackage\]', modpackage)
	
	tmpfile = os.path.join(app.path, modules_dir, modulename, 'services', 'Greeting.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'Greeting.java'), tmpfile)
	replaceAll(tmpfile, r'\[modulename\]', modulename)
	replaceAll(tmpfile, r'\[modpackage\]', modpackage)
	
	tmpfile = os.path.join(app.path, modules_dir, modulename, 'shared', 'FieldVerifier.java')
	shutil.copyfile(os.path.join(env["basedir"], gwt2_module_dir, 'resources', 'FieldVerifier.java'), tmpfile)
	replaceAll(tmpfile, r'\[modulename\]', modulename)	
	replaceAll(tmpfile, r'\[modpackage\]', modpackage)
	
	print "~"
	print "~ GWT Module " + modulename + " has been created" 
	print "~"
