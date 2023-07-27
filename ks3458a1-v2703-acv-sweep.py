#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import Step, AcVoltageDutSettings, AcVoltageCommand, run_procedure, check_valid_value

OUTPUT_FILE = 'ks3458a1-v2703-acv-sweep.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'ag3458a_1_value', 'temp_1', 'last_acal_1',
              'last_acal_1_cal72', '3458a_1_function', 'ag3458a_1_range')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 60
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    Step('F510', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('Valhalla 2703', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('Valhalla 2703', '10 V 1 kHz', AcVoltageDutSettings(range=10, value=10, freq=1e3), 'ag3458a_1', AcVoltageCommand(10, freq=1e3), True),
    Step('Valhalla 2703', '10 V 1 kHz', AcVoltageDutSettings(range=10, value=10, freq=1e3), 'ag3458a_1', AcVoltageCommand(100, freq=1e3)),
    Step('Valhalla 2703', '19 V 1 kHz', AcVoltageDutSettings(range=10, value=19, freq=1e3), 'ag3458a_1', AcVoltageCommand(19, freq=1e3), True),
    Step('Valhalla 2703', '100 V 1 kHz', AcVoltageDutSettings(range=100, value=100, freq=1e3), 'ag3458a_1', AcVoltageCommand(100, freq=1e3), True),
    Step('Valhalla 2703', '100 V 1 kHz', AcVoltageDutSettings(range=100, value=100, freq=1e3), 'ag3458a_1', AcVoltageCommand(1000, freq=1e3)),
    Step('Valhalla 2703', '700 V 1 kHz', AcVoltageDutSettings(range=1000, value=700, freq=1e3), 'ag3458a_1', AcVoltageCommand(1000, freq=1e3), True),
    Step('Valhalla 2703', '10 V 1 kHz', AcVoltageDutSettings(range=10, value=10, freq=1e3), 'ag3458a_1', AcVoltageCommand(10, freq=1e3), True),
    Step('Valhalla 2703', '1 V 1 kHz', AcVoltageDutSettings(range=1, value=1, freq=1e3), 'ag3458a_1', AcVoltageCommand(10, freq=1e3), True),
    Step('Valhalla 2703', '1 V 1 kHz', AcVoltageDutSettings(range=1, value=1, freq=1e3), 'ag3458a_1', AcVoltageCommand(1, freq=1e3)),
    Step('Valhalla 2703', '100 mV 1 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=1e3), 'ag3458a_1', AcVoltageCommand(1, freq=10e3), True),
    Step('Valhalla 2703', '100 mV 1 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=1e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=10e3)),
    Step('Valhalla 2703', '100 mV 10 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=10e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=10e3), True),
    Step('Valhalla 2703', '100 mV 10 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=10e3), 'ag3458a_1', AcVoltageCommand(1, freq=10e3)),
    Step('Valhalla 2703', '1 V 10 kHz', AcVoltageDutSettings(range=1, value=1, freq=10e3), 'ag3458a_1', AcVoltageCommand(1, freq=10e3), True),
    Step('Valhalla 2703', '1 V 10 kHz', AcVoltageDutSettings(range=1, value=1, freq=10e3), 'ag3458a_1', AcVoltageCommand(10, freq=10e3)),
    Step('Valhalla 2703', '10 V 10 kHz', AcVoltageDutSettings(range=10, value=10, freq=10e3), 'ag3458a_1', AcVoltageCommand(10, freq=10e3), True),
    Step('Valhalla 2703', '10 V 10 kHz', AcVoltageDutSettings(range=10, value=10, freq=10e3), 'ag3458a_1', AcVoltageCommand(100, freq=10e3)),
    Step('Valhalla 2703', '100 V 10 kHz', AcVoltageDutSettings(range=100, value=100, freq=10e3), 'ag3458a_1', AcVoltageCommand(100, freq=10e3), True),
    Step('Valhalla 2703', '100 V 10 kHz', AcVoltageDutSettings(range=100, value=100, freq=10e3), 'ag3458a_1', AcVoltageCommand(1000, freq=10e3)),
    Step('Valhalla 2703', '100 V 20 kHz', AcVoltageDutSettings(range=100, value=100, freq=20e3), 'ag3458a_1', AcVoltageCommand(1000, freq=20e3), True),
    Step('Valhalla 2703', '100 V 20 kHz', AcVoltageDutSettings(range=100, value=100, freq=20e3), 'ag3458a_1', AcVoltageCommand(100, freq=20e3)),
    Step('Valhalla 2703', '10 V 20 kHz', AcVoltageDutSettings(range=10, value=10, freq=20e3), 'ag3458a_1', AcVoltageCommand(100, freq=20e3), True),
    Step('Valhalla 2703', '10 V 20 kHz', AcVoltageDutSettings(range=10, value=10, freq=20e3), 'ag3458a_1', AcVoltageCommand(10, freq=20e3)),
    Step('Valhalla 2703', '1 V 20 kHz', AcVoltageDutSettings(range=1, value=1, freq=20e3), 'ag3458a_1', AcVoltageCommand(10, freq=20e3), True),
    Step('Valhalla 2703', '1 V 20 kHz', AcVoltageDutSettings(range=1, value=1, freq=20e3), 'ag3458a_1', AcVoltageCommand(1, freq=20e3)),
    Step('Valhalla 2703', '100 mV 20 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20e3), 'ag3458a_1', AcVoltageCommand(1, freq=100e3), True),
    Step('Valhalla 2703', '100 mV 20 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=100e3)),
    Step('Valhalla 2703', '100 mV 50 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=50e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=50e3), True),
    Step('Valhalla 2703', '100 mV 50 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=50e3), 'ag3458a_1', AcVoltageCommand(1, freq=50e3)),
    Step('Valhalla 2703', '1 V 50 kHz', AcVoltageDutSettings(range=1, value=1, freq=50e3), 'ag3458a_1', AcVoltageCommand(1, freq=50e3), True),
    Step('Valhalla 2703', '1 V 50 kHz', AcVoltageDutSettings(range=1, value=1, freq=50e3), 'ag3458a_1', AcVoltageCommand(10, freq=50e3)),
    Step('Valhalla 2703', '10 V 50 kHz', AcVoltageDutSettings(range=10, value=10, freq=50e3), 'ag3458a_1', AcVoltageCommand(10, freq=50e3), True),
    Step('Valhalla 2703', '10 V 50 kHz', AcVoltageDutSettings(range=10, value=10, freq=50e3), 'ag3458a_1', AcVoltageCommand(100, freq=50e3)),
    Step('Valhalla 2703', '100 V 50 kHz', AcVoltageDutSettings(range=100, value=100, freq=50e3), 'ag3458a_1', AcVoltageCommand(100, freq=50e3), True),
    Step('Valhalla 2703', '100 V 50 kHz', AcVoltageDutSettings(range=100, value=100, freq=50e3), 'ag3458a_1', AcVoltageCommand(1000, freq=50e3)),
    Step('Valhalla 2703', '100 V 100 kHz', AcVoltageDutSettings(range=100, value=100, freq=100e3), 'ag3458a_1', AcVoltageCommand(1000, freq=100e3), True),
    Step('Valhalla 2703', '100 V 100 kHz', AcVoltageDutSettings(range=100, value=100, freq=100e3), 'ag3458a_1', AcVoltageCommand(100, freq=100e3)),
    Step('Valhalla 2703', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=10, freq=100e3), 'ag3458a_1', AcVoltageCommand(100, freq=100e3), True),
    Step('Valhalla 2703', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=10, freq=100e3), 'ag3458a_1', AcVoltageCommand(10, freq=100e3)),
    Step('Valhalla 2703', '10 V 10 kHz', AcVoltageDutSettings(range=10, value=10, freq=10e3), 'ag3458a_1', AcVoltageCommand(10, freq=10), True),
    Step('Valhalla 2703', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('Valhalla 2703', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=10, freq=100e3), 'ag3458a_1', AcVoltageCommand(10, freq=100e3), True),
    Step('Valhalla 2703', '1 V 100 kHz', AcVoltageDutSettings(range=1, value=1, freq=100e3), 'ag3458a_1', AcVoltageCommand(10, freq=100e3), True),
    Step('Valhalla 2703', '1 V 100 kHz', AcVoltageDutSettings(range=1, value=1, freq=100e3), 'ag3458a_1', AcVoltageCommand(1, freq=100e3)),
    Step('Valhalla 2703', '100 mV 100 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=100e3), 'ag3458a_1', AcVoltageCommand(1, freq=100e3), True),
    Step('Valhalla 2703', '100 mV 100 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=100e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=100e3)),
    Step('Valhalla 2703', '100 mV 300 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=300), 'ag3458a_1', AcVoltageCommand(100e-3, freq=300), True),
    Step('Valhalla 2703', '100 mV 300 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=300), 'ag3458a_1', AcVoltageCommand(1, freq=300)),
    Step('Valhalla 2703', '1 V 300 Hz', AcVoltageDutSettings(range=1, value=1, freq=300), 'ag3458a_1', AcVoltageCommand(1, freq=300), True),
    Step('Valhalla 2703', '1 V 300 Hz', AcVoltageDutSettings(range=1, value=1, freq=300), 'ag3458a_1', AcVoltageCommand(10, freq=300)),
    Step('Valhalla 2703', '10 V 300 Hz', AcVoltageDutSettings(range=10, value=10, freq=300), 'ag3458a_1', AcVoltageCommand(10, freq=300), True),
    Step('Valhalla 2703', '10 V 300 Hz', AcVoltageDutSettings(range=10, value=10, freq=300), 'ag3458a_1', AcVoltageCommand(100, freq=300)),
    Step('Valhalla 2703', '100 V 300 Hz', AcVoltageDutSettings(range=100, value=100, freq=300), 'ag3458a_1', AcVoltageCommand(100, freq=300), True),
    Step('Valhalla 2703', '100 V 300 Hz', AcVoltageDutSettings(range=100, value=100, freq=300), 'ag3458a_1', AcVoltageCommand(1000, freq=300)),
    Step('Valhalla 2703', '700 V 300 Hz', AcVoltageDutSettings(range=1000, value=700, freq=300), 'ag3458a_1', AcVoltageCommand(1000, freq=300), True),
    Step('Valhalla 2703', '700 V 55 Hz', AcVoltageDutSettings(range=1000, value=700, freq=55), 'ag3458a_1', AcVoltageCommand(1000, freq=55), True),
    Step('Valhalla 2703', '100 V 55 Hz', AcVoltageDutSettings(range=100, value=100, freq=55), 'ag3458a_1', AcVoltageCommand(1000, freq=55), True),
    Step('Valhalla 2703', '100 V 55 Hz', AcVoltageDutSettings(range=100, value=100, freq=55), 'ag3458a_1', AcVoltageCommand(100, freq=55)),
    Step('Valhalla 2703', '10 V 55 Hz', AcVoltageDutSettings(range=10, value=10, freq=55), 'ag3458a_1', AcVoltageCommand(100, freq=55), True),
    Step('Valhalla 2703', '10 V 55 Hz', AcVoltageDutSettings(range=10, value=10, freq=55), 'ag3458a_1', AcVoltageCommand(10, freq=55)),
    Step('Valhalla 2703', '1 V 55 Hz', AcVoltageDutSettings(range=1, value=1, freq=55), 'ag3458a_1', AcVoltageCommand(10, freq=55), True),
    Step('Valhalla 2703', '1 V 55 Hz', AcVoltageDutSettings(range=1, value=1, freq=55), 'ag3458a_1', AcVoltageCommand(1, freq=55)),
    Step('Valhalla 2703', '100 mV 55 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=55), 'ag3458a_1', AcVoltageCommand(1, freq=55), True),
    Step('Valhalla 2703', '100 mV 55 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=55), 'ag3458a_1', AcVoltageCommand(100e-3, freq=55)),
    Step('Valhalla 2703', '10 mV 55 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=55), 'ag3458a_1', AcVoltageCommand(100e-3, freq=55), True),
    Step('Valhalla 2703', '10 mV 55 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=55), 'ag3458a_1', AcVoltageCommand(10e-3, freq=55)),
    Step('Valhalla 2703', '10 mV 20 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=10), 'ag3458a_1', AcVoltageCommand(10e-3, freq=10), True),
    Step('Valhalla 2703', '10 mV 20 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=20), 'ag3458a_1', AcVoltageCommand(100e-3, freq=20)),
    Step('Valhalla 2703', '100 mV 20 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20), 'ag3458a_1', AcVoltageCommand(100e-3, freq=20), True),
    Step('Valhalla 2703', '100 mV 20 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20), 'ag3458a_1', AcVoltageCommand(1, freq=20)),
    Step('Valhalla 2703', '1 V 20 Hz', AcVoltageDutSettings(range=1, value=1, freq=20), 'ag3458a_1', AcVoltageCommand(1, freq=20), True),
    Step('Valhalla 2703', '1 V 20 Hz', AcVoltageDutSettings(range=1, value=1, freq=20), 'ag3458a_1', AcVoltageCommand(10, freq=20)),
    Step('Valhalla 2703', '10 V 20 Hz', AcVoltageDutSettings(range=10, value=10, freq=20), 'ag3458a_1', AcVoltageCommand(10, freq=20), True),
    Step('Valhalla 2703', '10 V 20 Hz', AcVoltageDutSettings(range=10, value=10, freq=20), 'ag3458a_1', AcVoltageCommand(100, freq=20)),
    Step('Valhalla 2703', '100 V 20 Hz', AcVoltageDutSettings(range=100, value=100, freq=20), 'ag3458a_1', AcVoltageCommand(100, freq=20), True),
    Step('Valhalla 2703', '100 V 20 Hz', AcVoltageDutSettings(range=100, value=100, freq=20), 'ag3458a_1', AcVoltageCommand(1000, freq=20)),
    Step('Valhalla 2703', '700 V 20 Hz', AcVoltageDutSettings(range=1000, value=700, freq=20), 'ag3458a_1', AcVoltageCommand(1000, freq=20), True),
    Step('Valhalla 2703', '10 mV 300 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=300), 'ag3458a_1', AcVoltageCommand(10e-3, freq=300), True),
    Step('Valhalla 2703', '10 mV 300 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=300), 'ag3458a_1', AcVoltageCommand(100e-3, freq=300)),
    Step('Valhalla 2703', '10 mV 100 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=100e3), 'ag3458a_1', AcVoltageCommand(10e-3, freq=100e3), True),
    Step('Valhalla 2703', '10 mV 100 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=100e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=100e3)),
    Step('Valhalla 2703', '10 mV 50 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=50e3), 'ag3458a_1', AcVoltageCommand(10e-3, freq=50e3), True),
    Step('Valhalla 2703', '10 mV 50 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=50e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=50e3)),
    Step('Valhalla 2703', '10 mV 20 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=20e3), 'ag3458a_1', AcVoltageCommand(10e-3, freq=20e3), True),
    Step('Valhalla 2703', '10 mV 20 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=20e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=20e3)),
    Step('Valhalla 2703', '10 mV 10 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=10e3), 'ag3458a_1', AcVoltageCommand(10e-3, freq=10e3), True),
    Step('Valhalla 2703', '10 mV 10 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=10e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=10e3)),
    Step('Valhalla 2703', '10 mV 1 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=1e3), 'ag3458a_1', AcVoltageCommand(10e-3, freq=1e3), True),
    Step('Valhalla 2703', '10 mV 1 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=1e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=1e3)),
    Step('Valhalla 2703', '100 mV 1 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=1e3), 'ag3458a_1', AcVoltageCommand(100e-3, freq=1e3), True),
    Step('Valhalla 2703', '100 mV 1 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=1e3), 'ag3458a_1', AcVoltageCommand(1, freq=1e3)),
    Step('Valhalla 2703', '1 V 1 kHz', AcVoltageDutSettings(range=1, value=1, freq=1e3), 'ag3458a_1', AcVoltageCommand(1, freq=1e3), True),
    Step('Valhalla 2703', '1 V 1 kHz', AcVoltageDutSettings(range=1, value=1, freq=1e3), 'ag3458a_1', AcVoltageCommand(10, freq=1e3)),
    Step('Valhalla 2703', '10 V 1 kHz', AcVoltageDutSettings(range=10, value=10, freq=1e3), 'ag3458a_1', AcVoltageCommand(10, freq=1e3), True),
    Step('Valhalla 2703', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
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
    ag3458a_1 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,21::INSTR",
                                         reset=True)
    ag3458a_1._interface.timeout = 120
    if not DEBUG:
        ag3458a_1.advanced.aperture_time = 100
    temp_1 = ag3458a_1.utility.temp
    ag3458a_1.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'test'
    else:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'keep'
        # acal_3458a(ag3458a_1)
    return {'ag3458a_1': ag3458a_1}


def read_row(inits, instruments):
    ag3458a_1 = inits['ag3458a_1']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    if ((datetime.datetime.utcnow() - ag3458a_1.last_temp).total_seconds()
            > 30 * 60):
        temp_1 = ag3458a_1.utility.temp
        ag3458a_1.last_temp = datetime.datetime.utcnow()
        row['temp_1'] = temp_1
        row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
        row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
        ag3458a_1.measurement.read(360)
    else:
        ag3458a_1.measurement.initiate()
        row['ag3458a_1_value'] = ag3458a_1.measurement.fetch(360)
        row['temp_1'] = None
        row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
        row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
        row['ag3458a_1_range'] = ag3458a_1.range
        print(f"{row['ag3458a_1_value']}")
        check_valid_value(ag3458a_1, row['ag3458a_1_value'])
    return row, row['temp_1'] is None


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ac()


if __name__ == '__main__':
    main()
