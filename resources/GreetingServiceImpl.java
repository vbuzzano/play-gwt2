package gwt.gwtmodule.server;

import gwt.gwtmodule.client.GreetingService;
import gwt.gwtmodule.shared.FieldVerifier;

import play.modules.gwt2.GWTService;
import play.modules.gwt2.GWTServicePath;


import com.google.gwt.user.server.rpc.*;
 
@GWTServicePath("/gwtmodule/greet")
public class GreetingServiceImpl extends GWTService implements GreetingService {
 
    public String greetServer(String name) {

        // Verify that the input is valid. 
        if (!FieldVerifier.isValidName(name)) {
            // If the input is not valid, throw an IllegalArgumentException back to
            // the client.
            throw new IllegalArgumentException("Name must be at least 4 characters long");
		}
		
        return "Hello " + name;
    }
}
