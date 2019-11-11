from time import sleep

from fortithing import FortiThing

from credentials import wifi_essid, wifi_password, server, client_id, port, ssl, user, password

ft = FortiThing()


def subscribe_callback(topic, msg):
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


def loop():
    count = 0
    button = False
    try:
        while 1:
            ft.mqtt_check_msg()
            sleep(0.1)

            if button is False and ft.get_switch_status():
                button = True
                ft.mqtt_publish("iot-2/evt/switch/fmt/json", str(not button))
            elif button is True and not ft.get_switch_status():
                button = False
                ft.mqtt_publish("iot-2/evt/switch/fmt/json", str(not button))

            if count == 50: # Every 50 iterations of the loop, i.e. 5 secs, publish data
                result = ft.get_tph()
                t = result[0]
                p = result[1]
                h = result[2]
                adc = ft.get_adc()

                env_json = { 't': '{:.2f}'.format(t),
                             'p': '{:.2f}'.format(p/100),
                             'h': '{:.2f}'.format(h),
                             'l': '{:.2f}'.format(adc)}
                ft.mqtt_publish("iot-2/evt/environmental/fmt/json", str(env_json))

                # Alternatively use next lines to send 4 separate messages
                #
                # ft.mqtt_publish("iot-2/evt/temp/fmt/json", '{{ "t":{:.2f} }}'.format(t))
                # ft.mqtt_publish("iot-2/evt/pressure/fmt/json", '{{ "p":{:.2f} }}'.format(p/100))
                # ft.mqtt_publish("iot-2/evt/humidity/fmt/json", '{{ "h":{:.2f} }}'.format(h))
                # ft.mqtt_publish("iot-2/evt/light_sensor/fmt/json", '{{ "l":{:.2f} }}'.format(adc))

                ft.screen("Weather data", "Temp: {:.2f} C".format(t),
                       "Pres: {:.2f} hPa".format(p/100),
                       "Humi: {:.2f} %".format(h))
                count = 0

            count += 1

    except Exception as e:
        print("Exception occurred in loop..")
        print("Exception: " + str(e))
        ft.screen("Error", "Exception occurred", "in loop")
            

while True:
    ft.wifi_connect(wifi_essid, wifi_password)
    ft.mqtt_connect(client_id, server, port, ssl, user, password, subscribe_callback)
    ft.mqtt_subscribe("iot-2/cmd/switch_rgb_lights/fmt/json")
    ft.mqtt_subscribe("iot-2/cmd/set_left_rgb_light_color/fmt/json")
    ft.mqtt_subscribe("iot-2/cmd/set_right_rgb_light_color/fmt/json")
    ft.mqtt_subscribe("iot-2/cmd/set_led/fmt/json")
    loop()
