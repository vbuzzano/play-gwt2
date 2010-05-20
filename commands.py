# GWT

# ~~~~~~~~~~~~~~~~~~~~~~ Check paths
if play_command.startswith('gwt:'):
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

    if not gwt_path and os.environ.has_key('GWT_PATH'):
        gwt_path = os.path.normpath(os.path.abspath(os.environ['GWT_PATH']))

    if not gwt_path:
        print "~ You need to specify the path of you GWT installation, "
        print "~ either using the $GWT_PATH environment variable or with the --gwt option" 
        print "~ "
        sys.exit(-1)
        
    # check
    if not os.path.exists(os.path.join(gwt_path, 'gwt-user.jar')) or not os.path.exists(os.path.join(gwt_path, 'gwt-dev.jar')):
        print "~ %s seems not to be a valid GWT installation (checked for gwt-user.jar and gwt-dev.jar)" % gwt_path
        print "~ This module has been tested with GWT 2.0.3"
        print "~ "
        sys.exit(-1)


# ~~~~~~~~~~~~~~~~~~~~~~ [gwt:init] Init GWT project
if play_command == 'gwt:init' or play_command == 'gwt:create' or play_command == 'ec' or play_command == 'eclipsify':
    # Create gwt-public
    if not os.path.exists(os.path.join(application_path, 'gwt-public')):
        os.mkdir(os.path.join(application_path, 'gwt-public'))

    # Create app/gwt
    if not os.path.exists(os.path.join(application_path, 'app/gwt')):
        os.mkdir(os.path.join(application_path, 'app/gwt'))

# ~~~~~~~~~~~~~~~~~~~~~~ [eclipsify] make small modification to get access to source
if play_command == 'ec' or play_command == 'eclipsify':
	dotProject = os.path.join(application_path, '.project')
	replaceAll(dotProject, r'/gwt2/app</location>', "/gwt2/src</location>")

# ~~~~~~~~~~~~~~~~~~~~~~ [gwt:remove] Remove a GWT module
if play_command == 'gwt:remove':
	# ask for appname
	appname = raw_input('What is the gwt module name ? ')
	appname = appname.strip()

	# delete the  app
	if not os.path.exists(os.path.join(application_path, 'app/gwt/'+appname)):
		print "~ -> Error .. gwt module not found [" + appname + "]"
		sys.exit(1)
	
	if os.path.exists(os.path.join(application_path, 'app/gwt/'+appname)):
		shutil.rmtree(os.path.join(application_path, 'app/gwt/'+appname))
	
	if os.path.exists(os.path.join(application_path, 'gwt-public/'+appname)):
		shutil.rmtree(os.path.join(application_path, 'gwt-public/'+appname))
	
	print "~"
	print "~ Ok. Your GWT module has been deleted "
	print "~"
		
	sys.exit(0);


# ~~~~~~~~~~~~~~~~~~~~~~ [gwt:create] Create a GWT module
if play_command == 'gwt:create':

	# ask for appname
	appname = raw_input('What is the gwt module name ? ')
	appname = appname.strip()

	# create the new app
	if os.path.exists(os.path.join(application_path, 'app/gwt/'+appname)):
		print "~ -> Error .. an gwt module already exists for this name [" + appname + "]"
		sys.exit(1)

	os.mkdir(os.path.join(application_path, 'app/gwt/'+appname))
	os.mkdir(os.path.join(application_path, 'app/gwt/'+appname+'/public'))
	os.mkdir(os.path.join(application_path, 'app/gwt/'+appname+'/client'))
	os.mkdir(os.path.join(application_path, 'app/gwt/'+appname+'/shared'))
	os.mkdir(os.path.join(application_path, 'app/gwt/'+appname+'/server'))

#	shutil.copyfile(os.path.join(play_base, 'modules/gwt2/resources/index.html'), os.path.join(application_path, 'app/gwt/'+appname+'/public/index.html'))

	# copy index.html
	shutil.copyfile(os.path.join(application_path, 'modules/gwt2/resources/index.html'), os.path.join(application_path, 'app/gwt/'+appname+'/public/index.html'))
	indexFile = os.path.join(application_path, 'app/gwt/'+appname+'/public/index.html')
	replaceAll(indexFile, r'appname', appname)
	
	# copy entry point	
	shutil.copyfile(os.path.join(application_path, 'modules/gwt2/resources/Main.java'), os.path.join(application_path, 'app/gwt/'+appname+'/client/'+appname.capitalize()+'.java'))
	mainFile = os.path.join(application_path, 'app/gwt/'+appname+'/client/'+appname.capitalize()+'.java')
	replaceAll(mainFile, r'appname', appname)
	replaceAll(mainFile, r'cppname', appname.capitalize())	

	# copy app def
	shutil.copyfile(os.path.join(application_path, 'modules/gwt2/resources/Main.gwt.xml'), os.path.join(application_path, 'app/gwt/'+appname+'/'+appname.capitalize()+'.gwt.xml'))
	mainFile = os.path.join(application_path, 'app/gwt/'+appname+'/'+appname.capitalize()+'.gwt.xml')
	replaceAll(mainFile, r'appname', appname)
	replaceAll(mainFile, r'cppname', appname.capitalize())	
	

	# copy service class	
	shutil.copyfile(os.path.join(application_path, 'modules/gwt2/resources/GreetingService.java'), os.path.join(application_path, 'app/gwt/'+appname+'/client/GreetingService.java'))
	tmpFile = os.path.join(application_path, 'app/gwt/'+appname+'/client/GreetingService.java')
	replaceAll(tmpFile, r'appname', appname)

	shutil.copyfile(os.path.join(application_path, 'modules/gwt2/resources/GreetingServiceAsync.java'), os.path.join(application_path, 'app/gwt/'+appname+'/client/GreetingServiceAsync.java'))
	tmpFile = os.path.join(application_path, 'app/gwt/'+appname+'/client/GreetingServiceAsync.java')
	replaceAll(tmpFile, r'appname', appname)
	
	shutil.copyfile(os.path.join(application_path, 'modules/gwt2/resources/GreetingServiceImpl.java'), os.path.join(application_path, 'app/gwt/'+appname+'/server/GreetingServiceImpl.java'))
	tmpFile = os.path.join(application_path, 'app/gwt/'+appname+'/server/GreetingServiceImpl.java')
	replaceAll(tmpFile, r'appname', appname)	

	shutil.copyfile(os.path.join(application_path, 'modules/gwt2/resources/FieldVerifier.java'), os.path.join(application_path, 'app/gwt/'+appname+'/shared/FieldVerifier.java'))
	tmpFile = os.path.join(application_path, 'app/gwt/'+appname+'/shared/FieldVerifier.java')
	replaceAll(tmpFile, r'appname', appname)	
	
	print "~"
	print "~ Ok. A Main GWT module has been created in app/gwt" + appname + " and GWT static resources come to app/gwt/" + appname + "/public or in gwt-public"
	print "~ Run play gwt:devmode to run the GWT DevMode"
	print "~"
	print "~ Have fun !"
	print "~"
	
	sys.exit(0)
	

# ~~~~~~~~~~~~~~~~~~~~~~ [gwt:devmode] Run the gwt DevMode
if play_command == 'gwt:devmode':
    
    # Run
    print "~ Running com.google.gwt.dev.DevMode ..."
    print "~"
    do_classpath()
    do_java()
    cp = []
    cp.append(os.path.normpath(os.path.join(application_path, 'app')))
    cp.append(os.path.normpath(os.path.join(application_path, 'modules/gwt2/lib/gwt-user.jar')))
    cp.append(os.path.normpath(os.path.join(application_path, 'modules/gwt2/lib/gwt-dev.jar')))

    # get gwt module
    modulename = []
    for dir in os.listdir(os.path.join(application_path, 'app/gwt')):
   		modulename.append('gwt.'+dir+'.'+dir.capitalize())
    modulenames = ' '.join(modulename)

		    
    for jar in os.listdir(os.path.join(application_path, 'lib')):
        if jar.endswith('.jar'):
            cp.append(os.path.normpath(os.path.join(application_path, 'lib/%s' % jar)))
    cps = ':'.join(cp)
    if os.name == 'nt':
        cps = ';'.join(cp)
    # '-logLevel', 'DEBUG',
    gwt_cmd = [java_path, '-Xmx256M', '-classpath', cps, 'com.google.gwt.dev.DevMode', '-noserver', '-startupUrl', 'http://localhost:' + readConf('http.port') + '/app/'+modulenames[0]+'/index.html', '-war', os.path.normpath(os.path.join(application_path, 'gwt-public'))]
    gwt_cmd.insert(2, '-Xdebug')
    gwt_cmd.insert(2, '-Xrunjdwp:transport=dt_socket,address=%s,server=y,suspend=n' % '3408')
    for modul in modulename:
        gwt_cmd.append(modul)
    subprocess.call(gwt_cmd, env=os.environ)
    print "~"
    sys.exit(0)
    