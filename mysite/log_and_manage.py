import os, sys
import time, datetime
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
from django.utils import timezone
django.setup()
from greenhouse.models import DataPoint, Setting, SystemStatus
from sensor_com import (Lights, Pump, TempHumiditySensor, MoistureSensor,
                        Camera, get_free_space_mb)


def add_sensor_entry(temperature, humidity, moisture_1, moisture_2, light_on, image):
    d = DataPoint()
    d.time = timezone.now()
    d.temperature = temperature
    d.air_humidity = humidity
    d.soil_moisture_1 = moisture_1
    d.soil_moisture_2 = moisture_2
    d.light_on = light_on
    d.image = image
    d.save()


def update_system_status(last_watering):
    system_status = SystemStatus.objects.get()
    system_status.last_loop = timezone.now()
    system_status.message = 'OK'
    system_status.last_watering = last_watering
    system_status.ok = True
    system_status.free_space = get_free_space_mb('/')
    system_status.save()


def decide_debug():
    if len(sys.argv) >= 2:
        if sys.argv[1] == 'debug':
            return True
    return False


def main():
    debug = decide_debug()
    system_status = SystemStatus.objects.get()
    temp_humidity_sensor = TempHumiditySensor(pin=23, debug=debug)
    moisture_sensor = MoistureSensor(gain=1, channels=2, debug=debug)
    lights = Lights(pin=13, debug=debug)
    pump = Pump(pin=15, last_watering=system_status.last_watering, debug=debug)
    camera = Camera(debug=debug, resolution=[1296, 730])

    while True:
        settings = Setting.objects.get()

        if settings.self_regulate:

            temperature, humidity = temp_humidity_sensor.read()
            moisture_1, moisture_2 = moisture_sensor.read()
            pump.manage(
                moisture_1=moisture_1,
                moisture_2=moisture_2,
                soil_moisture_pump_level=settings.soil_moisture_pump_level,
                watering_time=settings.watering_time,
                watering_inactive_period=settings.watering_inactive_period
            )
            lights.manage(
                on_time=settings.start_light,
                off_time=settings.end_light
            )

            if settings.logging_active:
                update_system_status(last_watering=pump.last_watering)
                last_entry = DataPoint.objects.latest('time').time
                logging_interval = \
                    datetime.timedelta(minutes=settings.logging_interval)

                if (timezone.now() - last_entry) > logging_interval:
                    image_path = camera.capture(
                        capture_at_night=settings.save_night_images,
                        light_on=lights.on
                    )
                    add_sensor_entry(temperature=temperature,
                                     humidity=humidity,
                                     moisture_1=moisture_1,
                                     moisture_2=moisture_2,
                                     light_on=lights.on,
                                     image=image_path)

        time.sleep(settings.loop_interval)


if __name__ == "__main__":
    main()
