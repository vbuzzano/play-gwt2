package controllers;

import java.lang.reflect.InvocationTargetException;
import java.util.concurrent.Future;

import org.apache.commons.lang.NullArgumentException;

import play.Play;
import play.exceptions.JavaExecutionException;
import play.exceptions.PlayException;
import play.libs.IO;
import play.modules.gwt2.GWT2Invoker;
import play.modules.gwt2.GWT2Plugin;
import play.modules.gwt2.GWT2Plugin.GWT2Module;
import play.modules.gwt2.GWT2Service;
import play.modules.gwt2.GWT2ServiceAsync;
import play.modules.gwt2.chain.GWT2ChainAsync;
import play.modules.gwt2.chain.GWT2ChainRuntime;
import play.modules.gwt2.chain.GWT2ChainSync;
import play.mvc.Controller;

import com.google.gwt.user.client.rpc.SerializationException;
import com.google.gwt.user.client.rpc.impl.AbstractSerializationStream;
import com.google.gwt.user.server.rpc.RPC;
import com.google.gwt.user.server.rpc.RPCRequest;
/**
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
public class GWT2Controller extends Controller {
	
	public static boolean isGWT() {
		return request.contentType.equals("text/x-gwt-rpc");
	}

	public static void invoke(String module, String service) throws Exception {
 
		// find the module 
		GWT2Module mod = GWT2Plugin.getModule(module, service);
		if (mod == null)
			notFound("module not found !");

        // create service instance
    	GWT2Service gwtService;
		try {
			gwtService = (GWT2Service) mod.service.newInstance();

			if (mod.service == null)
	    		throw new NullArgumentException("module.service is null");
	    	
	        if (!GWT2Service.class.isAssignableFrom(mod.service))
	        	throw new Exception("module.service is not GWT2Service instance");

		} catch (Exception e) {
            StackTraceElement element = PlayException.getInterestingStrackTraceElement(e);
            if (element != null) {
                throw new JavaExecutionException(Play.classes.getApplicationClass(element.getClassName()), element.getLineNumber(), e);
            }
            throw new JavaExecutionException(e);
		}

    	// decode rpc request
		RPCRequest rpcRequest = 
			RPC.decodeRequest(IO.readContentAsString(request.body),
					gwtService.getClass(), gwtService);
		
		// response load
		String responseload = null;
    	
		// check GWT2ServiceAsync
		GWT2ServiceAsync gwt2AsyncCall = mod.service.getAnnotation(GWT2ServiceAsync.class);
		if (gwt2AsyncCall != null && gwt2AsyncCall.value()) {
			// async invokation
			responseload = invokeAsync(gwtService, rpcRequest);

		} else {
			// synced invokation
			// bt service can use GWT2Chain to do async job
			responseload = invoke(gwtService, rpcRequest);
		}
   
		
		renderText(responseload);
	}

	/**
	 * Invoke a Service async using GWT2Invoker Job
	 * @param mod
	 * @return
	 */
	private static String invokeAsync(GWT2Service service, RPCRequest rpcRequest) {
		// Get GWt2Invoker
		GWT2Invoker invoker = 
			new GWT2Invoker(service, request, response, session, rpcRequest);
			String responseload = await(invoker.now());
		return responseload;		
	}
	
	/**
	 * Invoke a Service 
	 * 
	 * This way GWT2Service is allowed to use GWT2Chain
	 * 
	 * @param mod
	 * @return
	 * @throws Exception 
	 */
	private static String invoke(GWT2Service service, RPCRequest rpcRequest) throws Exception {
		String responseload = null;
		
		try {
			// Get GWt2Invoker
			GWT2Invoker invoker = 
				new GWT2Invoker(service, request, response, session, rpcRequest);
			
			// run 
		   	boolean run = true;
	    	Object result = null;
	    	Object chainResult = null;
	    	boolean firstcall = true;
	    	GWT2ChainRuntime chain = null;
	    	while(run) {
		    	try {
		    		if (firstcall) {
		    			firstcall = false;
		    			// call service
		    			result = invoker.invoke();
			    		// get a result stop request
			    		run = false;
		    		} else if (chain != null) {
		    			// call callback
			    		result = chain.getChain().chain(chainResult);
			    		// get a result stop request
			    		run = false;
		    		} else {
		    			// no callback to call stop process
		    			run = false;
		    		}
		    	} catch (GWT2ChainAsync casync) {
		    		// async chain call
		    		 chain = casync;
		    		 chainResult = chainAwait(chain);
		    	} catch (GWT2ChainSync csync) {
		    		 chain = csync;
		    		 chainResult = chainDo(chain);
		    	} catch(InvocationTargetException ite) {
		    		if (ite.getTargetException() instanceof GWT2ChainAsync) {
			    		// async chain call
			    		 chain = (GWT2ChainAsync) ite.getTargetException();
			    		 chainResult = chainAwait(chain);
		    		} else if (ite.getTargetException() instanceof GWT2ChainSync) {
			    		 chain =  (GWT2ChainSync) ite.getTargetException();
			    		 chainResult = chainDo(chain);
		    		} else 
		    			throw ite;
		    	} 
	    	} 
		
	    	// encode result
	    	responseload = RPC.encodeResponseForSuccess(
            		rpcRequest.getMethod(),
            		result, 
            		rpcRequest.getSerializationPolicy(),
            		AbstractSerializationStream.DEFAULT_FLAGS);
		
	    	return responseload;
	    	
		} catch (Exception ex) {
            if (ex instanceof PlayException)
            	// Rethrow the enclosed exception
                throw (PlayException) ex;

            // if not gwt rpc rethrow
            if (! isGWT())
                throw ex;

            try {
	            // else encode error
	            responseload = RPC.encodeResponseForFailure(
		                		rpcRequest.getMethod(), ex, 
		                		rpcRequest.getSerializationPolicy(),
		                		AbstractSerializationStream.DEFAULT_FLAGS);
			
            } catch (SerializationException e) {
	            StackTraceElement element = PlayException.getInterestingStrackTraceElement(e);
	            if (element != null) {
	                throw new JavaExecutionException(Play.classes.getApplicationClass(element.getClassName()), element.getLineNumber(), e);
	            }
	            throw new JavaExecutionException(e);
			}	    		
    	}
		
		return responseload;
	}

	private static Object chainAwait(GWT2ChainRuntime chain) {
		 return await(chain.getFuture());		
	}

	private static Object chainDo(GWT2ChainRuntime chain) {
		 Future f = chain.getFuture();
		 while(f.isDone() || f.isCancelled()){  
			 await(100);  
		 }  
		 try {
			return f.get();
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
}
