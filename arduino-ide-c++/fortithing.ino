#include "FortiThing.h"

const char* ssid = "XXXXXXXXXXXX";
const char* password =  "XXXXXXXXXXXX";
const char* mqttServer = "m23.cloudmqtt.com";
const int mqttPort = 12012;
const char* mqttUser = "XXXXXXXXXXX";
const char* mqttPassword = "XXXXXXXXXX";

FortiThing* ftt = new FortiThing();

void setup() {
 
  Serial.begin(115200);

  ftt->setWifiSSID(ssid);
  ftt->setWifiPassword(password);
  ftt->connectWifi();

  ftt->setMqttServer(mqttServer, mqttPort);
  ftt->setMqttUserPassword(mqttUser, mqttPassword);
}
 
void loop() {

 float temp = ftt->readTemperature();
 ftt->publishTopic("/fortithing/temperature", temp);

 float pressure = ftt->readPressure();
 ftt->publishTopic("/fortithing/pressure", pressure);
 
 float humidity = ftt->readHumidity();
 ftt->publishTopic("/fortithing/humidity", humidity);

 float lightSensor = ftt->readLightSensor();
 ftt->publishTopic("/fortithing/lightsensor", lightSensor);

 bool sw_value = ftt->readSwitch();
 ftt->publishTopic("/fortithing/switch", sw_value);

 ftt->setLedRGB1(10,0,0);
 ftt->setLedRGB2(0,0,10);

 if (sw_value)
   ftt->setLed(255);
 else
   ftt->setLed(0);

 delay(2000);
 
}
