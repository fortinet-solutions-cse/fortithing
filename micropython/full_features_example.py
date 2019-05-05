from time import sleep

from fortithing import FortiThing

server = "xxxxx.messaging.internetofthings.ibmcloud.com"
client_id = "d:xxxxx:BME280:mynewdevice"
port = 1883
ssl = False
user = "use-token-auth"
password = "xxxxxxxx"

wifi_essid = 'xxxxxx'
wifi_password = 'xxxxxx'

ft = FortiThing()

def sub_cb(topic, msg):
    print((topic, msg))
    if 'switch_rgb_lights' in topic:
        light_value = int(msg) * 255
        ft.set_left_rgb_light(light_value, light_value, light_value)
        ft.set_right_rgb_light(light_value, light_value, light_value)
    elif 'set_left_rgb_light_color' in topic:
        value = msg.decode('utf-8').lstrip('#')
        lv = len(value)
        r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        ft.set_left_rgb_light(r, g, b)
    elif 'set_right_rgb_light_color' in topic:
        value = msg.decode('utf-8').lstrip('#')
        lv = len(value)
        r, g, b = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
        ft.set_right_rgb_light(r, g, b)
    elif 'set_led' in topic:
        value = int(msg)
        ft.set_led(value)


def connect():
    try:
        print("Connecting WiFi and MQTT Client")
        ft.screen("Status", "Connecting WiFi", "and MQTT Client")
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
            print("More than 60 attemps to connect to wifi")
            screen("Error", "WiFi connection failed", "More than 60 attemps")
            raise Exception

        global mqttClient
        mqttClient = MQTTClient(client_id=client_id, server=server, port=port, ssl=ssl, user=user, password=password)
        mqttClient.set_callback(sub_cb)
        mqttClient.connect()

        mqttClient.subscribe("iot-2/cmd/switch_rgb_lights/fmt/json")
        mqttClient.subscribe("iot-2/cmd/set_left_rgb_light_color/fmt/json")
        mqttClient.subscribe("iot-2/cmd/set_right_rgb_light_color/fmt/json")
        mqttClient.subscribe("iot-2/cmd/set_led/fmt/json")
    except:
        print("Exception occurred when connecting.")
        screen("Error", "Exception occurred", "when connecting")


def loop():
    count = 0
    button = False
    try:
        while 1:
            global mqttClient
            mqttClient.check_msg()
            sleep(0.1)

            if button is False and Pin(13, Pin.IN, Pin.PULL_UP).value():
                button = True
                mqttClient.publish("iot-2/evt/switch/fmt/json", str(not button))
            elif button is True and not Pin(13, Pin.IN, Pin.PULL_UP).value():
                button = False
                mqttClient.publish("iot-2/evt/switch/fmt/json", str(not button))

            if count == 30:
                result = bme.read_compensated_data()
                t = result[0]
                p = result[1]
                h = result[2]
                print(bme.values)
                mqttClient.publish("iot-2/evt/temp/fmt/json", '{{ "t":{:.2f} }}'.format(t))
                mqttClient.publish("iot-2/evt/pressure/fmt/json", '{{ "p":{:.2f} }}'.format(p/100))
                mqttClient.publish("iot-2/evt/humidity/fmt/json", '{{ "h":{:.2f} }}'.format(h))
                mqttClient.publish("iot-2/evt/light_sensor/fmt/json", '{{ "l":{:.2f} }}'.format(adc.read()))
                screen("Weather data", "Temp: {:.2f} C".format(t),
                       "Pres: {:.2f} hPa".format(p/100),
                       "Humi: {:.2f} %".format(h))
                count = 0

            count += 1

    except:
            print("Exception occurred in loop.")
            screen("Error", "Exception occurred", "in main loop")

while True:
    connect()
    loop()
