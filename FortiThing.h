//
// Created by mange on 10/03/2018.
//

#ifndef FORTITHING_FORTITHING_H
#define FORTITHING_FORTITHING_H

#include "Arduino.h"
#include <String>

#include <Adafruit_BME280.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_NeoPixel.h>


class FortiThing {

public:

    FortiThing();
    virtual ~FortiThing();

    virtual float readTemperature();
    virtual float readPressure();
    virtual float readHumidity();
	
    virtual int readLightSensor();

    virtual bool readSwitch();

    virtual bool setLed(float);
    virtual bool setLedRGB1(int, int, int);
    virtual bool setLedRGB2(int, int, int);


    // Wifi methods
    virtual bool setWifiSSID(const String& ssid);
    virtual bool setWifiPassword(const String& password);
    virtual bool connectWifi();


    // MQTT methods
    virtual bool setMqttServer(const String& server, const int port);
    virtual bool setMqttUserPassword(const String& user, const String& password);
    virtual bool publishTopic(const String& topic, float value);
    virtual bool publishTopic(const String& topic, bool value);
    virtual bool publishTopic(const String& topic, const String& value);
    virtual bool subscribeTopic(const char* topic, void (*func)(const char* payload));

    // Log (Serial printing)
    void log(const char* str, ...);

private:

    //virtual void callback(const char* payload);

    // Initialization functions
    virtual bool startBme();
    virtual bool connectToMQTTBroker();
    virtual bool startLeds();

    // Status variables
    bool bmeStarted_;
    bool ledsStarted_;
    bool mqttBrokerStarted_;

    // Resources    
    Adafruit_BME280 bme_;
    Adafruit_NeoPixel strip_;
    WiFiClient espClient_;
    PubSubClient client_;

    // Wifi and MQTT data
    String ssid_;
		String password_;
		String mqttServer_;
		String mqttUser_;
		String mqttPassword_;
    int    mqttPort_;

};

#endif //FORTITHING_FORTITHING_H
