#!/usr/bin/python3

import argparse
import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'k2000-20-4w-res-log.csv'
SAMPLE_INTERVAL = 10
FIELDNAMES = ('datetime', 'k2000_ohm', 'dut', 'dut_setting')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def init_func():
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,17::INSTR",
            id_query=True)
    k2000._interface.timeout = 120
    k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'four_wire_resistance'
    k2000.range = 110
    k2000._write(':FRES:NPLC 10')
    return {'k2000': k2000}


def loop_func(csvw, dut, dut_setting, k2000):
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    row['dut'] = dut
    row['dut_setting'] = dut_setting
    row['k2000_ohm'] = k2000.measurement.fetch(1)
    print(row['k2000_ohm'])
    csvw.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log Keithley 2000 4W resistance')
    parser.add_argument('dut', type=str)
    parser.add_argument('dut_setting', type=str, default='', nargs='?')

    args = parser.parse_args()
    inits = init_func()

    last_csvw_write = datetime.datetime(2018, 1, 1)
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        while True:
            loop_func(csvw, args.dut, args.dut_setting, **inits)
            time.sleep(SAMPLE_INTERVAL)
            if (datetime.datetime.utcnow() - last_csvw_write) \
                    > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                csv_file.flush()
                last_csvw_write = datetime.datetime.utcnow()
