#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import Step, Res4WDutSettings, FourWireResistanceCommand, run_procedure, check_valid_value

OUTPUT_FILE = 'ks3458a-d4700-resistance-sweep.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'ag3458a_2_ohm', 'temp_2', 'last_acal_2',
              'last_acal_2_cal72', '3458a_2_function', 'ag3458a_2_range', 'ag3458a_2_delay')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 60
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    Step('SR104', '10 kOhm', Res4WDutSettings(), 'ag3458a_2', FourWireResistanceCommand(10e3), True),
    Step('Datron 4700', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'ag3458a_2', FourWireResistanceCommand(10e3), True),
    Step('Datron 4700', 'short', Res4WDutSettings(range=10e3, value=0), 'ag3458a_2', FourWireResistanceCommand(10e3)),
    Step('Datron 4700', '1 kOhm', Res4WDutSettings(range=1e3, value=1e3), 'ag3458a_2', FourWireResistanceCommand(10e3)),
    Step('Datron 4700', '1 kOhm', Res4WDutSettings(range=1e3, value=1e3), 'ag3458a_2', FourWireResistanceCommand(1e3)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=1e3, value=0), 'ag3458a_2', FourWireResistanceCommand(1e3)),
    Step('Datron 4700', '100 Ohm', Res4WDutSettings(range=100, value=100), 'ag3458a_2', FourWireResistanceCommand(1e3)),
    Step('Datron 4700', '100 Ohm', Res4WDutSettings(range=100, value=100), 'ag3458a_2', FourWireResistanceCommand(100)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=100, value=0), 'ag3458a_2', FourWireResistanceCommand(100)),
    Step('Datron 4700', '10 Ohm', Res4WDutSettings(range=10, value=10), 'ag3458a_2', FourWireResistanceCommand(100)),
    Step('Datron 4700', '10 Ohm', Res4WDutSettings(range=10, value=10), 'ag3458a_2', FourWireResistanceCommand(10)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=10, value=0), 'ag3458a_2', FourWireResistanceCommand(10)),
    Step('Datron 4700', '10 Ohm', Res4WDutSettings(range=10, value=10), 'ag3458a_2', FourWireResistanceCommand(100)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=100, value=0), 'ag3458a_2', FourWireResistanceCommand(100)),
    Step('Datron 4700', '100 Ohm', Res4WDutSettings(range=100, value=100), 'ag3458a_2', FourWireResistanceCommand(100)),
    Step('Datron 4700', '100 Ohm', Res4WDutSettings(range=100, value=100), 'ag3458a_2', FourWireResistanceCommand(1e3)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=1e3, value=0), 'ag3458a_2', FourWireResistanceCommand(1e3)),
    Step('Datron 4700', '1 kOhm', Res4WDutSettings(range=1e3, value=1e3), 'ag3458a_2', FourWireResistanceCommand(1e3)),
    Step('Datron 4700', '1 kOhm', Res4WDutSettings(range=1e3, value=1e3), 'ag3458a_2', FourWireResistanceCommand(10e3)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=10e3, value=0), 'ag3458a_2', FourWireResistanceCommand(10e3)),
    Step('Datron 4700', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'ag3458a_2', FourWireResistanceCommand(10e3)),
    Step('Datron 4700', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'ag3458a_2', FourWireResistanceCommand(100e3)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=10e3, value=0), 'ag3458a_2', FourWireResistanceCommand(100e3)),
    Step('Datron 4700', '100 kOhm', Res4WDutSettings(range=100e3, value=100e3), 'ag3458a_2', FourWireResistanceCommand(100e3)),
    Step('Datron 4700', '100 kOhm', Res4WDutSettings(range=100e3, value=100e3), 'ag3458a_2', FourWireResistanceCommand(1e6)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=100e3, value=0), 'ag3458a_2', FourWireResistanceCommand(1e6)),
    Step('Datron 4700', '1 MOhm', Res4WDutSettings(range=1e6, value=1e6), 'ag3458a_2', FourWireResistanceCommand(1e6)),
    Step('Datron 4700', '1 MOhm', Res4WDutSettings(range=1e6, value=1e6), 'ag3458a_2', FourWireResistanceCommand(10e6, 'two_wire_resistance')),
    Step('Datron 4700', 'short', Res4WDutSettings(range=1e6, value=0), 'ag3458a_2', FourWireResistanceCommand(10e6, 'two_wire_resistance')),
    Step('Datron 4700', '10 MOhm', Res4WDutSettings(range=10e6, value=10e6), 'ag3458a_2', FourWireResistanceCommand(10e6, 'two_wire_resistance')),
    Step('Datron 4700', '10 MOhm', Res4WDutSettings(range=10e6, value=10e6), 'ag3458a_2', FourWireResistanceCommand(100e6, 'two_wire_resistance')),
    Step('Datron 4700', 'short', Res4WDutSettings(range=10e6, value=0), 'ag3458a_2', FourWireResistanceCommand(100e6, 'two_wire_resistance')),
    Step('Datron 4700', '100 MOhm', Res4WDutSettings(range=100e6, value=100e6), 'ag3458a_2', FourWireResistanceCommand(100e6, 'two_wire_resistance')),
    Step('Datron 4700', '10 MOhm', Res4WDutSettings(range=10e6, value=10e6), 'ag3458a_2', FourWireResistanceCommand(100e6, 'two_wire_resistance')),
    Step('Datron 4700', '10 MOhm', Res4WDutSettings(range=10e6, value=10e6), 'ag3458a_2', FourWireResistanceCommand(10e6, 'two_wire_resistance')),
    Step('Datron 4700', 'short', Res4WDutSettings(range=1e6, value=0), 'ag3458a_2', FourWireResistanceCommand(10e6, 'two_wire_resistance')),
    Step('Datron 4700', '1 MOhm', Res4WDutSettings(range=1e6, value=1e6), 'ag3458a_2', FourWireResistanceCommand(10e6, 'two_wire_resistance')),
    Step('Datron 4700', '1 MOhm', Res4WDutSettings(range=1e6, value=1e6), 'ag3458a_2', FourWireResistanceCommand(1e6)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=100e3, value=0), 'ag3458a_2', FourWireResistanceCommand(1e6)),
    Step('Datron 4700', '100 kOhm', Res4WDutSettings(range=100e3, value=100e3), 'ag3458a_2', FourWireResistanceCommand(1e6)),
    Step('Datron 4700', '100 kOhm', Res4WDutSettings(range=100e3, value=100e3), 'ag3458a_2', FourWireResistanceCommand(100e3)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=10e3, value=0), 'ag3458a_2', FourWireResistanceCommand(100e3)),
    Step('Datron 4700', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'ag3458a_2', FourWireResistanceCommand(100e3)),
    Step('Datron 4700', 'short', Res4WDutSettings(range=10e3, value=0), 'ag3458a_2', FourWireResistanceCommand(10e3)),
    Step('Datron 4700', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'ag3458a_2', FourWireResistanceCommand(10e3)),
    Step('SR104', '10 kOhm', Res4WDutSettings(), 'ag3458a_2', FourWireResistanceCommand(10e3), True),
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
        ag3458a_2.advanced.offset_compensation = 'on'
        ag3458a_2.advanced.aperture_time = 100
    ag3458a_2.measurement_function = 'four_wire_resistance'
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
    d4700 = ivi.datron_wavetek.datron4700("TCPIP::gpib4::gpib0,16::INSTR")
    return {'ag3458a_2': ag3458a_2, 'd4700': d4700}


def read_row(inits):
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
    else:
        ag3458a_2.measurement.initiate()
        row['ag3458a_2_ohm'] = ag3458a_2.measurement.fetch(360)
        row['temp_2'] = None
        row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
        row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
        row['ag3458a_2_range'] = ag3458a_2.range
        row['ag3458a_2_delay'] = ag3458a_2.trigger.delay
        print(f"{row['ag3458a_2_ohm']}")
        check_valid_value(ag3458a_2, row['ag3458a_2_ohm'])
    return row, row['temp_2'] is None


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ohms()


if __name__ == '__main__':
    main()
