#!/usr/bin/python3

import ivi
import time
import datetime
import csv
import os
from statistics import mean

OUTPUT_FILE = 'k2000-x2-6031A-ad588-log-v+-v-.csv'
SAMPLE_INTERVAL = 180
FIELDNAMES = ('datetime', 'ad588-1', 'ad588-2',
        'ad588-3', 'ad588-4', 'ad588-5',
        'ad588-6', 'ad588-7',
        'ad588-8', 'ad588-9', 'ad588-10',
        'v+', 'v-')
WRITE_INTERVAL_SECONDS = 3600

def init_func():
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    k2000._write(':INITIATE:CONTINUOUS OFF')
    k2000.measurement_function = 'dc_volts'
    k2000.range = 10
    k2000._write(':VOLT:DC:NPLC 10')
    k2000._write(':VOLT:DC:AVERAGE:STATE OFF')
    k2000._write(':DISPLAY:ENABLE OFF')
    k2000_20 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,17::INSTR",
            id_query=True)
    k2000_20._write(':INITIATE:CONTINUOUS OFF')
    k2000_20.measurement_function = 'dc_volts'
    k2000_20.range = 15
    k2000_20._write(':VOLT:DC:NPLC 10')
    k2000_20._write(':VOLT:DC:AVERAGE:STATE OFF')
    k2000_20._write(':DISPLAY:ENABLE OFF')
    prema6031a = ivi.prema.prema6031A("TCPIP::gpib1::gpib,7::INSTR",
            reset=True)
    prema6031a.measurement_function = 'dc_volts'
    prema6031a.range = 15
    prema6031a.advanced.aperture_time = 4
    return { 'k2000': k2000, 'k2000_20': k2000_20, 'prema6031a': prema6031a }

def loop_func(csvw, k2000, k2000_20, prema6031a):
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    vp_meas = []
    vm_meas = []
    for chan in range(10):
        k2000.path.connect('common', 'channel{0}'.format(chan+1))
        k2000.path.wait_for_debounce(0)
        time.sleep(180)
        meas = k2000.measurement.read(1)
        row[FIELDNAMES[chan+1]] = meas
        vp_meas.append(k2000_20.measurement.read(1))
        vm_meas.append(prema6031a.measurement.read(1))
    k2000.path.disconnect('common', 'channel1')
    row['v+'] = mean(vp_meas)
    row['v-'] = mean(vm_meas)
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
