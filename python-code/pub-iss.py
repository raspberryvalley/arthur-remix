#!/usr/bin/env python

"""
MQTT sender, which sends countdown information for ISS (international space station) until it is 
overhead.

This Python 3 code uses the **iss_overhead** class to forecast, when ISS is overhead, by providing
coordinates for a given location. See the **iss_overhead** documentation for more details.

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied
"""

import config
import time
import timetoISS
import logging

try:
    import paho.mqtt.client as paho
except ImportError:
    exit("This script requires the paho module\nInstall with: sudo pip install paho-mqtt")

logger = logging.getLogger()

print("ISS countdown publisher running. Location '{}' ({}, {})".format(config.location_name, config.location_longitude, config.location_latitude))
logging.info("Started ISS countdown publisher for Location '{}' ({}, {})".format(config.location_name, config.location_longitude, config.location_latitude))

#======================================================================
# MQTT broker code

# read MQTT settings from 'config.py'

MQTT_SERVER = config.broker
MQTT_PORT = config.broker_port

MQTT_USER = config.broker_user
MQTT_PASS = config.broker_pass

# initiate paho client

clientISS= paho.Client("pub-iss")
if MQTT_USER is not None and MQTT_PASS is not None:
    clientISS.username_pw_set(username=MQTT_USER, password=MQTT_PASS)
clientISS.connect(MQTT_SERVER, MQTT_PORT)

# publish iss topics

def pubISS():
    """ 
    Publish ISS data (status, time countdown) to MQTT broker.
    This function is called at timed intervals and reads the status 
    of the **iss_overhead** class instance.
    """
    
    status = iss.positionStatus()
    place = iss.place
    countdown = iss.stringCountdown()
    if status != None:
        logging.info("Publishing ISS data. Status [{}], Place [{}], Countdown [{}]".format(status, place, countdown))
        clientISS.publish(config.iss_status_topic, status)
        clientISS.publish(config.iss_place_topic, place)
        clientISS.publish(config.iss_countdown_topic, countdown)

#======================================================================
# Main Loop

try:
    # initiate the **iss_overhead** class
    iss = timetoISS.iss_overhead(config.location_latitude, config.location_longitude, config.location_name) 
    while True:
        pubISS()
        print("> " + iss.stringCountdown() + " [hours:minutes] to go!", end='\r')
        time.sleep(5)
except KeyboardInterrupt:
    print ("terminating ISS sender")
finally:
    print ("")
    print ("cleaning up")
