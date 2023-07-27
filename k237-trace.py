#!/usr/bin/env python3
import ivi
import numpy as np
from time import sleep
import csv
import datetime

OUTPUT_FILE = 'k237-trace-SNR-A150k-mov.csv'
FIELDNAMES = ['datetime', 'set_voltage', 'measure_current']

k237 = ivi.keithley.keithley237("TCPIP::gpib1::gpib,15::INSTR",
                                id_query=True)

k237_op = k237.outputs[0]
k237_op.current_limit = 0.01
k237_op.voltage_level = 0
k237_op.enabled = True

voltages = np.arange(-250, 260, 10)
with open(OUTPUT_FILE, 'w', newline='') as csv_file:
    csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
    csvw.writeheader()
    for volt in voltages:
        k237_op.voltage_level = volt
        sleep(10)
        csvw.writerow({
            'datetime': datetime.datetime.utcnow().isoformat(),
            'set_voltage': volt,
            'measure_current': k237_op.measure('current'),
        })
    k237_op.enabled = False
