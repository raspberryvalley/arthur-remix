/**
 * ISS RGB LED handling
 * 
 * Made for Raspberry Valley (http://raspberry-valley.azurewebsites.net) makerspace.
 * 
*/

#ifndef iss_rgb_led_h
#define iss_rgb_led_h

// #include "Arduino.h"

class iss_rgb_led
{
  public:
    iss_rgb_led(int red_pin, int green_pin, int blue_pin);
    void pulse();
    void set_iss_code(int code);
  private:
    void on_off();
    int _red_pin; 
    int _green_pin;
    int _blue_pin;
    int _iss_code;
};

#endif