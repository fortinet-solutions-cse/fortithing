import bme280_float, neopixel, network, ssd1306
from machine import Pin, I2C, ADC
from simple import MQTTClient
from time import sleep

class FortiThing(object):
    def __init__(self):
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        self._bme = bme280_float.BME280(i2c=self._i2c)
        self._adc = ADC(0)
        self._np = neopixel.NeoPixel(Pin(14), 2)
        self._blueled = Pin(16, Pin.OUT)
        self._blueled.off()
        self._oled = ssd1306.SSD1306_I2C(128, 64, self._i2c, 0x3c)
        self._mqttClient = None

    ####################################
    # Basic hardware operations
    ####################################
    
    def screen(self, *argv):
        print(argv)
        self._oled.fill(0)
        self._oled.text(argv[0], 0, 0)

        index = 0
        for arg in argv[1:]:
            self._oled.text(arg, 0, index*12 + 20)
            index += 1
        self._oled.show()
    
    def set_left_rgb_light(self, red, green, blue):
        self._np[0] = (red, green, blue)
        self._np.write()

    def set_right_rgb_light(self, red, green, blue):
        self._np[1] = (red, green, blue)
        self._np.write()
    
    def set_led(self, led_on):
        self._blueled.on() if led_on == 1 or led_on else self._blueled.off()

    def get_switch_status(self):
        return Pin(13, Pin.IN, Pin.PULL_UP).value()

    def get_tph(self):
        return self._bme.read_compensated_data()

    def get_adc(self):
        return self._adc.read()

    ####################################
    # Wifi connectivity
    ####################################

    def wifi_connect(self, wifi_essid, wifi_password):
        try:
            self.screen("Status", "Connecting WiFi")
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
                self.screen("Error", "WiFi connection failed", "More than 60 attemps")
                raise Exception

            self.screen("Status", "WiFi Connected")

        except Exception as e:
            print("Exception occurred when connecting.")
            print("Values: " + str(e))
            self.screen("Error", "Exception occurred", "when connecting")

    ####################################
    # IoT / MQTT services
    ####################################

    def mqtt_connect(self, client_id, server, port, ssl, user, password, sub_cb):
        self.screen("Status", "MQTT Connecting")
        self._mqttClient = MQTTClient(client_id=client_id, server=server, port=port, ssl=ssl, user=user, password=password)
        self._mqttClient.set_callback(sub_cb)
        self._mqttClient.connect()
        self.screen("Status", "MQTT Connected")
           

    def mqtt_subscribe(self, path):
        self.screen("Status", "Subscribing topic")
        self._mqttClient.subscribe(path)
        self.screen("Status", "Topic Subscribed")


    def mqtt_publish(self, path, value):
        self._mqttClient.publish(path, value)

    def mqtt_check_msg(self):
        self._mqttClient.check_msg()
