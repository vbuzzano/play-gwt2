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
 * GWT2ChainAsync
 * 
 * Use to chain a Future or Promise async
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
public class GWT2ChainAsync extends GWT2ChainRuntime {
	private static final long serialVersionUID = 1L;

	public GWT2ChainAsync(Future<?> future, GWT2Chain<Object> chain) {
		super(future, chain);
	}
}
