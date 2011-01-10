###############################################################################
# GWT2 Dev Mode Command - tested[2011-01-10]
#
# [gwt2:devmode]
# 
# run gwt devmode to run and debug gwt modules
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import os, string, sys, subprocess 

def getCommands():
	return ["gwt2:devmode"]

def getHelp():
	return "Start GWT2 DevMode"

def execute(args):
	app = args.get("app")
	application_path = args.get("app").path
	gwt2_module_path = args.get("gwt2_module_path")
	modules_path = args.get("modules_path")
	public_path =  args.get("public_path")
	gwt_path = args.get("gwt_path") 
	
	# Run dev mode
	print "~"
	print "~ Running com.google.gwt.dev.DevMode ..."
	
	cp = []
	cp.append(os.path.normpath(os.path.join(application_path, 'app')))
	cp.append(os.path.normpath(os.path.join(gwt2_module_path, 'hack')))
	cp.append(os.path.normpath(os.path.join(application_path, 'lib/gwt-user.jar')))
	cp.append(os.path.normpath(os.path.join(gwt_path, 'gwt-dev.jar')))
	
	# get gwt module
	modulename = []
	print "~ Loading modules : "
	for dir in os.listdir(os.path.join(application_path, modules_path)):
		if dir[0] != '.':
			modulename.append(dir)
			print " - " + dir
	print "~"
	
	# append classpath
	for jar in os.listdir(os.path.join(application_path, 'lib')):
		if jar.endswith('.jar'):
			cp.append(os.path.normpath(os.path.join(application_path, 'lib/%s' % jar)))
	
	# if windows
	if os.name == 'nt':
		cps = ';'.join(cp)
		cps = cps + ';' + app.cp_args()	
	else:
		cps = ':'.join(cp)
		cps = cps + ':' + app.cp_args()
	
	# '-logLevel', 'DEBUG',
	java_path = app.java_path()
	gwt_cmd = [java_path, '-Xmx256M', '-classpath', cps, 'com.google.gwt.dev.DevMode', '-noserver', '-war', os.path.normpath(os.path.join(application_path, public_path))]
	gwt_cmd.insert(2, '-Xdebug')
	gwt_cmd.insert(2, '-Xrunjdwp:transport=dt_socket,address=%s,server=y,suspend=n' % '3408')
	
	# append modules
	for modul in modulename:
		gwt_cmd.append('gwt.'+modul+'.'+modul.capitalize())
	for modul in modulename:
		gwt_cmd.append('-startupUrl')
		gwt_cmd.append('http://localhost:' + app.readConf('http.port') + '/app/'+modul+'/index.html')
	
	# execute devmode
	subprocess.call(gwt_cmd, env=os.environ)
	
	print "~"
