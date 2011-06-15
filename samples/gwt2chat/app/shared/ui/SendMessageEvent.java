package shared.ui;

public class SendMessageEvent {
	private String message;

	public SendMessageEvent(String message) {
		this.message = message;
	}

	public String getMessage() {
		return message;
	}

}
