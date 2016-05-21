from django.contrib import admin

from caltraindb.models import *

# Register your models here.
admin.site.register(Route)
admin.site.register(Stop)
admin.site.register(StopTime)
admin.site.register(Trip)
