#!/usr/bin/env python

"""
Configuration file for ISS (international space station) MQTT Sender.

This configuration configures the **pub-iss** MQTT sender. Intended use: configure
a Raspberry Pi to send data, via MQTT, to the Raspberry Valley IoT Device
(https://raspberry-valley.azurewebsites.net/IoT-Raspberry-Pi-Device/)

The configuration is also read by all MQTT publishers/subscribers to ISS data.

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied
"""

# Status codes
# ------------

iss_status_no_connection = 0
iss_status_error         = 1
iss_status_far_away      = 2
iss_status_coming_soon   = 3
iss_status_nearly_here   = 4
iss_status_overhead      = 5

# Broker Settings
# ---------------
# Configure the broker settings for **pub-iss**

broker = "localhost"
broker_port = 1883
broker_user = None
broker_pass = None

# Pub/Sub Topics for Broker
# -------------------------
# Configure MQTT broker topics for ISS countdown

iss_status_topic    = "iss/karlskrona/status"
iss_place_topic     = "iss/karlskrona/place"
iss_countdown_topic = "iss/karlskrona/countdown"

# Location Settings
# -----------------
# Configure location for countdown (used by publishers or stand-alone client code)

location_latitude  = 56.1612
location_longitude = 15.5869
location_name      = "Earth-Sweden-Karlskrona"

# RGB Led
# -------
# Configure pins for RGB LED. These are pin numbers (board mode). Used only by RGB Led modules

rgbled_red   = 16
rgbled_green = 18
rgbled_blue  = 22