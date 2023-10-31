import threading
import socket
import time


def port_s(count):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) 
        result = sock.connect_ex(("ec2-13-209-19-147.ap-northeast-2.compute.amazonaws.com", count))
        if result == 0:
            print(f"Port {count} is open")
        sock.close()
    except Exception as e:
        print(e)
    return

def thread(min_p,max_p):
    for i in range(min_p,max_p):
        thread_1 = threading.Thread(target=port_s,args=(i,))
        thread_1.start()

if __name__ == '__main__':
    start = time.time()
    thread(0,65536)
    end = time.time()

print(end-start)