#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
import readline
from enum import Enum, auto
from quantiphy import Quantity

OUTPUT_FILE = 'k2000-dcv-log.csv'
SAMPLE_INTERVAL = 1
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'k2000_dcv')
WRITE_INTERVAL_SECONDS = 3600
STABLE_THRESHOLD = 1e-3 # Should be stable within 0.1%
MIN_VALUE = 9.9
STABLE_WAIT_TIME_SECONDS = 10

DEBUG = False

class State(Enum):
    WAITING = auto()
    RECORDING = auto()

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0

def k2000_high_accuracy(k2000):
    k2000.is_high_speed = False
    k2000._write(':VOLT:DC:NPLC 10')

def k2000_high_speed(k2000):
    k2000.is_high_speed = True
    k2000._write(':VOLT:DC:NPLC 0.1')

def init_func():
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'dc_volts'
    k2000.range = 10
    k2000._write(':VOLT:DC:NPLC 10')
    return {'k2000': k2000}

def read_row(k2000):
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    if not k2000.is_high_speed:
        time.sleep(SAMPLE_INTERVAL)
    row['k2000_dcv'] = k2000.measurement.fetch(1)
    return row


if __name__ == '__main__':
    inits = init_func()
    readline.parse_and_bind('tab: self-insert')

    last_csvw_write = datetime.datetime(2018,1,1)
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        state = State.WAITING
        k2000_high_speed(inits['k2000'])
        last_row = None
        dut_setting = None
        device_name = None
        sample_no = 1
        while True:
            row = read_row(**inits)
            print(f"{sample_no:3d}: {row['k2000_dcv']}")
            sample_no += 1
            # The 3458A returns 1e38
            if (not last_row) or abs(row['k2000_dcv']) >= 1e38 or abs(row['k2000_dcv']) < MIN_VALUE:
                rel_diff = float('inf')
            else:
                rel_diff = abs((row['k2000_dcv'] - last_row['k2000_dcv']) / last_row['k2000_dcv'])
            if state is State.WAITING:
                if rel_diff < STABLE_THRESHOLD:
                    state = State.RECORDING
                    k2000_high_accuracy(inits['k2000'])
                    quant = Quantity(row["k2000_dcv"], "V")
                    dut_setting_guess = f'{quant:.2q}'
                    if device_name:
                        readline.set_startup_hook(lambda: readline.insert_text(device_name))
                    device_name = input('Name of device under test: ')
                    readline.set_startup_hook(lambda: readline.insert_text(dut_setting_guess))
                    dut_setting = input('DUT setting: ')
                    readline.set_startup_hook(None)
                    time.sleep(STABLE_WAIT_TIME_SECONDS)
                    sample_no = 1
            elif state is State.RECORDING:
                if rel_diff >= STABLE_THRESHOLD:
                    state = State.WAITING
                    k2000_high_speed(inits['k2000'])
                    sample_no = 1
                else:
                    row['dut'] = device_name
                    row['dut_setting'] = dut_setting
                    csvw.writerow(row)
                    if (datetime.datetime.utcnow() - last_csvw_write) \
                            > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                        csv_file.flush()
                        last_csvw_write = datetime.datetime.utcnow()
            last_row = row
