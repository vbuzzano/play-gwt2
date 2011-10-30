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

import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.concurrent.Future;

import play.Play;
import play.data.validation.Validation;
import play.exceptions.UnexpectedException;
import play.modules.gwt2.chain.GWT2Chain;
import play.modules.gwt2.chain.GWT2ChainAsync;
import play.modules.gwt2.chain.GWT2ChainSync;
import play.mvc.Http.Request;
import play.mvc.Http.Response;
import play.mvc.Router;
import play.mvc.Router.Route;
import play.mvc.Scope.Session;
import play.mvc.results.RenderStatic;

import com.google.gwt.user.server.rpc.RPCRequest;
import com.google.gwt.user.server.rpc.SerializationPolicy;
import com.google.gwt.user.server.rpc.SerializationPolicyLoader;
import com.google.gwt.user.server.rpc.SerializationPolicyProvider;

/**
 * GWT2Service Class
 *
 * Extends this class to create a GWT2 Service for Play! framework
 * This class is based on the GWT Plugin by **Rustem Suniev**.
 * 
 * For example, to implement this service:
 * 
 * <pre><code>
 * package gwt.mymod.client;
 * 
 * import com.google.gwt.user.client.rpc.RemoteService;
 * import com.google.gwt.user.client.rpc.RemoteServiceRelativePath;
 * 
 * @RemoteServiceRelativePath("hello")
 * public interface HelloService extends RemoteService {
 *     String sayHello(String name);
 * }
 * 
 * Create a class that extends the **play.modules.gwt.GWTService**, and define the service URL path with the **play.modules.gwt.GWTServicePath** annotation. Like this:
 *
 * package services;
 * 
 * import play.modules.gwt2.GWTService;
 * import play.modules.gwt2.GWTServicePath;
 * import gwt.mymod.client.HelloService;
 * 
 * @GWT2ServicePath("/module/hello")
 * public class HelloServiceImpl extends GWTService implements HelloService {
 *     public String sayHello(String name) {
 *         return "Hello " + name;
 *     }
 * }
 * 
 * or without GWT2ServicePath, just name your service class with the name in RemoteServiceRelativePath 
 * 
 * public class Hello extends GWTService implements HelloService {
 *     public String sayHello(String name) {
 *         return "Hello " + name;
 *     }
 * }
 * 
 * You Can use annotation @GWT2ServiceAsync to enable a service to be runned async using Play Job
 * 
 * This is the only difference from the GWT documentation.
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 */
public class GWT2Service implements SerializationPolicyProvider {
  
	protected Validation validation = Validation.current();
	
	protected Request request;
	protected Response response;
	protected Session session;
	protected RPCRequest rpcRequest;
	protected String payload;
	
	public RPCRequest getRpcRequest() {
		return rpcRequest;
	}

	public void setRpcRequest(RPCRequest rpcRequest) {
		this.rpcRequest = rpcRequest;
	}

	public void setRequest(Request request) {
		this.request = request;
	}

	public void setResponse(Response response) {
		this.response = response;
	}

	public void setSession(Session session) {
		this.session = session;
	}

	public void setPlayLoad(String pl) {
		payload = pl;
	}

    /**
     * 
     * 
     * @param moduleBaseURL
     * @param strongName
     * @return
     */
    protected SerializationPolicy doGetSerializationPolicy(String moduleBaseURL, String strongName) {

        // Find the module path
        String modulePath = null;
        if (moduleBaseURL != null) {
            try {
                modulePath = new URL(moduleBaseURL).getPath();
            } catch (MalformedURLException ex) {
                throw new UnexpectedException("Malformed moduleBaseURL: " + moduleBaseURL, ex);
            }
        }

        SerializationPolicy serializationPolicy = null;

        String serializationPolicyFilePath = SerializationPolicyLoader.getSerializationPolicyFileName(modulePath + strongName);

        // Ok. Will need to route this path as it's an URL
        for (Route route : Router.routes) {
            try {
                route.matches("GET", serializationPolicyFilePath);
            } catch(Throwable t) {                                          
                if(t instanceof RenderStatic) {
                    serializationPolicyFilePath = ((RenderStatic)t).file;
                    break;
                }
            }
        }

        // Open the RPC resource file read its contents.
        InputStream is = Play.getVirtualFile(serializationPolicyFilePath).inputstream();
        try {
            if (is != null) {
                try {
                    serializationPolicy = SerializationPolicyLoader.loadFromStream(is, null);
                } catch (Exception e) {
                    throw new UnexpectedException("ERROR: Failed to parse the policy file '" + serializationPolicyFilePath + "'", e);
                } 
            } else {
                throw new UnexpectedException("ERROR: The serialization policy file '" + serializationPolicyFilePath + "' was not found; did you forget to include it in this deployment?");
            }
        } finally {
            if (is != null) {
                try {
                    is.close();
                } catch (IOException e) {
                }
            }
        }
        return serializationPolicy;
    }
    
    public final SerializationPolicy getSerializationPolicy(String moduleBaseURL, String strongName) {
        return doGetSerializationPolicy(moduleBaseURL, strongName);
    }

    /**
     * Invoke the service
     * return the result to encode
     * @return
     * @throws InvocationTargetException 
     * @throws IllegalAccessException 
     * @throws IllegalArgumentException 
     */
    public Object invoke() throws IllegalArgumentException, IllegalAccessException, InvocationTargetException {
        ClassLoader cl = Thread.currentThread().getContextClassLoader();
        try {
            Thread.currentThread().setContextClassLoader(Play.classloader);

            Method serviceMethod = getServiceMethod();
            if (serviceMethod == null)
            	throw new NullPointerException("serviceMethod");

            SerializationPolicy serializationPolicy = getSerializationPolicy();
            if (serializationPolicy == null)
            	throw new NullPointerException("serializationPolicy");

            // invoke
            return serviceMethod.invoke(this, rpcRequest.getParameters());
        } finally {
            Thread.currentThread().setContextClassLoader(cl);
        }
    }

    protected SerializationPolicy getSerializationPolicy() {
    	return rpcRequest.getSerializationPolicy();
    }

	protected Method getServiceMethod() {
    	return rpcRequest.getMethod();
    }

	@SuppressWarnings({ "rawtypes", "unchecked" })
	protected static Object chainASync(Future<?> future, GWT2Chain chain) {
    	throw new GWT2ChainAsync(future, chain);
    }

	@SuppressWarnings("rawtypes")
	protected static Object chain(Future<?> future, GWT2Chain chain) {
    	throw new GWT2ChainSync(future, chain);
    }

}
