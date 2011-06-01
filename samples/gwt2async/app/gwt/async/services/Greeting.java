package gwt.async.services;


import gwt.async.client.GreetingService;
import gwt.async.shared.FieldVerifier;
import jobs.TestJob;
import play.modules.gwt2.GWT2Service;
import play.modules.gwt2.GWT2ServiceAsync;
import play.modules.gwt2.chain.GWT2Chain;
import play.mvc.Http.Request;

@GWT2ServiceAsync(false)
public class Greeting extends GWT2Service implements GreetingService {

    public String greetServer(String name) {
        return (String) chain(new TestJob().now(), new GWT2Chain<String>() {
        	public Object chain(String result) {
                return chainASync(new TestJob().now(), new GWT2Chain<String>() {
        			public Object chain(String result) {
        				return chainASync(new TestJob().now(), new GWT2Chain<String>() {
        					public Object chain(String result) {
        						return result;
        					}
        				});
        			}
        		});        		
        	}
		});
    }

    public static String greetServer2(String name, Request request) {

        // Verify that the input is valid. 
        if (!FieldVerifier.isValidName(name)) {
            // If the input is not valid, throw an IllegalArgumentException back to
            // the client.
            throw new IllegalArgumentException("Name must be at least 4 characters long");
		}

        return (String) chain(new TestJob().now(), new GWT2Chain<String>() {
        	public Object chain(String result) {
                return chainASync(new TestJob().now(), new GWT2Chain<String>() {
        			public Object chain(String result) {
        				return chainASync(new TestJob().now(), new GWT2Chain<String>() {
        					public Object chain(String result) {
        						return result;
        					}
        				});
        			}
        		});        		
        	}
		});
    }
}
