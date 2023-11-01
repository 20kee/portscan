from scapy.all import sr, IP, TCP
import argparse
import time
import socket


class scanner():
    def __init__(self, host_start, host_end):
        self.host_start = host_start
        self.host_end = host_end
        self.init_packet()
    
    def ip_range(self, start_ip, end_ip):
        start = list(map(int, start_ip.split(".")))
        end = list(map(int, end_ip.split(".")))
        temp = start
        ip_range = []
   
        ip_range.append(start_ip)
        while temp != end:
            start[3] += 1
            for i in (3, 2, 1):
                if temp[i] == 256:
                    temp[i] = 0
                    temp[i-1] += 1
            ip_range.append(".".join(map(str, temp)))    
     
        return ip_range
  
    
    def init_packet(self):
        if self.host_end != None:
            ip_range = self.ip_range(self.host_start, self.host_end)
            for ip in ip_range:
                packet = IP(dst=ip)
                packet /= TCP(dport=range(1, 1025), flags="S")            
                self.scan( packet, ip )
                time.sleep(1)
                
        else:
            packet = IP(dst=self.host_start)
            packet /= TCP(dport=range(1, 1025), flags="S")            
            self.scan( packet, self.host_start )
            time.sleep(1)
    

    def scan(self, packet, ip_address):
        answered, unanswered = sr(packet, timeout=1)
        res = {}

        #process unanswered packets
        for packet in unanswered:
            res[packet.dport] = "filtered"

        #processed answered packets
        for (send, recv) in answered:

            #got ICMP error message
            if recv.getlayer("ICMP"):

                type = recv.getlayer("ICMP").type
                code = recv.getlayer("ICMP").code

                #port unrecable
                if code == 3 and type == 3:
                    res[send.dport] = "Closed"
                else:
                    res[send.dport] = "Got ICMP with type " + str(type) + " and code " + str(code)

            else:

                flags = recv.getlayer("TCP").sprintf("%flags%")

                #Got SYN/ACK
                if flags == "SA":
                    res[send.dport] = "Open"
                #Got RST
                elif flags == "R" or flags == "RA":
                    res[send.dport] = "Closed"

                #Got something
                else:
                    res[send.dport] = "Got packets with flags " + str(flags)


        #Print res
        ports = list(res.keys())
        ports.sort()

        for port in ports:
            if 'filtered' not in res[port]:
                print ("[" + str(ip_address) + ":" + str(port) + "] " + res[port])


def main():
    url = ''
    ip = socket.gethostbyname(url) if url != '' else '3.142.251.166'

    s = scanner(ip, None)
    


if __name__ == "__main__":
    main()