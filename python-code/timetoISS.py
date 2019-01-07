#!/usr/bin/env python

"""
Calculates time remaining before **ISS** is overhead. Just configure your location

The Python 3 class takes a longitude/latitude and calls the Open Notify (http://open-notify.org)
service to forecast the next time the ISS is overhead above the coordinates provided.

Created by the Raspberry Valley team at Raspberry Valley, Karlskrona, Sweden
Learn more about Raspberry Valley: https://raspberry-valley.azurewebsites.net

This code is in the public domain and may be freely copied and used
No warranty is provided or implied

Inspiration: http://open-notify.org/Open-Notify-API/ISS-Location-Now/
Track ISS here (eesa): https://spotthestation.nasa.gov/tracking_map.cfm
Track ISS also here: https://www.n2yo.com/?s=28654

Interesting coordinates to re-use. We tried those with/for our friends there

- Karlskrona, Sweden: 56.16156, 15.58661
- Ronneby, Sweden: 56.20999, 15.27602
- Liberec, Czech Republic: 50.76711, 15.05619
- North Bay, Canada: 46.322536, -79.456360
"""

import config
import threading
import urllib.request
import json
import time
import netutil
import logging

logger = logging.getLogger()

class iss_overhead:
    """ Class providing a count-down for the location of ISS above a given coordinate (longitude, latitude). 
    
    The class gives a status of the ISS position, as well as some other bits of information about ISS, 
    using the Open Notify service.
    """

    def __init__(self, latitude, longitude, place):
        """ The constructor takes location coordinates (latitude, longitude) and a name of the location for display purposes. 
        parameters are stored as public properties for use / re-use in 'latitude', 'longitude', 'place' respectively.

        @param self The object pointer.
        @param latitude Latitude of location we wish to follow the ISS overhead
        @param longitude Longitude of location we wish to follow the ISS overhead
        @param place String value describing the location (humanly readable), used for notifications
        """
        self.riseTime = None # the latest calculated rise time of ISS over latitude/longitude
        self.duration = None # the latest calculated duration of visibility of ISS over latitude/longitude

        self.latitude = latitude
        self.longitude = longitude
        self.place = place

        self.timer = None
        self.timer = threading.Timer(self.__getTimeInterval(), self.__refreshPositionForecast)
        self.timer.daemon = True
        self.timer.start()

        logging.info("Creating ISS class at {} (latitude), {} (longitude) [{}]".format(self.latitude, self.longitude, self.place))

    def __del__(self):
        """ Class destructor. De-initialize the timer.

        @param self The object pointer.
        """

        if self.timer != None:
            self.timer.cancel()
        logging.info("Cleaning up ISS class at {} (latitude), {} (longitude) [{}]".format(self.latitude, self.longitude, self.place))

    # get the timeout interval for the web service callback. If risetime is hours away, we call the callback only occasionally, later more frequently
    def __getTimeInterval(self):
        """ Get timeout interval for the web service calls - the closer the ISS gets, the more often we call the web service.
        We assume the ISS prediction is being fine-tuned all the time. When it comes to hours away, we don't really need the high
        precision and can offload the web service. The closer the ISS gets, the more often we call the service (however the precision
        expected still allows us to call at 'reasonably long' intervals). Once the ISS is overhead, we don't call at all, until the next 
        prediction is used. This function calculates the time interval, based on the 'positionStatus' method value.
        
        @param self The object pointer.
        """

        if self.riseTime == None: # no callback yet called, we call fast
            return 1
        currentStatus = self.positionStatus
        if currentStatus == 0:
            return 10
        elif currentStatus == 1:
            return 10
        elif currentStatus == 2:
            return 600  # 10 minutes
        elif currentStatus == 3:
            return 120   # 2 minutes
        elif currentStatus == 4:
            return 10
        # if overhead, we calculate the new time for the new ISS orbit(s) (with a safety margin of 3 seconds). This allows to read only the new estimate
        currentUnixTimestamp = int(time.time())
        return self.riseTime + self.duration - currentUnixTimestamp + 3

    def positionStatus(self):
        """ The method returns a status of how for ISS is: 

        - 2 - far away, 
        - 3 - coming soon (in 30 minutes), 
        - 4 - nearly here (1 minute to go), 
        - 5 - overhead.

        Please note that statuses also include error codes 0 and 1, which are not handled in the class itself. This status call gets called only if no
        errors occur.

        @param self The object pointer.
        """

        currentUnixTimestamp = int(time.time())
        totalSeconds = self.secondsToISS()
        if totalSeconds == None:
            return config.iss_status_no_connection
        if self.riseTime <= currentUnixTimestamp <= self.riseTime + self.duration:
            return config.iss_status_overhead
        # 1/2 hour (30 minutes) = 60 * 30 = 1800
        if totalSeconds > 1800:
            return config.iss_status_far_away
        # coming soon
        if totalSeconds > 60:
            return config.iss_status_coming_soon
        return config.iss_status_nearly_here

    def __refreshPositionForecast(self):
        """ refreshPositionForecast is the internal callback function for re-reading the estimate of the ISS position overhead. 
        Called at various intervals, depending on current position. The callback methods takes care of timing and calls the actual
        methods to provide functionality of class.
        
        @param self The object pointer.
        """

        logging.info("Callback initiated: calling open-notify API")
        self.__readTimetoISS()
        self.timer = threading.Timer(self.__getTimeInterval(), self.__refreshPositionForecast)
        self.timer.start()
    
    def __readTimetoISS(self):
        """ return the first time ISS flies over latitude, longitude specified in constructor

        @param self The object pointer.
        """
        # get the prediction. Returns 1 prediction based on URL request
        requestString = "http://api.open-notify.org/iss-pass.json?lat={}&lon={}&n=1".format(self.latitude, self.longitude)
        req = urllib.request.Request(requestString)
        response = urllib.request.urlopen(req)
        res_body = response.read()
        # get first (and only) duration / risetime
        j = json.loads(res_body.decode("utf-8"))
        try:
            self.riseTime = int(j['response'][0]['risetime'])
            self.duration = int(j['response'][0]['duration'])
        except IndexError:
            # TODO: set infinity or other value, to show '99:99'
            self.riseTime = None
            self.duration = None
            logging.warn("Could not retrieve forecast for ISS overhead")
        logging.info("Retrieved data for {}: risetime {}, duration {} (lat: {} long: {})".format(self.place, self.riseTime, self.duration, self.latitude, self.longitude))
    
    def secondsToISS(self):
        """ Returns the number of seconds remaing for next pass of ISS over given latitude/longitude.
        
        @param self The object pointer.
        """

        if self.riseTime == None:
            return None
        currentUnixTimestamp = int(time.time())
        return self.riseTime - currentUnixTimestamp
    
    def timeToISS(self):
        """Return number of days / hours / minutes / seconds to ISS (tuple)
        
        @param self The object pointer.
        """
        
        totalSeconds = self.secondsToISS()
        if totalSeconds == None:
            return None
    
        # break down the seconds remaining
        days = totalSeconds // 86400
        totalSeconds -= 86400 * days
        hours = totalSeconds // 3600
        totalSeconds -= 3600 * hours
        minutes = totalSeconds // 60
        totalSeconds -= 60 * minutes
            
        return (days, hours, minutes, totalSeconds)
    
    # TODO (awaiting python 3.6 for f-strings) for making the display mask parametrized
    def stringCountdown(self):
        """return a string with the countdown values formatted. Humanly readable format for displaying countdown.
        
        The function returns the countdown value in the format of 'HH:MM', as we use it with simple displays only.

        @param self The object pointer.
        """
        
        breakdownTime = self.timeToISS()
        if breakdownTime != None:
            return "{:02d}:{:02d}".format(breakdownTime[1], breakdownTime[2])
        else:
            return ""

# main loop. This loop is called only when you invoke the class from the command-line and serves as a test program. 
# To invoke, run the following: 'python timetoISS.py'. When used as intended (as an included class) this code is 
# not invoked
if __name__ == "__main__":
    try:
        # get the logging argument, if any
        from argparse import ArgumentParser
        parser = ArgumentParser(description="iss_overhead class (timetoISS.py)")
        parser.add_argument("-ll", "--loglevel",
            type=str,
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
            help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)")
        args = parser.parse_args()
        logging.basicConfig(level=args.loglevel)

        # test the script, by printing out time to ISS every 5 seconds
        print("Running time to ISS for Karlskrona")
        print("----------------------------------")
        
        iss = iss_overhead(56.1612, 15.5869, "Karlskrona") 
        while True:
            secondsMessage = ""
            if iss.riseTime != None:
                secondsMessage = " [{} seconds in total]".format(iss.secondsToISS())
            breakdownTime = iss.timeToISS()
            if breakdownTime != None:
                print ("Time to ISS in {}: {} days, {} hours, {} minutes, {} seconds".format(
                    iss.place, breakdownTime[0], breakdownTime[1], breakdownTime[2], breakdownTime[3]) + secondsMessage)
            time.sleep(5)
    except KeyboardInterrupt:
        pass
