package play.modules.gwt2;

import java.util.ArrayList;
import java.util.List;

import javassist.CannotCompileException;
import javassist.CtClass;
import javassist.CtMethod;
import javassist.expr.ExprEditor;
import javassist.expr.MethodCall;

import org.apache.commons.javaflow.bytecode.transformation.asm.AsmClassTransformer;

import play.classloading.ApplicationClasses.ApplicationClass;
import play.classloading.enhancers.ControllersEnhancer;
import play.classloading.enhancers.Enhancer;

public class GWT2Enhancer extends Enhancer {

    static final List<String> continuationMethods = new ArrayList<String>();
    static {
        continuationMethods.add("play.modules.gwt2.GWT2Service.await(java.util.concurrent.Future,play.mvc.Http$Request)");
    }

    @Override
    public void enhanceThisClass(ApplicationClass applicationClass) throws Exception {
    	if (1==1)
    		return;
        CtClass ctClass = makeClass(applicationClass);
       
        if (!ctClass.subtypeOf(classPool.get(GWT2Service.class.getName()))) {
            return;
        }

        final boolean[] needsContinuations = new boolean[] {false};
        for(CtMethod m : ctClass.getDeclaredMethods()) {
            m.instrument(new ExprEditor() {

                @Override
                public void edit(MethodCall m) throws CannotCompileException {
                    try {
                        if(continuationMethods.contains(m.getMethod().getLongName())) {
                            needsContinuations[0] = true;
                        }
                    } catch(Exception e) {                        
                    }
                }

            });

            if(needsContinuations[0]) {
                break;
            }
        }

        if(!needsContinuations[0]) {
            return;
        }

        // Apply continuations
        applicationClass.enhancedByteCode = new AsmClassTransformer().transform(applicationClass.enhancedByteCode);

        ctClass.defrost();
    }

}
