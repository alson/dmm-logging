#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
import readline

OUTPUT_FILE = 'ks3458a-dcv-tc-log-w-acal.csv'
SAMPLE_INTERVAL = 10
FIELDNAMES = ('datetime', 'ag3458a_2_dcv', 'temp_2', 'last_acal_2', 'last_acal_2_cal72')
WRITE_INTERVAL_SECONDS = 900
STABLE_WAIT_TIME_SECONDS = 10

DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def acal_3458a(ag3458a, temp):
    ag3458a.acal.start_dcv()


def init_func():
    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
            reset=True)
    ag3458a_2._interface.timeout = 120
    ag3458a_2.measurement_function = 'dc_volts'
    ag3458a_2.range = 10
    temp_2 = ag3458a_2.utility.temp
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'keep'
    else:
        acal_3458a(ag3458a_2, temp_2)
    return {'ag3458a_2': ag3458a_2 }


def loop_func(csvw, ag3458a_2):
    row = {}
    # ACAL every 24h or 1°C change in internal temperature, per manual
    do_acal_3458a_2 = False
    # Measure temperature every 15 minutes
    temp_2 = None
    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 15 * 60):
        temp_2 = float(ag3458a_2._ask('TEMP?'))
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_2.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_2.last_acal_temp - temp_2) >= 1):
            do_acal_3458a_2 = True
    if do_acal_3458a_2:
        acal_3458a(ag3458a_2, temp_2)
        # pass
    if temp_2 is not None:
        # if we measured temperature, then skip one conversion
        res = ag3458a_2.measurement.read(360)
        if res is None:
            print('extra temp measurement failed')
        time.sleep(10)
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_2.measurement.initiate()
    time.sleep(SAMPLE_INTERVAL)
    row['ag3458a_2_dcv'] = ag3458a_2.measurement.fetch(0)
    row['temp_2'] = temp_2
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    print(row['ag3458a_2_dcv'])
    csvw.writerow(row)


if __name__ == '__main__':
    inits = init_func()
    readline.parse_and_bind('tab: self-insert')

    last_csvw_write = datetime.datetime(2018,1,1)
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
