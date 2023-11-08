from scapy.all import IP,TCP,sr,sr1

def syn_scan(target, port_range):
    for port in port_range:
        pkt = IP(dst=target)/TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=2, verbose=0)
        if resp is None:
            print(f"Port {port} is filtered (no response).")
        elif resp.haslayer(TCP):
            if resp.getlayer(TCP).flags == 0x12:
                send_rst = sr(IP(dst=target)/TCP(dport=port, flags="R"), timeout=1, verbose=0)
                print(f"Port {port} is open.")
            elif resp.getlayer(TCP).flags == 0x14:
                print(f"Port {port} is closed.")
        else:
            print(f"Port {port} is filtered (received non-TCP response).")

if __name__ == "__main__":
    target_ip = input("Enter target IP: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    port_range = range(start_port, end_port + 1)
    syn_scan(target_ip, port_range)
