#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import Step, run_procedure, check_valid_value, AcCurrentCommand, AcCurrentDutSettings

OUTPUT_FILE = 'ks3458a-v2703-acv-sweep.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'ag3458a_2_value', 'temp_2', 'last_acal_2',
              'last_acal_2_cal72', '3458a_2_function', 'ag3458a_2_range')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 60
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    Step('Valhalla 2703', '1 uA 20 Hz', AcCurrentDutSettings(range=1e-6, value=1e-6, freq=20), 'ag3458a_2', AcCurrentCommand(1-6, freq=20), True),
    Step('Valhalla 2703', '10 uA 20 Hz', AcCurrentDutSettings(range=10e-6, value=10e-6, freq=20), 'ag3458a_2', AcCurrentCommand(10e-6, freq=20), True),
    Step('Valhalla 2703', '100 uA 20 Hz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=20), 'ag3458a_2', AcCurrentCommand(100e-6, freq=20), True),
    Step('Valhalla 2703', '1 mA 20 Hz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=20), 'ag3458a_2', AcCurrentCommand(1e-3, freq=20), True),
    Step('Valhalla 2703', '10 mA 20 Hz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=20), 'ag3458a_2', AcCurrentCommand(10e-3, freq=20), True),
    Step('Valhalla 2703', '100 mA 20 Hz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=20), 'ag3458a_2', AcCurrentCommand(100e-3, freq=20), True),
    Step('Valhalla 2703', '1 A 20 Hz', AcCurrentDutSettings(range=1, value=1, freq=20), 'ag3458a_2', AcCurrentCommand(1, freq=20), True),
    Step('Valhalla 2703', '1 uA 55 Hz', AcCurrentDutSettings(range=1e-6, value=1e-6, freq=55), 'ag3458a_2', AcCurrentCommand(1e-6, freq=55), True),
    Step('Valhalla 2703', '10 uA 55 Hz', AcCurrentDutSettings(range=10e-6, value=10e-6, freq=55), 'ag3458a_2', AcCurrentCommand(10e-6, freq=55), True),
    Step('Valhalla 2703', '100 uA 55 Hz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=55), 'ag3458a_2', AcCurrentCommand(100e-6, freq=55), True),
    Step('Valhalla 2703', '1 mA 55 Hz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=55), 'ag3458a_2', AcCurrentCommand(1e-3, freq=55), True),
    Step('Valhalla 2703', '10 mA 55 Hz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=55), 'ag3458a_2', AcCurrentCommand(10e-3, freq=55), True),
    Step('Valhalla 2703', '100 mA 55 Hz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=55), 'ag3458a_2', AcCurrentCommand(100e-3, freq=55), True),
    Step('Valhalla 2703', '1 A 55 Hz', AcCurrentDutSettings(range=1, value=1, freq=55), 'ag3458a_2', AcCurrentCommand(1, freq=55), True),
    Step('Valhalla 2703', '1 uA 300 Hz', AcCurrentDutSettings(range=1e-6, value=1e-6, freq=300), 'ag3458a_2', AcCurrentCommand(1e-6, freq=300), True),
    Step('Valhalla 2703', '10 uA 300 Hz', AcCurrentDutSettings(range=10e-6, value=10e-6, freq=300), 'ag3458a_2', AcCurrentCommand(10e-6, freq=300), True),
    Step('Valhalla 2703', '100 uA 300 Hz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=300), 'ag3458a_2', AcCurrentCommand(100e-6, freq=300), True),
    Step('Valhalla 2703', '1 mA 300 Hz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=300), 'ag3458a_2', AcCurrentCommand(1e-3, freq=300), True),
    Step('Valhalla 2703', '10 mA 300 Hz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=300), 'ag3458a_2', AcCurrentCommand(10e-3, freq=300), True),
    Step('Valhalla 2703', '100 mA 300 Hz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=300), 'ag3458a_2', AcCurrentCommand(100e-3, freq=300), True),
    Step('Valhalla 2703', '1 A 300 Hz', AcCurrentDutSettings(range=1, value=1, freq=300), 'ag3458a_2', AcCurrentCommand(1, freq=300), True),
    Step('Valhalla 2703', '1 uA 1 kHz', AcCurrentDutSettings(range=1e-6, value=1e-6, freq=1e3), 'ag3458a_2', AcCurrentCommand(1e-6, freq=1e3), True),
    Step('Valhalla 2703', '10 uA 1 kHz', AcCurrentDutSettings(range=10e-6, value=10e-6, freq=1e3), 'ag3458a_2', AcCurrentCommand(10e-6, freq=1e3), True),
    Step('Valhalla 2703', '100 uA 1 kHz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=1e3), 'ag3458a_2', AcCurrentCommand(100e-6, freq=1e3), True),
    Step('Valhalla 2703', '1 mA 1 kHz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=1e3), 'ag3458a_2', AcCurrentCommand(1e-3, freq=1e3), True),
    Step('Valhalla 2703', '10 mA 1 kHz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=1e3), 'ag3458a_2', AcCurrentCommand(10e-3, freq=1e3), True),
    Step('Valhalla 2703', '100 mA 1 kHz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=1e3), 'ag3458a_2', AcCurrentCommand(100e-3, freq=1e3), True),
    Step('Valhalla 2703', '1 A 1 kHz', AcCurrentDutSettings(range=1, value=1, freq=1e3), 'ag3458a_2', AcCurrentCommand(1, freq=1e3), True),
    Step('Valhalla 2703', '100 uA 5 kHz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=5e3), 'ag3458a_2', AcCurrentCommand(100e-6, freq=5e3), True),
    Step('Valhalla 2703', '1 mA 5 kHz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=5e3), 'ag3458a_2', AcCurrentCommand(1e-3, freq=5e3), True),
    Step('Valhalla 2703', '10 mA 5 kHz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=5e3), 'ag3458a_2', AcCurrentCommand(10e-3, freq=5e3), True),
    Step('Valhalla 2703', '100 mA 5 kHz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=5e3), 'ag3458a_2', AcCurrentCommand(100e-3, freq=5e3), True),
    Step('Valhalla 2703', '1 A 5 kHz', AcCurrentDutSettings(range=1, value=1, freq=5e3), 'ag3458a_2', AcCurrentCommand(1, freq=5e3), True),
    Step('Valhalla 2703', '1 mA 10 kHz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=20), 'ag3458a_2', AcCurrentCommand(1e-3, freq=20), True),
    Step('Valhalla 2703', '10 mA 10 kHz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=20), 'ag3458a_2', AcCurrentCommand(10e-3, freq=20), True),
    Step('Valhalla 2703', '100 mA 10 kHz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=20), 'ag3458a_2', AcCurrentCommand(100e-3, freq=20), True),
    Step('Valhalla 2703', '1 A 10 kHz', AcCurrentDutSettings(range=1, value=1, freq=20), 'ag3458a_2', AcCurrentCommand(1, freq=20), True),
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
    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
                                         reset=True)
    ag3458a_2._interface.timeout = 120
    if not DEBUG:
        ag3458a_2.advanced.aperture_time = 100
    temp_2 = ag3458a_2.utility.temp
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
    else:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        # ag3458a_2.last_acal_cal72 = 'keep'
        acal_3458a(ag3458a_2)
    return {'ag3458a_2': ag3458a_2}


def read_row(inits, instruments):
    ag3458a_2 = inits['ag3458a_2']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 30 * 60):
        temp_2 = ag3458a_2.utility.temp
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        row['temp_2'] = temp_2
        row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
        row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
        ag3458a_2.measurement.read(360)
        return row, False
    else:
        ag3458a_2.measurement.initiate()
        row['ag3458a_2_value'] = ag3458a_2.measurement.fetch(360)
        row['temp_2'] = None
        row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
        row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
        row['ag3458a_2_range'] = ag3458a_2.range
        print(f"{row['ag3458a_2_value']}")
        check_valid_value(ag3458a_2, row['ag3458a_2_value'])
        return row, True


def acal_3458a(ag3458a):
    # ag3458a.acal.start_dcv()
    # ag3458a.acal.start_ohms()
    ag3458a.acal.start_ac()


if __name__ == '__main__':
    main()
