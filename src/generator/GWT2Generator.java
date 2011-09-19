package generator;

import com.google.gwt.core.ext.BadPropertyValueException;
import com.google.gwt.core.ext.Generator;
import com.google.gwt.core.ext.GeneratorContext;
import com.google.gwt.core.ext.PropertyOracle;
import com.google.gwt.core.ext.TreeLogger;
import com.google.gwt.core.ext.UnableToCompleteException;
import com.google.gwt.core.ext.typeinfo.TypeOracle;

public class GWT2Generator extends Generator {

	  /**
	   * The class loader used to get resources.
	   */
	  private ClassLoader classLoader = null;

	  /**
	   * The generator context.
	   */
	  private GeneratorContext context = null;

	  /**
	   * The {@link TreeLogger} used to log messages.
	   */
	  private TreeLogger logger = null;
	  
	@Override
	public String generate(TreeLogger logger, GeneratorContext context,
			String typeName) throws UnableToCompleteException {
		
	    this.logger = logger;
	    this.context = context;
	    this.classLoader = Thread.currentThread().getContextClassLoader();

	    System.out.println("-----------------");
	    System.out.println(typeName);
        TypeOracle typeOracle = context.getTypeOracle();
        System.out.println("classType " + typeOracle.findType(typeName));

        PropertyOracle propertyOracle = context.getPropertyOracle();
        try {
            System.out.println("user.agent " + propertyOracle.getPropertyValue(logger, "user.agent"));
        } catch (BadPropertyValueException e) {
            System.out.println("No user.agent property");
        }
		return null;
	}

}
