package play.modules.gwt2;


import org.apache.commons.lang.StringUtils;

import play.Play;
import play.PlayPlugin;
import play.mvc.Http.Request;
import play.mvc.Router;
import play.mvc.Router.Route;
import play.mvc.results.RedirectToStatic;

/**
 * GWT2Plugin Class 
 *
 * Main GWT2 Plugin Class
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 * based on the GWT Plugin by **Rustem Suniev**.
 */
public class GWT2Plugin extends PlayPlugin {
    private static final String DEFAULT_PATH = "/app";

    @Override
    public void onRoutesLoaded() {
        boolean useDefault = findRoute()==null;
        if (useDefault) {
        	String staticDir = "staticDir" + 
        		Play.configuration.getProperty("gwt2.publicpath", "gwt-public");
        	Router.addRoute("GET", DEFAULT_PATH, staticDir);
        }
        Router.addRoute("GET", "/@gwt", "dummy.dummy"); // protect it
    }

    private static Route findRoute(){
        for (Route route : Router.routes) {
            if (route.action.contains("gwt-public")) {
                return route;
            }
        }
        return null;
    }

	@Override
    public void routeRequest(Request request) {
        if (request.path.equals("/@gwt")) {
            throw new RedirectToStatic(Router.reverse(Play.getVirtualFile("/gwt-public/index.html")));
        }
    }

	public static GWT2Module getModule(String module, String service) {
		if (StringUtils.isEmpty(module) 
				||StringUtils.isEmpty(service))
			return null;
		
		String gwtpath = Play.configuration.getProperty("gwt2.modulespath", "gwt");
		
		GWT2Module mod = new GWT2Module();
		mod.name = module.replace(" ", "").trim();
		mod.path = gwtpath + "/" + module;
		
		String sClass = gwtpath + "."  + mod.name + ".services." + 
							service.replace(" ", "").trim();
		
		mod.service = Play.classloader.getClassIgnoreCase(sClass);
        
		return mod;
	}
}