import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

hours = mdates.HourLocator()
hours6 = mdates.HourLocator(interval=6)
days = mdates.DayLocator()
days7 = mdates.DayLocator(interval=7)
months = mdates.MonthLocator()
years = mdates.YearLocator()
daysFmt = mdates.DateFormatter('%Y-%m')
monthsFmt = mdates.DateFormatter('%Y-%m')
yearsFmt = mdates.DateFormatter('%Y')


def add_thp(thp, data):
    return pd.merge_asof(data.set_index('datetime'), thp, left_index=True, right_index=True, direction='nearest')


def read_data(filenames):
    thp2 = pd.read_csv('thp_log2.csv', parse_dates=['datetime'])
    thp2_pa = thp2.loc[thp2['pressure'] > 10000, 'pressure']
    thp2.loc[thp2['pressure'] > 10000, 'pressure'] = thp2_pa / 100
    thp2_sorted = thp2.set_index('datetime').sort_values('datetime')
    data_dict = {filename: add_thp(thp2_sorted, pd.read_csv(filename, parse_dates=['datetime'])) for filename in
                 filenames}
    return thp2_sorted, data_dict


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
              xminor_locator, xmajor_formatter):
    lns = []
    colors = plt.rcParams["axes.prop_cycle"]()
    for column_name in axis1_columns:
        column = filter_column_on_percentile(data[column_name].dropna())
        transformed_absolute = column_transformation_absolute(column)
        transformed_plot = column_transformation_plot(transformed_absolute)
        print(
            f"{column_name}: min/max : {min(transformed_absolute):e}/{max(transformed_absolute):e} {data_label_absolute},"
            f" mean (std): {transformed_absolute.mean():e} {data_label_absolute}"
            f" ({transformed_absolute.std():e} {data_label_absolute})")
        c = next(colors)["color"]
        lns.append(ax.plot(transformed_plot.index, transformed_plot, ',', label=column_name, color=c)[0])
    par1 = ax.twinx()
    for column_name in axis2_columns:
        column = filter_column_on_percentile(data[column_name].dropna())
        transformed_absolute = column_transformation_absolute(column)
        transformed_plot = column_transformation_plot(transformed_absolute)
        print(
            f"{column_name}: min/max : {min(transformed_absolute):e}/{max(transformed_absolute):e} {data_label_absolute},"
            f" mean (std): {transformed_absolute.mean():e} {data_label_absolute}"
            f" ({transformed_absolute.std():e} {data_label_absolute})")
        c = next(colors)["color"]
        lns.append(par1.plot(transformed_plot.index, transformed_plot, ',', label=column_name, color=c)[0])
    ax.set_xlabel("Time")
    ax.set_ylabel(data_label_plot)
    par1.set_ylabel(data_label_plot)
    ax.xaxis.set_minor_locator(xminor_locator)
    ax.xaxis.set_major_locator(xmajor_locator)
    ax.xaxis.set_major_formatter(xmajor_formatter)
    ax.legend(handles=lns, numpoints=10, loc='best')


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

    p1, = ax.plot(thp_data.index, thp_data['temperature'], ',', color=color1, label="Temperature")
    p2, = par1.plot(thp_data.index, thp_data['humidity'], ',', color=color2, label="Humidity")
    p3, = par2.plot(thp_data.index, thp_data['pressure'], ',', color=color3, label="Pressure")

    lns = [p1, p2, p3]
    ax.legend(handles=lns, numpoints=10, loc='best')

    par2.spines['right'].set_position(('outward', 60))

    ax.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    par2.yaxis.label.set_color(p3.get_color())


def plot_tempco(data, ax, axis1_columns, axis2_columns, column_transformation_absolute, column_transformation_plot,
                data_label_plot):
    lns = []
    colors = plt.rcParams["axes.prop_cycle"]()
    for column_name in axis1_columns:
        column_data = filter_column_on_percentile(data.dropna(subset=[column_name]), column_name)
        transformed_absolute = column_transformation_absolute(column_data[column_name])
        transformed_plot = column_transformation_plot(transformed_absolute)
        c = next(colors)["color"]
        lns.append(ax.plot(column_data['temperature'], transformed_plot, ',', label=column_name, color=c)[0])
    par1 = ax.twinx()
    for column_name in axis2_columns:
        column_data = filter_column_on_percentile(data.dropna(subset=[column_name]), column_name)
        transformed_absolute = column_transformation_absolute(column_data[column_name])
        transformed_plot = column_transformation_plot(transformed_absolute)
        c = next(colors)["color"]
        lns.append(par1.plot(column_data['temperature'], transformed_plot, ',', label=column_name, color=c)[0])

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel(data_label_plot)
    par1.set_ylabel(data_label_plot)
    ax.legend(handles=lns, numpoints=10, loc='best')


def plot(thp, data, axis1_columns, axis2_columns, column_transformation_absolute=lambda c: c,
         column_transformation_plot=ppm_for_column, data_label_absolute='V', data_label_plot='ppm',
         xmajor_locator=days, xminor_locator=hours6, xmajor_formatter=daysFmt):
    fig = plt.figure()
    ax_volt = plt.subplot2grid((2, 2), (0, 0))
    ax_thp = plt.subplot2grid((2, 2), (1, 0), sharex=ax_volt)
    ax_tc = plt.subplot2grid((2, 2), (0, 1), rowspan=2)
    fig.subplots_adjust(hspace=0, wspace=0.4, left=0.05, right=0.95, top=0.95, bottom=0.05)
    fig.subplots_adjust(wspace=0.35)
    plot_data(data, ax_volt, axis1_columns, axis2_columns, column_transformation_absolute, column_transformation_plot,
              data_label_absolute, data_label_plot, xmajor_locator,
              xminor_locator, xmajor_formatter)
    thp_during_data = thp[(thp.index >= data.index.min()) & (thp.index <= data.index.max())]
    plot_thp(thp_during_data, ax_thp)
    plot_tempco(data, ax_tc, axis1_columns, axis2_columns, column_transformation_absolute, column_transformation_plot,
                data_label_plot)
