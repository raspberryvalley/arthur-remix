#!/usr/bin/env python

"""
Runs the ISS overhead code in stand-alone mode, i.e. RGB Led only. Doesn't use MQTT publishers / subscribers, can be run
only as one script. For simple implementations, where the RGB Led is the only device connected (i.e. running in the Arthur
satellite dish model) 

Pin numbers of RGB Led connection and location configuration are stored and managed via the **config.py** configuration file.

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied
"""

import config
import time
import logging
import timetoISS
import iss_rgb_led

logger = logging.getLogger()

#======================================================================
# Main Loop

try:
    # initiate the **iss_overhead** class
    iss = timetoISS.iss_overhead(config.location_latitude, config.location_longitude, config.location_name)
    # initiate the **iss_rgb_led** class 
    blinker = iss_rgb_led.iss_rgb_led(config.rgbled_red, config.rgbled_green, config.rgbled_blue) 
    while True:
        status = iss.positionStatus()
        blinker.set_ISS_code(status)
        
        print("> " + iss.stringCountdown() + " [hours:minutes] to go!", end='\r')
        time.sleep(5)
except KeyboardInterrupt:
    print ("terminating ISS RGB Led")
finally:
    print ("")
    print ("cleaning up")
