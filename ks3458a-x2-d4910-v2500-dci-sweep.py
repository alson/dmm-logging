#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import Step2, run_procedure, check_valid_value, DcCurrentCommand, Instrument, DcVoltageCommand, \
    DcCurrentDutSettings

OUTPUT_FILE = 'ks3458a-x2-d4910-v2500-dci-sweep.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'ag3458a_1_current', 'temp_1', 'last_acal_1',
              'last_acal_1_cal72', '3458a_1_function', 'ag3458a_1_range', 'ag3458a_2_voltage', 'temp_2', 'last_acal_2',
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
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=1e-6, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '1 uA', DcCurrentDutSettings(range=1e-6, value=1e-6), [Instrument('ag3458a_1', DcCurrentCommand(1e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '-1 uA', DcCurrentDutSettings(range=1e-6, value=-1e-6), [Instrument('ag3458a_1', DcCurrentCommand(1e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=10e-6, value=0), [Instrument('ag3458a_1', DcCurrentCommand(10e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '-10 uA', DcCurrentDutSettings(range=10e-6, value=-10e-6), [Instrument('ag3458a_1', DcCurrentCommand(10e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '10 uA', DcCurrentDutSettings(range=10e-6, value=10e-6), [Instrument('ag3458a_1', DcCurrentCommand(10e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=100e-6, value=0), [Instrument('ag3458a_1', DcCurrentCommand(100e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '100 uA', DcCurrentDutSettings(range=100e-6, value=100e-6), [Instrument('ag3458a_1', DcCurrentCommand(100e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '-100 uA', DcCurrentDutSettings(range=100e-6, value=-100e-6), [Instrument('ag3458a_1', DcCurrentCommand(100e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=1e-3, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '-1 mA', DcCurrentDutSettings(range=1e-3, value=-1e-3), [Instrument('ag3458a_1', DcCurrentCommand(1e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '1 mA', DcCurrentDutSettings(range=1e-3, value=1e-3), [Instrument('ag3458a_1', DcCurrentCommand(1e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=10e-3, value=0), [Instrument('ag3458a_1', DcCurrentCommand(10e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '10 mA', DcCurrentDutSettings(range=10e-3, value=10e-3), [Instrument('ag3458a_1', DcCurrentCommand(10e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '-10 mA', DcCurrentDutSettings(range=10e-3, value=-10e-3), [Instrument('ag3458a_1', DcCurrentCommand(10e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=100e-3, value=0), [Instrument('ag3458a_1', DcCurrentCommand(100e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '-100 mA', DcCurrentDutSettings(range=100e-3, value=-100e-3), [Instrument('ag3458a_1', DcCurrentCommand(100e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '100 mA', DcCurrentDutSettings(range=100e-3, value=100e-3), [Instrument('ag3458a_1', DcCurrentCommand(100e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=1, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '1 A', DcCurrentDutSettings(range=1, value=1), [Instrument('ag3458a_1', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', '-1 A', DcCurrentDutSettings(range=1, value=-1), [Instrument('ag3458a_1', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    # Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=1, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=1, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=1e-6, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))]),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=10e-6, value=0), [Instrument('ag3458a_1', DcCurrentCommand(10e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))]),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=100e-6, value=0), [Instrument('ag3458a_1', DcCurrentCommand(100e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))]),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=1e-3, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))]),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=10e-3, value=0), [Instrument('ag3458a_1', DcCurrentCommand(10e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))]),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=100e-3, value=0), [Instrument('ag3458a_1', DcCurrentCommand(100e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))]),
    Step2('Datron 4910 + Valhalla 2500', 'short (spade lugs disconnected)', DcCurrentDutSettings(range=1, value=0), [Instrument('ag3458a_1', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))]),
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
    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
                                         reset=True)
    ag3458a_2._interface.timeout = 120

    if not DEBUG:
        ag3458a_1.advanced.aperture_time = 100
        ag3458a_2.advanced.aperture_time = 100
    temp_1 = ag3458a_1.utility.temp
    temp_2 = ag3458a_2.utility.temp
    ag3458a_1.last_temp = datetime.datetime.utcnow()
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'test'
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
    else:
        ag3458a_1.last_acal = datetime.datetime.utcnow()
        ag3458a_1.last_acal_temp = temp_1
        ag3458a_1.last_acal_cal72 = 'keep'
        # acal_3458a_1(ag3458a_1)
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'keep'
        # acal_3458a_2(ag3458a_2)
    return {'ag3458a_1': ag3458a_1, 'ag3458a_2': ag3458a_2}


def read_row(inits, retry_count=1):
    ag3458a_1 = inits['ag3458a_1']
    ag3458a_2 = inits['ag3458a_2']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    if ((datetime.datetime.utcnow() - ag3458a_1.last_temp).total_seconds()
            > 30 * 60):
        temp_1 = ag3458a_1.utility.temp
        ag3458a_1.last_temp = datetime.datetime.utcnow()
        temp_2 = ag3458a_2.utility.temp
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        row['temp_1'] = temp_1
        row['temp_2'] = temp_2
        row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
        row['last_acal_2'] = ag3458a_1.last_acal.isoformat()
        row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
        row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
        ag3458a_1.measurement.initiate()
        ag3458a_2.measurement.initiate()
        ag3458a_1.measurement.fetch(360)
        ag3458a_2.measurement.fetch(360)
        return row, False
    ag3458a_1.measurement.initiate()
    ag3458a_2.measurement.initiate()
    row['ag3458a_1_current'] = ag3458a_1.measurement.fetch(360)
    row['temp_1'] = None
    row['last_acal_1'] = ag3458a_1.last_acal.isoformat()
    row['last_acal_1_cal72'] = ag3458a_1.last_acal_cal72
    row['ag3458a_1_range'] = ag3458a_1.range
    row['ag3458a_2_voltage'] = ag3458a_2.measurement.fetch(360)
    row['temp_2'] = None
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    row['ag3458a_2_range'] = ag3458a_2.range
    print(f"{row['ag3458a_1_current']}", end='')
    print(f", ag3458a_2: {row['ag3458a_2_voltage']}")
    check_valid_value(ag3458a_1, row['ag3458a_1_current'])
    check_valid_value(ag3458a_2, row['ag3458a_2_voltage'])
    return row, True


def acal_3458a_2(ag3458a):
    ag3458a.acal.start_dcv()


def acal_3458a_1(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ohms()


if __name__ == '__main__':
    main()
