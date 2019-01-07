#!/usr/bin/env python

"""
MQTT listener, which reacts to the ISS (international space station) countdown status.

This Python 3 code is one in a series of MQTT listeners, reacting to the ISS countdown components, 
implemented on different hardware (but using the same principle).

In this code, we use the Pimoroni Micro dot pHat (https://shop.pimoroni.com/products/microdot-phat) device to 
indicate the proximity of ISS by subscribing to the timeout value (see 'iss_overhead' documentation).

This code expects an MQTT server running and providing updates on selected topics (defined in 'config.py'). 
Further, a publisher of some kind has to be running as well, to feed the MQTT server with appropriate data.
The publisher provided in our project is 'pub-iss.py'. You can of course use your own. For your convenience,
we have also provided launcher code ('launcher.py'), to run multiple scripts of choice at once.

Learn more about using the Micro dot pHat by visiting 
the tutorial: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-micro-dot-phat

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied
"""

import config
import time
import logging
from sys import exit

try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This example requires the paho-mqtt module\nInstall with: sudo pip install paho-mqtt")

from microdotphat import write_string, clear, show

logger = logging.getLogger()

# read MQTT settings from 'config.py'

MQTT_SERVER = config.broker
MQTT_PORT = config.broker_port
MQTT_COUNTDOWN_TOPIC = config.iss_countdown_topic

MQTT_USER = config.broker_user
MQTT_PASS = config.broker_pass

#======================================================================
# MQTT broker code

def on_connect(client, userdata, flags, rc):
    """Called when script has successfully connected to the given MQTT Broker."""

    print("Displaying Time to ISS for location [{}], as 'HH:MM' to ISS Overhead".format(config.location_name))
    logging.info("ISS Micro dot pHat subscriber connected with result code "+str(rc))
    client.subscribe(MQTT_COUNTDOWN_TOPIC)

def on_message(client, userdata, msg):
    """MQTT Callback function: message is available on the subscribed-to topic."""

    # print (msg.payload.decode('UTF-8'))
    # print (msg.topic)

    countdown = msg.payload.decode('UTF-8')
    topic = msg.topic
    logging.info("Received message [{}] on topic [{}]".format(countdown, topic))

    clear()
    write_string(countdown, kerning=False)
    show()

#======================================================================
# Microdot pHat code

#======================================================================
# Main Loop

try:
    client = mqtt.Client("sub-iss-microdot")
    client.on_connect = on_connect
    client.on_message = on_message

    if MQTT_USER is not None and MQTT_PASS is not None:
        client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

    client.connect(MQTT_SERVER, MQTT_PORT)
    client.loop_start()

    while True:
        pass

except KeyboardInterrupt:
    print ("Terminating ISS Listener for Micro dot pHat")
finally:
    print ("ISS listener for Micro dot pHat terminated")
    client.loop_stop()
