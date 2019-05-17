import paho.mqtt.client as mqtt
import time


"""
callback function 'on_message'
called when client receives a message
"""

def on_message(client, userdata, message):
    print(message)


host = 'localhost'
port = 1883

client = mqtt.Client('garoto_maroto')
client.on_message = on_message

client.connect(host, port)
client.subscribe('ping_t')

client.loop_start()
time.sleep(100)
client.loop_stop()
