#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'w4920-acv-log.csv'
SAMPLE_INTERVAL = 10
FIELDNAMES = ('datetime', 'w4920_acv', 'w4920_freq')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def init_func():
    w4920 = ivi.datron_wavetek.wavetek4920("TCPIP::gpib4::gpib0,4::INSTR",
                                           reset=True)
    w4920._interface.timeout = 120
    w4920.measurement_function = 'ac_volts'
    w4920.range = 10
    w4920.ac.frequency_min = 100
    return {'w4920': w4920}


loop_count = 0


def loop_func(csvw, w4920):
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    w4920.measurement.initiate()
    time.sleep(10)
    row['w4920_acv'] = w4920.measurement.fetch(0)
    row['w4920_freq'] = None
    print(f"{row['w4920_acv']} V, {row['w4920_freq']} Hz")
    csvw.writerow(row)


if __name__ == '__main__':
    inits = init_func()

    last_csvw_write = datetime.datetime(2018, 1, 1)
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        while True:
            loop_func(csvw, **inits)
            time.sleep(SAMPLE_INTERVAL)
            if (datetime.datetime.utcnow() - last_csvw_write) \
                    > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                csv_file.flush()
                last_csvw_write = datetime.datetime.utcnow()
