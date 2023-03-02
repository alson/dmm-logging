import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
from sklearn.linear_model import LinearRegression

hours = mdates.HourLocator()
hours6 = mdates.HourLocator(interval=6)
days = mdates.DayLocator()
days7 = mdates.DayLocator(interval=7)
months = mdates.MonthLocator()
years = mdates.YearLocator()
daysFmt = mdates.DateFormatter('%Y-%m')
monthsFmt = mdates.DateFormatter('%Y-%m')
yearsFmt = mdates.DateFormatter('%Y')
register_matplotlib_converters()

def add_thp(thp, data):
    return pd.merge_asof(data.set_index('datetime').sort_values('datetime'), thp, left_index=True, right_index=True,
                         direction='nearest')


def read_data(filenames):
    thp = pd.read_csv('thp_log.csv', parse_dates=['datetime'])
    thp_pa = thp.loc[thp['pressure'] > 10000, 'pressure']
    thp.loc[thp['pressure'] > 10000, 'pressure'] = thp_pa / 100
    thp_sorted = thp.set_index('datetime').sort_values('datetime')
    data_dict = {filename: add_thp(thp_sorted, pd.read_csv(filename, parse_dates=['datetime'], low_memory=False))
                 for filename in filenames}
    return thp_sorted, data_dict


def filter_column_on_percentile(data, column=None):
    if column:
        series = data[column]
    else:
        series = data
    p_low = np.percentile(series, 5)
    p_high = np.percentile(series, 95)
    return data[(series > p_low) & (series < p_high)]


def ppm_for_column(series):
    mean = series.mean()
    return (series - mean) / mean * 1e6


def plot_data(data, ax, axis1_columns, axis2_columns, column_transformation_absolute, column_transformation_plot,
              data_label_absolute, data_label_plot, xmajor_locator,
              xminor_locator, xmajor_formatter, plotting_char='.', plotting_marker_size=1):
    lns = []
    colors = plt.rcParams["axes.prop_cycle"]()
    par1 = ax.twinx()
    for my_ax, columns in ((ax, axis1_columns), (par1, axis2_columns)):
        ymin = None
        ymax = None
        for column_name in columns:
            transformed_absolute = column_transformation_absolute(data[column_name].dropna())
            transformed_plot = column_transformation_plot(transformed_absolute)
            percentile_data = filter_column_on_percentile(transformed_plot)
            ymin = min(ymin, percentile_data.min()) if ymin is not None else percentile_data.min()
            ymax = max(ymax, percentile_data.max()) if ymax is not None else percentile_data.max()
            print(
                f"{column_name}: min/max : {min(transformed_absolute):e}/{max(transformed_absolute):e} {data_label_absolute},"
                f" mean (std): {transformed_absolute.mean():e} {data_label_absolute}"
                f" ({transformed_absolute.std():e} {data_label_absolute})")
            c = next(colors)["color"]
            lns.append(ax.scatter(transformed_plot.index, transformed_plot, marker=plotting_char, label=column_name,
                                  color=c, s=plotting_marker_size))
        my_ax.set_ylim([ymin, ymax])
    # ax.scatter for some reason does not adjust the xscaling
    ax.set_xlim([min(transformed_plot.index), max(transformed_plot.index)])
    ax.set_xlabel("Time")
    ax.set_ylabel(data_label_plot)
    par1.set_ylabel(data_label_plot)
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.xaxis.set_major_formatter(xmajor_formatter)
    ax.legend(handles=lns, scatterpoints=10, loc='best')


def plot_thp(thp_data, ax):
    par1 = ax.twinx()
    par2 = ax.twinx()

    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    par1.set_ylabel("Humidity (%)")
    par2.set_ylabel("Pressure (Pa)")

    color1 = plt.cm.viridis(0)
    color2 = plt.cm.viridis(0.5)
    color3 = plt.cm.viridis(0.8)

    p1 = ax.scatter(thp_data.index, thp_data['temperature'], color=color1, label="Temperature", s=1)
    p2 = par1.scatter(thp_data.index, thp_data['humidity'], color=color2, label="Humidity", s=1)
    p3 = par2.scatter(thp_data.index, thp_data['pressure'], color=color3, label="Pressure", s=1)

    lns = [p1, p2, p3]
    ax.legend(handles=lns, scatterpoints=10, loc='best')

    par2.spines['right'].set_position(('outward', 60))
    ax.yaxis.label.set_color(p1.get_facecolor()[0])
    par1.yaxis.label.set_color(p2.get_facecolor()[0])
    par2.yaxis.label.set_color(p3.get_facecolor()[0])


def plot_tempco(data, ax, axis1_columns, axis2_columns, column_transformation_absolute, column_transformation_plot,
                data_label_plot, plotting_marker_size=1):
    lns = []
    colors = plt.rcParams["axes.prop_cycle"]()
    par1 = ax.twinx()
    for my_ax, columns in ((ax, axis1_columns), (par1, axis2_columns)):
        ymin = None
        ymax = None
        for column_name in columns:
            column_data = data.dropna(subset=[column_name])
            transformed_absolute = column_transformation_absolute(column_data[column_name])
            transformed_plot = column_transformation_plot(transformed_absolute)
            percentile_data = filter_column_on_percentile(transformed_plot)
            # Creating a Linear Regression model on our data
            lin = LinearRegression()
            lin.fit(column_data[['temperature']], transformed_plot.to_numpy().reshape(-1, 1))

            ymin = min(ymin, percentile_data.min()) if ymin is not None else percentile_data.min()
            ymax = max(ymax, percentile_data.max()) if ymax is not None else percentile_data.max()
            c = next(colors)["color"]
            lns.append(my_ax.scatter(column_data['temperature'], transformed_plot, marker='.', label=column_name,
                               color=c, s=plotting_marker_size))
            ax.plot(column_data['temperature'], lin.predict(column_data[['temperature']]), c=c)
        my_ax.set_ylim([ymin, ymax])
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel(data_label_plot)
    par1.set_ylabel(data_label_plot)
    ax.legend(handles=lns, scatterpoints=10, loc='best')


def plot(thp, data, axis1_columns, axis2_columns, column_transformation_absolute=lambda c: c,
         column_transformation_plot=ppm_for_column, data_label_absolute='V', data_label_plot='ppm',
         xmajor_locator=days, xminor_locator=hours6, xmajor_formatter=daysFmt, plotting_marker_size=1):
    fig = plt.figure()
    ax_volt = plt.subplot2grid((2, 2), (0, 0))
    ax_thp = plt.subplot2grid((2, 2), (1, 0), sharex=ax_volt)
    ax_tc = plt.subplot2grid((2, 2), (0, 1), rowspan=2)
    fig.subplots_adjust(hspace=0, wspace=0.4, left=0.05, right=0.95, top=0.95, bottom=0.05)
    fig.subplots_adjust(wspace=0.35)
    plot_data(data, ax_volt, axis1_columns, axis2_columns, column_transformation_absolute, column_transformation_plot,
              data_label_absolute, data_label_plot, xmajor_locator,
              xminor_locator, xmajor_formatter, plotting_marker_size=plotting_marker_size)
    thp_during_data = thp[(thp.index >= data.index.min()) & (thp.index <= data.index.max())]
    plot_thp(thp_during_data, ax_thp)
    plot_tempco(data, ax_tc, axis1_columns, axis2_columns, column_transformation_absolute, column_transformation_plot,
                data_label_plot, plotting_marker_size)
