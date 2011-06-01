package play.modules.gwt2.chain;

import java.util.concurrent.Future;

import play.modules.gwt2.GWT2Service;

/**
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
abstract public class GWT2ChainRuntime extends RuntimeException {
	private Future future;
	private GWT2Chain<Object> chain;
	
	public GWT2ChainRuntime(Future future, GWT2Chain<Object> chain) {
		this.future = future;
		this.chain = chain;
	}

	public Future getFuture() {
		return future;
	}
	
	public GWT2Chain<Object> getChain() {
		return chain;
	}
}
