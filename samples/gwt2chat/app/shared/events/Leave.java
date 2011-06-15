package shared.events;

import com.google.gwt.user.client.rpc.IsSerializable;


public class Leave extends Event implements IsSerializable {
    
    private String user;
    
    public Leave() {
    	super("leave");
    }
    
    public Leave(String user) {
        this();
        this.user = user;
    }
    
    public String getUser() {
    	return user;
    }
}