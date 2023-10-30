import subprocess
import threading
import socket
from threading import Thread
i=0;

def work2():
    try:
        temp = i;
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) 
        result = sock.connect_ex(("121.153.24.76", temp))
        if result == 0:
            print(f"Port {temp} is open")
        sock.close()
    except Exception as e:
        print('d')
    return
threads = []
for i in range(0,30000):
    t = threading.Thread(target=work2)
    i=i+1
    t.start()
    threads.append(t)
for thread in threads:
    thread.join()