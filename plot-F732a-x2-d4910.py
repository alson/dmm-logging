#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

from common_plotting import read_data, plot, months, days7, monthsFmt

filenames = [
    'k199-x2-3458A-x2-k2000-x2-D4910-F732A-x2-log.csv',
]
axis1_columns = ['k2000_20_d4910_avg_1',
                 'k199_1_d4910_avg_2',
                 'k199_2_d4910_avg_3',
                 'k2000_d4910_avg_4']
axis2_columns = ['ag3458a_2_f732a2_d4910_avg', 'ag3458a_1_f732a1_d4910_avg']

thp2, data_dict = read_data(filenames)
combined_data = pd.concat(data_dict.values(), sort=True)
plot(thp2, combined_data, axis1_columns, axis2_columns, column_transformation_plot=lambda c: (c-c.mean())*1e5,
     xmajor_locator=months, xminor_locator=days7, xmajor_formatter=monthsFmt)

plt.show()
