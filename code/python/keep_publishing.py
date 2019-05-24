import paho.mqtt.client as mqtt
from time import sleep
from threading import Thread
import sys


def on_publish(client, userdata, result):
    # print('data published')
    pass


def flood(nthread, msg=""):
    i = 0
    partial_msg = 'Thread ' + str(nthread) + ': ' + msg + ' '
    while True:
        sleep(1)
        i += 1
        errno, _ = client.publish('flood_t', partial_msg + str(i), 2)
        print(partial_msg, i)
        # print(mqtt.error_string(errno))


if __name__ == '__main__':
    host = 'localhost'
    port = 1883
    nthreads = 8

    threads = []
    clients = []
    for i in range(nthreads):
        client.append(mqtt.Client('keep_pub'))
        client.connect(host, port)
        client.on_publish = on_publish

        threads.append(Thread(target=flood, args=(i, "hello")))
        threads[i].start()


