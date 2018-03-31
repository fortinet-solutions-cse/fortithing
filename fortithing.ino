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
 ftt->publishTopic("/miguel/roomtemp", temp);
 delay(5000);
 
}
