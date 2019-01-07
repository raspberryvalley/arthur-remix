/**
 * Arduino basic sketch - connects to open notify every 5 seconds and reads the forecast for Karlskrona.
 * So far we publish the response to the serial monitor
 * 
 * Made for Raspberry Valley (http://raspberry-valley.azurewebsites.net) makerspace.
 * 
*/

#include <string>         //to use string

int pin_out_LED;          //LED
String msg;                //message_out content
String line;               //message_in  content

//Configure WIFI:
#include <ESP8266WiFi.h>  //Wifi-library
#include <ESP8266HTTPClient.h> //http client library

//WLAN-Config
const char* ssid     = "yourssid";          //Your WIFI Name?
const char* password = "yourpassword";      //Your WIFI Password?

//API call settings

// open-notify query for a forecast to retrieve the time of ISS above KARLSKRONA
// change the latitude / longitude to your place!
const char* open_notify_URL = "http://api.open-notify.org/iss-pass.json?lat=56.16156&lon=15.58661&n=1";

void setup() {

  Serial.begin(115200);                              //baud rate
  pin_out_LED = 14;
  pinMode(pin_out_LED, OUTPUT);

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);                         //Connect to WIFI
  digitalWrite(pin_out_LED, HIGH);
  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");
  }
  digitalWrite(pin_out_LED, LOW);                     //We are connected to SSID
  Serial.println("");
  Serial.println("Raspberry Valley IIS Overhead monitor (RGB Led)");
  Serial.println("-----------------------------------------------");
  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {

  if (WiFi.status() == WL_CONNECTED) { //Check WiFi connection status
 
    HTTPClient http;  //Declare an object of class HTTPClient
 
    http.begin(open_notify_URL);  //Specify request destination from settings above
    int httpCode = http.GET();                                                                  //Send the request
 
    if (httpCode > 0) { //Check the returning code
 
      String payload = http.getString();   //Get the request response payload
      Serial.println(payload);                     //Print the response payload
      delay(10000); // call every 10 secs
    }
 
    http.end();   //Close connection
  }
  else {
    Serial.print("no Wifi connection .... waiting 1 second");
    delay (1000);
  }

}
