import asyncio

TARGET_IP = "3.142.251.166"
PORT_RANGE = (1, 65535)
CONCURRENT_TASKS = 5000
TIMEOUT = 0.5  # seconds

SERVICE_IDENTIFIERS = {
    21: ("FTP", "USER anonymous\r\n"),
    22: ("SSH", ""),
    23: ("Telnet", ""),
    25: ("SMTP", "EHLO localhost\r\n"),
    80: ("HTTP", "GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(TARGET_IP)),
    443: ("HTTPS", ""),
    # ... 추가할 서비스와 포트 번호
}

async def check_port(ip: str, port: int) -> (bool, str):
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, port), timeout=TIMEOUT)
        
        service_info = SERVICE_IDENTIFIERS.get(port)
        if service_info and service_info[1]:
            writer.write(service_info[1].encode())
            await writer.drain()

        banner = await asyncio.wait_for(reader.read(1024), timeout=TIMEOUT)
        writer.close()
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
                service = SERVICE_IDENTIFIERS.get(port, ("Unknown",))[0]
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
    result = asyncio.run(port_scanner(TARGET_IP, *PORT_RANGE))
    # 출력 생략
