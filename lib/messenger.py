#!/usr/bin/python
# coding=utf-8

import simplejson as json
import time
import requests
from datetime import datetime

PAGE_ACCESS_TOKEN = 'EAADMQn0ZCogcBAOZBTTGmltC53kn73ZCJiHBafudYxD3dkhorAaZCEHnDApYudWOECoXomn3e4szuZA2dHY9UCOeqcnDXhegG8MHX3inYYFNzNhxJeYTEZB5CfEzAWpg3qK9NBhZCxeZCa8L31d0MjGZCjRbEZBXWZCPm0yb7ZBT3gZAA3wZDZD'

"""
Helper methods to generate and send Messenger messages. All new templates
and message types should be defined here.
"""

def _request(method, data):
    params = { 'access_token': PAGE_ACCESS_TOKEN }
    r = requests.request(
        method,
        'https://graph.facebook.com/v2.6/me/messages',
        params=params,
        json=data
    )
    return r.json()

def send_text_message(messenger_id, text):
    messageData = {
        'recipient': {
            'id': str(messenger_id)
        },
        'message': {
            'text': text
        }
    }
    return _request('POST', messageData)

def send_structured_message(messenger_id, data):
    messageData = {
        'recipient': {
            'id': str(messenger_id)
        },
        'message':{
            'attachment': data
        }
    }
    return _request('POST', messageData)

def generate_button_template(text, buttons):
    template = {
        'type': 'template',
        'payload': {
            'template_type': 'button',
            'text': text,
            'buttons': buttons,
        },
    }
    return template

def generate_button(button_type, title, url=None, payload=None):
    button = { 'title': title }
    if button_type == 'url':
        button['type'] = 'web_url'
        button['url'] = url
    elif button_type == 'postback':
        button['type'] = 'postback'
        button['payload'] = payload
    else:
        raise Exception('Invalid button type')
    return button

def get_user_info(messenger_id, fields=[]):
    params = {
        'access_token': PAGE_ACCESS_TOKEN,
        fields: fields
    }
    r = requests.request(
        'GET',
        'https://graph.facebook.com/v2.6/'+ str(messenger_id),
        params=params
    )
    return r.json()
