#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
import readline
from enum import Enum, auto
from quantiphy import Quantity

OUTPUT_FILE = 'ks3458a1-dcv-mv-log.csv'
SAMPLE_INTERVAL = 0
FIELDNAMES = ('datetime', 'dut_neg_lead', 'dut_pos_lead', 'ag3458a_1_dcv', 'temp_1', 'last_acal_1',
        'last_acal_1_cal72')
WRITE_INTERVAL_SECONDS = 3600
STABLE_THRESHOLD = 1e-2  # Should be stable within 1%
STABLE_WAIT_TIME_SECONDS = 10

DEBUG = False

class State(Enum):
    WAITING = auto()
    RECORDING = auto()

if DEBUG:
    WRITE_INTERVAL_SECONDS = 0


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.utility.display = 'on'


def ag3458a_high_accuracy(ag3458a):
    ag3458a.is_high_speed = False
    ag3458a.advanced.aperture_time = 100


def ag3458a_high_speed(ag3458a):
    ag3458a.is_high_speed = True
    ag3458a.advanced.aperture_time = 1
    time.sleep(3)


def init_func():
    ag3458a_1 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,21::INSTR",
            reset=True)
    ag3458a_1._interface.timeout = 120
    ag3458a_1._is_high_speed = False
    ag3458a_1.utility.display = 'on'
    ag3458a_1.measurement_function = 'dc_volts'
    ag3458a_1.auto_range = 'on'
    # ag3458a_1.range = 100e-3
    temp_1 = ag3458a_1.utility.temp
    ag3458a_1.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'test'
    else:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        # ag3458a_1.last_acal_cal72 = 'keep'
        acal_3458a(ag3458a_1)
    return {'ag3458a_1': ag3458a_1 }


def read_row(ag3458a_1):
    row = {}
    # ACAL every 24h or 1°C change in internal temperature, per manual
    do_acal_3458a_1 = False
    # Measure temperature every 15 minutes
    temp_1 = None
    if ((datetime.datetime.utcnow() - ag3458a_1.last_temp).total_seconds()
            > 15 * 60):
        temp_1 = ag3458a_1.utility.temp
        ag3458a_1.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_1.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_1.last_acal_temp - temp_1) >= 1):
            do_acal_3458a_1 = True
    if do_acal_3458a_1:
        acal_3458a(ag3458a_1)
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_1.measurement.initiate()
    if not ag3458a_1.is_high_speed:
        time.sleep(SAMPLE_INTERVAL)
    row['ag3458a_1_dcv'] = ag3458a_1.measurement.fetch(0)
    row['temp_1'] = temp_1
    row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
    row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
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
        ag3458a_high_speed(inits['ag3458a_1'])
        last_row = None
        dut_pos_lead = None
        dut_neg_lead = None
        while True:
            row = read_row(**inits)
            print(row['ag3458a_1_dcv'])
            # The 3458A returns 1e38
            if (not last_row) or abs(row['ag3458a_1_dcv']) >= 1e38:
                rel_diff = float('inf')
            else:
                rel_diff = abs((row['ag3458a_1_dcv'] - last_row['ag3458a_1_dcv']) / last_row['ag3458a_1_dcv'])
            if state is State.WAITING:
                if rel_diff < STABLE_THRESHOLD:
                    state = State.RECORDING
                    ag3458a_high_accuracy(inits['ag3458a_1'])
                    if dut_neg_lead:
                        readline.set_startup_hook(lambda: readline.insert_text(dut_neg_lead))
                    dut_neg_lead = input('DUT connected to negative lead: ')
                    if dut_pos_lead:
                        readline.set_startup_hook(lambda: readline.insert_text(dut_pos_lead))
                    dut_pos_lead = input('DUT connected to positive lead: ')
                    readline.set_startup_hook(None)
                    time.sleep(STABLE_WAIT_TIME_SECONDS)
            elif state is State.RECORDING:
                if rel_diff >= STABLE_THRESHOLD:
                    state = State.WAITING
                    ag3458a_high_speed(inits['ag3458a_1'])
                else:
                    row['dut_neg_lead'] = dut_neg_lead
                    row['dut_pos_lead'] = dut_pos_lead
                    csvw.writerow(row)
                    if (datetime.datetime.utcnow() - last_csvw_write) \
                            > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                        csv_file.flush()
                        last_csvw_write = datetime.datetime.utcnow()
            last_row = row
