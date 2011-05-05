package controllers;

import jobs.GWT2Invoker;
import play.modules.gwt2.GWT2Module;
import play.modules.gwt2.GWT2Plugin;
import play.mvc.Controller;

public class GWT2Controller extends Controller {
	
	public static void invoke(String module, String service) {

		GWT2Module mod = GWT2Plugin.getModule(module, service);
		
		// find the module 
		if (mod == null)
			notFound("module not found !");
		
		// invoke async
		GWT2Invoker invoker = 
			new GWT2Invoker(mod, request, response, session);
		Object ret = await(invoker.now());
		
		renderGWT(ret);
	}

	private static void renderGWT(Object ret) {
		renderText(ret);
		
	}
}
