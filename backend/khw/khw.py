import asyncio
import time
TARGET_IP = "3.142.251.166"
PORT_RANGE = (1, 65535)
CONCURRENT_TASKS = 5000
TIMEOUT = 0.5  # seconds
BUFFER_SIZE = 1024

SERVICE_IDENTIFIERS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    80: "HTTP",
    443: "HTTPS",
    # ... 추가할 서비스와 포트 번호
}

async def check_port(ip: str, port: int) -> (bool, str):
    conn = asyncio.open_connection(ip, port)
    try:
        reader, writer = await asyncio.wait_for(conn, timeout=TIMEOUT)
        banner = await reader.read(BUFFER_SIZE)
        writer.close()
        await writer.wait_closed()
        return True, banner.decode(errors='replace').strip()
    except:
        return False, ""

async def port_scanner(ip: str, start_port: int, end_port: int):
    open_ports = {}
    tasks = []

    async def process_ports():
        results = await asyncio.gather(*tasks)
        for port, (is_open, banner) in zip(range(start_port, end_port + 1), results):
            if is_open:
                service = SERVICE_IDENTIFIERS.get(port, "Unknown")
                open_ports[port] = {"service": service, "banner": banner}

    for current_port in range(start_port, end_port + 1):
        if len(tasks) >= CONCURRENT_TASKS:
            await process_ports()
            tasks = []

        tasks.append(check_port(ip, current_port))

    if tasks:
        await process_ports()

    return open_ports

if __name__ == "__main__":
    start = time.time()
    result = asyncio.run(port_scanner(TARGET_IP, *PORT_RANGE))
    for port, data in result.items():
        print(f"Port: {port}, Service: {data['service']}, Banner: {data['banner']}")
    print(time.time()- start)