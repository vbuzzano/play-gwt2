package shared.events;

import com.google.gwt.user.client.rpc.IsSerializable;


public class Message extends Event implements IsSerializable {
    
    private String user;
    private String text;
    
    public Message() {
    	super("message");
    }
    
    public Message(String user, String text) {
        this();
        this.user = user;
        this.text = text;
    }
    
    public String getUser() {
    	return user;
    }
    
    public String getText() {
    	return text;
    }
    
}
