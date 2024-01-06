#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
import readline

OUTPUT_FILE = 'k7001-voffset-test.csv'
FIELDNAMES = ('datetime', 'card', 'channel1', 'channel2', 'k182_dcv')
TEST_CARD_NUMBER = '2'

def init_func():
    k182 = ivi.keithley.Keithley182("TCPIP::gpib4::gpib0,13::INSTR", reset=True)
    k182._interface.timeout = 120
    # k182.auto_range = 'on'
    k182.range = 1e-3
    k7001 = ivi.keithley.keithley7001("TCPIP::gpib4::gpib0,7::INSTR")
    k7001.config.single_channel = 'on'
    k7001.path.disconnect_all()
    return {'k182': k182, 'k7001': k7001}


def read_row(k182, k7001):
    row = {}
    k182.measurement.initiate()
    row['k182_dcv'] = k182.measurement.fetch(0)
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    return row


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
                    for channel in k7001._channel_name:
                        if channel == 'common':
                            continue
                        if not channel.startswith(f'{TEST_CARD_NUMBER}!'):
                            continue
                        k7001.path.connect('common', channel)
                        k7001.path.wait_for_debounce(0)
                        time.sleep(0.5)
                        for count in range(500):
                            row = read_row(**inits)
                            if count % 50 == 0:
                                print(f'{count:4d}: ', end='')
                                print(f'k182_dcv: {row["k182_dcv"]}')
                            row['card'] = k7001.cards[TEST_CARD_NUMBER].model
                            row['channel1'] = 'common'
                            row['channel2'] = channel
                            csvw.writerow(row)
    finally:
        k7001.path.disconnect_all()