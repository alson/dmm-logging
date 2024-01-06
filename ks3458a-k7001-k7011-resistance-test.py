#!/usr/bin/python3

import time
import ivi
import datetime
import csv
import os

from common_step_execution import beep

OUTPUT_FILE = 'ks3458a-k7001-k7011-resistance-test.csv'
FIELDNAMES = ('datetime', 'terminal', 'card', 'bank', 'channel1', 'channel2', 'ag3458a_2_ohm', 'temp_2', 'last_acal_2', 'last_acal_2_cal72')
TEST_CARD_NUMBER = '1'
DEBUG = False


def acal_3458a(ag3458a):
    ag3458a.acal.start_dcv()
    ag3458a.acal.start_ohms()


def init_func():
    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
                                         reset=True)
    ag3458a_2._interface.timeout = 120
    if not DEBUG:
        ag3458a_2.advanced.offset_compensation = 'on'
        ag3458a_2.advanced.aperture_time = 100
    ag3458a_2.measurement_function = 'four_wire_resistance'
    ag3458a_2.range = 10
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
    k7001 = ivi.keithley.keithley7001("TCPIP::gpib4::gpib0,10::INSTR")
    k7001.config.single_channel = 'on'
    k7001.path.disconnect_all()
    return {'k7001': k7001, 'ag3458a_2': ag3458a_2}


def read_row(k7001, ag3458a_2):
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
        print(f"{row['ag3458a_2_ohm']}")
    return row, row['temp_2'] is None


if __name__ == '__main__':
    inits = init_func()
    k7001 = inits['k7001']
    last_csvw_write = datetime.datetime(2018, 1, 1)
    try:
        with open(OUTPUT_FILE, 'a', newline='') as csv_file:
            initial_size = os.fstat(csv_file.fileno()).st_size
            csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
            if initial_size == 0:
                csvw.writeheader()
            while True:
                bank_names = ('A', 'B', 'C', 'D')
                bank_offset = (0, 10, 20, 30)
                for bank in range(4):
                    for terminal in ('high', 'low'):
                        if bank < 3:
                            continue
                        print(f"Please connect the DMM LO sense and force inputs to the {terminal} terminal of bank {bank_names[bank]} of the card under test.")
                        beep()
                        input("Press Enter to continue...")
                        for repeat in range(10):
                            for channel_number in range(1, 11):
                                channel = f"{TEST_CARD_NUMBER}!{channel_number + bank_offset[bank]}"
                                print(f"channel: {channel}")
                                k7001.path.connect('common', channel)
                                k7001.path.wait_for_debounce(0)
                                time.sleep(0.5)
                                row_is_temp = False
                                while not row_is_temp:
                                    row, row_is_temp = read_row(**inits)
                                row['card'] = k7001.cards[TEST_CARD_NUMBER].model
                                row['card'] = 'C7011-0630504'
                                row['terminal'] = terminal
                                row['channel1'] = 'common'
                                row['channel2'] = channel
                                row['bank'] = bank_names[bank]
                                csvw.writerow(row)
    finally:
        k7001.path.disconnect_all()

