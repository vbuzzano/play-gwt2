package shared.events;

import java.io.Serializable;

public abstract class Event implements Serializable {
    
    private String type;
    public Long timestamp;
    public Long id;
    
    public Event() {
    }
    
    public Event(String type) {
        this.type = type;
    }
    
    public Event(Long id, String type) {
        this(type);
    	this.id = id;
    }
    
    public String getType() {
    	return type;
    }
    
	public void setId(Long id) {
		this.id = id;
	}
    
	public Long getId() {
		return id;
	}
}
