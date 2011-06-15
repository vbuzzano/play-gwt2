package libs.gwt2ws.client;

import java.util.HashMap;
import java.util.Map;

import com.google.gwt.core.client.JavaScriptObject;

/**
 * Websocket for Play! GWT2
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 */
public class GWT2WSClient {
    private final WSCallback callback;
    private final String server;
    private JavaScriptObject ws;
    
    static private Map<String, GWT2WSClient> clients =
    	new HashMap<String, GWT2WSClient>();

    /**
     * Get client
     * @param server
     * @return
     */
    static public GWT2WSClient get(String server) {
    	if (clients.containsKey(server)) {
    		return clients.get(server);
    	}
    	return null;
    }
    
    /**
     * Create a client
     * @param server
     * @param callback
     * @return
     */
    static public GWT2WSClient create(String server, WSCallback callback) {
    	if (clients.containsKey(server)) {
    		return clients.get(server);
    	}
    	
    	GWT2WSClient client = new GWT2WSClient(server, callback);
    	clients.put(server, client);
    	return client;
    }
    
    /**
     * Constructor
     * @param server
     * @param callback
     */
    private GWT2WSClient(String server, WSCallback callback) {
        this.server = server;
        this.callback = callback;
    }

    /**
     * return server
     */
    public final String server() {return server;}

    /**
     * Use to call callback.opened()
     */
    private final void opened() {callback.opened();}

    /**
     * Use to call callback.closed()
     */
    private final void closed() {callback.closed();}

    /**
     * Use to call calback.received
     * @param message
     */
    private final void received(String message) {callback.received(message);}

    /**
     * Open socket
     */
    public native void open() /*-{
		var $this = this;
		var server = this.@libs.gwt2ws.client.GWT2WSClient::server;
		if (!$wnd.WebSocket) {
			alert("HTML WebSocket not supported by this browser or disabled");
			return;
		}

		console.log("GWT2WSClient open " + server);
		var ws=new $wnd.WebSocket(server);
        this.@libs.gwt2ws.client.GWT2WSClient::ws = ws;
        
		ws.onopen = function() {
			console.log("GWT2WSClient "+server+" open state:"+ws.readyState);
			if(!ws) {
				return;
			}
			$this.@libs.gwt2ws.client.GWT2WSClient::opened()();
		};

		ws.onclose = function(m) {
			console.log("GWT2WSClient "+server+" close state:"+ws.readyState);
			$this.@libs.gwt2ws.client.GWT2WSClient::closed()();
		};

		ws.onmessage = function(response) {
			console.log("GWT2WSClient received data="+response.data);
			if (response.data) {
				$this.@libs.gwt2ws.client.GWT2WSClient::received(Ljava/lang/String;)( response.data );
			}
		};
	}-*/;

    /**
     * Close socket
     */
    public native void close() /*-{
		var ws = this.@libs.gwt2ws.client.GWT2WSClient::ws;
		console.log("GWT2WSClient close socket");
		ws.close();
	}-*/;

    /**
     * Send a message to server
     * @param message
     */
    public native void send(String message) /*-{
		var ws = this.@libs.gwt2ws.client.GWT2WSClient::ws;
		if (ws) {
			console.log("GWT2WSClient send: " + message);
			ws.send(message);
		} else {
			alert("Socket is not open !");
		}
	}-*/;


    static public interface WSCallback {
    	void opened();
    	void closed();
    	void received(String message);
    }
}

