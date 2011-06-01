/*
 * Copyright 2011 Vincent Buzzano
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
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