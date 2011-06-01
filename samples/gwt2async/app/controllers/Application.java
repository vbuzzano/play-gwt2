package controllers;

import java.util.concurrent.Future;

import gwt.async.services.Greeting;
import play.modules.gwt2.chain.GWT2ChainAsync;
import play.modules.gwt2.chain.GWT2ChainRuntime;
import play.modules.gwt2.chain.GWT2ChainSync;
import play.mvc.Controller;

public class Application extends Controller {

    public static void index() {
    	render();
    }

}