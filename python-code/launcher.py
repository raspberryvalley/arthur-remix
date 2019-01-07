#!/usr/bin/env python

"""
Arthur-Twist Launcher - launches all ISS code available.

The Python 3 code assumes your Pi has all hats we cover available and launches all processes
(MQTT Processes). A pre-requisite is the availability of an MQTT broker, Node-RED, Node-RED Dashboard. See 
our [Raspberry Pi IoT Device](https://raspberry-valley.azurewebsites.net/IoT-Raspberry-Pi-Device/) described
in detail (you can also download a Pi binary from this page)

!!! Please comment out the processes for hats you don't have plugged in !!!

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied

Inspiration: http://open-notify.org/Open-Notify-API/ISS-Location-Now/
Track ISS here (eesa): https://spotthestation.nasa.gov/tracking_map.cfm
Track ISS also here: https://www.n2yo.com/?s=28654
"""

import logging
import subprocess, time

logger = logging.getLogger()

try:
    logging.info("Starting ISS Launcher (CTRL-C to exit)")

    p1 = subprocess.Popen(['./pub-iss.py'])
    time.sleep(1)
    p2 = subprocess.Popen(['./sub-iss-blinkt.py'])
    p3 = subprocess.Popen(['./sub-iss-microdot.py'])

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    logging.info("Terminating ISS Launcher")

finally:
    p3.terminate()
    p2.terminate()
    p1.terminate()
