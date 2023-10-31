package khw_java;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;

public class khw_run extends Thread {
    @Override
    public void run(){
        String ipAddress = "ec2-13-209-65-115.ap-northeast-2.compute.amazonaws.com";
        int timeout = 1000;
        for (int port = 0; port <= 10000; port++){
            try{
                Socket socket = new Socket();
                socket.connect(new InetSocketAddress(ipAddress,port),timeout);
                socket.close();
                System.out.println("Port"+port+"is open");
            }catch (IOException ex){
            }
        }
    }
}
