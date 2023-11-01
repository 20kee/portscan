from scapy.all import *
import socket


def scan(dst, port, flag_):
    #S(SYN), F(FIN), N(NULL), X(XMAS)
    if(flag_.upper() == 'S'):
        response = port_scan(dst, port, 'S')
        if(response[TCP].flags == 0x12):
            return f'{str(response).split(' ')[3]} is open'
        else:
            return f'{dst}:{port} is close'
        
    elif(flag_.upper() == 'F'):
        response = port_scan(dst, port, 'F')
        if(not response):
            return f'{dst}:{port} is open'
        else:
            return f'{dst}:{port} is close'
        
    elif(flag_.upper() == 'N'):
        response = port_scan(dst, port, '')
        if(not response):
            return f'{dst}:{port} is open'
        else:
            return f'{dst}:{port} is close'
        
    elif(flag_.upper() == 'X'):
        response = port_scan(dst, port, 'FPU')
        if(not response):
            return f'{dst}:{port} is open'
        else:
            return f'{dst}:{port} is close'
        
    else:
        return 'flag 값을 잘못 입력 했습니다. ex) S(SYN), F(FIN), N(NULL), X(XMAS)'
    

def port_scan(dst, port, flag_):
        ip = IP(dst = dst)
        src_port = RandShort()
        tcp = TCP(sport = src_port, dport = port, flags=flag_)

        packet = ip /tcp
        response = sr1(packet, timeout=1, verbose = 0)          #패킷 응답
        print(response)
        return response
        
if __name__ == '__main__':
    #'13.209.19.147'
    #flag = 'A'
    #print(scan('13.209.19.147', 70, flag))
    print(scan('115.21.152.84', 80, 'S'))
'''
    ip = IP(dst = '115.21.152.84')
    src_port = RandShort()
    tcp = TCP(sport = src_port, dport = 50, flags='FA')
    packet = ip /tcp
    response = sr1(packet, timeout=1, verbose = 0)          #패킷 응답        
    print(response)
'''