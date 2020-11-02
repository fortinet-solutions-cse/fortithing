from time import sleep

from fortithing import FortiThing

from credentials import wifi_essid, wifi_password, server, client_id, port, ssl, user, password

from json import loads

import sys

ft = FortiThing()

def subscribe_callback(topic, msg):
    print((topic, msg))
    try: 
        if 'set' in msg:
            data=loads(msg)
            method=data['method']
            params=data['params']
            if 'set_led' in method:
                led_number = int(method[7])
                color_component = method[9:]
                ft.set_led_array(led_number, color_component, params)
            elif 'set_blue_led' in method:
                ft.set_blue_led(params)
    except Exception as e:
        print("Exception occurred in subscribe callback")
        print("Exception: " + str(e))
        sys.print_exception(e)
        ft.screen("Error", "Exception occurred", "in subscribe callback")  


def loop():
    count = 0
    button = False
    try:
        while 1:
            ft.mqtt_check_msg()
            sleep(0.1)

            if button is not ft.get_switch_status():
                button = not button
                env_json = { 'switch': button }
                ft.mqtt_publish("v1/devices/me/attributes", str(env_json))

            if count == 1: # Every 50 iterations of the loop, i.e. 5 secs, publish data
                result = ft.get_tph()
                t = result[0]
                p = result[1]
                h = result[2]
                adc = ft.get_adc()
                touchpad = ft.get_touchpad()
                x, y, z = ft.get_acceleration()

                env_json = { 'temperature': '{:.2f}'.format(t),
                             'pressure': '{:.2f}'.format(p/100),
                             'humidity': '{:.2f}'.format(h),
                             'light': '{:.2f}'.format(adc),
                             'touchpad': '{:.2f}'.format(touchpad),
                             'x': '{:.2f}'.format(x),
                             'y': '{:.2f}'.format(y),
                             'z': '{:.2f}'.format(z)
                             }
                ft.mqtt_publish("v1/devices/me/telemetry", str(env_json))

                ft.screen("Weather data", "Temp: {:.2f} C".format(t),
                       "Pres: {:.2f} hPa".format(p/100),
                       "Humi: {:.2f} %".format(h),
                       "Light: {:.2f}".format(adc),
                       "TouchPad: {:.2f}".format(touchpad),
                       "x: {:.2f}".format(x),
                       "y: {:.2f}".format(y),
                       "z: {:.2f}".format(z))
                       
                count = 0

            count += 1

    except Exception as e:
        print("Exception occurred in loop..")
        print("Exception: " + str(e))
        sys.print_exception(e)
        ft.screen("Error", "Exception occurred", "in loop")         

while True:
    ft.wifi_connect(wifi_essid, wifi_password)
    ft.mqtt_connect(client_id, server, port, ssl, user, password, subscribe_callback)
    ft.mqtt_subscribe("v1/devices/me/rpc/request/+")
    loop()
