#!/usr/bin/env python

"""
Python 3 utility module for network / internet 

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied
"""

import os
import requests
import logging

logger = logging.getLogger()

def check_internet(url='http://www.google.com/'):
    """
    Check an internet connection by requesting a provided URL. If no URL is provided,
    google.com is used.
    """
    
    logging.info("Checking internet connection (%s)", url)
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        logging.info("Internet connection (%s) available", url)
        return True
    except requests.ConnectionError:
        logging.warn("Internet connection (%s) unavailable", url)
    return False

# Won't work on windows
# def ping(hostname='8.8.8.8'):
#    response = os.system("ping -c 1 " + hostname)
#    if response == 0:
#        print ('is up!')
#    else:
#        print ('is down!')

# main loop. This loop is called only when you invoke the class from the command-line and serves as a test program. 
# To invoke, run the following: 'python netutil.py'. When used as intended (as an included class) this code is 
# not invoked
if __name__ == "__main__":
    import sys
    # we log to console if in test mode, otherwise we depend on the main module configuration
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # run self test on available functions
    available = check_internet()
    # print out the results
    print()
    print ("Raspberry Valley Network Utility Library")
    print ("----------------------------------------")
    if available:
        print ("Internet available")
    else:
        print ("No Internet connection available")
 