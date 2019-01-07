/**
 * ISS Huzzah RGB LED handling
 * 
 * Made for Raspberry Valley (http://raspberry-valley.azurewebsites.net) makerspace.
 * 
*/

#include <ESP8266WiFi.h>
#include "iss_rgb_led.h"

#include "Thread.h"

// RGB LED Pins
#define Red   0
#define Green 15
#define Blue  13

iss_rgb_led led(Red, Green, Blue);

void setup() 
{
  Serial.begin(115200);  
  Serial.println("RGB Heartbeat for ISS");
}

void loop() {
  led.pulse();
}


