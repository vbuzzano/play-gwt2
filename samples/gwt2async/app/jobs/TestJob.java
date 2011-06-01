package jobs;
import play.jobs.Job;


public class TestJob extends Job<String> {
	private String result = null;
	
	public String doJobWithResult() {
		doJob();
		return result;
	}
	
	public void doJob() {
		try {
			Thread.sleep(3000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		result = "JOBJOBJOBJOBJOJBJOBJOBJOJBJOBJOBJOBJOB";
		System.out.println(result);
    }
}
