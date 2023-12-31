 
# some imports
import socket, sys
from struct import *
import random


def checksum(msg):
    s = 0
    # loop taking 2 characters at a time
    for i in range(0, len(msg), 2):
        w = ((msg[i]) << 8) + ((msg[i+1]) )
        s = s + w
     
    s = (s>>16) + (s & 0xffff);

    #complement and mask to 4 byte short
    s = ~s & 0xffff
     
    return s
 
#create a raw socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
except socket.error as msg:
    print ('Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()
 

s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
     
# now start constructing the packet
packet = '';
 
source_ip = '115.21.152.84'
dest_ip = '13.209.19.147' # or socket.gethostbyname('www.google.com')
 
# ip header fields
ihl = 5
version = 4
tos = 0
tot_len = 20 + 20  
id = 54321  
frag_off = 0
ttl = 255
protocol = socket.IPPROTO_TCP
check = 10  
saddr = socket.inet_aton ( source_ip ) 
daddr = socket.inet_aton ( dest_ip )
 
ihl_version = (version << 4) + ihl
 
ip_header = pack('!BBHHHBBH4s4s' , ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)
 
# tcp header fields
source = random.randint(1024, 60000)   # source port
dest = 80   
seq = 0
ack_seq = 0
doff = 5    
#tcp flags
fin = 0
syn = 1
rst = 0
psh = 0
ack = 0
urg = 0
window = socket.htons (5840)    
urg_ptr = 0
 
offset_res = (doff << 4) + 0
tcp_flags = fin + (syn << 1) + (rst << 2) + (psh <<3) + (ack << 4) + (urg << 5)
 
tcp_header = pack('!HHLLBBHHH' , source, dest, seq, ack_seq, offset_res, tcp_flags,  window, check, urg_ptr)
 
source_address = socket.inet_aton( source_ip )
dest_address = socket.inet_aton(dest_ip)
placeholder = 0
protocol = socket.IPPROTO_TCP
tcp_length = len(tcp_header)
 
psh = pack('!4s4sBBH' , source_address , dest_address , placeholder , protocol , tcp_length);
psh = psh + tcp_header;
 
tcp_checksum = checksum(psh)
 
tcp_header = pack('!HHLLBBHHH' , source, dest, seq, ack_seq, offset_res, tcp_flags,  window, tcp_checksum , urg_ptr)
 
packet = ip_header + tcp_header
 
s.sendto(packet, (dest_ip , 0 ))