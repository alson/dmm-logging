#!/usr/bin/python3
from typing import List

import time

import ivi
import datetime
import csv
import os

from common_step_execution import (Step3, run_procedure, AcVoltageDutSettings, AcVoltageCommand, check_valid_value, Instrument, Dut)

OUTPUT_FILE = 'ks3458a1-w4920-w4950-v2703-acv-sweep.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'w4920_function', 'w4920_range', 'w4920_freq',
              'w4920_value', 'w4950_function', 'w4950_range', 'w4950_percentage', 'w4950_freq',
              'w4950_value', 'w4950_nsamples', 'w4950_std_abs', 'w4950_temp', 'ag3458a_1_value',
              'temp_1', 'last_acal_1', 'last_acal_1_cal72', '3458a_1_function', 'ag3458a_1_range')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 60
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    # 4920 + 4950
    # Step3(Dut('Valhalla 2703', '1000 V 1 kHz', AcVoltageDutSettings(range=1000, value=1000, freq=1e3)), [Instrument('w4920', AcVoltageCommand(1000, freq=1e31)), Instrument('w4950', AcVoltageCommand(1000, freq=1e3))], True),
    # Step3(Dut('Valhalla 2703', '1000 V 300 Hz', AcVoltageDutSettings(range=1000, value=1000, freq=300)), [Instrument('w4920', AcVoltageCommand(1000, freq=3001)), Instrument('w4950', AcVoltageCommand(1000, freq=300))], True),
    # Step3(Dut('Valhalla 2703', '1000 V 55 Hz', AcVoltageDutSettings(range=1000, value=1000, freq=55)), [Instrument('w4920', AcVoltageCommand(1000, freq=551)), Instrument('w4950', AcVoltageCommand(1000, freq=55))], True),
    # Step3(Dut('Valhalla 2703', '1000 V 20 Hz', AcVoltageDutSettings(range=1000, value=1000, freq=20)), [Instrument('w4920', AcVoltageCommand(1000, freq=201)), Instrument('w4950', AcVoltageCommand(1000, freq=20))], True),

    # 4920 + 3458
    # Step3(Dut('Valhalla 2703', '700 V 1 kHz', AcVoltageDutSettings(range=1000, value=700, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(700, freq=1e3)), Instrument('w4920', AcVoltageCommand(700, freq=1e31))], True),
    # Step3(Dut('Valhalla 2703', '700 V 300 Hz', AcVoltageDutSettings(range=1000, value=700, freq=300)), [Instrument('ag3458a_1', AcVoltageCommand(700, freq=300)), Instrument('w4920', AcVoltageCommand(700, freq=3001))], True),
    # Step3(Dut('Valhalla 2703', '700 V 55 Hz', AcVoltageDutSettings(range=1000, value=700, freq=55)), [Instrument('ag3458a_1', AcVoltageCommand(700, freq=55)), Instrument('w4920', AcVoltageCommand(700, freq=551))], True),
    # Step3(Dut('Valhalla 2703', '700 V 20 Hz', AcVoltageDutSettings(range=1000, value=700, freq=20)), [Instrument('ag3458a_1', AcVoltageCommand(700, freq=20)), Instrument('w4920', AcVoltageCommand(700, freq=201))], True),
    # Step3(Dut('F510', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=2.4e3)), Instrument('w4920', AcVoltageCommand(10, freq=2.4e31))], True),
    # Step3(Dut('Valhalla 2703', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=10, freq=2.4e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=2.4e3)), Instrument('w4920', AcVoltageCommand(10, freq=2.4e31))], True),

    # 4920 + 4950 + 3458
    # Step3(Dut('Valhalla 2703', '10 V 1 kHz', AcVoltageDutSettings(range=10, value=10, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=1e3)), Instrument('w4920', AcVoltageCommand(10, freq=1e31)), Instrument('w4950', AcVoltageCommand(10, freq=1e3))], True),
    # Step3(Dut('Valhalla 2703', '10 V 10 kHz', AcVoltageDutSettings(range=10, value=10, freq=10e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=10e3)), Instrument('w4920', AcVoltageCommand(10, freq=10e31)), Instrument('w4950', AcVoltageCommand(10, freq=10e3))], True),
    # Step3(Dut('Valhalla 2703', '10 V 20 kHz', AcVoltageDutSettings(range=10, value=10, freq=20e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=20e3)), Instrument('w4920', AcVoltageCommand(10, freq=20e31)), Instrument('w4950', AcVoltageCommand(10, freq=20e3))], True),
    # Step3(Dut('Valhalla 2703', '10 V 50 kHz', AcVoltageDutSettings(range=10, value=10, freq=50e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=50e3)), Instrument('w4920', AcVoltageCommand(10, freq=50e31)), Instrument('w4950', AcVoltageCommand(10, freq=50e3))], True),
    # Step3(Dut('Valhalla 2703', '10 V 100 kHz', AcVoltageDutSettings(range=10, value=10, freq=100e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=100e3)), Instrument('w4920', AcVoltageCommand(10, freq=100e31)), Instrument('w4950', AcVoltageCommand(10, freq=100e3))], True),
    # Step3(Dut('Valhalla 2703', '10 V 300 Hz', AcVoltageDutSettings(range=10, value=10, freq=300)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=300)), Instrument('w4920', AcVoltageCommand(10, freq=3001)), Instrument('w4950', AcVoltageCommand(10, freq=300))], True),
    # Step3(Dut('Valhalla 2703', '10 V 55 Hz', AcVoltageDutSettings(range=10, value=10, freq=55)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=55)), Instrument('w4920', AcVoltageCommand(10, freq=551)), Instrument('w4950', AcVoltageCommand(10, freq=55))], True),
#     Step3(Dut('Valhalla 2703', '10 V 20 Hz', AcVoltageDutSettings(range=10, value=10, freq=20)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=20)), Instrument('w4920', AcVoltageCommand(10, freq=201)), Instrument('w4950', AcVoltageCommand(10, freq=20))], True),
#     Step3(Dut('Valhalla 2703', '19 V 1 kHz', AcVoltageDutSettings(range=10, value=19, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(19, freq=1e3)), Instrument('w4920', AcVoltageCommand(19, freq=1e31)), Instrument('w4950', AcVoltageCommand(19, freq=1e3))], True),
#     Step3(Dut('Valhalla 2703', '100 V 1 kHz', AcVoltageDutSettings(range=100, value=100, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=1e3)), Instrument('w4920', AcVoltageCommand(100, freq=1e31)), Instrument('w4950', AcVoltageCommand(100, freq=1e3))], True),
#     Step3(Dut('Valhalla 2703', '100 V 10 kHz', AcVoltageDutSettings(range=100, value=100, freq=10e3)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=10e3)), Instrument('w4920', AcVoltageCommand(100, freq=10e31)), Instrument('w4950', AcVoltageCommand(100, freq=10e3))], True),
#     Step3(Dut('Valhalla 2703', '100 V 20 kHz', AcVoltageDutSettings(range=100, value=100, freq=20e3)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=20e3)), Instrument('w4920', AcVoltageCommand(100, freq=20e31)), Instrument('w4950', AcVoltageCommand(100, freq=20e3))], True),
#     Step3(Dut('Valhalla 2703', '100 V 50 kHz', AcVoltageDutSettings(range=100, value=100, freq=50e3)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=50e3)), Instrument('w4920', AcVoltageCommand(100, freq=50e31)), Instrument('w4950', AcVoltageCommand(100, freq=50e3))], True),
#     Step3(Dut('Valhalla 2703', '100 V 100 kHz', AcVoltageDutSettings(range=100, value=100, freq=100e3)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=100e3)), Instrument('w4920', AcVoltageCommand(100, freq=100e31)), Instrument('w4950', AcVoltageCommand(100, freq=100e3))], True),
    # Step3(Dut('Valhalla 2703', '100 V 300 Hz', AcVoltageDutSettings(range=100, value=100, freq=300)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=300)), Instrument('w4920', AcVoltageCommand(100, freq=3001)), Instrument('w4950', AcVoltageCommand(100, freq=300))], True),
    # Step3(Dut('Valhalla 2703', '100 V 55 Hz', AcVoltageDutSettings(range=100, value=100, freq=55)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=55)), Instrument('w4920', AcVoltageCommand(100, freq=551)), Instrument('w4950', AcVoltageCommand(100, freq=55))], True),
    # Step3(Dut('Valhalla 2703', '100 V 20 Hz', AcVoltageDutSettings(range=100, value=100, freq=20)), [Instrument('ag3458a_1', AcVoltageCommand(100, freq=20)), Instrument('w4920', AcVoltageCommand(100, freq=201)), Instrument('w4950', AcVoltageCommand(100, freq=20))], True),
    # Step3(Dut('Valhalla 2703', '1 V 1 kHz', AcVoltageDutSettings(range=1, value=1, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=1e3)), Instrument('w4920', AcVoltageCommand(1, freq=1e31)), Instrument('w4950', AcVoltageCommand(1, freq=1e3))], True),
    # Step3(Dut('Valhalla 2703', '1 V 10 kHz', AcVoltageDutSettings(range=1, value=1, freq=10e3)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=10e3)), Instrument('w4920', AcVoltageCommand(1, freq=10e31)), Instrument('w4950', AcVoltageCommand(1, freq=10e3))], True),
    # Step3(Dut('Valhalla 2703', '1 V 20 kHz', AcVoltageDutSettings(range=1, value=1, freq=20e3)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=20e3)), Instrument('w4920', AcVoltageCommand(1, freq=20e31)), Instrument('w4950', AcVoltageCommand(1, freq=20e3))], True),
    # Step3(Dut('Valhalla 2703', '1 V 50 kHz', AcVoltageDutSettings(range=1, value=1, freq=50e3)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=50e3)), Instrument('w4920', AcVoltageCommand(1, freq=50e31)), Instrument('w4950', AcVoltageCommand(1, freq=50e3))], True),
    # Step3(Dut('Valhalla 2703', '1 V 100 kHz', AcVoltageDutSettings(range=1, value=1, freq=100e3)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=100e3)), Instrument('w4920', AcVoltageCommand(1, freq=100e31)), Instrument('w4950', AcVoltageCommand(1, freq=100e3))], True),
    # Step3(Dut('Valhalla 2703', '1 V 300 Hz', AcVoltageDutSettings(range=1, value=1, freq=300)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=300)), Instrument('w4920', AcVoltageCommand(1, freq=3001)), Instrument('w4950', AcVoltageCommand(1, freq=300))], True),
    # Step3(Dut('Valhalla 2703', '1 V 55 Hz', AcVoltageDutSettings(range=1, value=1, freq=55)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=55)), Instrument('w4920', AcVoltageCommand(1, freq=551)), Instrument('w4950', AcVoltageCommand(1, freq=55))], True),
    # Step3(Dut('Valhalla 2703', '1 V 20 Hz', AcVoltageDutSettings(range=1, value=1, freq=20)), [Instrument('ag3458a_1', AcVoltageCommand(1, freq=20)), Instrument('w4920', AcVoltageCommand(1, freq=201)), Instrument('w4950', AcVoltageCommand(1, freq=20))], True),
    # Step3(Dut('Valhalla 2703', '100 mV 1 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=1e3)), Instrument('w4920', AcVoltageCommand(100e-3, freq=1e31)), Instrument('w4950', AcVoltageCommand(100e-3, freq=1e3))], True),
    # Step3(Dut('Valhalla 2703', '10 mV 900 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=1e3)), Instrument('w4920', AcVoltageCommand(10e-3, freq=1e31)), Instrument('w4950', AcVoltageCommand(10e-3, freq=1e3))], True),
    # Step3(Dut('Valhalla 2703', '100 mV 10 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=10e3)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=10e3)), Instrument('w4920', AcVoltageCommand(100e-3, freq=10e31)), Instrument('w4950', AcVoltageCommand(100e-3, freq=10e3))], True),
    # Step3(Dut('Valhalla 2703', '10 mV 10 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=10e3)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=10e3)), Instrument('w4920', AcVoltageCommand(10e-3, freq=10e31)), Instrument('w4950', AcVoltageCommand(10e-3, freq=10e3))], True),
    # Step3(Dut('Valhalla 2703', '100 mV 20 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20e3)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=100e3)), Instrument('w4920', AcVoltageCommand(100e-3, freq=100e31)), Instrument('w4950', AcVoltageCommand(100e-3, freq=100e3))], True),
    # Step3(Dut('Valhalla 2703', '10 mV 20 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=20e3)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=20e3)), Instrument('w4920', AcVoltageCommand(10e-3, freq=20e31)), Instrument('w4950', AcVoltageCommand(10e-3, freq=20e3))], True),
    # Step3(Dut('Valhalla 2703', '100 mV 50 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=50e3)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=50e3)), Instrument('w4920', AcVoltageCommand(100e-3, freq=50e31)), Instrument('w4950', AcVoltageCommand(100e-3, freq=50e3))], True),
    # Step3(Dut('Valhalla 2703', '10 mV 50 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=50e3)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=50e3)), Instrument('w4920', AcVoltageCommand(10e-3, freq=50e31)), Instrument('w4950', AcVoltageCommand(10e-3, freq=50e3))], True),
    # Step3(Dut('Valhalla 2703', '100 mV 100 kHz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=100e3)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=100e3)), Instrument('w4920', AcVoltageCommand(100e-3, freq=100e31)), Instrument('w4950', AcVoltageCommand(100e-3, freq=100e3))], True),
    # Step3(Dut('Valhalla 2703', '10 mV 100 kHz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=100e3)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=100e3)), Instrument('w4920', AcVoltageCommand(10e-3, freq=100e31)), Instrument('w4950', AcVoltageCommand(10e-3, freq=100e3))], True),
    # Step3(Dut('Valhalla 2703', '100 mV 300 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=300)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=300)), Instrument('w4920', AcVoltageCommand(100e-3, freq=3001)), Instrument('w4950', AcVoltageCommand(100e-3, freq=300))], True),
    # Step3(Dut('Valhalla 2703', '10 mV 300 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=300)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=300)), Instrument('w4920', AcVoltageCommand(10e-3, freq=3001)), Instrument('w4950', AcVoltageCommand(10e-3, freq=300))], True),
    # Step3(Dut('Valhalla 2703', '100 mV 55 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=55)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=55)), Instrument('w4920', AcVoltageCommand(100e-3, freq=551)), Instrument('w4950', AcVoltageCommand(100e-3, freq=55))], True),
    # Step3(Dut('Valhalla 2703', '10 mV 55 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=55)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=55)), Instrument('w4920', AcVoltageCommand(10e-3, freq=551)), Instrument('w4950', AcVoltageCommand(10e-3, freq=55))], True),
    Step3(Dut('Valhalla 2703', '100 mV 20 Hz', AcVoltageDutSettings(range=100e-3, value=100e-3, freq=20)), [Instrument('ag3458a_1', AcVoltageCommand(100e-3, freq=20)), Instrument('w4920', AcVoltageCommand(100e-3, freq=201)), Instrument('w4950', AcVoltageCommand(100e-3, freq=20))], True),
    Step3(Dut('Valhalla 2703', '10 mV 20 Hz', AcVoltageDutSettings(range=10e-3, value=10e-3, freq=20)), [Instrument('ag3458a_1', AcVoltageCommand(10e-3, freq=20)), Instrument('w4920', AcVoltageCommand(10e-3, freq=201)), Instrument('w4950', AcVoltageCommand(10e-3, freq=20))], True),
    Step3(Dut('Valhalla 2703', '10 V 1 kHz', AcVoltageDutSettings(range=10, value=10, freq=1e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=1e3)), Instrument('w4920', AcVoltageCommand(10, freq=1e31)), Instrument('w4950', AcVoltageCommand(10, freq=1e3))], True),
    
    # 4920 + 3458
    Step3(Dut('Valhalla 2703', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=10, freq=2.4e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=2.4e3)), Instrument('w4920', AcVoltageCommand(10, freq=2.4e31))], True),
    Step3(Dut('F510', '10 V 2.4 kHz', AcVoltageDutSettings(range=10, value=-10, freq=2.4e3)), [Instrument('ag3458a_1', AcVoltageCommand(10, freq=2.4e3)), Instrument('w4920', AcVoltageCommand(10, freq=2.4e31))], True),

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
    w4920 = ivi.datron_wavetek.wavetek4920("TCPIP::gpib4::gpib0,4::INSTR", reset=True)
    w4920._interface.timeout = 120
    w4950 = ivi.datron_wavetek.wavetek4950("TCPIP::gpib4::gpib0,20::INSTR", reset=True)
    w4950._interface.timeout = 120
    w4950.last_temp = datetime.datetime.utcnow()
    return {'w4920': w4920, 'ag3458a_1': ag3458a_1, 'w4950': w4950}


def read_row(inits, instruments: List[Instrument]):
    all_instruments = ['w4920', 'ag3458a_1', 'w4950']
    ag3458a_1 = inits['ag3458a_1']
    w4920 = inits['w4920']
    w4950 = inits['w4950']

    row = {}

    for instrument in instruments:
        if instrument.name == 'w4950':
            init_w4950(row, w4950)
        elif instrument.name.startswith('ag3458a_'):
            init_ag3458a(ag3458a_1, row)
        elif instrument.name == 'w4920':
            init_w4920(w4920, row)

    row['datetime'] = datetime.datetime.utcnow().isoformat()

    for instrument in instruments:
        if instrument.name == 'w4920':
            read_w4920(w4920, row)  # 8s
        elif instrument.name.startswith('ag3458a_'):
            read_ag3458a(ag3458a_1, row)  # 12s
        elif instrument.name == 'w4950':
            read_w4950(row, w4950)  # 30s
    if 'w4920' not in {i.name for i in instruments}:
        for field in ('w4920_function', 'w4920_range', 'w4920_freq',
                      'w4920_value'):
            row[field] = None
    if 'ag3458a_1' not in {i.name for i in instruments}:
        for field in ('ag3458a_1_value', 'temp_1', 'last_acal_1',
                      'last_acal_1_cal72', 'ag3458a_1_range'):
            row[field] = None
    if 'w4950' not in {i.name for i in instruments}:
        for field in ('w4950_function', 'w4950_range',
                      'w4950_percentage', 'w4950_freq', 'w4950_value',
                      'w4950_nsamples', 'w4950_std_abs', 'w4950_temp'):
            row[field] = None

    print()
    return row, row['temp_1'] is None


def init_ag3458a(ag3458a_1, row):
    if ((datetime.datetime.utcnow() - ag3458a_1.last_temp).total_seconds()
            > 30 * 60):
        temp_1 = ag3458a_1.utility.temp
        ag3458a_1.last_temp = datetime.datetime.utcnow()
        row['temp_1'] = temp_1
        #ag3458a_1.measurement.initiate()
    else:
        row['temp_1'] = None
        #ag3458a_1.measurement.initiate()


def read_ag3458a(ag3458a, row):
    row['last_acal_1'] = ag3458a.last_acal.isoformat()
    row['last_acal_1_cal72'] = ag3458a.last_acal_cal72
    row['ag3458a_1_range'] = ag3458a.range
    value = ag3458a.measurement.read(360)
    if row['temp_1'] is None:
        row['ag3458a_1_value'] = value
        print(f"ag3458a: {value}")
        check_valid_value(ag3458a, value)


def init_w4950(row, w4950):
    if ((datetime.datetime.utcnow() - w4950.last_temp).total_seconds()
            > 30 * 60):
        row['w4950_temp'] = w4950.measurement.temp.internal
    w4950.measurement.initiate()


def read_w4950(row, w4950):
    row['w4950_function'] = w4950.measurement_function
    row['w4950_range'] = w4950.range
    row['w4950_percentage'] = w4950.measurement.percentage
    row['w4950_value'] = w4950.measurement.fetch(60)
    row['w4950_nsamples'] = w4950.measurement.quality.nsamples
    row['w4950_std_abs'] = w4950.measurement.quality.absolute
    print(f"w4950: {row['w4950_value']}", end='')
    if w4950.measurement_function in ('ac_volts', 'ac_current'):
        row['w4950_freq'] = w4950.measurement.freq
        print(f", freq: {row['w4950_freq']}")
    else:
        row['w4950_freq'] = None
        print()
    check_valid_value(w4950, row['w4950_value'])


def init_w4920(w4920, row):
    w4920.measurement.initiate()

def read_w4920(w4920, row):
    row['w4920_function'] = w4920.measurement_function
    row['w4920_range'] = w4920.range
    time.sleep(4)
    row['w4920_value'] = w4920.measurement.fetch(0)
    print(f"w4920: {row['w4920_value']}", end='')
    if w4920.measurement_function in ('ac_volts', 'ac_millivolts'):
        row['w4920_freq'] = w4920.measurement.freq
        print(f", freq: {row['w4920_freq']} Hz")
    else:
        row['w4920_freq'] = None
        print()
    check_valid_value(w4920, row['w4920_value'])


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ac()


if __name__ == '__main__':
    main()
