#!/usr/bin/env python

import time
import simplejson as json
import requests
import logging
logger = logging.getLogger('django')

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

from lib.witbot import WitBot
from lib import messenger
from lib.tokens import *

cached_sessions = {}

def say(session_id, cxt, msg):
    messenger.send_text_message(cxt['messenger_id'], msg)

witbot = WitBot(WITAI_TOKEN, say)

@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        return _get(request)
    else:
        return _post(request)

def _get(request):
    verify_token = request.GET.get('hub.verify_token')
    challenge_code = request.GET.get('hub.challenge')

    if challenge_code and verify_token == 'jarjarbinks':
        return HttpResponse(challenge_code)
    else:
        return HttpResponseNotFound('Missing challenge code.')

def _post(request):
    req = json.loads(request.body)
    messaging_events = req['entry'][0]['messaging']
    request_time = req['entry'][0]['time']
    for event in messaging_events:
        logger.info('Cached sessions:')
        logger.info(json.dumps(cached_sessions, indent=2))
        _handle_message_event(request_time, event)
    return HttpResponse()

def _handle_message_event(request_time, event):
    if event.get('delivery', None):
        logger.info('Message delivered:')
        logger.info(event)
        return

    # Ignore repeated requests in the case of an error
    if request_time - event.get('timestamp') > 6000:
        logger.info('Dropping repeated message')
        return

    sender = event.get('sender')
    sender_id = sender.get('id')

    if event.get('postback', None):
        if event['postback'] == 'yes' or event['postback'] == 'no':
            messenger.send_text_message(sender_id, 'Your wish is my command.')
        else:
            messenger.send_text_message(sender_id, 'All rightttttt')
    else:
        message = event.get('message')
        text = message['text']

        if sender_id:
            updated_context = witbot.chat(sender_id, 'America/Los_Angeles', text, str(int(time.time())), cached_sessions.get(sender_id, {}))
            cached_sessions[sender_id] = updated_context
