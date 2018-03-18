//
// Created by mange on 10/03/2018.
//

#ifndef FORTITHING_FORTITHING_H
#define FORTITHING_FORTITHING_H

#include "Arduino.h"
#include <String>

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
    virtual bool setMqttHost(const String& host);
    virtual bool setMqttUserPassword(const String& user, const String& password);
    virtual bool publishTopic(const String& topic, float value);
    virtual bool subscribeTopic(const String& topic, void (FortiThing::*func)(const String& payload));

private:

    //virtual void callback(const char* payload);
	
	String ssid;
	String password;
  String mqtthost;
  String mqttuser;
  String mqttpassword;

};




#endif //FORTITHING_FORTITHING_H
