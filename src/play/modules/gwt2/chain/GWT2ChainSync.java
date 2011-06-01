package play.modules.gwt2.chain;

import java.util.concurrent.Future;

import play.modules.gwt2.GWT2Service;

/**
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
public class GWT2ChainSync extends GWT2ChainRuntime {
	public GWT2ChainSync(Future future, GWT2Chain<Object> chain) {
		super(future, chain);
	}
}
