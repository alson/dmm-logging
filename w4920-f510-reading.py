#!/usr/bin/python3
import time

import ivi
import datetime
import csv
import os

from common_step_execution import Step, run_procedure, AcVoltageDutSettings, AcVoltageCommand, check_valid_value

OUTPUT_FILE = 'w4920-f510-reading.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'w4920_function', 'w4920_range', 'w4920_freq',
              'w4920_value')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 57
STEP_SOAK_TIME = 12
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'w4920', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'w4920', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'w4920', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4920', AcVoltageCommand(10, freq=2.4e3), True),
]


def main():
    inits = init_func()
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        run_procedure(csvw, procedure, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)


def init_func():
    w4920 = ivi.datron_wavetek.wavetek4920("TCPIP::gpib4::gpib0,4::INSTR", reset=True)
    w4920._interface.timeout = 120
    return {'w4920': w4920}


def read_row(inits, instruments, **kwargs):
    w4920 = inits['w4920']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    w4920.measurement.initiate()
    row['w4920_function'] = w4920.measurement_function
    row['w4920_range'] = w4920.range
    time.sleep(4)
    row['w4920_value'] = w4920.measurement.fetch(0)
    print(f"{row['w4920_value']}", end='')
    if w4920.measurement_function in ('ac_volts', 'ac_millivolts'):
        row['w4920_freq'] = w4920.measurement.freq
        print(f", freq: {row['w4920_freq']} Hz")
    else:
        row['w4920_freq'] = None
        print()
    check_valid_value(w4920, row['w4920_value'])
    return row, True


if __name__ == '__main__':
    main()
