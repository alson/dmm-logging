#!/usr/bin/python3

import time
import datetime
import csv
import os
import board
import busio
import adafruit_bme280

OUTPUT_FILE='thp_log.csv'
SAMPLE_INTERVAL=5

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c)
sensor.mode = adafruit_bme280.MODE_FORCE
sensor.overscan_pressure = adafruit_bme280.OVERSCAN_X16
sensor.overscan_humidity = adafruit_bme280.OVERSCAN_X16
sensor.overscan_temperature = adafruit_bme280.OVERSCAN_X16

with open(OUTPUT_FILE, 'a') as csv_file:
    initial_size = os.fstat(csv_file.fileno()).st_size
    csvw = csv.DictWriter(csv_file, fieldnames=('datetime', 'temperature', 'pressure', 'humidity'))
    if initial_size == 0:
        csvw.writeheader()
    while True:
        degrees = sensor.temperature
        pascals = sensor.pressure
        humidity = sensor.humidity
        csvw.writerow({
            'datetime': datetime.datetime.utcnow().isoformat(),
            'temperature': degrees, 
            'pressure': pascals,
            'humidity': humidity,
            })
        time.sleep(SAMPLE_INTERVAL)
