package shared.ui;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.shared.EventHandler;

public interface SendMessageListener extends EventHandler {

	void onSend(SendMessageEvent event);

}