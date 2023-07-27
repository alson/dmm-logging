#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'ks3458a1-w4920-acv-log.csv'
SAMPLE_INTERVAL = 10
FIELDNAMES = ('datetime', 'ag3458a_1_acv', 'temp_1', 'last_acal_1',
        'last_acal_1_cal72', 'w4920_acv')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ac()


def init_func():
    ag3458a_1 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,21::INSTR",
            reset=True)
    ag3458a_1._interface.timeout = 120
    ag3458a_1.measurement_function = 'ac_volts_sync'
    ag3458a_1.range = 10
    w4920 = ivi.datron_wavetek.wavetek4920("TCPIP::gpib4::gpib0,4::INSTR",
                                           reset=True)
    w4920._interface.timeout = 120
    w4920.measurement_function = 'ac_volts'
    w4920.range = 10
    w4920.ac.frequency_min = 100
    temp_1 = ag3458a_1.utility.temp
    ag3458a_1.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'test'
    else:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        # ag3458a_1.last_acal_cal72 = 'keep'
        acal_3458a(ag3458a_1)
    return {'ag3458a_1': ag3458a_1, 'w4920': w4920}


loop_count = 0


def loop_func(csvw, ag3458a_1, w4920):
    global loop_count
    loop_count += 1
    # if loop_count % 60 == 0:
    #     ag3458a_2.range = 10e3
    #     temp_1 = ag3458a_1.utility.temp
    #     acal_3458a(ag3458a_2, temp_1)
    row = {}
    # ACAL every 24h or 1°C change in internal temperature, per manual
    do_acal_3458a_1 = False
    # Measure temperature every 15 minutes
    temp_1 = None
    if ((datetime.datetime.utcnow() - ag3458a_1.last_temp).total_seconds()
            > 15 * 60):
        temp_1 = ag3458a_1.utility.temp
        ag3458a_1.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_1.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_1.last_acal_temp - temp_1) >= 1):
            do_acal_3458a_1 = True
    if do_acal_3458a_1:
        # acal_3458a(ag3458a_1)
        pass
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_1.measurement.initiate()
    w4920.measurement.initiate()
    time.sleep(70)
    row['ag3458a_1_acv'] = ag3458a_1.measurement.fetch(0)
    row['temp_1'] = temp_1
    row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
    row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
    row['w4920_acv'] = w4920.measurement.fetch(0)
    print(row['ag3458a_1_acv'], row['w4920_acv'])
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
