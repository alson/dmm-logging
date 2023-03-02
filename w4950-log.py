#!/usr/bin/python3
import argparse

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'w4950-log.csv'
SAMPLE_INTERVAL = 0
FIELDNAMES = ('datetime', 'w4950_function', 'w4950_range', 'w4950_percentage', 'w4950_freq', 'w4950_value',
              'w4950_nsamples', 'w4950_std_abs', 'dut')
WRITE_INTERVAL_SECONDS = 3600
DEBUG = False

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def init_func(function, range_, percentage, freq):
    w4950 = ivi.datron_wavetek.wavetek4950("TCPIP::gpib4::gpib0,20::INSTR", reset=True)
    w4950._interface.timeout = 120
    w4950.measurement_function = function
    w4950.range = range_
    w4950.measurement.percentage = percentage
    if freq:
        w4950.ac.frequency_min = freq
    w4950.measurement.guard = 'remote'
    return {'w4950': w4950}


loop_count = 0


def loop_func(csvw, dut, w4950):
    global loop_count
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    row['dut'] = dut
    w4950.measurement.initiate()
    row['w4950_function'] = w4950.measurement_function
    row['w4950_range'] = w4950.range
    row['w4950_percentage'] = w4950.measurement.percentage
    row['w4950_value'] = w4950.measurement.fetch(60)
    row['w4950_nsamples'] = w4950.measurement.quality.nsamples
    row['w4950_std_abs'] = w4950.measurement.quality.absolute
    if w4950.measurement_function in ('ac_volts', 'ac_current'):
        row['w4950_freq'] = w4950.measurement.freq
    else:
        row['w4950_freq'] = None
    print(f"{loop_count}: {row['w4950_value']} V/Ohm/A, {row['w4950_freq']} Hz")
    csvw.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Log Wavetek 4950 measurements')
    parser.add_argument('dut', type=str)
    parser.add_argument('function', type=str)
    parser.add_argument('range', type=float)
    parser.add_argument('percentage', type=int)
    parser.add_argument('nreadings', type=int)
    parser.add_argument('freq', type=float, default=0.0)

    args = parser.parse_args()

    inits = init_func(args.function, args.range, args.percentage, args.freq)

    if args.function in ('dc_volts', 'two_wire_resistance', 'four_wire_resistance', 'dc_current'):
        print("Please connect the cable for zero:")
        if args.function == 'dc_volts':
            print("Black into the back of Red, all others disconnected")
        elif args.function in ('two_wire_resistance', 'four_wire_resistance'):
            print("Brown into Blue into Black Into Red, white remains disconnected")
        elif args.function == 'dc_current':
            print("All 4mm leads disconnected from one another")
        response = input('Press enter to zero')
        print("Zeroing...")
        inits['w4950'].utility.zero()
        print("Zeroed. Connect the cable to measure")
        response = input('Press enter to continue')

    last_csvw_write = datetime.datetime(2018, 1, 1)
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        while loop_count < args.nreadings:
            loop_func(csvw, args.dut, **inits)
            loop_count += 1
            time.sleep(SAMPLE_INTERVAL)
            if (datetime.datetime.utcnow() - last_csvw_write) \
                    > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                csv_file.flush()
                last_csvw_write = datetime.datetime.utcnow()
