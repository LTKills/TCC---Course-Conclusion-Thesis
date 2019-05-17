import paho.mqtt.client as mqtt
from time import sleep
import sys


def on_publish(client, userdata, result):
    print('data published')


host = 'localhost'
port = 1883


client = mqtt.Client('keep_pub')
client.connect(host, port)
client.on_publish = on_publish

i = 0
while True:
    i += 1
    sleep(1)
    errno, _ = client.publish('ping_t', str(i) + ' yello and goodbye in hawaii')
    print(mqtt.error_string(errno))
