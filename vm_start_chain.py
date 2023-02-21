"""EE 250L Lab 04 Starter Code
Run vm_sub.py in a separate terminal on your VM."""

from multiprocessing.sharedctypes import Value
import time
import paho.mqtt.client as mqtt



"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    time.sleep(2)
    client.subscribe("barring/pong") 
    client.message_callback_add("barring/pong", pong_func)
    client.publish("barring/ping", 3) 
def on_message(client, userdata, msg):
    print("Default callback - topic: " + msg.topic + "   msg: " + str(msg.payload, "utf-8"))

def pong_func(client, userdata, message): 
   print("Custom callback - Pong: " + (message.payload.decode()))
   next_step = int(message.payload.decode()) + 1
   time.sleep(2)
   client.publish("barring/ping", f"{next_step}") 
   print("Publishing ping value")

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="172.20.10.9", port=1883, keepalive=60) 
    time.sleep(2)
    client.loop_forever()
