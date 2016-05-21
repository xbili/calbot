#!/usr/bin/python
# coding=utf-8

import requests

from lib.utils import convert_time

class CalDbInterface:
    def __init__(self):
        self.prefix = 'http://localhost:8000/caldb'

    def get_trip(self, start_stop, end_stop, stated_time):
        print('Getting trip')
        r = requests.request(
            'GET',
            self.prefix + '/trip',
            params={
                'start_stop': start_stop,
                'end_stop': end_stop,
                'stated_time': convert_time(stated_time),
            },
        )
        return r.json()
