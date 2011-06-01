package play.modules.gwt2;


import org.apache.commons.lang.StringUtils;

import play.Play;
import play.PlayPlugin;
import play.classloading.ApplicationClasses.ApplicationClass;
import play.mvc.Http.Request;
import play.mvc.Router;
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

	/**
	 * Default public path
	 */
    private static final String DEFAULT_PATH = "/app";
    
    /**
     * Default public directory
     */
    private static final String DEFAULT_PUBLIC_DIR = "gwt-public";
    
    /**
     * Default gwt modules directory
     */
    private static final String DEFAULT_MODULES_DIR = "gwt";
    
    @Override
    public void onRoutesLoaded() {
        Router.addRoute("GET", "/@gwt", "dummy.dummy"); // protect it
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
		
		String gwtpath = modulesDir();
		
		GWT2Module mod = new GWT2Module();
		mod.name = module.replace(" ", "").trim();
		mod.path = gwtpath + "/" + module;
		
		String sClass = gwtpath + "."  + mod.name + ".services." + 
							service.replace(" ", "").trim();
		
		mod.service = Play.classloader.getClassIgnoreCase(sClass);
        
		if (mod.service == null) {
			// try to find with annotation
	           for (Class<?> cservice : Play.classloader.getAnnotatedClasses(GWT2ServicePath.class)) {
	                String path = ((GWT2ServicePath) cservice.getAnnotation(GWT2ServicePath.class)).value();
	                if (("/"+module+"/"+service).equals(path)) {
	                	mod.service = cservice;
	                	break;
	                }
	            }
		}		
		
		return mod;
	}

    public void enhance(ApplicationClass applicationClass) throws Exception {
    	GWT2Enhancer enhancer = new GWT2Enhancer();
    	System.out.println("ok");
    	enhancer.enhanceThisClass(applicationClass);
    }
	
    /**
	 * Get gwt public directory
	 * @return
	 */
	public static String publicDir() {
		return Play.configuration.getProperty("gwt2.publicdir", DEFAULT_PUBLIC_DIR);
	}
	
	/**
	 * Get gwt public url path
	 * @return
	 */
	public static String publicPath() {
		return Play.configuration.getProperty("gwt2.publicpath", DEFAULT_PATH);
	}
	
	/**
	 * Get gwt modules directory
	 * @return
	 */
	public static String modulesDir() {
		return Play.configuration.getProperty("gwt2.modulesdir", DEFAULT_MODULES_DIR);
	}

	static public class GWT2Module  {
		public String name;
		public String path;
		
		public Class<?> service;
	}
}