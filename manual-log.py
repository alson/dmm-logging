#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
import readline
from enum import Enum, auto

OUTPUT_FILE = 'manual-log.csv'
FIELDNAMES = ('datetime', 'test_instrument', 'setting', 'measurement_unit', 'dut', 'dut_setting', 'value')


def init_func():
    test_instrument = input('Test instrument: ')
    measurement_unit = input('Measurement unit: ')
    return {'test_instrument': test_instrument, 'measurement_unit': measurement_unit}


def read_row(test_instrument, measurement_unit):
    row = {}
    row['value'] = input('Value: ')
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    row['test_instrument'] = test_instrument
    row['measurement_unit'] = measurement_unit
    return row


if __name__ == '__main__':
    inits = init_func()
    readline.parse_and_bind('tab: self-insert')

    last_csvw_write = datetime.datetime(2018, 1, 1)
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        setting = None
        dut = None
        dut_setting = None
        while True:

            if setting:
                readline.set_startup_hook(lambda: readline.insert_text(setting))
            setting = input('Test instrument setting: ')
            if dut:
                readline.set_startup_hook(lambda: readline.insert_text(dut))
            dut = input('DUT: ')
            if dut_setting:
                readline.set_startup_hook(lambda: readline.insert_text(dut_setting))
            dut_setting = input('DUT setting: ')

            readline.set_startup_hook(None)
            row = read_row(**inits)
            row['setting'] = setting
            row['dut'] = dut
            row['dut_setting'] = dut_setting
            csvw.writerow(row)
