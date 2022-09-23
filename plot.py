import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("incoming/data")

def on_message(client, userdata, msg):
    print(msg.topic)
    print(msg.payload)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.199", 1883, 60)