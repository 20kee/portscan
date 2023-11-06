#기본적인 TCP 포트 스캔
 
import socket
import threading
import multiprocessing
import time
import json
import copy


class NormalScanner:
    def __init__(self):
        self._results = {}
        self._send_messages = dict()
        self._send_messages[80] = "GET / HTTP/1.1\r\n\r\n"

    def scan(self, ip, start_port, end_port, fast=True):
        manager = multiprocessing.Manager()
        processes = []
        ports = [start_port]
        if fast == True:
            process_number = 4
        else:
            process_number = 1
        
        if end_port - start_port  < 100:
            process_number = 1
    
        for i in range(1, process_number):
            ports.append((end_port-start_port)*i//process_number)
        ports.append(end_port+1)
        result = manager.dict()
        
        for i in range(process_number):
            processes.append(multiprocessing.Process(target=self.scan_process, args=(ip, ports[i], ports[i+1]-1, result)))
            processes[i].start()
        for p in processes:
            p.join()
        
        return json.dumps(dict(result))
        
    
    def scan_process(self, ip, start_port, end_port, result):
        port_count = end_port - start_port + 1 
        task_number = port_count // 2500 + 1
        threads = []
        for i in range(start_port, end_port, task_number):
            t = threading.Thread(target=self.work, args=(ip, i, i+task_number-1, result))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()
        

    def work(self, ip, start_port, end_port, result):
        if end_port >= 65536:
            end_port = 65535
        for port in range(start_port, end_port+1):
            try:
                with socket.socket() as s:
                    s.settimeout(3)
                    s.connect((ip, port))
                    s.send("Python Connect\n".encode())
                    banner = s.recv(1024) 
                    if banner:
                        result[str(port)] = [banner.decode().split('\n')[0].rstrip('\r'), banner.decode()]
                        
                            
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
    url = 'github.com'
    ip = socket.gethostbyname(url) if url != '' else '142.250.31.105'
    scanner = NormalScanner()

    print('========== Fast Version ==========')
    start_time = time.time()
    print(scanner.scan(ip, 1, 5000))
    print('Execution Time :', time.time() - start_time)
    
if __name__ == '__main__':
    main()
