#!/usr/bin/env python

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bot', include('bot_middleware.urls')),
    url(r'^bot/', include('bot_middleware.urls')),
    url(r'^caldb/', include('caltraindb.urls')),
]
