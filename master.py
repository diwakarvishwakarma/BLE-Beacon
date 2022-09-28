import json, math, time
import numpy as np
import statistics as st
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

d1 = []

incoming_topic_copy1 = "Reader3/data"
incoming_topic_copy2 = "Reader2/data"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Reader1/data")
    client.subscribe("Reader2/data")
    client.subscribe("Reader3/data")

def on_message(client, userdata, msg):
    global incoming_topic_copy1
    global incoming_topic_copy2
    global d1

    incoming_topic = msg.topic
    value = msg.payload.decode('utf-8')
    reading = json.loads(value)

    def trackLocation(x1, y1, r1, x2, y2, r2, x3, y3, r3):
       A = 2*x2 - 2*x1
       B = 2*y2 - 2*y1
       C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
       D = 2*x3 - 2*x2
       E = 2*y3 - 2*y2
       F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
       x = (C*E - F*B) / (E*A - B*D)
       y = (C*D - A*F) / (B*D - A*E)
       return x, y

    #x1, y1 = -3.58, 5.58
    x2, y2 = 3.58, 5.58
    x3, y3 = 3.58, -5.58
    x1, y1 = -3.58, -5.58

    if (len(d1) <= 3):
        if (incoming_topic_copy1 != incoming_topic and incoming_topic_copy2 != incoming_topic):
            d1.append(reading["0c:43:14:f0:2d:3e"])
            incoming_topic_copy2 = incoming_topic_copy1
            incoming_topic_copy1 = incoming_topic

    if (len(d1) == 3):
        b1r1 = d1[0]
        b1r2 = d1[1]
        b1r3 = d1[2]
        b1x, b1y = trackLocation(x1, y1, b1r1, x2, y2, b1r2, x3, y3, b1r3)
        print(b1x, b1y)
        cod = str(b1x) + "," + str(b1y)
        client.publish("incoming/data", cod)
        d1.clear()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.199", 1883, 60)
client.loop_forever()
