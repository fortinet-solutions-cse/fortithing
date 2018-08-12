//
// Created by mange on 10/03/2018.
//

#ifndef FORTITHING_FORTITHING_H
#define FORTITHING_FORTITHING_H

#include "Arduino.h"
#include <String>

#include <Adafruit_BME280.h>

class FortiThing {

public:

    FortiThing();
    virtual ~FortiThing();

    virtual float readTemperature();
    virtual float readPressure();
    virtual float readHumidity();
	
    virtual float readLightSensor();

    virtual bool setLed(bool);
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

private:

    //virtual void callback(const char* payload);
    bool startBme();

    Adafruit_BME280 bme_;
    
    String ssid_;
		String password_;
		String mqttServer_;
		String mqttUser_;
		String mqttPassword_;
    int    mqttPort_;

};

#endif //FORTITHING_FORTITHING_H
