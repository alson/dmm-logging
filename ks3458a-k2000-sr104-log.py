#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'ks3458a-k2000-sr104-log.csv'
SAMPLE_INTERVAL = 0
FIELDNAMES = ('datetime', 'ag3458a_2_ohm', 'temp_2', 'last_acal_2',
        'last_acal_2_cal72', 'k2000_temp_ohm')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def start_acal_3458a_dcv(ag3458a, temp):
    ag3458a._write('ACAL DCV')
    ag3458a.last_acal = datetime.datetime.utcnow()
    ag3458a.last_acal_temp = temp


def start_acal_3458a_ohms(ag3458a, temp):
    ag3458a._write('ACAL OHMS')


def finish_acal_3458a(ag3458a):
    ag3458a.last_acal_cal72 = ag3458a._ask('CAL? 72').strip()
    ag3458a._write('DISP OFF,"                 "')


def acal_3458a(ag3458a, temp):
    start_acal_3458a_dcv(ag3458a, temp)
    time.sleep(3*60)
    check_3458a_error(ag3458a)
    start_acal_3458a_ohms(ag3458a, temp)
    time.sleep(12*60)
    check_3458a_error(ag3458a)
    finish_acal_3458a(ag3458a)


def check_3458a_error(ag3458a):
    errstr = ag3458a._ask('ERRSTR?')
    if errstr != '0,"NO ERROR"':
        ag3458a._ask('ERR?')
        raise IOError(errstr)


def init_func():
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'four_wire_resistance'
    k2000.range = 10e3
    k2000._write(':FRES:NPLC 10')

    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
            reset=True)
    ag3458a_2.measurement_function = 'four_wire_resistance'
    ag3458a_2.range = 10e3
    ag3458a_2._write('OCOMP ON')
    ag3458a_2._write('DELAY 3')
    temp_2 = float(ag3458a_2._ask('TEMP?'))
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
        #finish_acal_3458a(ag3458a_2)
    else:
        acal_3458a(ag3458a_2, temp_2)
    return {'ag3458a_2': ag3458a_2, 'k2000': k2000}


def loop_func(csvw, ag3458a_2, k2000):
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
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_2.measurement.initiate()
    time.sleep(70)
    row['ag3458a_2_ohm'] = ag3458a_2.measurement.fetch(0)
    row['temp_2'] = temp_2
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    row['k2000_temp_ohm'] = k2000.measurement.fetch(1)
    csvw.writerow(row)


if __name__ == '__main__':
    inits = init_func()

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
