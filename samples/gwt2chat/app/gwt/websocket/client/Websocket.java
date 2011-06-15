package gwt.websocket.client;



import libs.gwt2ws.client.GWT2WSClient;
import libs.gwt2ws.client.GWT2WSClient.WSCallback;
import shared.ui.AppHelper;
import shared.ui.NewMessagePanel;
import shared.ui.SendMessageEvent;
import shared.ui.SendMessageListener;
import shared.ui.ThreadPanel;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.RootPanel;

/**
 * Generated Entry Point
 * play-gwt2
 */
public class Websocket implements EntryPoint {

	private String server;
	private String user;

	ThreadPanel threadPanel;
	NewMessagePanel newMessagePanel;
	
	GWT2WSClient client;
	
	public void onModuleLoad() {
		server = AppHelper.getWebsocketServer();
		if (server == null || server.length() == 0) {
			Window.alert("No server found");
			return;
		}

		client = GWT2WSClient.create(
				server, new WSClientCallback());

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
				client.send(event.getMessage());
			}
		});
		chat.add(newMessagePanel);
		
		client.open();
	}

	public class WSClientCallback implements WSCallback {
		
		@Override
		public void received(String message) {
			String[] event = 
				message.split(":");
			if (event[0].equals("join"))
				threadPanel.addJoinMessage(event[1]);
			else if (event[0].equals("leave"))
				threadPanel.addLeaveMessage(event[1]);
			else if (event[0].equals("message"))
				threadPanel.addMessage(event[1], event[2]);
			else if (event[0].equals("quit")) {
				if (event[1].equals("ok"))
					AppHelper.redirect("/");
				else
					Window.alert(event[1]);
			} else
				Window.alert("Unknown message : " + message);
		}
		
		@Override
		public void opened() {
		}
		
		@Override
		public void closed() {
		}
	}
}
