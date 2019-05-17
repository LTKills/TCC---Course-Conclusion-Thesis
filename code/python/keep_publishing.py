import paho.mqtt.client as mqtt
from time import sleep
import sys


host = 'localhost'
port = 1883


client = mqtt.Client('garoto_maroto')
client.connect(host, port)

i = 0
while True:
    i += 1
    #sleep(1)
    client.publish('ping_t', str(i) + ' yello and goodbye in hawaii')
