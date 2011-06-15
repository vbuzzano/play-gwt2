package gwt.longPolling.client;


import java.util.List;

import shared.events.Event;
import shared.ui.AppHelper;
import shared.ui.NewMessagePanel;
import shared.ui.SendMessageEvent;
import shared.ui.SendMessageListener;
import shared.ui.ThreadPanel;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.RootPanel;

/**
 * Generated Entry Point
 * play-gwt2
 */
public class Longpolling implements EntryPoint {
	
	private final ChatRoomServiceAsync chatRoom = GWT.create(ChatRoomService.class);
	private String user;
	private Long lastReceived;
	
	ThreadPanel threadPanel;
	NewMessagePanel newMessagePanel;
	
	public void onModuleLoad() {

		// get chat panel
		RootPanel chat = RootPanel.get("chat");
	
		// String user
		user = AppHelper.getUserFromPage();
		if (user == null)
			user = "Guest";

		// create Thread panel
		threadPanel = new ThreadPanel();
		chat.add(threadPanel);
	
		// create new message panel
		newMessagePanel = new NewMessagePanel();
		newMessagePanel.addSendMessageListener(new SendMessageListener() {
			
			@Override
			public void onSend(SendMessageEvent event) {
				chatRoom.say(event.getMessage(), user, new AsyncCallback<List<Void>>() {
					
					@Override
					public void onSuccess(List<Void> result) {
					}
					
					@Override
					public void onFailure(Throwable caught) {						
					}
				});
			}
		});
		chat.add(newMessagePanel);
		
		// load chatroom messages
		lastReceived = new Long(0);
		chatRoom.waitMessages(lastReceived, new GetMessages());
	}
	
	
	private class GetMessages implements AsyncCallback<List<Event>> {

		@Override
		public void onFailure(Throwable caught) {
			Window.alert(caught.getLocalizedMessage());
		}

		@Override
		public void onSuccess(List<Event> result) {
			for (Event event : result) {
				lastReceived = event.getId();
				threadPanel.addEvent(event);				
			}
			threadPanel.scrollDown();
			newMessagePanel.focus();
			
			chatRoom.waitMessages(lastReceived, new GetMessages());
		}		
	}
}
