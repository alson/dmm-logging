#!/usr/bin/python3
from typing import List

import ivi
import datetime
import csv
import os

from common_step_execution import Step, run_procedure, AcVoltageDutSettings, AcVoltageCommand, beep, check_valid_value, Instrument

OUTPUT_FILE = 'w4950-v2703-acv-sweep.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'w4950_function', 'w4950_range', 'w4950_percentage', 'w4950_freq',
              'w4950_value', 'w4950_nsamples', 'w4950_std_abs', 'w4950_temp')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 60
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    Step('Valhalla 2703', '100 mV 20 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20), 'w4950', AcVoltageCommand(100e-3, freq=20), True),
    Step('Valhalla 2703', '1 V 20 Hz', AcVoltageDutSettings(range=1, value=1, freq=20), 'w4950', AcVoltageCommand(1, freq=20), True),
    Step('Valhalla 2703', '10 V 20 Hz', AcVoltageDutSettings(range=10, value=10, freq=20), 'w4950', AcVoltageCommand(10, freq=20), True),
    Step('Valhalla 2703', '100 V 20 Hz', AcVoltageDutSettings(range=100, value=100, freq=20), 'w4950', AcVoltageCommand(100, freq=20), True),
    Step('Valhalla 2703', '1000 V 20 Hz', AcVoltageDutSettings(range=1000, value=1000, freq=20), 'w4950', AcVoltageCommand(1000, freq=20), True),
    Step('Valhalla 2703', '1000 V 55 Hz', AcVoltageDutSettings(range=1000, value=1000, freq=55), 'w4950', AcVoltageCommand(1000, freq=55), True),
    Step('Valhalla 2703', '100 V 55 Hz', AcVoltageDutSettings(range=100, value=100, freq=55), 'w4950', AcVoltageCommand(100, freq=55), True),
    Step('Valhalla 2703', '10 V 55 Hz', AcVoltageDutSettings(range=10, value=10, freq=55), 'w4950', AcVoltageCommand(10, freq=55), True),
    Step('Valhalla 2703', '1 V 55 Hz', AcVoltageDutSettings(range=1, value=1, freq=55), 'w4950', AcVoltageCommand(1, freq=55), True),
    Step('Valhalla 2703', '100 mV 55 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=55), 'w4950', AcVoltageCommand(100e-3, freq=55), True),
    Step('Valhalla 2703', '100 mV 300 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=300), 'w4950', AcVoltageCommand(100e-3, freq=300), True),
    Step('Valhalla 2703', '1 V 300 Hz', AcVoltageDutSettings(range=1, value=1, freq=300), 'w4950', AcVoltageCommand(1, freq=300), True),
    Step('Valhalla 2703', '10 V 300 Hz', AcVoltageDutSettings(range=10, value=10, freq=300), 'w4950', AcVoltageCommand(10, freq=300), True),
    Step('Valhalla 2703', '100 V 300 Hz', AcVoltageDutSettings(range=100, value=100, freq=300), 'w4950', AcVoltageCommand(100, freq=300), True),
    Step('Valhalla 2703', '1000 V 300 Hz', AcVoltageDutSettings(range=1000, value=1000, freq=300), 'w4950', AcVoltageCommand(1000, freq=300), True),
    Step('Valhalla 2703', '1000 V 1 kHz', AcVoltageDutSettings(range=1000, value=1000, freq=1e3), 'w4950', AcVoltageCommand(1000, freq=1e3), True),
    Step('Valhalla 2703', '100 V 1 kHz', AcVoltageDutSettings(range=100, value=100, freq=1e3), 'w4950', AcVoltageCommand(100, freq=1e3), True),
    Step('Valhalla 2703', '10 V 1 kHz', AcVoltageDutSettings(range=10, value=10, freq=1e3), 'w4950', AcVoltageCommand(10, freq=1e3), True),
    Step('Valhalla 2703', '19 V 1 kHz', AcVoltageDutSettings(range=10, value=19, freq=1e3), 'w4950', AcVoltageCommand(19, freq=1e3), True),
    Step('Valhalla 2703', '1 V 1 kHz', AcVoltageDutSettings(range=1, value=1, freq=1e3), 'w4950', AcVoltageCommand(1, freq=1e3), True),
    Step('Valhalla 2703', '100 mV 1 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=1e3), 'w4950', AcVoltageCommand(100e-3, freq=1e3), True),
    Step('Valhalla 2703', '100 mV 10 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=10e3), 'w4950', AcVoltageCommand(100e-3, freq=10e3), True),
    Step('Valhalla 2703', '1 V 10 kHz', AcVoltageDutSettings(range=1, value=1, freq=10e3), 'w4950', AcVoltageCommand(1, freq=10e3), True),
    Step('Valhalla 2703', '10 V 10 kHz', AcVoltageDutSettings(range=10, value=10, freq=10e3), 'w4950', AcVoltageCommand(10, freq=10e3), True),
    Step('Valhalla 2703', '100 V 10 kHz', AcVoltageDutSettings(range=100, value=100, freq=10e3), 'w4950', AcVoltageCommand(100, freq=10e3), True),
    Step('Valhalla 2703', '100 V 20 kHz', AcVoltageDutSettings(range=100, value=100, freq=20e3), 'w4950', AcVoltageCommand(100, freq=20e3), True),
    Step('Valhalla 2703', '10 V 20 kHz', AcVoltageDutSettings(range=10, value=10, freq=20e3), 'w4950', AcVoltageCommand(10, freq=20e3), True),
    Step('Valhalla 2703', '1 V 20 kHz', AcVoltageDutSettings(range=1, value=1, freq=20e3), 'w4950', AcVoltageCommand(1, freq=20e3), True),
    Step('Valhalla 2703', '100 mV 20 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20e3), 'w4950', AcVoltageCommand(100e-3, freq=100e3), True),
    Step('Valhalla 2703', '100 mV 50 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=50e3), 'w4950', AcVoltageCommand(100e-3, freq=50e3), True),
    Step('Valhalla 2703', '1 V 50 kHz', AcVoltageDutSettings(range=1, value=1, freq=50e3), 'w4950', AcVoltageCommand(1, freq=50e3), True),
    Step('Valhalla 2703', '10 V 50 kHz', AcVoltageDutSettings(range=10, value=10, freq=50e3), 'w4950', AcVoltageCommand(10, freq=50e3), True),
    Step('Valhalla 2703', '100 V 50 kHz', AcVoltageDutSettings(range=100, value=100, freq=50e3), 'w4950', AcVoltageCommand(100, freq=50e3), True),
    Step('Valhalla 2703', '100 V 100 kHz', AcVoltageDutSettings(range=100, value=100, freq=100e3), 'w4950', AcVoltageCommand(100, freq=100e3), True),
    Step('Valhalla 2703', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=10, freq=100e3), 'w4950', AcVoltageCommand(10, freq=100e3), True),
    Step('Valhalla 2703', '1 V 100 kHz', AcVoltageDutSettings(range=1, value=1, freq=100e3), 'w4950', AcVoltageCommand(1, freq=100e3), True),
    Step('Valhalla 2703', '100 mV 100 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=100e3), 'w4950', AcVoltageCommand(100e-3, freq=100e3), True),
    Step('Valhalla 2703', '10 mV 100 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=100e3), 'w4950', AcVoltageCommand(10e-3, freq=100e3), True),
    Step('Valhalla 2703', '10 mV 50 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=50e3), 'w4950', AcVoltageCommand(10e-3, freq=50e3), True),
    Step('Valhalla 2703', '10 mV 20 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=20e3), 'w4950', AcVoltageCommand(10e-3, freq=20e3), True),
    Step('Valhalla 2703', '10 mV 10 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=10e3), 'w4950', AcVoltageCommand(10e-3, freq=10e3), True),
    Step('Valhalla 2703', '10 mV 900 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=900), 'w4950', AcVoltageCommand(10e-3, freq=1e3), True),
    Step('Valhalla 2703', '10 mV 300 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=300), 'w4950', AcVoltageCommand(10e-3, freq=300), True),
    Step('Valhalla 2703', '10 mV 55 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=55), 'w4950', AcVoltageCommand(10e-3, freq=55), True),
    Step('Valhalla 2703', '10 mV 20 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=20), 'w4950', AcVoltageCommand(10e-3, freq=20), True),
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
    return {'w4950': w4950}


def read_row(inits, instruments: List[Instrument]):
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
