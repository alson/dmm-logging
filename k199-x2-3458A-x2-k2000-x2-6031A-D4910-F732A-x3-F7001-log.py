#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'k199-x2-3458A-x2-k2000-x2-6031A-D4910-F732A-x3-F7001-log.csv'
SAMPLE_INTERVAL = 0

FIELDNAMES = ('datetime', 'k199_1_d4910_avg_2', 'k199_2_d4910_avg_3',
              'temp_1', 'last_acal_1', 'last_acal_1_cal72',
              'ag3458a_1_d4910_avg_f732a3', 'temp_2', 'last_acal_2',
              'last_acal_2_cal72', 'ag3458a_2_d4910_avg_f7001',
              'k2000_d4910_avg_f732a1', 'k2000_20_d4910_avg_1',
              'prema6031a_d4910_avg_f732a2')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0

def start_acal_3458a(ag3458a, temp):
    ag3458a._write('ACAL DCV')
    ag3458a.last_acal = datetime.datetime.utcnow()
    ag3458a.last_acal_temp = temp

def finish_acal_3458a(ag3458a):
    ag3458a.last_acal_cal72 = ag3458a._ask('CAL? 72').strip()
    ag3458a._write('DISP OFF,"                 "')

def init_func():
    k199_25 = ivi.keithley.keithley199("TCPIP::gpib1::gpib,25::INSTR",
            reset=True)
    k199_25._interface.timeout = 60
    k199_25.measurement_function = 'dc_volts'
    k199_25.range = 1e-3
    k199_26 = ivi.keithley.keithley199("TCPIP::gpib1::gpib,26::INSTR",
            reset=True)
    k199_26._interface.timeout = 60
    k199_26.measurement_function = 'dc_volts'
    k199_26.range = 1e-3
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    if not DEBUG:
        k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'dc_volts'
    k2000.range = 1e-3
    k2000._write(':VOLT:DC:NPLC 10')
    k2000_20 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,17::INSTR",
            id_query=True)
    if not DEBUG:
        k2000_20._write(':DISPLAY:ENABLE OFF')
    k2000_20.measurement_function = 'dc_volts'
    k2000_20.range = 1e-3
    k2000_20._write(':VOLT:DC:NPLC 10')
    prema6031a = ivi.prema.prema6031A("TCPIP::gpib1::gpib,7::INSTR",
                                      reset=True)
    prema6031a.measurement_function = 'dc_volts'
    prema6031a.range = 1e-3
    prema6031a.advanced.aperture_time = 4
    ag3458a_1 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,21::INSTR",
            reset=True)
    ag3458a_1._interface.timeout = 60
    ag3458a_1.measurement_function = 'dc_volts'
    ag3458a_1.range = 1e-3
    temp_1 = float(ag3458a_1._ask('TEMP?'))
    ag3458a_1.last_temp = datetime.datetime.utcnow()
    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
            reset=True)
    ag3458a_2._interface.timeout = 60
    ag3458a_2.measurement_function = 'dc_volts'
    ag3458a_2.range = 1e-3
    temp_2 = float(ag3458a_2._ask('TEMP?'))
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'test'
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
        # finish_acal_3458a(ag3458a_1)
        # finish_acal_3458a(ag3458a_2)
    else:
        start_acal_3458a(ag3458a_1, temp_1)
        start_acal_3458a(ag3458a_2, temp_2)
        time.sleep(3*60)
        finish_acal_3458a(ag3458a_1)
        finish_acal_3458a(ag3458a_2)
    return {
        'k199_25': k199_25, 'k199_26': k199_26,
        'k2000': k2000, 'k2000_20': k2000_20,
        'ag3458a_1': ag3458a_1, 'ag3458a_2': ag3458a_2,
        'prema6031a': prema6031a,
        }


def loop_func(csvw, k199_25, k199_26, k2000, k2000_20, ag3458a_1, ag3458a_2, prema6031a):
    row = {}
    # ACAL every 24h or 1°C change in internal temperature, per manual
    do_acal_3458a_1 = False
    do_acal_3458a_2 = False
    # Measure temperature every 15 minutes
    temp_1 = None
    temp_2 = None
    if ((datetime.datetime.utcnow() - ag3458a_1.last_temp).total_seconds()
            > 15 * 60):
        temp_1 = float(ag3458a_1._ask('TEMP?'))
        ag3458a_1.last_temp = datetime.datetime.utcnow()

        if ((datetime.datetime.utcnow() - ag3458a_1.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_1.last_acal_temp - temp_1) >= 1):
            do_acal_3458a_1 = True
    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 15 * 60):
        temp_2 = float(ag3458a_2._ask('TEMP?'))
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_2.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_2.last_acal_temp - temp_2) >= 1):
            do_acal_3458a_2 = True
    if do_acal_3458a_1 or do_acal_3458a_2:
        if do_acal_3458a_1:
            start_acal_3458a(ag3458a_1, temp_1)
        if do_acal_3458a_2:
            start_acal_3458a(ag3458a_2, temp_2)
        time.sleep(3*60)
        if do_acal_3458a_1:
            finish_acal_3458a(ag3458a_1)
        if do_acal_3458a_2:
            finish_acal_3458a(ag3458a_2)
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    row['k199_1_d4910_avg_2'] = k199_25.measurement.read(0)
    row['k199_2_d4910_avg_3'] = k199_26.measurement.read(0)
    row['k2000_d4910_avg_f732a1'] = k2000.measurement.fetch(1)
    row['k2000_20_d4910_avg_1'] = k2000_20.measurement.fetch(1)
    row['temp_1'] = temp_1
    row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
    row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
    row['ag3458a_1_d4910_avg_f732a3'] = ag3458a_1.measurement.read(0)
    row['prema6031a_d4910_avg_f732a2'] = prema6031a.measurement.read(0)
    row['temp_2'] = temp_2
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    row['ag3458a_2_d4910_avg_f7001'] = ag3458a_2.measurement.read(0)
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
