package gwt.refresh.services;

import gwt.refresh.client.ChatRoomService;

import java.util.List;

import play.modules.gwt2.GWT2Service;
import shared.events.Event;
import shared.events.EventDummy;

public class ChatRoom extends GWT2Service implements ChatRoomService {
	
	@Override
    public List<Event> archive() {
    	return models.ChatRoom.get().archive();
    }

	@Override
	public List<Event> say(String message, String user) throws IllegalArgumentException {
		models.ChatRoom.get().say(user, message);
		return archive();
	}

	@Override
	public EventDummy dummy(EventDummy d) {
		return d;
	}
    
}
