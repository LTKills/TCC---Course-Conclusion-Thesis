import paho.mqtt.client as mqtt
from time import sleep
from threading import Thread
import sys


def on_publish(client, userdata, result):
    # print('data published')
    pass


def flood(nthread, msg=""):
    i = 0
    while True:
        i += 1
        complete_msg = 'Thread ' + str(nthread) + ':' + str(i) + ' ' + msg
        errno, _ = client.publish('flood_t', complete_msg, 2)
        print(complete_msg)
        # print(mqtt.error_string(errno))


if __name__ == '__main__':
    host = 'localhost'
    port = 1883
    nthreads = 8

    client = mqtt.Client('keep_pub')
    client.connect(host, port)
    client.on_publish = on_publish

    threads = []
    for i in range(nthreads):
        threads.append(Thread(target=flood, args=(i, "hello")))
        threads[i].start()


