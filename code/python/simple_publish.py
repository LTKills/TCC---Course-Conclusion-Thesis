import paho.mqtt.client as mqtt


host = 'localhost'
port = 1883

client = mqtt.Client('garoto_maroto')

client.connect(host, port)
client.publish('aloha', 'hello and goodbye in hawaii')
