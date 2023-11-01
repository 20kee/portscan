from scapy.all import *
import socket


def scan(dst, port, flag):
    try:
        src_port = RandShort()    
        ip = IP(dst=dst)
        tcp = TCP(sport = src_port, dport = port, flags=flag.upper())

        packet = ip /tcp
        response = sr1(packet, timeout=1, verbose = 0)

        if response is not None :
            if response.haslayer(TCP):
                if response[TCP].flags == 0x12:     # syn, ack 로 답 오기 떄문에 0x12
                    print(response)
                elif response[TCP].flags == 0x14:   # rst, ack 로 답오기 떄문
                    print(f'{port} port is close')
        elif flag.upper().find('F') != -1:          # fin, xmas 스캔 일경우 모두 FIN flag를 사룡함
            print(f'{port} port is open')
        elif not flag :                             # null scan
            print(f'{port} port is open')
    except ValueError :
        print('flag 값을 잘못 입력 했습니다. ex) S(SYN), A(ACK), F(FIN), R(RST), P(PSH), U(URG)')


if __name__ == '__main__':
    #'13.209.19.147'
    scan('13.209.19.147', 2, 'f')