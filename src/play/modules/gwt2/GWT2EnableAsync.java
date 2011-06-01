package play.modules.gwt2;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * 
 * 
 * 
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface GWT2EnableAsync {
   
	/**
	 *
	 * GLOBAL = run the service as a Job
	 * INTERN = enable the service to use await command
	 */
	public static enum Enable {
		GLOBAL,
		INTERN
	}
	
	/**
	 * Value can be
	 * 
	 * @return
	 */
	public String value();    
}
