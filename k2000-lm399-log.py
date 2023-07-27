#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os

OUTPUT_FILE = 'k2000-lm399-log.csv'
SAMPLE_INTERVAL = 180
FIELDNAMES = ('datetime', 'lm399-1', 'lm399-2', 'lm399-4', 'lm399-6', 'lm399-7',
              'lm399-8', 'lm399-9', 'lm399-10', 'lm399-11', 'lm399-12')
WRITE_INTERVAL_SECONDS = 3600

def init_func():
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'dc_volts'
    k2000.range = 7
    k2000._write(':VOLT:DC:NPLC 10')
    return { 'k2000': k2000 }

def loop_func(csvw, k2000):
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    for chan in range(10):
        k2000.path.connect('common', 'channel{0}'.format(chan+1))
        k2000.path.wait_for_debounce(0)
        time.sleep(180)
        meas = k2000.measurement.fetch(1)
        print(f'ch{chan}: {meas}')
        row[FIELDNAMES[chan+1]] = meas
    k2000.path.disconnect('common', 'channel1')
    csvw.writerow(row)

if __name__ == '__main__':
    inits = init_func()

    last_csvw_write = datetime.datetime(2018,1,1)
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        while True:
            loop_func(csvw, **inits)
            time.sleep(SAMPLE_INTERVAL)
            if (datetime.datetime.utcnow() - last_csvw_write) \
                    > datetime.timedelta(seconds=WRITE_INTERVAL_SECONDS):
                csv_file.flush()
                last_csvw_write = datetime.datetime.utcnow()
