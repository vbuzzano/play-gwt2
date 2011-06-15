package controllers;

import static play.libs.F.Matcher.ClassOf;
import static play.libs.F.Matcher.Equals;
import static play.mvc.Http.WebSocketEvent.SocketClosed;
import static play.mvc.Http.WebSocketEvent.TextFrame;
import models.ChatRoom;
import play.libs.F.Either;
import play.libs.F.EventStream;
import play.libs.F.Promise;
import play.mvc.Controller;
import play.mvc.Http.WebSocketClose;
import play.mvc.Http.WebSocketEvent;
import play.mvc.WebSocketController;
import shared.events.Event;
import shared.events.Join;
import shared.events.Leave;
import shared.events.Message;

public class WebSocket extends Controller {
    
    public static void room(String user) {
        render(user);
    }

    public static class ChatRoomSocket extends WebSocketController {
        
        public static void join(String user) {
            
            ChatRoom room = ChatRoom.get();
            
            // Socket connected, join the chat room
            EventStream<Event> roomMessagesStream = room.join(user);
         
            // Loop while the socket is open
            while(inbound.isOpen()) {
                
                // Wait for an event (either something coming on the inbound socket channel, or ChatRoom messages)
                Either<WebSocketEvent,Event> e = await(Promise.waitEither(
                    inbound.nextEvent(), 
                    roomMessagesStream.nextEvent()
                ));
                
                // Case: User typed 'quit'
                for(String userMessage: TextFrame.and(Equals("quit")).match(e._1)) {
                    room.leave(user);
                    outbound.send("quit:ok");
                    disconnect();
                }
                
                // Case: TextEvent received on the socket
                for(String userMessage: TextFrame.match(e._1)) {
                    room.say(user, userMessage);
                }
                
                // Case: Someone joined the room
                for(Join joined: ClassOf(Join.class).match(e._2)) {
                    outbound.send("join:%s", joined.getUser());
                }
                
                // Case: New message on the chat room
                for(Message message: ClassOf(Message.class).match(e._2)) {
                    outbound.send("message:%s:%s", message.getUser(), message.getText());
                }
                
                // Case: Someone left the room
                for(Leave left: ClassOf(Leave.class).match(e._2)) {
                    outbound.send("leave:%s", left.getUser());
                }
                
                // Case: The socket has been closed
                for(WebSocketClose closed: SocketClosed.match(e._1)) {
                    room.leave(user);
                    disconnect();
                }
                
            }
            
        }
        
    }
    
}

