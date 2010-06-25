
###############################################################################
# [gwt2:init] Init GWT project - tested[X]
###############################################################################
def init():
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

###############################################################################
# [gwt2:modules] List GWT modules - tested[X]
###############################################################################
def displayModules():
	displayModules()

###############################################################################
# [gwt2:remove] Remove a GWT module - tested[X]
###############################################################################
def removeModule():
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

###############################################################################
# [gwt2:clean] Clean a GWT module - tested[X]
###############################################################################
def cleanModule():
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

###############################################################################
# [gwt2:cleanall] Clean all GWT modules - tested[X]
###############################################################################
def cleanAll():
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		pathmodule = os.path.join(application_path, gwt2_public_path, dir) 
		if os.path.exists(pathmodule):		
			shutil.rmtree(pathmodule)
		print "~ " + dir + " has been cleaned."
	print "~"

###############################################################################
# [gwt2:compile] Compile a module - tested[X]
###############################################################################
def compileModule():
	displayModule()
	gwtmodule = raw_input('~ gwt module to compile : ')
	gwtmodule = gwtmodule.strip()
	gwtmodule = string.replace(gwtmodule, ' ', '_')
	print "~"
	compile(gwtmodule)

###############################################################################
# [gwt2:compileall] Compile a all modules - tested[X]
###############################################################################
def compileAll():
	print "~"
	print "~ Compiling all modules ... "
	print "~"
	for dir in os.listdir(os.path.join(application_path, gwt2_modules_path)):
		compile(dir)

###############################################################################
# [gwt2:create] Create a GWT module - tested[X]
###############################################################################
def createModule():
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
	shutil.copyfile(os.path.join(env["basedir"], this_path, 'resources','index.html'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'public','index.html'))
	indexFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'public', 'index.html')
	replaceAll(indexFile, r'gwtmodule', gwtmodule)
	# copy entry point	
	shutil.copyfile(os.path.join(env["basedir"], this_path, 'resources', 'Main.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', gwtmodule.capitalize()+'.java'))
	mainFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', gwtmodule.capitalize()+'.java')
	replaceAll(mainFile, r'gwtmodule', gwtmodule)
	replaceAll(mainFile, r'classmodule', gwtmodule.capitalize())	
	# copy app def
	shutil.copyfile(os.path.join(env["basedir"], this_path, 'resources', 'Main.gwt.xml'), os.path.join(application_path, gwt2_modules_path, gwtmodule, gwtmodule.capitalize()+'.gwt.xml'))
	mainFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, gwtmodule.capitalize()+'.gwt.xml')
	replaceAll(mainFile, r'gwtmodule', gwtmodule)
	replaceAll(mainFile, r'classmodule', gwtmodule.capitalize())	
	# copy service class	
	shutil.copyfile(os.path.join(env["basedir"], this_path, 'resources', 'GreetingService.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingService.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingService.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)
	shutil.copyfile(os.path.join(env["basedir"], this_path, 'resources', 'GreetingServiceAsync.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingServiceAsync.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'client', 'GreetingServiceAsync.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)
	shutil.copyfile(os.path.join(env["basedir"], this_path, 'resources', 'GreetingServiceImpl.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'server', 'GreetingServiceImpl.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule,'server', 'GreetingServiceImpl.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)	
	shutil.copyfile(os.path.join(env["basedir"], this_path, 'resources', 'FieldVerifier.java'), os.path.join(application_path, gwt2_modules_path, gwtmodule, 'shared', 'FieldVerifier.java'))
	tmpFile = os.path.join(application_path, gwt2_modules_path, gwtmodule, 'shared', 'FieldVerifier.java')
	replaceAll(tmpFile, r'gwtmodule', gwtmodule)	
	print "~"
	print "~ GWT Module " + gwtmodule + " has been created" 
	print "~"

###############################################################################
# [gwt2:devmode] Run the gwt DevMode - tested[24.05.2010]
###############################################################################
def runDevMode():
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

###############################################################################
# function: Display a list of exising modules - tested[X]
###############################################################################
def listModules():
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
# function: Compile a gwt module - tested[X]
###############################################################################
def compile(gwtmodule):
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
    