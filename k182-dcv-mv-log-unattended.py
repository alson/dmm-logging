#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
import readline
from enum import Enum, auto
import argparse

OUTPUT_FILE = 'k182-dcv-mv-log-unattended.csv'
SAMPLE_INTERVAL = 0
FIELDNAMES = ('datetime', 'dut_neg_lead', 'dut_pos_lead', 'k182_dcv')
WRITE_INTERVAL_SECONDS = 3600
STABLE_THRESHOLD = 1e-1  # Should be stable within 10%
ABS_STABLE_THRESHOLD = 2e-6 # Or within 2 uV
STABLE_WAIT_TIME_SECONDS = 10

DEBUG = False

class State(Enum):
    WAITING = auto()
    RECORDING = auto()

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0

def init_func():
    k182 = ivi.keithley.Keithley182("TCPIP::gpib4::gpib0,13::INSTR", reset=True)
    k182._interface.timeout = 120
    # k182.auto_range = 'on'
    k182.range = 1e-3
    return {'k182': k182}


def read_row(k182):
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    k182.measurement.initiate()
    time.sleep(SAMPLE_INTERVAL)
    row['k182_dcv'] = k182.measurement.fetch(0)
    return row


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('output_file_suffix', type=str)
    parser.add_argument('dut_neg_lead', type=str)
    parser.add_argument('dut_pos_lead', type=str)
    args = parser.parse_args()
    if args.output_file_suffix:
        output_file = OUTPUT_FILE.replace('.csv', f'-{args.output_file_suffix}.csv')
    else:
        output_file = OUTPUT_FILE
    inits = init_func()
    readline.parse_and_bind('tab: self-insert')

    last_csvw_write = datetime.datetime(2018,1,1)
    with open(output_file, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        dut_pos_lead = args.dut_pos_lead
        dut_neg_lead = args.dut_neg_lead
        sample_no = 1
        while True:
            start_sample_time = time.time()
            row = read_row(**inits)
            print(f"{sample_no:4d}: {row['k182_dcv']}")
            sample_no += 1
            row['dut_neg_lead'] = dut_neg_lead
            row['dut_pos_lead'] = dut_pos_lead
            csvw.writerow(row)
            if (datetime.datetime.utcnow() - last_csvw_write) \
                    > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                csv_file.flush()
                last_csvw_write = datetime.datetime.utcnow()
            last_row = row
