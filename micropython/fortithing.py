import bme280_float, network, ssd1306
from machine import SPI, Pin, I2C, ADC, freq, TouchPad
from micropython_dotstar import DotStar
from lis3dh import LIS3DH_I2C
from umqttsimple import MQTTClient
from time import sleep

class FortiThing(object):
    def __init__(self):
        freq(160000000)
        self._i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
        self._bme = bme280_float.BME280(i2c=self._i2c)
        self._adc = ADC(Pin(37))
        self._lis3dh = lis3dh=LIS3DH_I2C(self._i2c,address=0x19, int1=Pin(15))
        self._touchPad = TouchPad(Pin(32))
        self._blueled = Pin(4, Pin.OUT)
        self._blueled.off()
        self._mqttClient = None
        self._nb_leds   = 4
        self._clock_pin = 14 
        self._data_pin  = 13 
        self._empty_pin = 12
        self._spi = SPI(1, baudrate=10000000, sck=Pin(self._clock_pin),
            mosi=Pin(self._data_pin),
            miso=Pin(self._empty_pin)) 
        self._leds = DotStar(self._spi, self._nb_leds)
        for i in range (0, self._nb_leds):
            self._leds[i]=(0,0,0)
              
        try:
            self._oled = ssd1306.SSD1306_I2C(128, 64, self._i2c, 0x3c)
        except Exception as e:
            self._oled = None
            print("Exception occurred when initializing OLED.")
            print("Exception: " + str(e))



    ####################################
    # Basic hardware operations
    ####################################
    
    def screen(self, *argv):
        print(argv)
        try:
            self._oled.fill(0)
            self._oled.text(argv[0], 0, 0)

            index = 0
            for arg in argv[1:]:
                self._oled.text(arg, 0, index*12 + 20)
                index += 1
            self._oled.show()
        except Exception as e:
            pass
    
    def set_led_array(self, number, color, value):
        if color == 'red':
            self._leds[number] = (value, self._leds[number][1], self._leds[number][2] )
        if color == 'green':
            self._leds[number] = (self._leds[number][0], value, self._leds[number][2] )
        if color == 'blue':
            self._leds[number] = (self._leds[number][0], self._leds[number][1], value )
  
    def set_blue_led(self, led_on):
        self._blueled.on() if led_on == 1 or led_on else self._blueled.off()

    def get_switch_status(self):
        return not Pin(18, Pin.IN, Pin.PULL_UP).value()

    def get_tph(self):
        return self._bme.read_compensated_data()

    def get_adc(self):
        return self._adc.read()
    
    def get_touchpad(self):
        return (self._touchPad.read())

    def get_acceleration(self):
        return self._lis3dh.acceleration

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
            print("Exception: " + str(e))
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

