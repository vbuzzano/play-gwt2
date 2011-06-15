package shared.events;

import com.google.gwt.user.client.rpc.IsSerializable;


public class Join extends Event implements IsSerializable {
    
    private String user;
    
    public Join() {
    	super("join");
    }
    
    public Join(String user) {
    	this();
        this.user = user;
    }
    
    public String getUser() {
    	return user;
    }
}