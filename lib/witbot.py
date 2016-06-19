#!/usr/bin/python
# coding=utf-8

import logging
import simplejson as json
from wit import Wit
logger = logging.getLogger('django')

from lib import messenger
from lib.caltraindb_interface import CalDbInterface

station_mapping = {
    'Redwood City': '70142',
    'Lawrence': '70232',
    'Sunnyvale': '70222',
}

class WitBot():
    def __init__(self, witai_key, say_func):
        actions = {
            'say': say_func,
            'merge': self.merge,
            'error': self.error,
            'get_trip': self.get_trip,
            'clear_context': self.clear_context,
        }
        self._wit_client = Wit(witai_key, actions)
        self._caldb = CalDbInterface()

    def chat(self, username, timezone, input_msg, session_id, context={}):
        if 'messenger_id' not in context:
            context['messenger_id'] = username

        if 'timezone' not in context:
            context['timezone'] = 'America/Los_Angeles'

        context = self._wit_client.run_actions(session_id, input_msg, context)
        return context

    def merge(self, session_id, cxt, entities, msg):
        logger.info(json.dumps(cxt, indent=4))
        for name, vals in entities.items():
            if name == 'caltrain_station_start':
                cxt['start_stop'] = vals[0]
            elif name == 'caltrain_station_end':
                cxt['end_stop'] = vals[0]
            elif name == 'datetime':
                cxt['stated_time'] = vals[0]

        return cxt

    def error(self, session_id, cxt, e):
        logger.error('Wit.ai error occurred.')
        raise e

    def clear_context(self, session_id, cxt):
        new_cxt = {
            'messenger_id': cxt['messenger_id'],
            'timezone': cxt['timezone'],
        }
        return new_cxt

    def get_trip(self, session_id, cxt):
        stated_time = cxt.get('stated_time')['value']
        start_stop = cxt.get('start_stop')['value']
        end_stop = cxt.get('end_stop')['value']
        bullet = cxt.get('bullet')

        start_stop = station_mapping.get(start_stop)
        end_stop = station_mapping.get(end_stop)

        trip = self._caldb.get_trip(start_stop, end_stop, stated_time, bullet)

        cxt['train_time'] = trip['min_time']
        return cxt
