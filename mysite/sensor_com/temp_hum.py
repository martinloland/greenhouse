# Wiring:
# http://www.circuitbasics.com/how-to-set-up-the-dht11-humidity-sensor-on-the-raspberry-pi/

import random
from . import Adafruit_DHT
# https://github.com/adafruit/Adafruit_Python_DHT


class TempHumiditySensor(object):
    def __init__(self, pin, debug=False):
        self.pin = pin
        self.debug = debug
        if not debug:
            self.sensor = Adafruit_DHT.DHT11

    def read(self):
        if not self.debug:
            humidity, temperature = \
                Adafruit_DHT.read_retry(self.sensor, self.pin)
            if humidity is not None and temperature is not None:
                print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'
                      .format(temperature, humidity))
            else:
                print('Failed to get reading. Try again!')
        else:
            humidity, temperature = \
                random.randrange(0, 100), random.randrange(20, 30),
        return temperature, humidity
