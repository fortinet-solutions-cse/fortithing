#include "FortiThing.h"
#include <ESP8266WiFi.h>
#include <Adafruit_BMP280.h>


FortiThing::FortiThing():
ssid(""),password(""),mqtthost(""),
mqttuser(""),mqttpassword("")
{
}

FortiThing::~FortiThing()
{	
}

float FortiThing::readTemperature()
{
   Adafruit_BMP280 bme;
   bool status;
   status = bme.begin();  
   if (!status) {
      Serial.println("Could not find a valid BME280 sensor, check wiring!");
      while (1);
   }
   return bme.readTemperature();
}

float FortiThing::readPressure()
{
   Adafruit_BMP280 bme;
   bool status;
   status = bme.begin();  
   if (!status) {
      Serial.println("Could not find a valid BME280 sensor, check wiring!");
      while (1);
   }
   return bme.readPressure();
}

float FortiThing::readHumidity()
{
   return 85.2;	
}

float FortiThing::readLightSensor()
{
	return 2.0;
}

bool FortiThing::setLed(bool)
{
	return true;
}

bool FortiThing::setLedRGB1(int, int, int)
{
	return true;
}

bool FortiThing::setLedRGB2(int, int, int)
{
	return true;
}

// Wifi methods
bool FortiThing::setWifiSSID(const String& ssid)
{
	this->ssid = ssid;
	return true;
}

bool FortiThing::setWifiPassword(const String& password)
{
	this->password = password;
	return true;
}

bool FortiThing::connectWifi()
{
  wl_status_t status1 = WiFi.begin(this->ssid.c_str(), this->password.c_str());
  wl_status_t status2 = WL_IDLE_STATUS;
  
  while ((status2 = WiFi.status()) != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
    char *str ="S1 %d $d";
    sprintf(str, "S1 %d %d", status1, status2);
    Serial.println(str);
  }
  Serial.println("Connected to the WiFi network");
  Serial.println(WiFi.isConnected());
  Serial.println(WiFi.localIP());
  Serial.println(WiFi.gatewayIP());
  Serial.println(WiFi.dnsIP());
 	
   return true;
}

// MQTT methods
bool FortiThing::setMqttHost(const String& host)
{
  mqtthost=host;
	return true;
}

bool FortiThing::setMqttUserPassword(const String& user, const String& password)
{
  mqttuser=user;
  mqttpassword=password;
	return true;
}

bool FortiThing::publishTopic(const String& topic, float value)
{
	return true;
}

bool FortiThing::subscribeTopic(const String& topic, void (FortiThing::*func)(const String& payload))
{
	return true;
}


