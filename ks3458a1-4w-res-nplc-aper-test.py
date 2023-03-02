#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'ks3458a1-4w-res-nplc-aper-test.csv'
FIELDNAMES = ('datetime', 'ag3458a_1_ohm', 'temp_1', 'last_acal_1',
              'last_acal_1_cal72', 'ag3458a_1_delay', 'ag3458a_1_range', 'ag3458a_1_aper_or_nplc')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False
SWITCH_APER_NPLC_TIME = 3600

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ohms()


def init_func():
    ag3458a_1 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,21::INSTR",
            reset=True)
    ag3458a_1._interface.timeout = 120
    ag3458a_1.measurement_function = 'four_wire_resistance'
    ag3458a_1.range = 10e3
    ag3458a_1.advanced.offset_compensation = 'on'

    temp_1 = float(ag3458a_1._ask('TEMP?'))
    ag3458a_1.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'test'
        #finish_acal_3458a(ag3458a_1)
    else:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'keep'
        # acal_3458a(ag3458a_1)
    return {'ag3458a_1': ag3458a_1 }


def loop_func(csvw, using_nplc, ag3458a_1):
    row = {}
    # ACAL every 24h or 1°C change in internal temperature, per manual
    do_acal_3458a_1 = False
    # Measure temperature every 15 minutes
    temp_1 = None
    if ((datetime.datetime.utcnow() - ag3458a_1.last_temp).total_seconds()
            > 15 * 60):
        temp_1 = float(ag3458a_1._ask('TEMP?'))
        ag3458a_1.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_1.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_1.last_acal_temp - temp_1) >= 1):
            do_acal_3458a_1 = True
    if do_acal_3458a_1:
        # acal_3458a(ag3458a_1)
        pass
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_1.measurement.initiate()
    row['ag3458a_1_ohm'] = ag3458a_1.measurement.fetch(360)
    row['temp_1'] = temp_1
    row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
    row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
    row['ag3458a_1_range'] = ag3458a_1.range
    row['ag3458a_1_delay'] = ag3458a_1.trigger.delay
    row['ag3458a_1_aper_or_nplc'] = 'nplc' if using_nplc else 'aper'
    csvw.writerow(row)
    return row


if __name__ == '__main__':
    inits = init_func()

    last_csvw_write = datetime.datetime(2018,1,1)
    sample_no = 1
    inits['ag3458a_1']._write('NPLC 100')
    using_nplc = True
    last_switch_time = time.time()
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        while True:
            row = loop_func(csvw, using_nplc, **inits)
            print(f"{sample_no:3d}: {row['ag3458a_1_ohm']}")
            sample_no += 1
            if time.time() - last_switch_time > SWITCH_APER_NPLC_TIME:
                using_nplc = not using_nplc
                print(f"Switching to using {'NPLC' if using_nplc else 'APER'}")
                if using_nplc:
                    inits['ag3458a_1']._write('NPLC 100')
                else:
                    inits['ag3458a_1']._write('APER 1')
                last_switch_time = time.time()
            if (datetime.datetime.utcnow() - last_csvw_write) \
                    > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                csv_file.flush()
                last_csvw_write = datetime.datetime.utcnow()
