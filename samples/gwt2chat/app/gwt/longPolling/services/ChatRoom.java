package gwt.longPolling.services;

import gwt.longPolling.client.ChatRoomService;

import java.util.LinkedList;
import java.util.List;

import play.libs.F.IndexedEvent;
import play.modules.gwt2.GWT2Service;
import play.modules.gwt2.chain.GWT2Chain;
import shared.events.Event;
import shared.events.EventDummy;

public class ChatRoom extends GWT2Service implements ChatRoomService {
	
	@Override
    public List<Event> waitMessages(Long lastReceived) {        
		// Here we use continuation to suspend 
		// the execution until a new message has been received
		return (List) chainASync(
				models.ChatRoom.get().nextMessages(lastReceived),
				new GWT2Chain<List<IndexedEvent<Event>>>() {

					@Override
					public Object chain(List<IndexedEvent<Event>> events) {
						List<Event> messages = new LinkedList<Event>();
						for (IndexedEvent<Event> e : events) {
							e.data.setId(e.id);
							messages.add(e.data);
						}
						return messages;
					}
				});
	}
    

	
	@Override
	public void say(String message, String user) throws IllegalArgumentException {
		models.ChatRoom.get().say(user, message);
	}

	@Override
	public EventDummy dummy(EventDummy d) {
		return d;
	}
    
}
