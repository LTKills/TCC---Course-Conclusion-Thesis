import paho.mqtt.client as mqtt
import time
from threading import Thread

curr_time = time.time()

def on_message(client, userdata, message):
    print(message)
    print(time.time() - curr_time)


def recver(host, port):
    print('Recver>> Starting...')

    client = mqtt.Client('garoto_maroto')
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

    recver(host, port)

