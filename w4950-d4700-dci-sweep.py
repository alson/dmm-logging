#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import Step, run_procedure, DcCurrentDutSettings, DcCurrentCommand, check_valid_value

OUTPUT_FILE = 'w4950-d4700-dci-sweep.csv'
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
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=100e-6, value=0), 'w4950', DcCurrentCommand(100e-6)),
    Step('Datron 4700', '-100 uA', DcCurrentDutSettings(range=100e-6, value=-100e-6), 'w4950', DcCurrentCommand(100e-6)),
    Step('Datron 4700', '100 uA', DcCurrentDutSettings(range=100e-6, value=100e-6), 'w4950', DcCurrentCommand(100e-6)),
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=1e-3, value=0), 'w4950', DcCurrentCommand(1e-3)),
    Step('Datron 4700', '-1 mA', DcCurrentDutSettings(range=1e-3, value=-1e-3), 'w4950', DcCurrentCommand(1e-3)),
    Step('Datron 4700', '1 mA', DcCurrentDutSettings(range=1e-3, value=1e-3), 'w4950', DcCurrentCommand(1e-3)),
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=10e-3, value=0), 'w4950', DcCurrentCommand(10e-3)),
    Step('Datron 4700', '-10 mA', DcCurrentDutSettings(range=10e-3, value=-10e-3), 'w4950', DcCurrentCommand(10e-3)),
    Step('Datron 4700', '10 mA', DcCurrentDutSettings(range=10e-3, value=10e-3), 'w4950', DcCurrentCommand(10e-3)),
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=100e-3, value=0), 'w4950', DcCurrentCommand(100e-3)),
    Step('Datron 4700', '-100 mA', DcCurrentDutSettings(range=100e-3, value=-100e-3), 'w4950', DcCurrentCommand(100e-3)),
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=100e-3, value=0), 'w4950', DcCurrentCommand(100e-3)),
    Step('Datron 4700', '100 mA', DcCurrentDutSettings(range=100e-3, value=100e-3), 'w4950', DcCurrentCommand(100e-3)),
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=1, value=0), 'w4950', DcCurrentCommand(1)),
    Step('Datron 4700', '1 A', DcCurrentDutSettings(range=1, value=1), 'w4950', DcCurrentCommand(1)),
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=1, value=0), 'w4950', DcCurrentCommand(1)),
    Step('Datron 4700', '-1 A', DcCurrentDutSettings(range=1, value=-1), 'w4950', DcCurrentCommand(1)),
    Step('Datron 4700', 'short', DcCurrentDutSettings(range=1, value=0), 'w4950', DcCurrentCommand(1)),
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
    d4700 = ivi.datron_wavetek.datron4700("TCPIP::gpib4::gpib0,16::INSTR")
    return {'w4950': w4950, 'd4700': d4700}


def read_row(inits, instruments):
    w4950 = inits['w4950']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
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
    if w4950.measurement_function in ('ac_volts', 'ac_current'):
        row['w4950_freq'] = w4950.measurement.freq
    else:
        row['w4950_freq'] = None
    print(f"{row['w4950_value']}")
    check_valid_value(w4950, row['w4950_value'])
    return row, True


if __name__ == '__main__':
    main()
