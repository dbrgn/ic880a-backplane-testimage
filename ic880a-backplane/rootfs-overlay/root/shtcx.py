# -*- coding: utf-8 -*-
"""
SHTC1/SHTC3 module.
The code uses the shtc1 hwmon kernel driver to query the sensor.
"""
from __future__ import print_function, division
from __future__ import absolute_import, unicode_literals

import os.path


DEV_REG = '/sys/bus/i2c/devices/i2c-1/new_device'
DEV_REG_PARAM = b'shtc1 0x70'
DEV_TMP = '/sys/class/hwmon/hwmon0/temp1_input'
DEV_HUM = '/sys/class/hwmon/hwmon0/humidity1_input'


def init():
    if os.path.isfile(DEV_TMP) and os.path.isfile(DEV_HUM):
        print('shtcx: Sensor already registered')
    else:
        with open(DEV_REG, 'wb') as f:
            f.write(DEV_REG_PARAM)
        print('shtcx: Sensor successfully registered in sysfs')


def read():
    # Read values
    with open(DEV_TMP, 'rb') as f:
        val = f.read().strip()
        temperature = float(int(val)) / 1000
    with open(DEV_HUM, 'rb') as f:
        val = f.read().strip()
        humidity = float(int(val)) / 1000
    return (temperature, humidity)
