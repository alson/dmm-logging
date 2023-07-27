#!/usr/bin/env python3
import ivi
import numpy as np
from time import sleep
import csv
import datetime

OUTPUT_FILE = 'k2400-trace-headlight-st-part.csv'
FIELDNAMES = ['datetime', 'set_voltage', 'measure_current']
RANGE = 100

k2400 = ivi.keithley.keithley2400("TCPIP::gpib4::gpib0,24::INSTR",
                                id_query=True)

k2400_op = k2400.outputs[0]
k2400_op.mode = 'voltage'
k2400_op.current_limit = 100e-6
k2400_op.configure_range('voltage', RANGE)
k2400_op.voltage_level = 0
k2400_op.enabled = True

voltages = np.concatenate([np.arange(-120, -100, 1), np.arange(-100, -98, .01), np.arange(-98, 100, 5), np.arange(95, 120, 1)])
with open(OUTPUT_FILE, 'w', newline='') as csv_file:
    csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
    csvw.writeheader()
    for volt in voltages:
        k2400_op.voltage_level = volt
        sleep(0.1)
        csvw.writerow({
            'datetime': datetime.datetime.utcnow().isoformat(),
            'set_voltage': volt,
            'measure_current': k2400_op.measure('current'),
        })
    k2400_op.enabled = False
