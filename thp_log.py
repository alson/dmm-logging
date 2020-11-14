#!/usr/bin/python3
from __future__ import print_function

import time
import datetime
import csv
import os
from Adafruit_BME280 import *

OUTPUT_FILE='thp_log.csv'
SAMPLE_INTERVAL=5

sensor = BME280(t_mode=BME280_OSAMPLE_16, p_mode=BME280_OSAMPLE_16, h_mode=BME280_OSAMPLE_16, busnum=2, forced_mode=True)

with open(OUTPUT_FILE, 'a') as csv_file:
    initial_size = os.fstat(csv_file.fileno()).st_size
    csvw = csv.DictWriter(csv_file, fieldnames=('datetime', 'temperature', 'pressure', 'humidity'))
    if initial_size == 0:
        csvw.writeheader()
    while True:
        degrees = sensor.read_temperature()
        pascals = sensor.read_pressure()
        humidity = sensor.read_humidity()
        csvw.writerow({
            'datetime': datetime.datetime.now().isoformat(),
            'temperature': degrees, 
            'pressure': pascals,
            'humidity': humidity,
            })
        time.sleep(SAMPLE_INTERVAL)
