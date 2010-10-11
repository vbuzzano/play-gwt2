package gwt.modelservice.client;

import java.util.List;

import models.MyModel;

import com.google.gwt.user.client.rpc.RemoteService;
import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;

/**
 * The client side stub for the RPC service.
 */
@RemoteServiceRelativePath("mymodel")
public interface MyModelService extends RemoteService {
	String save(MyModel name) throws IllegalArgumentException;
	List<MyModel> findAll() throws IllegalArgumentException;
}
