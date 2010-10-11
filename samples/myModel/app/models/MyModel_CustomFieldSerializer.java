package models;


import com.google.gwt.user.client.rpc.SerializationException;
import com.google.gwt.user.client.rpc.SerializationStreamReader;
import com.google.gwt.user.client.rpc.SerializationStreamWriter;

public class MyModel_CustomFieldSerializer {
	
	public static MyModel instantiate(SerializationStreamReader reader)
		throws SerializationException {
		return new MyModel();
	}
	
	public static void serialize(SerializationStreamWriter writer,
			MyModel instance)
		throws SerializationException {
		writer.writeObject(instance.id);
		writer.writeString(instance.someText);
	
	}
	
	public static void deserialize(SerializationStreamReader reader,
			MyModel instance)
		throws SerializationException {
		instance.id = (Long) reader.readObject();
		instance.someText = reader.readString();
	}
}