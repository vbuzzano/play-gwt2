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

/**
 * GWT2Chain Interface
 * 
 * Use to chain gwt2 call as (future/promise)
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
public interface GWT2Chain<T> {
	public Object chain(T result);
}
