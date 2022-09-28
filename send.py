import time
from beacontools import BeaconScanner, IBeaconFilter, IBeaconAdvertisement
import statistics as st
import json
import paho.mqtt.client as mqtt

mac_id = set()
dict_1 = dict()
dict_2 = dict()
mean_value = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("192.168.0.199", 1883, 60)

def callback(bt_addr, rssi, packet, additional_info):
    global mean_value
    value = str(packet)
    mac_id.add(bt_addr)
    rssi = rssi
    a = -55
    n = 3
    d = 10 ** ((a - rssi) / (10 * n))
    if bt_addr in mac_id:
        if bt_addr == "0c:43:14:f0:2d:3e":
            dict_1.setdefault(bt_addr, []).append(d)
            if (len(dict_1[bt_addr]) == 20):
                mean_value = st.mean(dict_1[bt_addr])
                dict_2[bt_addr] = mean_value
                data =json.dumps(dict_2)
                print(data)
                client.publish("Reader1/data", data)
                dict_1[bt_addr].pop(0)
scanner = BeaconScanner(callback,packet_filter = IBeaconAdvertisement)
scanner.start()
client.loop_forever()
