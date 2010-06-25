###############################################################################
# GWT2 Init command - tested[2010-06-25]
#
# [gwt2:init] 
#
# Init GWT project. Create needed folder and copy gwt-user.jar 
# to the targeted application
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com>
###############################################################################
import os, shutil

def getCommands():
	return ["gwt2:init"]

def execute(args):
	app = args.get("app")
	gwt2_public_path = args.get("gwt2_public_path")
	gwt2_modules_path = args.get("gwt2_modules_path")
	gwt_path = args.get("gwt_path")
	
	# Create gwt2_public_path
	if not os.path.exists(os.path.join(app.path, gwt2_public_path)):
		os.mkdir(os.path.join(app.path, gwt2_public_path))
		
	# Create gwt2_modules_path
	if not os.path.exists(os.path.join(app.path, gwt2_modules_path)):
		os.mkdir(os.path.join(app.path, gwt2_modules_path))
		
	# Copy libs
	shutil.copyfile(os.path.join(gwt_path, 'gwt-user.jar'), os.path.join(app.path, 'lib/gwt-user.jar'))
	print "~ Application ready..."
	print "~"
