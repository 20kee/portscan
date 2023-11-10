#기본적인 TCP 포트 스캔
from scapy.all import sr, IP, TCP
import socket
import threading
import multiprocessing
import json

class NormalScanner:
    def __init__(self):
        self._results = {}
        self._half_results = {}
        self._send_msg = {
                80 : b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n',     # HTTP 
                443 : b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n',    # SSL
                21 : b'USER anonymous\r\n',                              # FTP
                25 : b'EHLO example.com\r\n',                            # SMTP
                110 : b'USER test\r\n',                                  # POP3
                143 : b'a1 LOGIN user password\r\n',                     # IMAP
                161 : b'',                                               # SNMP
                389 : b'ldapsearch -x -h example.com -s base "(objectclass=)"',  #LDAP
                1433 : b'',#SQL Server
                1521 : b'(CONNECT_DATA=(COMMAND=version))',#Oracle DB 
                123: b'',#NTP (123)
                5060: b'OPTIONS sip:nouser@example.com SIP/2.0\r\n',#SIP (5060)
                9200 : b'GET /Redis (6379)INFO\r\nMongoDB (27017){ "ismaster": 1 }',#Elasticsearch (9200)
                53: b'', #DNS (53)
                111: b'No specific message; an RPC call is needed to grab a banner.', #RPCbind (111)
                2049: b'No specific message; an NFS call is needed to grab a banner.', #NFS (2049)
                5222: b"<stream:stream to='example.com' xmlns:stream='http://etherx.jabber.org/streams' version='1.0'>",#XMPP (5222)
                6667: b'NICK guest\r\nUSER guest 0 :guest\r\n'#IRC (6667)
            }
        self._check_banner = {
            22 : 'SSH',
            25 : 'ESMTP',
            80 : 'HTTP',
            110 : 'Dovecot',
            143 : 'IMAPrev1',
            443 : 'HTTP'
        }

    def half_open_scan(self, ip, start_port, end_port):
        packet = IP(dst=ip)
        packet /= TCP(dport=range(start_port, end_port), flags="S")
        answered, unanswered = sr(packet, timeout=5, verbose=0)

        for (send, recv) in answered:
            flags = recv.getlayer("TCP").sprintf("%flags%")
            if flags == "SA":
                self._half_results[send.dport] = 'open'

        return json.dumps(self._half_results)

    def scan(self, ip, start_port, end_port, fast=True):
        manager = multiprocessing.Manager()
        processes = []
        ports = [start_port]
        if fast == True:
            process_number = 6
        else:
            process_number = 1
        
        if end_port - start_port  < 100:
            process_number = 1
    
        for i in range(1, process_number):
            ports.append(start_port+(end_port-start_port)*i//process_number)
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
                    s.settimeout(8)
                    s.connect((ip, port))
                    s.send(self._send_msg[port] if port in self._send_msg.keys() else "Python Connect\n".encode())
                    banner = s.recv(4096)
                    if banner:
                        try:
                            resp_msg = banner.decode()
                            if port in self._check_banner.keys():
                                if self._check_banner[port] in resp_msg:
                                    result[str(port)] = [resp_msg.split('\n')[0].rstrip('\r') + ' True', resp_msg]
                                else:
                                    result[str(port)] = [resp_msg.split('\n')[0].rstrip('\r') + ' hmm..', resp_msg]
                            else:
                                result[str(port)] = [resp_msg.split('\n')[0].rstrip('\r') + ' False', resp_msg]
                        except:
                            resp_msg = banner
                            result[str(port)] = [str(resp_msg) + ' hmm..', str(resp_msg)]
                        
                
            except Exception as e:
                pass
 
if __name__ == '__main__':
    scanner = NormalScanner()
    scanner.scan('115.21.152.84', 1, 65535)
