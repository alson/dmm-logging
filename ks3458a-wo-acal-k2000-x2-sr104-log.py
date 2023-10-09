#!/usr/bin/python3

import csv
import datetime
import ivi
import time
import os

OUTPUT_FILE = 'ks3458a-wo-acal-k2000-x2-sr104-log.csv'
FIELDNAMES = ('datetime', 'ag3458a_2_ohm', 'ag3458a_2_range', 'ag3458a_2_delay', 'temp_2', 'last_acal_2',
              'last_acal_2_cal72', 'k2000_temp_ohm', 'k2000_20_pt100_ohm')
WRITE_INTERVAL_SECONDS = 900
DEBUG = False
SAMPLE_INTERVAL = 0

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0

def acal_3458a(ag3458a, temp):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ohms()


def ag3458a_setup(ag3458a):
    ag3458a.measurement_function = 'four_wire_resistance'
    ag3458a.advanced.offset_compensation = 'on'
    if DEBUG:
        ag3458a.advanced.offset_compensation = 'off'
        ag3458a.advanced.aperture_time = 1
    ag3458a.auto_range = 'off'
    # 100k
    # ag3458a_2.range = 100e3
    # 10k
    ag3458a.range = 10e3

def init_func():
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    k2000._interface.timeout = 120
    if not DEBUG:
        k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'four_wire_resistance'
    k2000.range = 10e3
    k2000._write(':FRES:NPLC 10')
    k2000_20 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,17::INSTR",
            id_query=True)
    k2000_20._interface.timeout = 120
    if not DEBUG:
        k2000_20._write(':DISPLAY:ENABLE OFF')
    k2000_20.measurement_function = 'four_wire_resistance'
    k2000_20.range = 10e3
    k2000_20._write(':FRES:NPLC 10')

    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
            reset=True)
    ag3458a_2._interface.timeout = 120
    ag3458a_setup(ag3458a_2)
    temp_2 = ag3458a_2.utility.temp
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
        # finish_acal_3458a(ag3458a_2)
    else:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        # ag3458a_2.last_acal_cal72 = 'keep'
        acal_3458a(ag3458a_2, temp_2)
    return {'ag3458a_2': ag3458a_2, 'k2000': k2000, 'k2000_20': k2000_20}


def loop_func(csvw, ag3458a_2, k2000, k2000_20):
    row = {}
    # ACAL every 24h or 1°C change in internal temperature, per manual
    do_acal_3458a_2 = False
    temp_2 = None
    # Measure temperature every 15 minutes
    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 15 * 60):
        temp_2 = ag3458a_2.utility.temp
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_2.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_2.last_acal_temp - temp_2) >= 1):
            do_acal_3458a_2 = True
    if do_acal_3458a_2:
        # acal_3458a(ag3458a_2, temp_2)
        pass
    if temp_2 is not None:
        # if we measured temperature, then skip one conversion
        res = ag3458a_2.measurement.read(360)
        if res is None:
            print('extra temp measurement failed')
        time.sleep(10)
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_2.measurement.initiate()
    # start_time = time.time()
    row['ag3458a_2_ohm'] = ag3458a_2.measurement.fetch(360)
    # print(f'Time to acquire sample: {(time.time() - start_time)} s')
    print(row['ag3458a_2_ohm'])
    if row['ag3458a_2_ohm'] is None:
        print('measurement failed')
    row['temp_2'] = temp_2
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    row['ag3458a_2_range'] = ag3458a_2.range
    row['ag3458a_2_delay'] = ag3458a_2.trigger.delay
    row['k2000_temp_ohm'] = k2000.measurement.fetch(1)
    row['k2000_20_pt100_ohm'] = k2000_20.measurement.fetch(1)

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
