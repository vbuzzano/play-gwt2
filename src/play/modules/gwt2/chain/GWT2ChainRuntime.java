/*
 * Copyright 2011 Vincent Buzzano
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package play.modules.gwt2.chain;

import java.util.concurrent.Future;

/**
 * GWT2ChainRuntime
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
abstract public class GWT2ChainRuntime extends RuntimeException {
	private static final long serialVersionUID = 1L;
	private Future<?> future;
	private GWT2Chain<Object> chain;
	
	public GWT2ChainRuntime(Future<?> future, GWT2Chain<Object> chain) {
		this.future = future;
		this.chain = chain;
	}

	public Future<?> getFuture() {
		return future;
	}
	
	public GWT2Chain<Object> getChain() {
		return chain;
	}
}
