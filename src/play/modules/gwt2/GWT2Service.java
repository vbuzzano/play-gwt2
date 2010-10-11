package play.modules.gwt2;

import java.io.IOException;
import java.io.InputStream;
import java.net.MalformedURLException;
import java.net.URL;

import play.Logger;
import play.Play;
import play.data.validation.Validation;
import play.exceptions.UnexpectedException;
import play.libs.IO;
import play.mvc.Router;
import play.mvc.Http.Request;
import play.mvc.Router.Route;
import play.mvc.results.RenderStatic;

import com.google.gwt.user.server.rpc.RPC;
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
 * This is the only difference from the GWT documentation.
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 */
public class GWT2Service implements SerializationPolicyProvider {
  
	protected Validation validation = Validation.current();
	
	protected Request request;
	
	public void setRequest(Request request) {
		this.request = request;
	}
	
    public final SerializationPolicy getSerializationPolicy(String moduleBaseURL, String strongName) {
        return doGetSerializationPolicy(moduleBaseURL, strongName);
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

    /**
     * Invoke the service
     * @return
     */
    public String invoke() {
        ClassLoader cl = Thread.currentThread().getContextClassLoader();
        try {
            Thread.currentThread().setContextClassLoader(Play.classloader);
            String payload = IO.readContentAsString(Request.current().body);
            RPCRequest rpcRequest = RPC.decodeRequest(payload, this.getClass(), this);
            return RPC.invokeAndEncodeResponse(this, rpcRequest.getMethod(), rpcRequest.getParameters(), rpcRequest.getSerializationPolicy());
        } catch (Exception ex) {
            Logger.error(ex, "An IncompatibleRemoteServiceException was thrown while processing this call.");
            try {
                return RPC.encodeResponseForFailure(null, ex);
            } catch (Exception exx) {
                exx.printStackTrace();
                return null;
            }
        } finally {
            Thread.currentThread().setContextClassLoader(cl);
        }
    }
}
