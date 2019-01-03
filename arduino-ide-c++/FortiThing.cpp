#include "FortiThing.h"
#include <Wire.h>

FortiThing::FortiThing():
ssid_(""),password_(""),mqttServer_(""),
mqttUser_(""),mqttPassword_(""), client_(espClient_),
bmeStarted_(false), ledsStarted_(false), mqttBrokerStarted_(false),
strip_(Adafruit_NeoPixel(2, D5))
{
  pinMode(A0, INPUT);   // Analog input pin (Light Sensor)
  pinMode(D0, OUTPUT);  // Analog output pin (LED)
  pinMode(D7, INPUT_PULLUP); // Digital input (Switch)
}

FortiThing::~FortiThing()
{	
}

bool FortiThing::startBme()
{
  if (bmeStarted_) return true;
  bool status;
  Wire.begin();
  status = bme_.begin(0x76);  
  if (!status) 
  {
    log("Could not find a valid BME280 sensor!");
    return false;
  }
  bmeStarted_ = true;
  return true;
}

bool FortiThing::startLeds()
{
  if (ledsStarted_) return true;

  strip_.setBrightness(100);
  strip_.begin();
  strip_.show();

  ledsStarted_ = true;
  return true;  
}

float FortiThing::readTemperature()
{
   if (startBme())
   {
      float temp = bme_.readTemperature();
      log("Temperature = %5.2f", temp);
      return temp; 
   }
}

float FortiThing::readPressure()
{
   if (startBme())
   {
      float pressure = bme_.readPressure();
      log("Pressure = %5.2f", pressure);
      return pressure; 
   }
}

float FortiThing::readHumidity()
{
   if (startBme())
   {
      float humidity = bme_.readHumidity();
      log("Humidity = %5.2f", humidity);
      return humidity; 
   }
}

int FortiThing::readLightSensor()
{
  int value = analogRead(A0);
  log("Light Sensor output: %d", value);
	return value;
}

bool FortiThing::readSwitch()
{
  bool value = digitalRead(D7);
  log("Switch status: %d", value);
  return value;
}

bool FortiThing::setLed(float value)
{
  analogWrite(D0, (int) value % 256);
	return true;
}

bool FortiThing::setLedRGB1(int red, int green, int blue)
{
  if (startLeds())
  {
    strip_.setPixelColor(0, red, green, blue);
    strip_.show();
    return true;
  }
 
	return false;
}

bool FortiThing::setLedRGB2(int red, int green, int blue)
{
  if (startLeds())
  {
    strip_.setPixelColor(1, red, green, blue);
    strip_.show();
    return true;
  }
  return false;
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
  
  log("Connecting to WiFi... begin: %d", status1);
 
  while ((status2 = WiFi.status()) != WL_CONNECTED) {
    delay(2000);
    log("Connection status: %d", status2);
  }
  log("Connected to the WiFi network: %d", WiFi.isConnected());
  log("IP: %s", WiFi.localIP().toString().c_str());
  log("Gateway: %s", WiFi.gatewayIP().toString().c_str());
  log("DNS: %s", WiFi.dnsIP().toString().c_str());
 	
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

bool FortiThing::connectToMQTTBroker()
{
  if (mqttBrokerStarted_) return true;
  client_.setServer(mqttServer_.c_str(), mqttPort_);
  while (!client_.connected()) 
  {
    log("Connecting to MQTT broker...");
    if (!client_.connect("djerufj3843d", mqttUser_.c_str(), mqttPassword_.c_str() )) 
    {
      log("Connection to MQTT broker failed with state: %d", client_.state());
      delay(2000);
    } 
  }
  log("Connected to MQTT broker.");  
  mqttBrokerStarted_ = true;
  return true;  
}

bool FortiThing::publishTopic(const String& topic, float value)
{
  if (!connectToMQTTBroker())
     return false;

  char buff[10]="";
  sprintf(buff, "%5.2f", value);
  client_.publish(topic.c_str(), buff);
	return true;
}

bool FortiThing::publishTopic(const String& topic, bool value)
{
  if (!connectToMQTTBroker())
     return false;
     
  client_.publish(topic.c_str(), value ? "true" : "false");
  return true;
}

bool FortiThing::publishTopic(const String& topic, const String& value)
{
  if (!connectToMQTTBroker())
     return false;
     
  client_.publish(topic.c_str(), value.c_str());
  return true;
}

bool FortiThing::subscribeTopic(const char* topic, void (*func)(const char* payload))
{
  log("Topic received: %s", topic);
	return true;
}

void FortiThing::log(const char* format, ...)
{
  char buff[128]="";
  va_list argptr;
  va_start(argptr, format);
  vsnprintf(buff, 100, format, argptr);
  va_end(argptr);
  Serial.println(buff);
}
