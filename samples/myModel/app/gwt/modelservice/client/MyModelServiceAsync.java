package gwt.modelservice.client;

import java.util.List;

import models.MyModel;

import com.google.gwt.user.client.rpc.AsyncCallback;

/**
 * The async counterpart of <code>MyModelService</code>.
 */
public interface MyModelServiceAsync {
	void save(MyModel input, AsyncCallback<String> callback)
			throws IllegalArgumentException;

	void findAll(AsyncCallback<List<MyModel>> callback)
	throws IllegalArgumentException;
}
