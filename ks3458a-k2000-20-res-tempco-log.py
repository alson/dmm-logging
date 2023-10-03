#!/usr/bin/python3
import argparse
import csv
import datetime
import ivi
import time
import os

from common_step_execution import Dut, FourWireResistanceCommand, Instrument, Step2, Res4WDutSettings, Step3, TransferDirection, generate_resistance_transfer_steps, resistance_is_4w, Res2WDutSettings, run_procedure

OUTPUT_FILE = 'ks3458a-k2000-20-res-tempco-log.csv'
FIELDNAMES = ('datetime', 'dut_setting', 'dut', 'ag3458a_2_ohm', 'ag3458a_2_range', 'ag3458a_2_delay', 'temp_2', 'last_acal_2',
              'last_acal_2_cal72', 'k2000_20_pt100_ohm')
WRITE_INTERVAL_SECONDS = 900
DEBUG = False
SAMPLE_INTERVAL = 0
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 300
if DEBUG:
    SAMPLES_PER_STEP = 2
    STEP_SOAK_TIME = 1
    WRITE_INTERVAL_SECONDS = 0

def acal_3458a(ag3458a, temp):
    if DEBUG:
        ag3458a.last_acal_cal72 = 'keep'
        return
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ohms()


def ag3458a_setup(ag3458a):
    ag3458a.measurement_function = 'four_wire_resistance'
    ag3458a.advanced.offset_compensation = 'on'
    if DEBUG:
        ag3458a.advanced.offset_compensation = 'off'
        ag3458a.advanced.aperture_time = 1


def main():
    parser = argparse.ArgumentParser(description='Transfer resistance from SR104 using F5450A and log tempco of resistor under test')
    parser.add_argument('dut', type=str)
    parser.add_argument('dut_value', type=float)

    args = parser.parse_args()

    inits = init_func()
    ag3458a = Instrument('ag3458a_2', FourWireResistanceCommand(range=args.dut_value))
    sr104_dut = Dut(name='SR104', setting='10 kOhm', dut_setting_cmd=Res4WDutSettings(value=10e3))
    f5450a_dut = Dut(name='Fluke 5450A', setting='', dut_setting_cmd=Res4WDutSettings())
    subject_dut = Dut(name=args.dut, setting=f'{args.dut_value} Ohm', dut_setting_cmd=(Res4WDutSettings() if resistance_is_4w(args.dut_value) else Res2WDutSettings()))
    steps = generate_resistance_transfer_steps(ag3458a, sr104_dut, f5450a_dut, args.dut_value, TransferDirection.FORWARD)
    steps.append(Step3(subject_dut, [ag3458a], True, True))
    steps.extend(generate_resistance_transfer_steps(ag3458a, sr104_dut, f5450a_dut, args.dut_value, TransferDirection.REVERSE))

    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        run_procedure(csvw, steps, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)


def init_func():
    k2000_20 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,17::INSTR",
            id_query=True)
    k2000_20._interface.timeout = 120
    if not DEBUG:
        k2000_20._write(':DISPLAY:ENABLE OFF')
    k2000_20.measurement_function = 'four_wire_resistance'
    k2000_20.range = 110
    k2000_20._write(':FRES:NPLC 10')

    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
            reset=True)
    ag3458a_2._interface.timeout = 120
    ag3458a_setup(ag3458a_2)
    temp_2 = ag3458a_2.utility.temp
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
        # finish_acal_3458a(ag3458a_2)
    else:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        acal_3458a(ag3458a_2, temp_2)
    return {'ag3458a_2': ag3458a_2, 'k2000_20': k2000_20}


def read_row(inits, instruments):
    ag3458a_2 = inits['ag3458a_2']
    k2000_20 = inits['k2000_20']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 30 * 60):
        do_acal_3458a_2 = False
        temp_2 = ag3458a_2.utility.temp
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        if ((datetime.datetime.utcnow() - ag3458a_2.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_2.last_acal_temp - temp_2) >= 1):
            do_acal_3458a_2 = True
        if do_acal_3458a_2:
            acal_3458a(ag3458a_2, temp_2)
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
        row['k2000_20_pt100_ohm'] = k2000_20.measurement.fetch(1)
        print(f"{row['ag3458a_2_ohm']}")
    return row, row['temp_2'] is None


if __name__ == '__main__':
    main()
