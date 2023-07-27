#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import Step2, run_procedure, check_valid_value, DcCurrentCommand, Instrument, DcVoltageCommand, \
    DcCurrentDutSettings

OUTPUT_FILE = 'w4950-ks3458a-d4910-v2500-dci-sweep.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'w4950_function', 'w4950_range', 'w4950_percentage', 'w4950_freq',
              'w4950_value', 'w4950_nsamples', 'w4950_std_abs', 'w4950_temp', 'ag3458a_2_value', 'temp_2', 'last_acal_2',
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
    Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=100e-6, value=0), [Instrument('w4950', DcCurrentCommand(100e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '100 uA', DcCurrentDutSettings(range=100e-6, value=100e-6), [Instrument('w4950', DcCurrentCommand(100e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '-100 uA', DcCurrentDutSettings(range=100e-6, value=-100e-6), [Instrument('w4950', DcCurrentCommand(100e-6)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=1e-3, value=0), [Instrument('w4950', DcCurrentCommand(1e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '-1 mA', DcCurrentDutSettings(range=1e-3, value=-1e-3), [Instrument('w4950', DcCurrentCommand(1e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '1 mA', DcCurrentDutSettings(range=1e-3, value=1e-3), [Instrument('w4950', DcCurrentCommand(1e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=10e-3, value=0), [Instrument('w4950', DcCurrentCommand(10e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '10 mA', DcCurrentDutSettings(range=10e-3, value=10e-3), [Instrument('w4950', DcCurrentCommand(10e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '-10 mA', DcCurrentDutSettings(range=10e-3, value=-10e-3), [Instrument('w4950', DcCurrentCommand(10e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=100e-3, value=0), [Instrument('w4950', DcCurrentCommand(100e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '-100 mA', DcCurrentDutSettings(range=100e-3, value=-100e-3), [Instrument('w4950', DcCurrentCommand(100e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '100 mA', DcCurrentDutSettings(range=100e-3, value=100e-3), [Instrument('w4950', DcCurrentCommand(100e-3)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=1, value=0), [Instrument('w4950', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '1 A', DcCurrentDutSettings(range=1, value=1), [Instrument('w4950', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', '-1 A', DcCurrentDutSettings(range=1, value=-1), [Instrument('w4950', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
    Step2('Datron 4910 + Valhalla 2500', 'short', DcCurrentDutSettings(range=1, value=0), [Instrument('w4950', DcCurrentCommand(1)), Instrument('ag3458a_2', DcVoltageCommand(1))], True),
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
        ag3458a_2.last_acal_cal72 = 'keep'
        # acal_3458a(ag3458a_2)
    return {'w4950': w4950, 'ag3458a_2': ag3458a_2}


def read_row(inits, retry_count=1):
    w4950 = inits['w4950']
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
    ag3458a_2.measurement.initiate()
    if ((datetime.datetime.utcnow() - w4950.last_temp).total_seconds()
            > 30 * 60):
        row['w4950_temp'] = w4950.measurement.temp.internal
        w4950.last_temp = datetime.datetime.utcnow()
    w4950.measurement.initiate()
    row['w4950_function'] = w4950.measurement_function
    row['w4950_range'] = w4950.range
    row['w4950_percentage'] = w4950.measurement.percentage
    row['w4950_value'] = w4950.measurement.fetch(60)
    row['w4950_nsamples'] = w4950.measurement.quality.nsamples
    row['w4950_std_abs'] = w4950.measurement.quality.absolute
    row['ag3458a_2_value'] = ag3458a_2.measurement.fetch(360)
    row['temp_2'] = None
    row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
    row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
    row['ag3458a_2_range'] = ag3458a_2.range

    print(f"{row['w4950_value']}", end='')
    if w4950.measurement_function in ('ac_volts', 'ac_current'):
        row['w4950_freq'] = w4950.measurement.freq
        print(f", freq: {row['w4950_freq']}", end='')
    else:
        row['w4950_freq'] = None
    print(f", ag3458a_2: {row['ag3458a_2_value']}")
    try:
        check_valid_value(w4950, row['w4950_value'])
        check_valid_value(ag3458a_2, row['ag3458a_2_value'])
    except IOError:
        if retry_count > 20:
            raise
        return read_row(inits, retry_count+1)
    return row, True


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()


if __name__ == '__main__':
    main()
