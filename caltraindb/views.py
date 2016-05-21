#!/usr/bin/env python

from time import strptime, strftime
import simplejson as json

from django.forms.models import model_to_dict
from django.core.serializers import serialize
from django.views.decorators.http import require_GET
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

from caltraindb.models import *

WEEKEND_SERVICE_IDS = (
    'CT-16APR-Caltrain-Saturday-02',
    'CT-16APR-Caltrain-Sunday-02',
)

@require_GET
def stop(request, stop_id):
    stop = Stop.objects.get(stop_id=stop_id)
    payload = {
        'status': '200',
        'stop': model_to_dict(stop),
    }

    return HttpResponse(
        json.dumps(payload, indent=4)
    )

@require_GET
def trip(request):
    start_stop = request.GET.get('start_stop')
    end_stop = request.GET.get('end_stop')
    stated_time = request.GET.get('stated_time')
    weekend = request.GET.get('weekend', False)

    stop_times = list(
            map(
                model_to_dict,
                StopTime.objects \
                    .filter(stop__in=(start_stop, end_stop))
            )
        )

    def filter_weekends(trips):
        if weekend:
            return stop_time['service_id'] in WEEKEND_SERVICE_IDS
        return stop_time['service_id'] not in WEEKEND_SERVICE_IDS

    def format_time(stop_time):
        depart_time = stop_time['departure_time']
        try:
            if int(depart_time[:2]) >= 24:
                depart_time = str(int(depart_time[:2]) - 24) + depart_time[2:]
        except:
            pass
        stop_time['departure_time'] = depart_time
        return stop_time

    def filter_time(stop_time):
        departure_time = stop_time['departure_time']
        return strptime(departure_time, '%H:%M:%S') >= strptime(stated_time, '%H:%M:%S')

    def get_valid_trips(stop_times, valid_trip_ids):
        ht = {}
        for st in stop_times:
            if st['trip'] not in valid_trip_ids:
                continue
            if ht.get(st['trip'], None):
                ht[st['trip']] += 1
            else:
                ht[st['trip']] = 1
        return [trip for trip, x in ht.items() if x == 2]

    stop_times = list(
            filter(filter_time,
                map(format_time, stop_times),
            )
        )

    trips = Trip.objects.exclude(service_id__in=WEEKEND_SERVICE_IDS)
    if weekend:
        trips = Trip.objects.filter(service_id__in=WEEKEND_SERVICE_IDS)
    trip_ids = list(
        map(
            lambda x: x['trip_id'],
            map(
                model_to_dict,
                trips,
            )
        )
    )

    valid_trips = get_valid_trips(stop_times, trip_ids)
    stop_times = list(filter(
        lambda x: x['trip'] in valid_trips,
        stop_times,
    ))

    min_time = min(
        list(
            map(
                lambda x: strptime(x['departure_time'], '%H:%M:%S'),
                stop_times,
            )
        )
    )

    trip_ids = list(
        map(
            lambda x: x['trip'],
            filter(
                lambda x: x['departure_time'] == strftime('%H:%M:%S', min_time),
                stop_times,
            )
        )
    )

    payload = {
        'status': '200',
        'min_time': strftime('%H:%M:%S', min_time),
        'trips': list(filter(lambda x: x['trip_id'] in trip_ids, map(model_to_dict, trips))),
    }

    return HttpResponse(
        json.dumps(payload, indent=4)
    )
