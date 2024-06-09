#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import DcVoltageCommand, DcVoltageDutSettings, Step, AcVoltageDutSettings, AcVoltageCommand, run_procedure, check_valid_value

OUTPUT_FILE = 'ks3458a1-f510-reading.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'ag3458a_1_value', 'temp_1', 'last_acal_1',
              'last_acal_1_cal72', '3458a_1_function', 'ag3458a_1_range')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 33
STEP_SOAK_TIME = 12
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    Step('F7001', '10 V', DcVoltageDutSettings(range=10, value=10), 'ag3458a_1', DcVoltageCommand(10), True),
    Step('F7001', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'ag3458a_1', DcVoltageCommand(10), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'ag3458a_1', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'ag3458a_1', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-4072009', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-2400-3253020', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F510-100000-4272047', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=-10, freq=100e3), 'ag3458a_1', AcVoltageCommand(10, freq=100e3), True),
    Step('F510-2400-4290014', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3), 'ag3458a_1', AcVoltageCommand(10, freq=2.4e3), True),
    Step('F7001', '10 V', DcVoltageDutSettings(range=10, value=10), 'ag3458a_1', DcVoltageCommand(10), True),
    Step('F7001', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'ag3458a_1', DcVoltageCommand(10), True),
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
        # ag3458a_1.last_acal_cal72 = 'keep'
        acal_3458a(ag3458a_1)
    return {'ag3458a_1': ag3458a_1}


def read_row(inits, instruments, **kwargs):
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
