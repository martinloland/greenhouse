# Relay wiring:
# http://yourduino.com/sunshop//index.php?l=product_detail&p=201
# https://forum.arduino.cc/index.php?topic=102978.0
# http://www.susa.net/wordpress/2012/06/raspberry-pi-relay-using-gpio/

import platform
import datetime
from django.utils import timezone
if platform.system() is not 'Windows':
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
# https://elinux.org/RPi_GPIO_Code_Samples#RPi.GPIO


class Lights(object):

    def __init__(self, pin, debug=False):
        self.pin = pin
        self.on = False
        self.debug = debug
        if not debug:
            GPIO.setup(self.pin, GPIO.OUT)

    def manage(self, on_time, off_time):
        now = timezone.now().astimezone().time()
        if on_time < now < off_time and not self.on:
            self.toggle()
        elif (now < on_time or now > off_time) and self.on:
            self.toggle()

    def toggle(self):
        if self.on:
            if not self.debug:
                GPIO.output(self.pin, GPIO.LOW)
            else:
                print('lights off - {}'.format(timezone.now().astimezone()))
        else:
            if not self.debug:
                GPIO.output(self.pin, GPIO.HIGH)
            else:
                print('lights on - {}'.format(timezone.now().astimezone()))
        self.on = not self.on


class Pump(object):

    def __init__(self, pin, last_watering, debug=False):
        self.pin = pin
        self.last_watering = last_watering
        self.on = False
        self.debug = debug
        if not debug:
            GPIO.setup(self.pin, GPIO.OUT)

    def manage(self,
               moisture_1,
               moisture_2,
               soil_moisture_pump_level,
               watering_time,
               watering_inactive_period):

        if self.on:
            now = timezone.now()
            watering_time = datetime.timedelta(seconds=watering_time)
            if (now - self.last_watering) > watering_time:
                self.toggle()
        elif self.ready_to_water(watering_inactive_period):
            avg_moisture = (moisture_1+moisture_2)/2
            if avg_moisture < soil_moisture_pump_level:
                self.toggle()

    def ready_to_water(self, watering_inactive_period):
        waiting_time = datetime.timedelta(minutes=watering_inactive_period)
        now = timezone.now()

        if (now - self.last_watering) > waiting_time:
            return True
        else:
            return False

    def toggle(self):
        if self.on:
            if not self.debug:
                GPIO.output(self.pin, GPIO.LOW)
            else:
                print('pump off - {}'.format(timezone.now().astimezone()))
        else:
            if not self.debug:
                GPIO.output(self.pin, GPIO.HIGH)
            else:
                print('pump on - {}'.format(timezone.now().astimezone()))
            self.last_watering = timezone.now()
        self.on = not self.on
