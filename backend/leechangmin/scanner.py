#기본적인 TCP 포트 스캔
from scapy.all import sr, IP, TCP
import time
import socket
import socket
import threading
import multiprocessing
import time
import json
import copy


class NormalScanner:
    def __init__(self):
        self._results = {}
        self._open_ports = []

    def half_open_scan(self, ip, start_port, end_port):
        packet = IP(dst=ip)
        packet /= TCP(dport=range(start_port, end_port), flags="S")
        answered, unanswered = sr(packet, timeout=1)

        for (send, recv) in answered:
            flags = recv.getlayer("TCP").sprintf("%flags%")
            if flags == "SA":
                self._open_ports.append(send.dport)

        return self._open_ports

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
            processes.append(multiprocessing.Process(target=self.scan_process, args=(ip, range(ports[i], ports[i+1]), result)))
            processes[i].start()
        for p in processes:
            p.join()
        
        return json.dumps(dict(result))
        
    
    def scan_process(self, ip, ports, result):
        task_number = len(ports) // 2500 + 1
        threads = []
        for i in range(ports[0], ports[-1], task_number):
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
    result = list()
    scanner = NormalScanner()
    open_ports = scanner.half_open_scan(ip, 1, 5000)
    print(open_ports)
    
if __name__ == '__main__':
    main()
