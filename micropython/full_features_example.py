import bme280_float, neopixel, network 
from simple import MQTTClient
from time import sleep
from machine import Pin, I2C, ADC

server = "xxxxx.messaging.internetofthings.ibmcloud.com"
client_id = "d:xxxxx:BME280:mynewdevice"
port = 1883
ssl = False
user = "use-token-auth"
password = "xxxxxxxx"

wifi_essid = 'xxxxxx'
wifi_password = 'xxxxxx'

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
bme = bme280_float.BME280(i2c=i2c)
adc = ADC(0)
np = neopixel.NeoPixel(Pin(14), 2)
blueled = Pin(16, Pin.OUT)
blueled.off()
c = None


def sub_cb(topic, msg):
    print((topic, msg))
    if 'switch_rgb_lights' in topic:
        light_value = int(msg) * 255
        np[0] = (light_value, light_value, light_value)
        np[1] = (light_value, light_value, light_value)
        np.write()
    elif 'set_left_rgb_light_color' in topic:
        value = msg.decode('utf-8').lstrip('#')
        lv = len(value)
        r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        np[0] = (r, g, b)
        np.write()
    elif 'set_right_rgb_light_color' in topic:
        value = msg.decode('utf-8').lstrip('#')
        lv = len(value)
        r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        np[1] = (r, g, b)
        np.write()
    elif 'set_led' in topic:
        value = int(msg)
        if value >= 1:
            blueled.on()
        else:
            blueled.off()


def connect():
    try:
        print("Connecting WiFi and MQTT Client")
        sta_if = network.WLAN(network.STA_IF)
        ap_if = network.WLAN(network.AP_IF)

        ap_if.active(False)  # Deactivate Access Point
        sta_if.active(True)  # Activate Station interface

        sta_if.connect(wifi_essid, wifi_password)

        count = 0
        while not sta_if.isconnected() and count < 60:
            sleep(0.5)
            count += 1

        if count >= 60:
            raise Exception

        global c
        c = MQTTClient(client_id=client_id, server=server, port=port, ssl=ssl, user=user, password=password)
        c.set_callback(sub_cb)
        c.connect()

        c.subscribe("iot-2/cmd/switch_rgb_lights/fmt/json")
        c.subscribe("iot-2/cmd/set_left_rgb_light_color/fmt/json")
        c.subscribe("iot-2/cmd/set_right_rgb_light_color/fmt/json")
        c.subscribe("iot-2/cmd/set_led/fmt/json")
    except:
        print("Exception occurred when connecting.")


def loop():
    count = 0
    button = False
    try:
        while 1:
            global c
            c.check_msg()
            sleep(0.1)

            if button is False and Pin(13, Pin.IN, Pin.PULL_UP).value():
                button = True
                c.publish("iot-2/evt/switch/fmt/json", str(not button))
            elif button is True and not Pin(13, Pin.IN, Pin.PULL_UP).value():
                button = False
                c.publish("iot-2/evt/switch/fmt/json", str(not button))

            if count == 30:
                result = bme.read_compensated_data()
                t = result[0]
                p = result[1]
                h = result[2]
                print(bme.values)
                c.publish("iot-2/evt/temp/fmt/json", '{{ "t":{:.2f} }}'.format(t))
                c.publish("iot-2/evt/pressure/fmt/json", '{{ "p":{:.2f} }}'.format(p/100))
                c.publish("iot-2/evt/humidity/fmt/json", '{{ "h":{:.2f} }}'.format(h))
                c.publish("iot-2/evt/light_sensor/fmt/json", '{{ "l":{:.2f} }}'.format(adc.read()))
                count = 0

            count += 1

    except:
            print("Exception occurred in loop.")

while True:
    connect()
    loop()
