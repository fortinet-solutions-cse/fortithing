#include "FortiThing.h"
#include <ESP8266WiFi.h>
#include <PubSubClient.h>


FortiThing::FortiThing():
ssid_(""),password_(""),mqttServer_(""),
mqttUser_(""),mqttPassword_("")
{
}

FortiThing::~FortiThing()
{	
}

float FortiThing::readTemperature()
{
   if (startBmp())
   {
      return bmp_.readTemperature(); 
   }
}

float FortiThing::readPressure()
{
   if (startBmp())
   {
      return bmp_.readPressure(); 
   }
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
	ssid_ = ssid;
	return true;
}

bool FortiThing::setWifiPassword(const String& password)
{
	password_ = password;
	return true;
}

bool FortiThing::connectWifi()
{
  wl_status_t status1 = WiFi.begin(ssid_.c_str(), password_.c_str());
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
bool FortiThing::setMqttServer(const String& server, const int port)
{
  mqttServer_ = server;
  mqttPort_   = port;
	return true;
}

bool FortiThing::setMqttUserPassword(const String& user, const String& password)
{
  mqttUser_     = user;
  mqttPassword_ = password;
	return true;
}

bool FortiThing::publishTopic(const String& topic, float value)
{
  WiFiClient espClient;
  PubSubClient client(espClient);
  
  client.setServer(mqttServer_.c_str(), mqttPort_);
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
   if (client.connect("djerufj3843d", mqttUser_.c_str(), mqttPassword_.c_str() )) {
      Serial.println("connected");  
    } else {
     Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  char buff[10]="";
  sprintf(buff, "%5.2f", value);
  client.publish(topic.c_str(), buff);
	return true;
}

bool FortiThing::startBmp()
{
   bool status;
   status = bmp_.begin();  
   if (!status) {
      Serial.println("Could not find a valid BMP280 sensor, check wiring!");
      return false;
   }
  return true;
}
