


import testpaho.mqtt.client as mqtt
from time import sleep

host = 'localhost'
port = 1883


def on_publish(client, userdata, result):
    print('Done!')

client = mqtt.Client('no_pubrel')

client.on_publish = on_publish
client.connect(host, port)





client.loop_start()


ans = client.publish('topic', 'message', 2)
ans.wait_for_publish()



client.loop_stop()
client.disconnect()
