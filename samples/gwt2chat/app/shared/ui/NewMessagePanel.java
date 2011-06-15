package shared.ui;

import java.util.ArrayList;
import java.util.List;

import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.KeyCodes;
import com.google.gwt.event.dom.client.KeyDownEvent;
import com.google.gwt.event.dom.client.KeyDownHandler;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.FlowPanel;
import com.google.gwt.user.client.ui.ScrollPanel;
import com.google.gwt.user.client.ui.TextBox;

public class NewMessagePanel extends FlowPanel {
	List<SendMessageListener> listeners;
	
	ScrollPanel scroll;
	FlowPanel list;
	TextBox messageBox;
	Button sendMessageButon;
	
	public NewMessagePanel() {
    	super();
    	
    	// init handlers
    	listeners = new ArrayList<SendMessageListener>();
    	
    	// set style
    	setStyleName("newMessage");
    	
    	// add message textbox
    	messageBox = new TextBox();
    	messageBox.addKeyDownHandler(new KeyDownHandler() {
			
			@Override
			public void onKeyDown(KeyDownEvent event) {
				if (event.getNativeKeyCode() == KeyCodes.KEY_ENTER)
					sendMessageButon.click();
			}
    	});
    	messageBox.setStyleName("messagebox");
    	add(messageBox);
    	
    	// add send button
    	sendMessageButon = new Button("send");
    	sendMessageButon.addClickHandler(new ClickHandler() {
			
			@Override
			public void onClick(ClickEvent event) {
				String message = messageBox.getText();
				messageBox.setText("");
				fireSendMessage(new SendMessageEvent(message));
			}
		});
    	add(sendMessageButon);
	}
	
	public void addSendMessageListener(SendMessageListener handler) {
		listeners.add(handler);
	}

	protected void fireSendMessage(SendMessageEvent event) {
		for (SendMessageListener listener : listeners) {
			listener.onSend(event);
		}
	}

	public void focus() {
		messageBox.setFocus(true);
	}
}
