package [modpackage][modulename].server;

import [modpackage][modulename].client.GreetingService;
import [modpackage][modulename].shared.FieldVerifier;

import play.modules.gwt2.GWT2Service;
import play.modules.gwt2.GWT2ServicePath;


import com.google.gwt.user.server.rpc.*;
 
public class Greeting extends GWT2Service implements GreetingService {
 
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
