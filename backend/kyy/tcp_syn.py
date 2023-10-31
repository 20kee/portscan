from scapy.all import *


def is_open(ip, port, re1, timeout=0.2):
    
    tcpRequest = IP(dst=ip)/ TCP(sport=RandShort(), dport=port, flags='S')
    tcpResponese = sr1(tcpRequest, timeout = timeout, verbose = 0)
    try:
        if tcpResponese.getlayer(TCP).flags == "SA":
            #print(tcpRequest.getlayer(TCP).dport)
            re1.append(tcpRequest.getlayer(TCP).dport)
            print(tcpResponese)
    except AttributeError:
        pass

def thread(ip, sp, ep):
    re1 = list()
    for i in range(sp, ep):
        thread_1 = threading.Thread(target=is_open, args=(ip, i, re1))
        thread_1.start()
    print(re1)
    
    
        

if __name__ == '__main__':
    ip="13.209.19.147"
    start = time.time()
    thread(ip,0,4000)
    end = time.time()
    print(end-start)