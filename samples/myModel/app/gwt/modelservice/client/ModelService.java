package gwt.modelservice.client;

import java.lang.annotation.Annotation;
import java.util.List;

import models.MyModel;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.core.client.GWT;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.KeyPressEvent;
import com.google.gwt.event.dom.client.KeyPressHandler;
import com.google.gwt.user.client.Window;
import com.google.gwt.user.client.rpc.AsyncCallback;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.HTML;
import com.google.gwt.user.client.ui.Label;
import com.google.gwt.user.client.ui.RootPanel;
import com.google.gwt.user.client.ui.TextArea;
import com.google.gwt.user.client.ui.TextBox;


public class ModelService implements EntryPoint {
	private TextBox modelText = new TextBox();
	private HTML modelList = new HTML();
	
	private final MyModelServiceAsync myModelService = GWT.create(MyModelService.class);
	
	public void onModuleLoad() {

		// Save Button click handler
		Button saveButton = new Button("Save", new ClickHandler() {
			public void onClick(ClickEvent event) {
				saveModel();
			}
		});

		modelText.addKeyPressHandler(new KeyPressHandler() {
			@Override
			public void onKeyPress(KeyPressEvent event) {
				if (event.getCharCode() == 13) { // ENTER
					modelText.setFocus(false);
					saveModel();
				}
			}
		});
		
		HTML modelListTitle = new HTML("<h2>Models List</h2>");
		
		RootPanel.get("content").add(modelText);
		RootPanel.get("content").add(saveButton);
		RootPanel.get("content").add(modelListTitle);
		RootPanel.get("content").add(modelList);

		updateModelList();
	}

	/**
	 * Save Model
	 */
	private void saveModel() {
		// create a new Model
		MyModel model = new MyModel();
		model.someText = modelText.getText();
		myModelService.save(model, new SaveModelCallBack());
	}

	/**
	 * Update Model List
	 */
	public void updateModelList() {
		// look for existing mod
		myModelService.findAll(new FindAllModelCallBack());
	}
	
	
	/**
	 * Save Model Callback
	 */
	public class SaveModelCallBack implements AsyncCallback<String> {
		
		public void onSuccess(String result) {
			Window.alert(result);
			updateModelList();
			modelText.setFocus(true);
		}
		
		public void onFailure(Throwable caught) {
			Window.alert(caught.getLocalizedMessage());
			modelText.setFocus(true);
		}
	}

	/**
	 * Find All Model Callback
	 */
	public class FindAllModelCallBack implements AsyncCallback<List<MyModel>> {

		@Override
		public void onSuccess(List<MyModel> result) {
			String html = "<ul>";
			for (MyModel model : result)
				html += "<li>" + model.someText + "</li>";
			html += "</ul>";
			modelList.setHTML(html);
		}

		@Override
		public void onFailure(Throwable caught) {
			Window.alert(caught.getLocalizedMessage());
		}
	}
}

