package gwt.modelservice.server;

import java.util.List;

import gwt.modelservice.client.MyModelService;
import models.MyModel;
import play.modules.gwt2.GWT2Service;
import play.modules.gwt2.GWT2ServicePath;
 
@GWT2ServicePath("/modelservice/mymodel")
public class MyModelServiceImpl extends GWT2Service implements MyModelService {
 
	@Override
	public String save(MyModel model) {
    	
    	validation.valid(model);
	    if(validation.hasErrors()) {
            throw new IllegalArgumentException("MyModel is not valid");
	    }
    	model.save();
        return "MyModel has been saved";
    }

	@Override
	public List<MyModel> findAll() throws IllegalArgumentException {
		List<MyModel> l = MyModel.findAll();
		return l;
	}
}
