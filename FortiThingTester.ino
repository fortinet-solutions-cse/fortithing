#include <FortiThing.h>

#define SEALEVELPRESSURE_HPA (1013.25)

const char* ssid = "XXXXXXXXXXXX";
const char* password =  "XXXXXXXXXXXX";
const char* mqttServer = "m23.cloudmqtt.com";
const int mqttPort = 12012;
const char* mqttUser = "XXXXXXXXXXX";
const char* mqttPassword = "XXXXXXXXXX";
 
void setup() {
 
  Serial.begin(115200);

  FortiThing* ftt = new FortiThing();
  ftt->setWifiSSID(ssid);
  ftt->setWifiPassword(password);
  ftt->connectWifi();

  ftt->setMqttHost(mqttServer);

  delete ftt;
 
}
 
void loop() {
}
