package models;



import java.util.List;

import play.libs.F.ArchivedEventStream;
import play.libs.F.EventStream;
import play.libs.F.IndexedEvent;
import play.libs.F.Promise;
import shared.events.Event;
import shared.events.Join;
import shared.events.Leave;
import shared.events.Message;

public class ChatRoom {
    
    // ~~~~~~~~~ Let's chat! 
    
    final ArchivedEventStream<Event> chatEvents = new ArchivedEventStream<Event>(100);
    
    /**
     * For WebSocket, when a user join the room we return a continuous event stream
     * of ChatEvent
     */
    public EventStream<Event> join(String user) {
        chatEvents.publish(new Join(user));
        return chatEvents.eventStream();
    }
    
    /**
     * A user leave the room
     */
    public void leave(String user) {
        chatEvents.publish(new Leave(user));
    }
    
    /**
     * A user say something on the room
     */
    public void say(String user, String text) {
        if(text == null || text.trim().equals("")) {
            return;
        }
        chatEvents.publish(new Message(user, text));
    }
    
    /**
     * For long polling, as we are sometimes disconnected, we need to pass 
     * the last event seen id, to be sure to not miss any message
     */
    public Promise<List<IndexedEvent<Event>>> nextMessages(long lastReceived) {
        return chatEvents.nextEvents(lastReceived);
    }
    
    /**
     * For active refresh, we need to retrieve the whole message archive at
     * each refresh
     */
    public List<Event> archive() {
        return chatEvents.archive();
    }
    
    // ~~~~~~~~~ Chat room factory

    static ChatRoom instance = null;
    public static ChatRoom get() {
        if(instance == null) {
            instance = new ChatRoom();
        }
        return instance;
    }
    
}

