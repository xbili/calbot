#!/usr/bin/python
# coding=utf-8

import os

ENVIRONMENT = os.environ.get('ENV')
WITAI_TOKEN = '' # Set local wit.ai token

if ENVIRONMENT == 'prod':
    WITAI_TOKEN = os.environ.get('WITAI_TOKEN')
