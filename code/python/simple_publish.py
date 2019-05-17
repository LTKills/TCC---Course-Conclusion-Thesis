import paho.mqtt.client as mqtt


host = 'localhost'
port = 1883

client = mqtt.Client('simple_pub')

client.connect(host, port)
client.publish('ping_t', 'hello and goodbye in hawaii')
