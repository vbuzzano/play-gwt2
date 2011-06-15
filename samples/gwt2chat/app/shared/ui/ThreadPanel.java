package shared.ui;

import shared.events.Event;
import shared.events.Join;
import shared.events.Leave;
import shared.events.Message;

import com.google.gwt.safehtml.shared.SafeHtmlBuilder;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.ui.Composite;
import com.google.gwt.user.client.ui.FlowPanel;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.HTMLPanel;
import com.google.gwt.user.client.ui.ScrollPanel;

public class ThreadPanel extends FlowPanel {
	ScrollPanel scroll;
	FlowPanel list;
	
	public ThreadPanel() {
    	super();
    	setStyleName("thread");
    	scroll = new ScrollPanel();
    	add(scroll);
    	scroll.setHeight("100%");
    	list = new FlowPanel();
    	scroll.add(list);
    }

	public void addEvent(Event event) {
		if (event instanceof Message)
			addMessage(((Message) event).getUser(), ((Message) event).getText());
		else if(event instanceof Join) {
			addJoinMessage(((Join)event).getUser());
		} else if(event instanceof Leave) {
			addLeaveMessage(((Leave)event).getUser());
		}
	}

    public void addMessage(String user, String message) {
    	String msg = "<h2>" + user + "</h2><p>" + message + "</p>";
    	HTML html = new HTML(msg);
		html.setStyleName("message");
		list.add(html);
	}

    public void addJoinMessage(String user) {
    	String msg = "<h2></h2><p>" + user + " join the room</p>";
    	HTML html = new HTML(msg);
		html.setStyleName("message notice");
		list.add(html);
	}

    public void addLeaveMessage(String user) {
    	String msg = "<h2></h2><p>" + user + " leave the room</p>";
    	HTML html = new HTML(msg);
		html.setStyleName("message notice");
		list.add(html);
	}

    @Override
	public void clear() {
    	list.clear();
    }

	public void scrollDown() {
    	scroll.scrollToBottom();
    }
}
