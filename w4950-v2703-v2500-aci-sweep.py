#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import Step, run_procedure, AcCurrentDutSettings, AcCurrentCommand, beep, check_valid_value

OUTPUT_FILE = 'w4950-v2703-v2500-aci-sweep.csv'
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
    Step('Valhalla 2703', '100 uA 20 Hz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=20), 'w4950', AcCurrentCommand(100e-6, freq=20), True),
    Step('Valhalla 2703', '1 mA 20 Hz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=20), 'w4950', AcCurrentCommand(1e-3, freq=20), True),
    Step('Valhalla 2703', '10 mA 20 Hz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=20), 'w4950', AcCurrentCommand(10e-3, freq=20), True),
    Step('Valhalla 2703', '100 mA 20 Hz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=20), 'w4950', AcCurrentCommand(100e-3, freq=20), True),
    Step('Valhalla 2703', '1 A 20 Hz', AcCurrentDutSettings(range=1, value=1, freq=20), 'w4950', AcCurrentCommand(1, freq=20), True),
    Step('Valhalla 2703', '100 uA 55 Hz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=55), 'w4950', AcCurrentCommand(100e-6, freq=55), True),
    Step('Valhalla 2703', '1 mA 55 Hz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=55), 'w4950', AcCurrentCommand(1e-3, freq=55), True),
    Step('Valhalla 2703', '10 mA 55 Hz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=55), 'w4950', AcCurrentCommand(10e-3, freq=55), True),
    Step('Valhalla 2703', '100 mA 55 Hz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=55), 'w4950', AcCurrentCommand(100e-3, freq=55), True),
    Step('Valhalla 2703', '1 A 55 Hz', AcCurrentDutSettings(range=1, value=1, freq=55), 'w4950', AcCurrentCommand(1, freq=55), True),
    Step('Valhalla 2703', '100 uA 300 Hz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=300), 'w4950', AcCurrentCommand(100e-6, freq=300), True),
    Step('Valhalla 2703', '1 mA 300 Hz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=300), 'w4950', AcCurrentCommand(1e-3, freq=300), True),
    Step('Valhalla 2703', '10 mA 300 Hz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=300), 'w4950', AcCurrentCommand(10e-3, freq=300), True),
    Step('Valhalla 2703', '100 mA 300 Hz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=300), 'w4950', AcCurrentCommand(100e-3, freq=300), True),
    Step('Valhalla 2703', '1 A 300 Hz', AcCurrentDutSettings(range=1, value=1, freq=300), 'w4950', AcCurrentCommand(1, freq=300), True),
    Step('Valhalla 2703', '100 uA 1 kHz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=1e3), 'w4950', AcCurrentCommand(100e-6, freq=1e3), True),
    Step('Valhalla 2703', '1 mA 1 kHz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=1e3), 'w4950', AcCurrentCommand(1e-3, freq=1e3), True),
    Step('Valhalla 2703', '10 mA 1 kHz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=1e3), 'w4950', AcCurrentCommand(10e-3, freq=1e3), True),
    Step('Valhalla 2703', '100 mA 1 kHz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=1e3), 'w4950', AcCurrentCommand(100e-3, freq=1e3), True),
    Step('Valhalla 2703', '1 A 1 kHz', AcCurrentDutSettings(range=1, value=1, freq=1e3), 'w4950', AcCurrentCommand(1, freq=1e3), True),
    Step('Valhalla 2703', '100 uA 5 kHz', AcCurrentDutSettings(range=100e-6, value=100e-6, freq=5e3), 'w4950', AcCurrentCommand(100e-6, freq=5e3), True),
    Step('Valhalla 2703', '1 mA 5 kHz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=5e3), 'w4950', AcCurrentCommand(1e-3, freq=5e3), True),
    Step('Valhalla 2703', '10 mA 5 kHz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=5e3), 'w4950', AcCurrentCommand(10e-3, freq=5e3), True),
    Step('Valhalla 2703', '100 mA 5 kHz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=5e3), 'w4950', AcCurrentCommand(100e-3, freq=5e3), True),
    Step('Valhalla 2703', '1 A 5 kHz', AcCurrentDutSettings(range=1, value=1, freq=5e3), 'w4950', AcCurrentCommand(1, freq=5e3), True),
    Step('Valhalla 2703', '1 mA 10 kHz', AcCurrentDutSettings(range=1e-3, value=1e-3, freq=10e3), 'w4950', AcCurrentCommand(1e-3, freq=10e3), True),
    Step('Valhalla 2703', '10 mA 10 kHz', AcCurrentDutSettings(range=10e-3, value=10e-3, freq=10e3), 'w4950', AcCurrentCommand(10e-3, freq=10e3), True),
    Step('Valhalla 2703', '100 mA 10 kHz', AcCurrentDutSettings(range=100e-3, value=100e-3, freq=10e3), 'w4950', AcCurrentCommand(100e-3, freq=10e3), True),
    Step('Valhalla 2703', '1 A 10 kHz', AcCurrentDutSettings(range=1, value=1, freq=10e3), 'w4950', AcCurrentCommand(1, freq=10e3), True),
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


def read_row(inits, retry_count=1):
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
    try:
        check_valid_value(w4950, row['w4950_value'])
    except IOError:
        if retry_count > 20:
            raise
        return read_row(inits, retry_count+1)
    return row, True


if __name__ == '__main__':
    main()
