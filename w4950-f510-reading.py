#!/usr/bin/python3
from typing import List

import ivi
import datetime
import csv
import os

from common_step_execution import DcVoltageCommand, DcVoltageDutSettings, Step, run_procedure, AcVoltageDutSettings, AcVoltageCommand, beep, check_valid_value, Instrument

OUTPUT_FILE = 'w4950-f510-reading.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'w4950_function', 'w4950_range', 'w4950_percentage', 'w4950_freq',
              'w4950_value', 'w4950_nsamples', 'w4950_std_abs', 'w4950_temp')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 12
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    Step('F7001', '10 V', DcVoltageDutSettings(range=10, value=10), 'w4950', DcVoltageCommand(10), True),
    Step('F7001', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'w4950', DcVoltageCommand(10), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'w4950', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'w4950', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'w4950', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('F7001', '10 V', DcVoltageDutSettings(range=10, value=10), 'w4950', DcVoltageCommand(10), True),
    Step('F7001', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'w4950', DcVoltageCommand(10), True),
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
    w4950 = ivi.datron_wavetek.wavetek4950("TCPIP::gpib4::gpib0,20::INSTR", reset=True)
    w4950._interface.timeout = 120
    w4950.last_temp = datetime.datetime.utcnow()
    w4950.measurement.band_limits = 'off'
    w4950.measurement.guard = 'remote'
    print("Please connect the cable for zero:")
    print("Black into the back of Red, all others disconnected")
    response = input('Press enter to zero')
    print("Zeroing...")
    w4950.utility.zero()
    print("Zeroed. Connect the cable to measure")
    return {'w4950': w4950}


def read_row(inits, instruments: List[Instrument], **kwargs):
    w4950 = inits['w4950']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    if ((datetime.datetime.utcnow() - w4950.last_temp).total_seconds()
            > 30 * 60):
        row['w4950_temp'] = w4950.measurement.temp.internal
    w4950.measurement.initiate()
    row['w4950_function'] = w4950.measurement_function
    row['w4950_range'] = w4950.range
    row['w4950_percentage'] = w4950.measurement.percentage
    row['w4950_value'] = w4950.measurement.fetch(60)
    row['w4950_nsamples'] = w4950.measurement.quality.nsamples
    row['w4950_std_abs'] = w4950.measurement.quality.absolute
    print(f"{row['w4950_value']}", end='')
    if w4950.measurement_function in ('ac_volts', 'ac_current'):
        row['w4950_freq'] = w4950.measurement.freq
        print(f", freq: {row['w4950_freq']}")
    else:
        row['w4950_freq'] = None
        print()
    check_valid_value(w4950, row['w4950_value'])
    return row, True


if __name__ == '__main__':
    main()
