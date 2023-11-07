from scapy.all import sr, IP, TCP
import argparse
import time
import socket


class scanner():
    def __init__(self, ip):
        self.ip = ip
        self.init_packet()
  
    
    def init_packet(self):
        packet = IP(dst=self.ip)
        packet /= TCP(dport=range(1, 1025), flags="S")            
        self.scan( packet, self.ip )
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
                    print(res[send.dport])

        #Print res
        ports = list(res.keys())
        ports.sort()

        for port in ports:
            if 'filtered' not in res[port]:
                print ("[" + str(ip_address) + ":" + str(port) + "] " + res[port])


def main():
    url = ''
    ip = socket.gethostbyname(url) if url != '' else '13.58.152.115'

    s = scanner(ip)
    


if __name__ == "__main__":
    main()