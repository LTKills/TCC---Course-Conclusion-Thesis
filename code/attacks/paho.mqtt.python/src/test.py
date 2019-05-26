




import testpaho.mqtt.client as mqtt


client = mqtt.Client('testpaho_client')


client.connect('localhost', 1883)

print(client.publish('asd', 'asd', qos=2))


