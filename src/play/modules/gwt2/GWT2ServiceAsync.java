package play.modules.gwt2;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * Define if a gwt2 service must be run async
 * If yes you won't be able to use GWT2Chain
 * 
 * @author Vincent Buzzano <vincent.buzzano@gmail.com>
 *
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface GWT2ServiceAsync {

	/**
	 * True or false
	 * @return
	 */
    public boolean value() default true;
    
}
