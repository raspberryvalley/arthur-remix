#!/usr/bin/env python

"""
Common anode RGB Led class, intended for the ISS monitor applications

The Python 3 class initiates a common anode RGB Led and blinks it, based
on statuses of ISS overhead. See readme file for statuses (2-far away,
3-coming soon, 4-nearly here, 5-overhead). This is a helper class for multiple
ISS overhead solutions.

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied
"""

# common anode rgb led class, for ISS monitor

import RPi.GPIO as GPIO
import time
import threading
import config
import logging

logger = logging.getLogger()
class iss_rgb_led:

    def __init__(self, red_pin, green_pin, blue_pin):
        """
        Constructor of 'iss_rgb_led'. We initialize it with PIN numbers for red, green, blue respectively (in board mode)
        """
        
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin
        # we map to ISS code: ISS is: 0 - far away, 1 - coming soon (in 30 minutes), 2 - nearly here (1 minute to go), 3 - overhead.
        # this is the code which drives colors, timeouts etc.
        self.__iss_code = config.iss_status_far_away  # ignored
        self.__color_code = "000"  # ignored
        self.set_ISS_code(config.iss_status_no_connection)
        # initialize GPIO    
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        # heartbeat interval is boolen: if False, we timeout shorter, if True, we timeout longer
        self.__heartbeat_interval = False
        # switch off led
        self.rgb_blink()

        # setup the timers
        self.timer = threading.Timer(self.__getTimeInterval(), self.__heartbeat)
        self.timer.daemon = True
        self.timer.start()

        def __del__(self):
            print("Cleaning up.")
            GPIO.cleanup()

    def __getTimeInterval(self):
        """
        Return a blink timeout value, to achieve a 'beating heart effect'. For proximity codes 4 & 5, we invoke a 
        continuous blinking (looks more 'urgent').
        """

        if self.__iss_code > 3: # we switch on the heartbeat for ISS in proximity or error codes
            self.__heartbeat_interval = False
        if self.__heartbeat_interval:
            rv = 2.0
        else:
            rv = 0.3
        self.__heartbeat_interval = not self.__heartbeat_interval
        return rv

    def set_ISS_code(self, iss_code):
        """
        Setter for the ISS code. The only required entry point of the class. This stores the current ISS proximity code,
        and sets the color mask of the RGB Led.

        Please note that this mask is for a LED with a common anode. Reverse for a Led with a common Cathode
        """

        self.__iss_code = iss_code
        if self.__iss_code == config.iss_status_no_connection: # keep it red, but with a heartbeat
            self.__color_code = "011"
        if self.__iss_code == config.iss_status_error: # keep it red, but with a heartbeat
            self.__color_code = "011"
        if self.__iss_code == config.iss_status_far_away:
            self.__color_code = "110"
        elif  self.__iss_code == config.iss_status_coming_soon:
            self.__color_code = "100"
        elif  self.__iss_code == config.iss_status_nearly_here:
            self.__color_code = "001"
        elif  self.__iss_code == config.iss_status_overhead:
            self.__color_code = "011"

    def rgb_blink(self):
        """
        Blinks the Led once. Color is read from the property __color_code and depends on the current proximity code.
        """

        GPIO.output(self.red_pin, int(self.__color_code[0]))
        GPIO.output(self.green_pin, int(self.__color_code[1]))
        GPIO.output(self.blue_pin, int(self.__color_code[2]))
        time.sleep(0.1)
        GPIO.output(self.red_pin, True)
        GPIO.output(self.green_pin, True)
        GPIO.output(self.blue_pin, True)

    def __heartbeat(self):
        self.rgb_blink()
        self.timer = threading.Timer(self.__getTimeInterval(), self.__heartbeat).start()

# main loop. This loop is called only when you invoke the class from the command-line and serves as a test program. 
# To invoke, run the following: 'python iss_rgb_led.py'. When used as intended (as an included class) this code is 
# not invoked
if __name__ == "__main__":
    try:
        # get the logging argument, if any
        from argparse import ArgumentParser
        parser = ArgumentParser(description="iss_rgb_led class (iss_rgb_led.py)")
        parser.add_argument("-ll", "--loglevel",
            type=str,
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
        args = parser.parse_args()
        logging.basicConfig(level=args.loglevel)

         # test the script, by setting the RGB Led color via numerical status on the command line
        print("Launching RGB Blink Class Tester")
        print("--------------------------------")
        print()
        print("Enter the corresponding ISS proximity codes [0,1,2,3,4,5] to test the LED functionality. To quit, press CTRL-C")
        print()
        blinker = iss_rgb_led(config.rgbled_red, config.rgbled_green, config.rgbled_blue) 
        while True:
            request = input("isscode:")
            blinker.set_ISS_code(int(request))
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print()