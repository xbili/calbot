#!/usr/bin/python
# coding=utf-8

from time import strftime, strptime

def convert_time(time):
    time_inst = strptime(time, '%Y-%m-%dT%H:%M:%S.000-07:00')
    return strftime('%H:%M:%S', time_inst)
