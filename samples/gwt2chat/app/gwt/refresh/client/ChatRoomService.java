package gwt.refresh.client;


import java.util.List;

import shared.events.Event;
import shared.events.EventDummy;


import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

/**
 * The client side stub for the RPC service.
 */
@RemoteServiceRelativePath("chatroom")
public interface ChatRoomService extends RemoteService {
	
	EventDummy dummy(EventDummy dummy);
	
	List<Event> archive() throws IllegalArgumentException;
	List<Event> say(String message, String user) throws IllegalArgumentException;
}
