from django.contrib import admin
from .models import Setting, DataPoint, SystemStatus

admin.site.register(Setting)
admin.site.register(DataPoint)
admin.site.register(SystemStatus)
