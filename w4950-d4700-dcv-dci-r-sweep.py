#!/usr/bin/python3

import ivi
import datetime
import csv
import os

from common_step_execution import (Step, DcVoltageDutSettings, run_procedure, DcVoltageCommand, check_valid_value, Res4WDutSettings, FourWireResistanceCommand, DcCurrentCommand,
                                   DcCurrentDutSettings)

OUTPUT_FILE_DCV = 'w4950-d4700-dcv-sweep.csv'
OUTPUT_FILE_DCI = 'w4950-d4700-dci-sweep.csv'
OUTPUT_FILE_R = 'w4950-d4700-resistance-sweep.csv'
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

procedure_r4w1 = [
    # Step('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'w4950', FourWireResistanceCommand(10e3), True),
]

procedure_dcv1 = [
    # Step('F7001bat', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'w4950', DcVoltageCommand(10), True),
    # Step('F7001bat', '10 V', DcVoltageDutSettings(range=10, value=10), 'w4950', DcVoltageCommand(10), True),
    # Step('Datron 4700', 'short', DcVoltageDutSettings(range=10, value=0), 'w4950', DcVoltageCommand(10), True),
    # Step('Datron 4700', '10 V', DcVoltageDutSettings(range=10, value=10), 'w4950', DcVoltageCommand(10)),
    # Step('Datron 4700', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'w4950', DcVoltageCommand(10)),
    # Step('Datron 4700', '19 V', DcVoltageDutSettings(range=10, value=19), 'w4950', DcVoltageCommand(19)),
    # Step('Datron 4700', '-19 V', DcVoltageDutSettings(range=10, value=-19), 'w4950', DcVoltageCommand(19)),
    # Step('Datron 4700', 'short', DcVoltageDutSettings(range=100, value=0), 'w4950', DcVoltageCommand(100)),
    # Step('Datron 4700', '100 V', DcVoltageDutSettings(range=100, value=100), 'w4950', DcVoltageCommand(100)),
    # Step('Datron 4700', '-100 V', DcVoltageDutSettings(range=100, value=-100), 'w4950', DcVoltageCommand(100)),
    # Step('Datron 4700', 'short', DcVoltageDutSettings(range=1000, value=0), 'w4950', DcVoltageCommand(1000)),
    # Step('Datron 4700', '1000 V', DcVoltageDutSettings(range=1000, value=1000), 'w4950', DcVoltageCommand(1000)),
    # Step('Datron 4700', '-1000 V', DcVoltageDutSettings(range=1000, value=-1000), 'w4950', DcVoltageCommand(1000)),
    # Step('Datron 4700', 'short', DcVoltageDutSettings(range=100e-3, value=0), 'w4950', DcVoltageCommand(100e-3)),
    # Step('Datron 4700', '100 mV', DcVoltageDutSettings(range=100e-3, value=100e-3), 'w4950', DcVoltageCommand(100e-3)),
    # Step('Datron 4700', '-100 mV', DcVoltageDutSettings(range=100e-3, value=-100e-3), 'w4950', DcVoltageCommand(100e-3)),
    # Step('Datron 4700', 'short', DcVoltageDutSettings(range=1, value=0), 'w4950', DcVoltageCommand(1)),
    # Step('Datron 4700', '1 V', DcVoltageDutSettings(range=1, value=1), 'w4950', DcVoltageCommand(1)),
    # Step('Datron 4700', '-1 V', DcVoltageDutSettings(range=1, value=-1), 'w4950', DcVoltageCommand(1)),
    # Step('Datron 4700', 'short', DcVoltageDutSettings(range=10, value=0), 'w4950', DcVoltageCommand(10)),
    # Step('Datron 4700', '10 V', DcVoltageDutSettings(range=10, value=10), 'w4950', DcVoltageCommand(10)),
    # Step('Datron 4700', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'w4950', DcVoltageCommand(10)),
]

procedure_dci = [
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=100e-6, value=0), 'w4950', DcCurrentCommand(100e-6)),
    # Step('Datron 4700', '-100 uA', DcCurrentDutSettings(range=100e-6, value=-100e-6), 'w4950', DcCurrentCommand(100e-6)),
    # Step('Datron 4700', '100 uA', DcCurrentDutSettings(range=100e-6, value=100e-6), 'w4950', DcCurrentCommand(100e-6)),
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=1e-3, value=0), 'w4950', DcCurrentCommand(1e-3)),
    # Step('Datron 4700', '-1 mA', DcCurrentDutSettings(range=1e-3, value=-1e-3), 'w4950', DcCurrentCommand(1e-3)),
    # Step('Datron 4700', '1 mA', DcCurrentDutSettings(range=1e-3, value=1e-3), 'w4950', DcCurrentCommand(1e-3)),
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=10e-3, value=0), 'w4950', DcCurrentCommand(10e-3)),
    # Step('Datron 4700', '-10 mA', DcCurrentDutSettings(range=10e-3, value=-10e-3), 'w4950', DcCurrentCommand(10e-3)),
    # Step('Datron 4700', '10 mA', DcCurrentDutSettings(range=10e-3, value=10e-3), 'w4950', DcCurrentCommand(10e-3)),
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=100e-3, value=0), 'w4950', DcCurrentCommand(100e-3)),
    # Step('Datron 4700', '-100 mA', DcCurrentDutSettings(range=100e-3, value=-100e-3), 'w4950', DcCurrentCommand(100e-3)),
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=100e-3, value=0), 'w4950', DcCurrentCommand(100e-3)),
    # Step('Datron 4700', '100 mA', DcCurrentDutSettings(range=100e-3, value=100e-3), 'w4950', DcCurrentCommand(100e-3)),
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=1, value=0), 'w4950', DcCurrentCommand(1)),
    # Step('Datron 4700', '1 A', DcCurrentDutSettings(range=1, value=1), 'w4950', DcCurrentCommand(1)),
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=1, value=0), 'w4950', DcCurrentCommand(1)),
    # Step('Datron 4700', '-1 A', DcCurrentDutSettings(range=1, value=-1), 'w4950', DcCurrentCommand(1)),
    # Step('Datron 4700', 'short', DcCurrentDutSettings(range=1, value=0), 'w4950', DcCurrentCommand(1)),
]

procedure_r4w2 = [
    # Step('Datron 4700', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'w4950', FourWireResistanceCommand(10e3)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=10e3, value=0), 'w4950', FourWireResistanceCommand(10e3)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=1e3, value=0), 'w4950', FourWireResistanceCommand(1e3)),
    # Step('Datron 4700', '1 kOhm', Res4WDutSettings(range=1e3, value=1e3), 'w4950', FourWireResistanceCommand(1e3)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=100, value=0), 'w4950', FourWireResistanceCommand(100)),
    # Step('Datron 4700', '100 Ohm', Res4WDutSettings(range=100, value=100), 'w4950', FourWireResistanceCommand(100)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=10, value=0), 'w4950', FourWireResistanceCommand(10)),
    # Step('Datron 4700', '10 Ohm', Res4WDutSettings(range=10, value=10), 'w4950', FourWireResistanceCommand(10)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=100e6, value=0), 'w4950', FourWireResistanceCommand(100e6)),
    # Step('Datron 4700', '100 MOhm', Res4WDutSettings(range=100e6, value=100e6), 'w4950', FourWireResistanceCommand(100e6)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=10e6, value=0), 'w4950', FourWireResistanceCommand(10e6)),
    # Step('Datron 4700', '10 MOhm', Res4WDutSettings(range=10e6, value=10e6), 'w4950', FourWireResistanceCommand(10e6)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=1e6, value=0), 'w4950', FourWireResistanceCommand(1e6)),
    # Step('Datron 4700', '1 MOhm', Res4WDutSettings(range=1e6, value=1e6), 'w4950', FourWireResistanceCommand(1e6)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=100e3, value=0), 'w4950', FourWireResistanceCommand(100e3)),
    # Step('Datron 4700', '100 kOhm', Res4WDutSettings(range=100e3, value=100e3), 'w4950', FourWireResistanceCommand(100e3)),
    # Step('Datron 4700', 'short', Res4WDutSettings(range=10e3, value=0), 'w4950', FourWireResistanceCommand(10e3)),
    # Step('Datron 4700', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'w4950', FourWireResistanceCommand(10e3)),
    # Step('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3), 'w4950', FourWireResistanceCommand(10e3), True),
]

procedure_dcv2 = [
    Step('F7001bat', '-10 V', DcVoltageDutSettings(range=10, value=-10), 'w4950', DcVoltageCommand(10), True),
    Step('F7001bat', '10 V', DcVoltageDutSettings(range=10, value=10), 'w4950', DcVoltageCommand(10), True),
]

def main():
    inits = init_func()
    with open(OUTPUT_FILE_DCV, 'a', newline='') as csv_file_dcv, open(OUTPUT_FILE_DCI, 'a', newline='') as csv_file_dci, open(OUTPUT_FILE_R, 'a', newline='') as csv_file_r:
        initial_size_dcv = os.fstat(csv_file_dcv.fileno()).st_size
        initial_size_dci = os.fstat(csv_file_dci.fileno()).st_size
        initial_size_r = os.fstat(csv_file_r.fileno()).st_size
        csvw_dcv = csv.DictWriter(csv_file_dcv, fieldnames=FIELDNAMES)
        csvw_dci = csv.DictWriter(csv_file_dci, fieldnames=FIELDNAMES)
        csvw_r = csv.DictWriter(csv_file_r, fieldnames=FIELDNAMES)
        if initial_size_dcv == 0:
            csvw_dcv.writeheader()
        if initial_size_dci == 0:
            csvw_dci.writeheader()
        if initial_size_r == 0:
            csvw_r.writeheader()
        run_procedure(csvw_r, procedure_r4w1, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)
        run_procedure(csvw_dcv, procedure_dcv1, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)
        run_procedure(csvw_dci, procedure_dci, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)
        run_procedure(csvw_r, procedure_r4w2, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)
        run_procedure(csvw_dcv, procedure_dcv2, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)


def init_func():
    w4950 = ivi.datron_wavetek.wavetek4950("TCPIP::gpib4::gpib0,20::INSTR", reset=True)
    w4950._interface.timeout = 120
    w4950.last_temp = datetime.datetime.utcnow()
    # d4700 = ivi.datron_wavetek.datron4700("TCPIP::gpib4::gpib0,16::INSTR")
    d4700 = None
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
