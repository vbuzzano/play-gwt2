package shared.events;

import java.io.Serializable;

/**
 * Hack to add necessary class to rpc white list
 * @author vincent
 *
 */
public class EventDummy implements Serializable {
	public Event event;
	public Join join;
	public Leave leave;
	public Message message;
}
