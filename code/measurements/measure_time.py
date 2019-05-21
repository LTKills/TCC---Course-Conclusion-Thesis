import paho.mqtt.client as mqtt
import time
from threading import Thread


def on_message(client, userdata, message):
    # print(message)
    print('Recver>> Received message')


def sender(host, port, payload):
    print('Sender>> Starting...')
    client = mqtt.Client('measure_sender')
    client.connect(host, port)
    print('Sender>> Connected')
    while True:
        time.sleep(1)
        client.publish('ping_t', payload)
        print('Sender>> Published ' + payload)


def recver(host, port):
    print('Recver>> Starting...')

    client = mqtt.Client('measure_recver')
    client.on_message = on_message
    client.connect(host, port)
    print('Recver>> Connected')
    client.subscribe('ping_t')
    print('Recver>> Subscribed')

    client.loop_start()
    time.sleep(100000)
    client.loop_stop()



if __name__ == '__main__':
    host = 'localhost'
    port = 1883
    payload = 'test'

    sender = Thread(target=sender, args=(host, port, payload))
    recver = Thread(target=recver, args=(host, port))
    sender.start()
    recver.start()

    while True:
        pass

    sender.stop()
    recver.stop()

