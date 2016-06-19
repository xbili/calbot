#!/usr/bin/python
# coding=utf-8

import requests
from datetime import datetime

from lib.utils import convert_time

class CalDbInterface:
    def __init__(self):
        self.prefix = 'https://calbot.xbili.com/caldb'

    def get_trip(self, start_stop, end_stop, stated_time, bullet):
        print('Getting trip')
        params={
            'start_stop': start_stop,
            'end_stop': end_stop,
            'stated_time': convert_time(stated_time),
        }

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
