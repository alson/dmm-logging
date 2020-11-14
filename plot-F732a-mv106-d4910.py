#!/usr/bin/python3

import pandas as pd
import matplotlib.pyplot as plt

from common_plotting import read_data, plot, hours

filenames = [
    'k199-x2-3458A-x2-k2000-x2-D4910-F732A-MV106-log.csv',
]
axis1_columns = ['k199_2_d4910_avg_4',
                 'ag3458a_1_d4910_avg_3',
                 'ag3458a_2_f732a_d4910_avg',
                 'k2000_d4910_avg_1',
                 'k2000_20_d4910_avg_2']
axis2_columns = ['k199_1_f732a_mv106']

thp2, data_dict = read_data(filenames)
combined_data = pd.concat(data_dict.values(), sort=True)
plot(thp2, combined_data, axis1_columns, axis2_columns, column_transformation_plot=lambda c: (c-c.mean())*1e5,
     xminor_locator=hours)

plt.show()
