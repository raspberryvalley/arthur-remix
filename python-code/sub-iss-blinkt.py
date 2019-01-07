#!/usr/bin/env python

"""
MQTT listener, which reacts to the ISS (international space station) countdown status.

This Python 3 code is one in a series of MQTT listeners, reacting to the ISS countdown components, 
implemented on different hardware (but using the same principle).

In this code, we use the Pimoroni Blinkt! (https://shop.pimoroni.com/products/blinkt) device to 
indicate the proximity of ISS by subscribing to the status feed (see 'iss_overhead' documentation).
Basically, we have 6 statuses to react to, indicating either error or time away from our location

The indicator itself is a modification of the 'pulse.py' example from the Pimoroni library, with 
a different context. Make your own, and share with us using this template!

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
import colorsys
import time
import logging
from sys import exit

try:
    import numpy as np
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")

try:
    import paho.mqtt.client as mqtt
except ImportError:
    exit("This example requires the paho-mqtt module\nInstall with: sudo pip install paho-mqtt")

import blinkt

logger = logging.getLogger()

ProximityCode = config.iss_status_no_connection

blinkt.set_clear_on_exit()

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

    print("ISS Blinkt! subscriber connected")
    logging.info("ISS Blinkt! subscriber connected with result code "+str(rc))
    client.subscribe(MQTT_STATUS_TOPIC)

def on_message(client, userdata, msg):
    """MQTT Callback function: message is available on the subscribed-to topic."""

    global ProximityCode
    # print (msg.payload.decode('UTF-8'))
    # print (msg.topic)

    proximity = int(msg.payload.decode('UTF-8'))
    topic = msg.topic
    
    logging.info("Received message [{}] on topic [{}]".format(proximity, topic))

    ProximityCode = proximity

#======================================================================
# Blinkt! code

def make_gaussian(fwhm):
    x = np.arange(0, blinkt.NUM_PIXELS, 1, float)
    y = x[:, np.newaxis]
    x0, y0 = 3.5, 3.5
    fwhm = fwhm
    gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
    return gauss

#======================================================================
# Main Loop

try:
    client = mqtt.Client("sub-iss-blinkt")
    client.on_connect = on_connect
    client.on_message = on_message

    if MQTT_USER is not None and MQTT_PASS is not None:
        client.username_pw_set(username=MQTT_USER, password=MQTT_PASS)

    client.connect(MQTT_SERVER, MQTT_PORT)
    client.loop_start()

    while True:
        for z in list(range(1, 10)[::-1]) + list(range(1, 10)):
            fwhm = 5.0/z
            gauss = make_gaussian(fwhm)
            start = time.time()
            y = 4
            for x in range(blinkt.NUM_PIXELS):
                # h = 0.5 cyan
                # h = 1.0 red
                # h = 0.1 yellow
                # h = 0.3 green
                # h = 0.65 blue
                if ProximityCode == config.iss_status_no_connection:
                    h = 1.0
                elif ProximityCode == config.iss_status_error:
                    h = 1.0
                elif ProximityCode == config.iss_status_far_away:
                    h = 0.65
                elif ProximityCode == config.iss_status_coming_soon:
                    h = 0.5
                elif ProximityCode == config.iss_status_nearly_here: 
                    h = 0.1
                else:  # we are overhead JUST NOW!
                    h = 1.0
                
                s = 1.0
                v = gauss[x, y]
                rgb = colorsys.hsv_to_rgb(h, s, v)
                r, g, b = [int(255.0 * i) for i in rgb]
                blinkt.set_pixel(x, r, g, b)
            blinkt.show()
            end = time.time()
            t = end - start
            if t < 0.04:
                time.sleep(0.04 - t)

except KeyboardInterrupt:
    print ("Terminating ISS Listener for Blinkt!")
finally:
    print ("ISS listener for Blinkt! terminated")
    client.loop_stop()
