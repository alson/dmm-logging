#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'ks3458a-k2000-transfer-sr104-log.csv'
FIELDNAMES = ('datetime', 'ag3458a_2_ohm', 'temp_2', 'last_acal_2',
        'last_acal_2_cal72', 'k2000_temp_ohm')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0

def acal_3458a(ag3458a, temp):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ohms()
    ag3458a.utility.display = 'on'


def init_func():
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    if not DEBUG:
        k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'four_wire_resistance'
    k2000.range = 10e3
    k2000._write(':FRES:NPLC 10')

    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
            reset=True)
    ag3458a_2.measurement_function = 'four_wire_resistance'

    ag3458a_2.advanced.offset_compensation = 'on'
    # 100k
    # ag3458a_2.range = 100e3
    # 10k
    ag3458a_2.range = 10e3
    ag3458a_2.trigger_delay = 1
    temp_2 = ag3458a_2.utility.temp
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
        #finish_acal_3458a(ag3458a_2)
    else:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        # ag3458a_2.last_acal_cal72 = 'keep'
        acal_3458a(ag3458a_2, temp_2)
    return {'ag3458a_2': ag3458a_2, 'k2000': k2000}


loop_count = 0


def loop_func(csvw, ag3458a_2, k2000):
    global loop_count
    loop_count += 1
    # if loop_count % 60 == 0:
    #     ag3458a_2.range = 10e3
    #     temp_2 = ag3458a_2.utility.temp
    #     acal_3458a(ag3458a_2, temp_2)
    row = {}
    # ACAL every 24h or 1°C change in internal temperature, per manual
    do_acal_3458a_2 = False
    # Measure temperature every 15 minutes
    temp_2 = None
    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 15 * 60):
        temp_2 = ag3458a_2.utility.temp
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_2.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_2.last_acal_temp - temp_2) >= 1):
            do_acal_3458a_2 = True
    if do_acal_3458a_2:
        acal_3458a(ag3458a_2, temp_2)
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_2.measurement.initiate()
    row['ag3458a_2_ohm'] = ag3458a_2.measurement.fetch(150)
    row['temp_2'] = temp_2
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    row['k2000_temp_ohm'] = k2000.measurement.fetch(1)
    print(row['ag3458a_2_ohm'])
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
