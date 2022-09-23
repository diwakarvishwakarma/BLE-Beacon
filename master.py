import json
import math
import time
import numpy as np
import statistics as st
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
from matplotlib import animation as animation, pyplot as plt, cm

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
    
    x1, y1 = 0.0, 1.2
    x2, y2 = 0.5, 0.0
    x3, y3 = 0.9, 3.0

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
        cod = str(b1x) + "," + str(b1y)
        client.publish("incoming/data", cod)
        print("beacon1 : ", "(",round(b1x, 2),",",round(b1y, 2),")")
        d1.clear()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.199", 1883, 60)
client.loop_forever()

    # def trackLocation(x1, y1, r1, x2, y2, r2, x3, y3, r3):
    #     R = math.sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
    #     A = 0.5 * (x1 + x2)
    #     B = ((r1**2 - r2**2) * (x2 - x1)) / (2 * (R**2))
    #     C = 0.5 * math.sqrt((2 * ((r1**2 + r2**2)) / (R**2)) - (((r1**2 - r2**2)**2) / (R**4)) - 1) * (y2 - y1)
    #     D = 0.5 * (y1 + y2)
    #     E = ((r1**2 - r2**2) * (y2 - y1)) / (2 * (R**2))
    #     F = 0.5 * math.sqrt((2 * ((r1**2 + r2**2)) / (R**2)) - (((r1**2 - r2**2)**2) / (R**4)) - 1) * (x1 - x2)

    #     ix1 = A + B + C
    #     ix2 = A + B - C
    #     iy1 = D + E + F
    #     iy2 = D + E - F

    #     d1 = math.sqrt((ix1 - x3) ** 2 + (iy1 - y3) ** 2)
    #     d2 = math.sqrt((ix2 - x3) ** 2 + (iy2 - y3) ** 2)

    #     if ((d1 - r3) < (d2 - r3)):
    #         a, b = ix1, iy1
    #     else:
    #         a, b = ix2, iy2

    #     return a, b
 
# while len(d)<=3:
#     print("executed")
#     if incoming_topic=="Reader1/data":
#         d.insert(0,{"Reader=":incoming_topic,"Reader_MAC":data_mac,"Beacon_Distance":data_distance,"Beacon_ID":data_uuid})
#     elif incoming_topic=="Reader2/data":
#         d.insert(1,{"Reader=":incoming_topic,"Reader_MAC":data_mac,"Beacon_Distance":data_distance,"Beacon_ID":data_uuid})
#     elif incoming_topic=="Reader3/data":
#         d.insert(2,{"Reader=":incoming_topic,"Reader_MAC":data_mac,"Beacon_Distance":data_distance,"Beacon_ID":data_uuid})
#     else:
#         print("no topic found")
    #if (len(d2) <= 3):
        #if (data_mac == "c8:c9:a3:cb:bc:76"):
            #if (incoming_topic_copy3 != incoming_topic and incoming_topic_copy4 != incoming_topic):
               #d2.append(data_distance)
               #incoming_topic_copy4 = incoming_topic_copy3
               #incoming_topic_copy3 = incoming_topic

    #if (len(d2) == 3):

       #b2r1 = d2[0]
       #b2r2 = d2[1]
       #b2r3 = d2[2]
       #b2x, b2y = trackLocation(x1, y1, b2r1, x2, y2, b2r2, x3, y3, b2r3)
       #print("beacon2 : ",b2x, b2y)
       #d2.clear()

    #print(time.time() - start_time)
    #start_time = time.time()
    #if msg.topic=="Reader1/data":
    #d.insert(0,{"Reader=":msg.topic,"Reader_MAC":data_mac,"Beacon_Distance":data_distance,"Beacon_ID":data_uuid})
    #elif msg.topic=="Reader2/data":
    #    d.insert(1,{"Reader=":msg.topic,"Reader_MAC":data_mac,"Beacon_Distance":data_distance,"Beacon_ID":data_uuid})
    #elif msg.topic=="Reader3/data":
    #    d.insert(2,{"Reader=":msg.topic,"Reader_MAC":data_mac,"Beacon_Distance":data_distance,"Beacon_ID":data_uuid})
        # c1.append(round(b1x, 1))
        # c2.append(round(b1y, 1))

        # if (len(c1) == 10):
        #     x = st.mean(c1)
        #     y = st.mean(c2)
        #     print(x, y)
        #     c1.pop(0)
        #     c2.pop(0)

        # # a1, b1 = trackLocation(x1, y1, r1, x2, y2, r2, x3, y3, r3)
        # # a2, b2 = trackLocation(x3, y3, r3, x1, y1, r1, x2, y2, r2)
        # # a3, b3 = trackLocation(x2, y2, r2, x3, y3, r3, x1, y1, r1)
        # # print(((a1 + a2 + a3) / 3), ((b1 + b2 + b3) / 3))
        
