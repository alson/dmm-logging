#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

from common_plotting import read_data, plot, years, months, yearsFmt

filenames = [
    'ks3458a-sr104-log.csv',
    'ks3458a-k2000-sr104-log.csv',
    'ks3458a-k2000-transfer-sr104-log.csv',
]
axis1_columns = ['ag3458a_2_ohm']
axis2_columns = ['k2000_temp_ohm']

thp, data_dict = read_data(filenames)
combined_data = pd.concat(data_dict.values(), sort=True)
plot(thp, combined_data, axis1_columns, axis2_columns, xmajor_locator=years, xminor_locator=months,
     xmajor_formatter=yearsFmt)
plt.show()
