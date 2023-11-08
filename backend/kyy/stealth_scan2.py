from scapy.all import *
from multiprocessing import Pool

def scan(args):
    dst, port, flag_ = args
    # S(SYN), F(FIN), N(NULL), X(XMAS)
    if(flag_.upper() == 'S'):
        response = port_scan(dst, port, 'S')
        if(response and response.haslayer(TCP) and response[TCP].flags == 0x12):
            return {port}
        else:
            return None
        
    elif(flag_.upper() == 'F'):
        response = port_scan(dst, port, 'F')
        if(not response):
            return {port}
        else:
            return None
        
    elif(flag_.upper() == 'N'):
        response = port_scan(dst, port, '')
        if(not response):
            return {port}
        else:
            return None
        
    elif(flag_.upper() == 'X'):
        response = port_scan(dst, port, 'FPU')
        if(not response):
            return {port}
        else:
            return None
        
    else:
        return 'flag 값을 잘못 입력 했습니다. ex) S(SYN), F(FIN), N(NULL), X(XMAS)'
    

def port_scan(dst, port, flag_):
    ip = IP(dst=dst)
    src_port = RandShort()
    tcp = TCP(sport=src_port, dport=port, flags=flag_)

    packet = ip / tcp
    response = sr1(packet, timeout=0.2, verbose=0)  # 패킷 응답
    return response

if __name__ == '__main__':
    s = time.time()
    pool = Pool(processes=40)  # 사용할 프로세스 수 지정
    args = [('3.142.53.115', port, 'S') for port in range(1, 65536)]
    results = pool.map(scan, args)
    e = time.time() 
    
    for result in results:
        if(result):
            print(result)
    print(e - s)