#!/usr/bin/env python

"""
Author: Bili Xu
## Schedule Parser Script ##

Script that fetches the latest data from Caltrain Developer GTFS and parses the
required data into a Python dictionary.

Only parses the `routes`, `stops`, `stop_times` and `trips` data.

Result is a dictionary of 2D arrays.

To be run as a cronjob every week.
"""

import os
import io
import csv
import requests
import zipfile

from caltraindb.models import *


CALTRAIN_GTFS_URL = 'http://www.caltrain.com/Assets/GTFS/caltrain/Caltrain-GTFS.zip'
SCHEDULE_PATH = os.path.dirname(os.path.abspath(__file__)) + '/schedules'

def get_parsed_schedule():
    r = requests.get(CALTRAIN_GTFS_URL)
    z = zipfile.ZipFile(io.BytesIO(r.content))

    required_files = ('routes.txt', 'stops.txt', 'stop_times.txt', 'trips.txt')

    results = {
        'routes': [],
        'stops': [],
        'stop_times': [],
        'trips': [],
    }

    curr_data = ''
    for name in z.namelist():
        if not name.endswith(required_files):
            continue

        for k in results:
            if k in name:
                curr_data = k

        with open(SCHEDULE_PATH + '/' + name, newline='') as f:
            reader = csv.reader(f, delimiter=',')
            next(reader) # Skip the header line
            for row in reader:
                results[curr_data].append(row)

    return results
