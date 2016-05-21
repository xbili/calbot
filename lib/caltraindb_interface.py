#!/usr/bin/python
# coding=utf-8

import requests
from datetime import datetime

from lib.utils import convert_time

class CalDbInterface:
    def __init__(self):
        self.prefix = 'http://localhost:8000/caldb'

    def get_trip(self, start_stop, end_stop, stated_time, bullet):
        print('Getting trip')
        params={
            'start_stop': start_stop,
            'end_stop': end_stop,
            'stated_time': convert_time(stated_time),
        }

        # Checks if stated_time is a weekend, actually it's just checking if today is a weekend, amirite?
        if datetime.today().weekday() > 4:
            print('weekend yeah!')
            params['weekend'] = True

        if bullet:
            paramts['bullet'] = True

        r = requests.request(
            'GET',
            self.prefix + '/trip',
            params=params,
        )
        return r.json()
