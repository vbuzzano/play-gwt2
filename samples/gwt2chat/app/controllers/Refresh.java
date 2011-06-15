package controllers;

import play.*;
import play.mvc.*;

import java.util.*;

import models.*;

public class Refresh extends Controller {

    public static void index(String user) {
        ChatRoom.get().join(user);
        room(user);
    }
    
    public static void room(String user) {
        render(user);
    }
    
    public static void leave(String user) {
        ChatRoom.get().leave(user);
        Application.index();
    }    
}

