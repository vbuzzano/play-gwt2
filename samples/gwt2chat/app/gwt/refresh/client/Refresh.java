package gwt.refresh.client;


import java.util.List;

import shared.events.Event;
import shared.ui.AppHelper;
import shared.ui.NewMessagePanel;
import shared.ui.SendMessageEvent;
import shared.ui.SendMessageListener;
import shared.ui.ThreadPanel;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.user.client.Timer;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.RootPanel;

/**
 * Generated Entry Point
 * play-gwt2
 */
public class Refresh implements EntryPoint {
	
	private final ChatRoomServiceAsync chatRoom = GWT.create(ChatRoomService.class);
	private String user;
	
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
				chatRoom.say(event.getMessage(), user, new refreshThreadCallback());
			}
		});
		chat.add(newMessagePanel);
		
		// load chatroom archive
		chatRoom.archive(new refreshThreadCallback());	

		Timer refresher = new Timer() {
			
			@Override
			public void run() {
				chatRoom.archive(new refreshThreadCallback());
				this.schedule(5000);
			}
		};
		
		refresher.schedule(5000);
	}
	
	
	private class refreshThreadCallback implements AsyncCallback<List<Event>> {

		@Override
		public void onFailure(Throwable caught) {
			Window.alert(caught.getLocalizedMessage());
		}

		@Override
		public void onSuccess(List<Event> result) {
			threadPanel.clear();
			for (Event event : result) {
				threadPanel.addEvent(event);				
			}
			threadPanel.scrollDown();
			newMessagePanel.focus();
		}

	}
}
