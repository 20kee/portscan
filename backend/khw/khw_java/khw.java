package khw_java;

public class khw{
    public static void main(String[] args){
        Thread run_task1 = new khw_run();
        run_task1.start();
        Thread run_task2 = new khw_run_2();
        run_task2.start();        
    }
}
