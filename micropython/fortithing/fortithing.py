import bme280_float, neopixel, network, ssd1306
from machine import Pin, I2C, ADC
from simple import MQTTClient

class FortiThing(object):
    def init(self):
        self._i2c = I2C(scl=Pin(5), sda=Pin(4), freq=400000)
        self._bme = bme280_float.BME280(i2c=i2c)
        self._adc = ADC(0)
        self._np = neopixel.NeoPixel(Pin(14), 2)
        self._blueled = Pin(16, Pin.OUT)
        self._blueled.off()
        self._oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)
        self._mqttClient = None
    
    def screen(self, *argv):
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


    def subscribe(self, ):
        pass

    def publish(self, ):
        pass