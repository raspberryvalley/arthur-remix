#!/usr/bin/env python

"""
MQTT listener, which reacts to the ISS (international space station) countdown status.

This Python 3 code is one in a series of MQTT listeners, reacting to the ISS countdown components, 
implemented on different hardware (but using the same principle).

In this code, we use an RGB Led (common anode) to indicate the proximity of ISS by subscribing to the 
status value (see 'iss_overhead' documentation).

This code expects an MQTT server running and providing updates on selected topics (defined in 'config.py'). 
Further, a publisher of some kind has to be running as well, to feed the MQTT server with appropriate data.
The publisher provided in our project is 'pub-iss.py'. You can of course use your own. For your convenience,
we have also provided launcher code ('launcher.py'), to run multiple scripts of choice at once.

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied
"""

import config
import time
import logging
from sys import exit
import iss_rgb_led

try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This example requires the paho-mqtt module\nInstall with: sudo pip install paho-mqtt")

logger = logging.getLogger()

ProximityCode = 0

# read MQTT settings from 'config.py'

MQTT_SERVER = config.broker
MQTT_PORT = config.broker_port
MQTT_STATUS_TOPIC = config.iss_status_topic

MQTT_USER = config.broker_user
MQTT_PASS = config.broker_pass

#======================================================================
# MQTT broker code

def on_connect(client, userdata, flags, rc):
    """Called when script has successfully connected to the given MQTT Broker."""

    print("ISS RGB LED subscriber connected.")
    logging.info("ISS RGB LED subscriber connected with result code "+str(rc))
    client.subscribe(MQTT_STATUS_TOPIC)

def on_message(client, userdata, msg):
    """MQTT Callback function: message is available on the subscribed-to topic."""

    proximity = msg.payload.decode('UTF-8')
    topic = msg.topic
    logging.info("Received message [{}] on topic [{}]".format(proximity, topic))

    led_rgb.set_ISS_code(int(proximity))
    

#======================================================================
# Main Loop

try:
    client = mqtt.Client("sub-iss-rgb-led")
    client.on_connect = on_connect
    client.on_message = on_message

    if MQTT_USER is not None and MQTT_PASS is not None:
        client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

    client.connect(MQTT_SERVER, MQTT_PORT)
    client.loop_start()

    led_rgb = iss_rgb_led.iss_rgb_led(config.rgbled_red, config.rgbled_green, config.rgbled_blue)

    while True:
        pass

except KeyboardInterrupt:
    print ("Terminating ISS Listener for RGB Led")
finally:
    print ("ISS listener for RGB Led terminated")
    client.loop_stop()
