package play.modules.gwt2;

import play.Play;
import play.PlayPlugin;
import play.exceptions.JavaExecutionException;
import play.exceptions.PlayException;
import play.mvc.Http.Request;
import play.mvc.Router;
import play.mvc.Router.Route;
import play.mvc.results.RedirectToStatic;
import play.mvc.results.RenderText;

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
            Router.addRoute("GET", DEFAULT_PATH, "staticDir:gwt-public");
        }
        Router.addRoute("GET", "/@gwt", "dummy.dummy"); // protect it
    }

    private Route findRoute(){
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
        // Hand made routing;
        if (request.method == "POST") {

            final Route route = findRoute();
            String routePath = route!=null? route.path: DEFAULT_PATH;
            if(routePath.endsWith("/")){
                routePath = routePath.substring(0, routePath.length()-1);
            }

            for (Class<?> service : Play.classloader.getAnnotatedClasses(GWT2ServicePath.class)) {
                String path = ((GWT2ServicePath) service.getAnnotation(GWT2ServicePath.class)).value();
                if (request.path.equals(routePath+path)) {
                    invokeService(service, request);
                    break;
                }
            }
        }
    }

    /**
     * Invoke a service
     * @param service
     */
    public void invokeService(Class service, Request request) {
        String result = "";
        if (GWT2Service.class.isAssignableFrom(service)) {
            try {
            	GWT2Service gwts = (GWT2Service) service.newInstance();
            	gwts.request = request;
                result = gwts.invoke();
                
            } catch (Exception ex) {
                // Rethrow the enclosed exception
                if (ex instanceof PlayException) {
                    throw (PlayException) ex;
                }
                StackTraceElement element = PlayException.getInterestingStrackTraceElement(ex);
                if (element != null) {
                    throw new JavaExecutionException(Play.classes.getApplicationClass(element.getClassName()), element.getLineNumber(), ex);
                }
                throw new JavaExecutionException(ex);
            }
        }
        throw new RenderText(result);
    }
}