#기본적인 TCP 포트 스캔
 
import socket
import threading
import time
url = 'ec2-13-209-19-147.ap-northeast-2.compute.amazonaws.com'
ip = socket.gethostbyname(url)
# ip = "18.116.88.166"  #취약한 서버 IP 주소
ports = list(range(464, 466))

def scan(start_port, end_port):
    if end_port >= 65536:
        end_port = 65535
    for port in range(start_port, end_port+1):
        try:
            with socket.socket() as s:
                s.settimeout(2)
                s.connect((ip, port))
                s.send("Python Connect\n".encode())
                banner = s.recv(1024) 
                if banner:
                    print("[+] {} port is opened: {}\n".format(port, banner.decode()[:20]))
                        
        except Exception as e:
            if str(e) == "timed out":
                pass
            else:
                if 'Errno 61' in str(e):
                    pass
                else:
                    print(e, port)
 
def main():
    start_port = 1
    end_port = 65536
    task_number = 25
    threads = []
    start_time = time.time()
    for i in range(start_port, end_port, task_number):
        t = threading.Thread(target=scan, args=(i, i+task_number-1))
        t.start()
        threads.append(t)
    for thread in threads:
        thread.join()
    
    print(time.time()-start_time)
    
if __name__ == '__main__':
    main()

