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
package play.modules.gwt2;

import java.lang.reflect.InvocationTargetException;

import play.Play;
import play.exceptions.JavaExecutionException;
import play.exceptions.PlayException;
import play.jobs.Job;
import play.libs.IO;
import play.modules.gwt2.chain.GWT2ChainRuntime;
import play.mvc.Http.Request;
import play.mvc.Http.Response;
import play.mvc.Scope.Session;

import com.google.gwt.user.client.rpc.SerializationException;
import com.google.gwt.user.client.rpc.impl.AbstractSerializationStream;
import com.google.gwt.user.server.rpc.RPC;
import com.google.gwt.user.server.rpc.RPCRequest;

/**
 * GWTI2Invoker
 * 
 * Class use to invoke GWT2Service
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
public class GWT2Invoker extends Job<String> {
	private GWT2Service service;
	private Request request;
	private Response response;
	private Session session;
	private String body;
	private Object result;
	private String responseload;
	private RPCRequest rpcRequest;
		
	public GWT2Invoker(GWT2Service service, Request request, Response response, Session session, RPCRequest rpcRequest) {
		this.rpcRequest = rpcRequest;
		this.service = service;
		this.request = request;
		this.response = response;
		this.session = session;
		this.body = IO.readContentAsString(request.body);
	}
	
	
    public String doJobWithResult() throws Exception {
    	doJob();
		return responseload;
	}
	
    /**
     * Invoke a service
     * @param service
     */
    public void doJob() {

        result = null;
        try {
            // invoke
            result = invoke();
            // encode result
            responseload = RPC.encodeResponseForSuccess(
            		rpcRequest.getMethod(),
            		result, 
            		rpcRequest.getSerializationPolicy(),
            		AbstractSerializationStream.DEFAULT_FLAGS);

        } catch (Exception ex) {
            if (ex instanceof PlayException)
            	// Rethrow the enclosed exception
                throw (PlayException) ex;
            
            try {
                if (GWT2ChainRuntime.class.isAssignableFrom(ex.getClass())) {
					responseload = RPC.encodeResponseForFailure(
							rpcRequest.getMethod(), new JavaExecutionException("Chain call is not allowed when runngin Service in async mode", ex), 
							rpcRequest.getSerializationPolicy(),
							AbstractSerializationStream.DEFAULT_FLAGS);
	            } else {
	                responseload = RPC.encodeResponseForFailure(
	                		rpcRequest.getMethod(), ex, 
	                		rpcRequest.getSerializationPolicy(),
	                		AbstractSerializationStream.DEFAULT_FLAGS);
	            }
			} catch (SerializationException e) {
	            StackTraceElement element = PlayException.getInterestingStrackTraceElement(e);
	            if (element != null) {
	                throw new JavaExecutionException(Play.classes.getApplicationClass(element.getClassName()), element.getLineNumber(), e);
	            }
	            throw new JavaExecutionException(e);
			}
        }
    }

    
    /**
     * invoke service
     * @throws InvocationTargetException 
     * @throws IllegalAccessException 
     * @throws IllegalArgumentException 
     */
    public Object invoke() throws IllegalArgumentException, IllegalAccessException, InvocationTargetException {

		// init service
		service.setRequest(request);
    	service.setResponse(response);
    	service.setSession(session);
    	service.setPlayLoad(body);
    	service.setRpcRequest(rpcRequest);
    	
    	// invoke
    	return service.invoke();            
    }
}
