package jobs;

import play.Play;
import play.exceptions.JavaExecutionException;
import play.exceptions.PlayException;
import play.jobs.Job;
import play.libs.IO;
import play.modules.gwt2.GWT2Module;
import play.modules.gwt2.GWT2Service;
import play.mvc.Http.Request;
import play.mvc.Http.Response;
import play.mvc.Scope.Session;

public class GWT2Invoker extends Job<Object> {
	GWT2Module module;
	Request request;
	Response response;
	Session session;

	String body;
	
	String result;
	
	
	public GWT2Invoker(GWT2Module module, Request request, Response response, Session session) {
		this.module = module;
		this.request = request;
		this.response = response;
		this.session = session;
		this.body = IO.readContentAsString(request.body);
	}
	
	
    public Object doJobWithResult() throws Exception {
    	doJob();
		return result;
	}
	
    /**
     * Invoke a service
     * @param service
     */
    public void doJob() {

    	
    	if (module.service == null)
    		return;
    	
        if (!GWT2Service.class.isAssignableFrom(module.service))
        	return;

        result = null;
        try {
        	GWT2Service gwts = (GWT2Service) module.service.newInstance();
        	gwts.setRequest(request);
        	gwts.setResponse(response);
        	gwts.setSession(session);
        	gwts.setPlayLoad(body);
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

}
