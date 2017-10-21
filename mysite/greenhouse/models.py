from django.db import models
from django.utils import timezone
from datetime import timedelta


class Setting(models.Model):
    self_regulate = models.BooleanField(default=True)
    logging_active = models.BooleanField(default=True)
    logging_interval = models.IntegerField('Logging interval (minutes)')
    loop_interval = models.IntegerField('Loop interval (seconds)',
                                        default=2)
    save_night_images = models.BooleanField()
    start_light = models.TimeField()
    end_light = models.TimeField()
    soil_moisture_pump_level = models.FloatField()
    watering_time = models.IntegerField('Watering time (seconds)')
    watering_inactive_period = \
        models.IntegerField('Watering inactive period (minutes)')
    graph_range_normal = models.IntegerField('Graph range normal (hours)')
    graph_range_detailed = models.IntegerField('Graph range detailed (hours)')

    def __str__(self):
        return 'Settings'


class DataPoint(models.Model):
    time = models.DateTimeField()
    temperature = models.FloatField('Temperature degrees Celsius')
    air_humidity = models.FloatField()
    soil_moisture_1 = models.FloatField('Soil moisture coriander')
    soil_moisture_2 = models.FloatField('Soil moisture basil')
    image = models.ImageField(upload_to='camera')
    light_on = models.BooleanField()

    url_to_variables = {'time':['time'],
                        'temperature':['temperature'],
                        'moisture':['soil_moisture_1', 'soil_moisture_2'],
                        'humidity':['air_humidity'],
                        'video':['image'],
                        'light':['light_on']}

    variable_lookup = {'time':
                           {'verbal':'Time',
                            'suffix':''},
                       'temperature':
                           {'verbal':'Temperature',
                            'suffix':''},
                       'soil_moisture_1':
                           {'verbal':'Moisture coriander',
                            'suffix':''},
                       'soil_moisture_2':
                           {'verbal':'Moisture basil',
                            'suffix':''},
                       'light_on':
                           {'verbal':'Lights',
                            'suffix':''},
                       'air_humidity':
                           {'verbal':'Humidity',
                            'suffix':''},
                       }

    def __str__(self):

        # return str(self.image.path)
        return str(self.time.astimezone().strftime("%Y-%m-%d %H:%M:%S"))


class SystemStatus(models.Model):
    last_loop = models.DateTimeField()
    message = models.CharField(max_length=140, default='OK')
    free_space = models.FloatField(default=1000.0)
    ok = models.BooleanField(default=True)
    last_watering = models.DateTimeField()

    @property
    def report(self):
        now = timezone.now()
        max_delta = timedelta(seconds=Setting.objects.get().loop_interval+1)
        free = self.free_space_verbal()
        if (now-self.last_loop) > max_delta:
            return {'ok': False,
                    'message': 'Sensors not responding',
                    'free_space':free}
        elif self.ok is False:
            return {'ok': False,
                    'message': self.message,
                    'free_space':free}
        else:
            return {'ok': True,
                    'message': 'OK',
                    'free_space':free}

    def free_space_verbal(self):
        mb_free = float(self.free_space)
        if mb_free > 1000:
            gb_free = mb_free/1000
            if gb_free > 10:
                return '{} GB'.format(int(gb_free))
            else:
                return '{.1f} GB'.format(gb_free)
        else:
            return '{} MB'.format(mb_free)

    def __str__(self):
        return 'System status'
