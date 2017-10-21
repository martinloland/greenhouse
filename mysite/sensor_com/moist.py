# Configure I2C:
# https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c
# Wiring:
# https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
# Install Adafruit_Python_GPIO
# https://github.com/adafruit/Adafruit_Python_GPIO

from . import Adafruit_ADS1x15
import random
#https://github.com/adafruit/Adafruit_Python_ADS1x15


class MoistureSensor(object):
    def __init__(self, gain, channels, debug=False):
        self.gain = gain
        self.channels = channels
        self.debug = debug
        if not debug:
            self.adc = Adafruit_ADS1x15.ADS1115()

    def read(self):
        values = [0] * self.channels
        for i in range(self.channels):
            if not self.debug:
                values[i] = self.adc.read_adc(i, gain=self.gain)
            else:
                values[i] = random.randrange(50,100)
        return values[0], values[1]

'''
# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)
# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*4
    for i in range(4):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN)
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)
'''
