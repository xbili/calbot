#!/usr/bin/env python

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^stop/(?P<stop_id>[\d\w.@-]+)', views.stop, name='stop'),
    url(r'^trip$', views.trip, name='trip'),
]
