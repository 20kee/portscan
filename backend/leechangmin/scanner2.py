#기본적인 TCP 포트 스캔
 
import socket
import threading
import multiprocessing
import time
import json


class NormalScanner:
    def __init__(self):
        self._results = {}

    def scan(self, ip, start_port, end_port, fast=True):
        processes = []
        ports = [start_port]
        if fast == True:
            process_number = 8
            for i in range(1, process_number):
                ports.append((end_port-start_port)*i//process_number)
            ports.append(end_port+1)
            
            for i in range(process_number):
                processes.append(multiprocessing.Process(target=self.scan_process, args=(ip, ports[i], ports[i+1]-1)))
                processes[i].start()
            for p in processes:
                p.join()
                
            return json.dumps(self._results)
        else:
            process_number = 1
            for i in range(1, process_number):
                ports.append((end_port-start_port)*i//process_number)
            ports.append(end_port+1)
            
            for i in range(process_number):
                processes.append(multiprocessing.Process(target=self.scan_process, args=(ip, ports[i], ports[i+1]-1)))
                processes[i].start()
            for p in processes:
                p.join()
                
            return json.dumps(self._results)
        
    
    def scan_process(self, ip, start_port, end_port):
        port_count = end_port - start_port + 1 
        task_number = port_count // 2500 + 1
        threads = []
        for i in range(start_port, end_port, task_number):
            t = threading.Thread(target=self.work, args=(ip, i, i+task_number-1))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
        

    def work(self, ip, start_port, end_port):
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
                        print(str(port), [banner.decode().split('\n')[0].rstrip('\r'), banner.decode()])
                        
                            
            except Exception as e:
                if str(e) == "timed out":
                    pass
                else:
                    if 'Errno 61' in str(e):
                        pass
                    else:
                        # print(e, port)
                        pass
 
def main():
    ip = socket.gethostbyname('ec2-13-209-65-115.ap-northeast-2.compute.amazonaws.com')
    ip = '3.142.251.166'
    scanner = NormalScanner()
    # print('========== Slow Version ==========')
    # start_time = time.time()
    # results = scanner.scan(ip, 1, 65535, fast=False)
    # print('Execution Time :', time.time() - start_time)


    print('========== Fast Version ==========')
    start_time = time.time()
    results = scanner.scan(ip, 1, 65535, fast=True)
    print('Execution Time :', time.time() - start_time)
    
if __name__ == '__main__':
    main()

