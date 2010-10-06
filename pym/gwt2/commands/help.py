###############################################################################
# GWT2 Help Command - tested[2010-06-25]
#
# [gwt2:help]
# 
# Display the GWT2 Plugin Help
#
# @author Vincent Buzzano <vincent.buzzano@gmail.com> 
###############################################################################

def getCommands():
	return ["gwt2:help", "gwt2:"]

def getHelp():
	return "Show this help"

def execute(args):
	print "~"
	print "~ GWT2 Plugin for Play! Help"
	print "~ --------------------------"
	print "~"
	print "~ Usage: play gwt2:cmd [app_path] [--options]"
	print "~ "
	print "~ cmd:"  
	print "~        init           Initialize the application"
	print "~        modules, list  List all GWT Modules"
	print "~        create         Create a new GWT Module"
	print "~        remove         Remove a GWT Module"
	print "~        clean          Clean a compiled GWT Module"
	print "~        cleanall       Clean all compiled GWT Modules"
	print "~        compile        Compile a GWT Module"
	print "~        compileall     Compile all GWT Modules"
	print "~        devmode        Start GWT2 DevMode"
	print "~        help           Show this help"
	print "~"
	print "~ options: "
	print "~        --gwt          path to gwt sdk"
	print "~"
