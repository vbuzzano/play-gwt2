package shared.ui;

public class AppHelper {
	
	/**
	 * Get username
	 * @return
	 */
	public static native String getUserFromPage() /*-{
		var user = eval('$wnd.appInit.user');
		return user;
	}-*/; 
	
	/**
	 * Get Websocket server url
	 * @return
	 */
	public static native String getWebsocketServer() /*-{
		var ws = eval('$wnd.appInit.ws');
		return ws;
	}-*/; 
	
	/**
	 * redirect the browser to the given url
	 * @param url
	 */
	public static native void redirect(String url)/*-{
	      $wnd.location = url;
	  }-*/;
}