/**
 * ISS RGB LED handling
 * 
 * Made for Raspberry Valley (http://raspberry-valley.azurewebsites.net) makerspace.
 * 
*/

#include "Arduino.h"
#include "iss_rgb_led.h"

// RGB Led setup. Call this function from **setup()**
// this function assumes you have set the correct device pins for connecting the controller to
// an RGB Led (Red, Green, Blue variables)
// sets up the rgb led. Has to be called from setup()
iss_rgb_led::iss_rgb_led(int red_pin, int green_pin, int blue_pin)
{
  _iss_code = 0;

  _red_pin   = red_pin;
  _green_pin = green_pin;
  _blue_pin  = blue_pin;

  pinMode(_red_pin, OUTPUT);
  pinMode(_green_pin, OUTPUT);
  pinMode(_blue_pin, OUTPUT);

  digitalWrite(_red_pin, HIGH);
  digitalWrite(_green_pin, HIGH);
  digitalWrite(_blue_pin, HIGH);

}

// main function to call for blinking an RGB Led. Color of the led reacts to the **iss_code** variable value
// can be called directly, or from a 'thread' control (https://github.com/ivanseidel/ArduinoThread)
void iss_rgb_led::pulse()
{
  // blink the led 2 times in rapid succession, then wait a bit (don't delay if ISS is nearly here, i.e. code>3)
  on_off();
  on_off();
  if (_iss_code > 3)
  {
    delay(100);
  }
  else
  {
  }
  delay(1000);
}

void iss_rgb_led::set_iss_code(int code)
{
  // TODO
  _iss_code = code;
}

// internal function to switch a led on and off, as a part of a heartbeat pattern. Don't call externally
void iss_rgb_led::on_off()
{
  switch(_iss_code) {
    case 0: // no connection available
      digitalWrite(_red_pin, LOW);
      digitalWrite(_green_pin, HIGH);
      digitalWrite(_blue_pin, HIGH);
      break;
    case 1: // other error
      digitalWrite(_red_pin, LOW);
      digitalWrite(_green_pin, HIGH);
      digitalWrite(_blue_pin, HIGH);
      break;
    case 2: // ISS is far away (takes longer than 30 minutes to arrive)
      digitalWrite(_red_pin, HIGH);
      digitalWrite(_green_pin, HIGH);
      digitalWrite(_blue_pin, LOW);
      break;
    case 3: // ISS is coming soon (takes 1-30 minutes to arrive)
      digitalWrite(_red_pin, HIGH);
      digitalWrite(_green_pin, LOW);
      digitalWrite(_blue_pin, HIGH);
      break;
    case 4: // ISS is nearly here (arrives within a minute)
      digitalWrite(_red_pin, HIGH);
      digitalWrite(_green_pin, LOW);
      digitalWrite(_blue_pin, HIGH);
      break;
    case 5: // ISS is overhead
      digitalWrite(_red_pin, LOW);
      digitalWrite(_green_pin, HIGH);
      digitalWrite(_blue_pin, HIGH);
      break;
  }
  delay(100);
  digitalWrite(_red_pin, HIGH);
  digitalWrite(_green_pin, HIGH);
  digitalWrite(_blue_pin, HIGH);
  delay(100);
}
