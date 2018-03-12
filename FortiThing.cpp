#include <FortiThing.h>
#include <ESP8266WiFi.h>


FortiThing::FortiThing()
{
	
}


FortiThing::~FortiThing()
{
	
	
}


float FortiThing::readTemperature()
{

   return 2.5;
}

float FortiThing::readPressure()
{
   return 1020;
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
bool FortiThing::setMqttHost(const char* host)
{
	return true;
}

bool FortiThing::setMqttUserPassword(const char* user, const char* password)
{
	return true;
}

bool FortiThing::publishTopic(const char* topic, float value)
{
	return true;
}

bool FortiThing::subscribeTopic(const char* topic, void (FortiThing::*func)(const char* payload))
{
	return true;
}


