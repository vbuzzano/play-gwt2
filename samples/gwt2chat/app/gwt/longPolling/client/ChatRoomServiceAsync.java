package gwt.longPolling.client;


import java.util.List;

import shared.events.Event;
import shared.events.EventDummy;

import com.google.gwt.user.client.rpc.AsyncCallback;

/**
 * The async counterpart of <code>GreetingService</code>.
 */
public interface ChatRoomServiceAsync {
	
	void dummy(EventDummy dummy, AsyncCallback< EventDummy > callback);
	
	void waitMessages(Long lastReceived, AsyncCallback<List<Event>> events)
			throws IllegalArgumentException;

	void say(String message, String user, AsyncCallback<List<Void>> callback)
		throws IllegalArgumentException;
}
