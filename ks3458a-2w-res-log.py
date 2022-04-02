#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
import readline
from enum import Enum, auto
from quantiphy import Quantity

OUTPUT_FILE = 'ks3458a-2w-res-log.csv'
SAMPLE_INTERVAL = 10
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'ag3458a_2_ohm', 'temp_2', 'last_acal_2',
        'last_acal_2_cal72')
WRITE_INTERVAL_SECONDS = 3600
STABLE_THRESHOLD = 1e-3 # Should be stable within 0.1%
STABLE_WAIT_TIME_SECONDS = 10

DEBUG = True

class State(Enum):
    WAITING = auto()
    RECORDING = auto()

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

def acal_3458a(ag3458a, temp):
    start_acal_3458a_ohms(ag3458a, temp)
    time.sleep(12*60)
    finish_acal_3458a(ag3458a)

def ag3458a_high_accuracy(ag3458a):
    ag3458a._is_high_speed = False
    ag3458a._write('OCOMP OFF; DELAY 1; NDIG 9; NPLC 100')

def ag3458a_high_speed(ag3458a):
    ag3458a._is_high_speed = True
    ag3458a._write('OCOMP OFF; DELAY 0; NPLC 1')
    time.sleep(3)

def init_func():
    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
            reset=True)
    ag3458a_2._interface.timeout = 30
    ag3458a_2._is_high_speed = False
    ag3458a_2._write('DISP ON')
    ag3458a_2.measurement_function = 'two_wire_resistance'
    ag3458a_2.auto_range = 'on'
    # ag3458a_2.range = 100e3
    temp_2 = float(ag3458a_2._ask('TEMP?'))
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
        #finish_acal_3458a(ag3458a_2)
    else:
        acal_3458a(ag3458a_2, temp_2)
    return {'ag3458a_2': ag3458a_2 }

def read_row(ag3458a_2):
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
    if not ag3458a_2._is_high_speed:
        time.sleep(SAMPLE_INTERVAL)
    row['ag3458a_2_ohm'] = ag3458a_2.measurement.fetch(0)
    row['temp_2'] = temp_2
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    return row


if __name__ == '__main__':
    inits = init_func()
    readline.parse_and_bind('tab: self-insert')

    last_csvw_write = datetime.datetime(2018,1,1)
    with open(OUTPUT_FILE, 'a') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        state = State.WAITING
        ag3458a_high_speed(inits['ag3458a_2'])
        last_row = None
        dut_setting = None
        device_name = None
        while True:
            row = read_row(**inits)
            print(row['ag3458a_2_ohm'])
            # The 3458A returns 1e38
            if (not last_row) or abs(row['ag3458a_2_ohm']) >= 1e38:
                rel_diff = float('inf')
            else:
                rel_diff = abs((row['ag3458a_2_ohm'] - last_row['ag3458a_2_ohm']) / last_row['ag3458a_2_ohm'])
            if state is State.WAITING:
                if rel_diff < STABLE_THRESHOLD:
                    state = State.RECORDING
                    ag3458a_high_accuracy(inits['ag3458a_2'])
                    quant = Quantity(row["ag3458a_2_ohm"], "Ohm")
                    dut_setting_guess = f'{quant:.2q}'
                    if device_name:
                        readline.set_startup_hook(lambda: readline.insert_text(device_name))
                    device_name = input('Name of device under test: ')
                    readline.set_startup_hook(lambda: readline.insert_text(dut_setting_guess))
                    dut_setting = input('DUT setting: ')
                    readline.set_startup_hook(None)
                    time.sleep(STABLE_WAIT_TIME_SECONDS)
            elif state is State.RECORDING:
                if rel_diff >= STABLE_THRESHOLD:
                    state = State.WAITING
                    ag3458a_high_speed(inits['ag3458a_2'])
                else:
                    row['dut'] = device_name
                    row['dut_setting'] = dut_setting
                    csvw.writerow(row)
                    if (datetime.datetime.utcnow() - last_csvw_write) \
                            > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                        csv_file.flush()
                        last_csvw_write = datetime.datetime.utcnow()
            last_row = row
