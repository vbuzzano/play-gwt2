package controllers;


import java.util.List;

import models.ChatRoom;
import play.libs.F.IndexedEvent;
import play.mvc.Controller;
import shared.events.Event;

import com.google.gson.reflect.TypeToken;

public class LongPolling extends Controller {

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

