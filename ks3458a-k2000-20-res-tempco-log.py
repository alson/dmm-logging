#!/usr/bin/python3
import argparse
import csv
import datetime
import sys
from typing import List
import ivi
from quantiphy import Quantity
import os
from copy import deepcopy

from common_step_execution import Dut, FourWireResistanceCommand, Instrument, Step2, Res4WDutSettings, Step3, StepInterrupted, TransferDirection, disable_manual_prompt_for_steps_with_same_dut, generate_resistance_transfer_steps, resistance_is_4w, Res2WDutSettings, run_procedure

OUTPUT_FILE = 'ks3458a-k2000-20-res-tempco-log.csv'
FIELDNAMES = ('datetime', 'dut_setting', 'dut', 'ag3458a_2_ohm', 'ag3458a_2_range', 'ag3458a_2_delay', 'temp_2', 'last_acal_2',
              'last_acal_2_cal72', 'k2000_20_pt100_ohm')
DEBUG = False
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 150
if DEBUG:
    SAMPLES_PER_STEP = 2
    STEP_SOAK_TIME = 0

def acal_3458a(ag3458a, temp):
    print()
    print(f'Running ACAL on {ag3458a._interface.name} at {temp}')
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
    subject_dut = Dut(name=args.dut, setting=Quantity(args.dut_value, 'Ohm'), dut_setting_cmd=(Res4WDutSettings(value=args.dut_value, range=args.dut_value) if resistance_is_4w(args.dut_value) else Res2WDutSettings(value=args.dut_value, range=args.dut_value)))
    start_steps = generate_resistance_transfer_steps(ag3458a, sr104_dut, f5450a_dut, subject_dut, TransferDirection.FORWARD)[:-1]
    steps = []
    steps.extend(start_steps)
    subject_dut_step = Step3(subject_dut, [Instrument(ag3458a.name, setting=FourWireResistanceCommand(range=ag3458a.setting.range, allow_acal=True))], manual_prompt=True, run_until_interrupted=True)
    steps.append(subject_dut_step)
    end_steps = generate_resistance_transfer_steps(ag3458a, sr104_dut, f5450a_dut, subject_dut, TransferDirection.REVERSE)[1:]
    steps.extend(end_steps)
    steps = disable_manual_prompt_for_steps_with_same_dut(deepcopy(steps))
    steps[0].manual_prompt = False

    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        while True:
            try:
                run_procedure(csvw, steps, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)
            except StepInterrupted as step_interrupted:
                for instrument in steps[step_interrupted.step_number].instruments:
                    inits[instrument.name]._interface.clear()
                steps = ask_user_for_procedure(step_interrupted.step_number, steps, start_steps, subject_dut_step, end_steps, inits)
                steps = disable_manual_prompt_for_steps_with_same_dut(deepcopy(steps))
            else:
                break


def ask_user_for_procedure(step_number: int, steps: List[Step3], start_steps: List[Step3], subject_dut_step: Step3, end_steps: List[Step3], inits: dict):
    if step_equal_except_manual_prompt(steps[step_number], subject_dut_step):
        return ask_user_for_procedure_subject_dut_step(step_number, steps, start_steps, subject_dut_step, end_steps, inits)
    else:
        return ask_user_for_procedure_other_step(step_number, steps, start_steps, subject_dut_step, end_steps, inits)

def ask_user_for_procedure_subject_dut_step(step_number: int, steps: List[Step3], start_steps: List[Step3], subject_dut_step: Step3, end_steps: List[Step3], inits: dict):
    while True:
        print('Subject step interrupted, do you want to:')
        print('0. Immediately quit')
        print('1. Continue from the interrupted step')
        print('2. Run acal and continue from interrupted step')
        print('3. Continue from next step')
        print('4. Repeat from the beginning')
        print('5. End the measurement')
        print('6. Measure reference resistor and continue')

        response = input('Enter 0, 1, 2, 3, 4, 5 or 6: ')
        if response == '0':
            sys.exit()
        elif response == '1':
            return steps[step_number:]
        elif response == '2':
            acal_3458a(inits[subject_dut_step.instruments[0].name], 'manual_acal')
            return steps[step_number:]
        elif response == '3':
            return steps[step_number+1:]
        elif response == '4':
            return start_steps + [subject_dut_step] + end_steps
        elif response == '5':
            return end_steps
        elif response == '6':
            return end_steps + start_steps[1:] + [subject_dut_step] + end_steps


def ask_user_for_procedure_other_step(step_number: int, steps: List[Step3], start_steps: List[Step3], subject_dut_step: Step3, end_steps: List[Step3], inits: dict):
    while True:
        print('Step interrupted, do you want to:')
        print('0. Immediately quit')
        print('1. Continue from the interrupted step')
        print('2. Run acal and continue from interrupted step')
        print('3. Continue from next step')
        print('4. Repeat from the beginning')

        response = input('Enter 0, 1, 2, 3, or 4: ')
        if response == '0':
            sys.exit()
        elif response == '1':
            return steps[step_number:]
        elif response == '2':
            acal_3458a(inits['ag3458a_2'], 'manual_acal')
            return steps[step_number:]
        elif response == '3':
            return steps[step_number+1:]
        elif response == '4':
            return start_steps + [subject_dut_step] + end_steps


def step_equal_except_manual_prompt(step1: Step3, step2: Step3):
    step1_copy = deepcopy(step1)
    step2_copy = deepcopy(step2)
    step1_copy.manual_prompt = False
    step2_copy.manual_prompt = False
    return step1_copy == step2_copy


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
    else:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
    acal_3458a(ag3458a_2, temp_2)
    return {'ag3458a_2': ag3458a_2, 'k2000_20': k2000_20}


def read_row(inits, instruments: List[Instrument]):
    ag3458a_2 = inits['ag3458a_2']
    ag3458a_2_instrument = instruments[0]
    k2000_20 = inits['k2000_20']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 30 * 60):
        do_acal_3458a_2 = False
        temp_2 = ag3458a_2.utility.temp
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        if ag3458a_2_instrument.setting.allow_acal and ((datetime.datetime.utcnow() - ag3458a_2.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_2.last_acal_temp - temp_2) >= 0.5):
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
