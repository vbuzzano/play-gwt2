package gwt.gwtmodule.client;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.RootPanel;

public class classmodule implements EntryPoint {
	
	private final GreetingServiceAsync greetingService = GWT.create(GreetingService.class);
	
	public void onModuleLoad() {
		Button b = new Button("Click me", new ClickHandler() {
			public void onClick(ClickEvent event) {
				greetingService.greetServer("Ajax", new AsyncCallback<String>() {
					
					public void onSuccess(String result) {
						Window.alert(result);
					}
					public void onFailure(Throwable caught) {
						Window.alert("error");
					}
				});
			}
		});
		RootPanel.get("content").add(b);
	}
}
