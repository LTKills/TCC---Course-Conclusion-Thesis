from scapy.all import send, IP, TCP
from scapy.contrib.mqtt import *
import sys


ip_tcp_pkt = IP(dst='localhost')/TCP(dport=1883)

send(ip_tcp_pkt/MQTT())

