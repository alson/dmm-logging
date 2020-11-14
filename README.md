# dmm-logging

This is a loose collection of scripts to collect and plot data from several DMMs for different experiments, generally related to metrology and comparing the stability and temperature/humidity/pressure coefficients of sources.

## General scripts

`thp_log.py` and `start_thp_log.sh` log the temperature, humidity and pressure from a BME280 sensor connected via I2C.

`common_plotting.py` module with commonly used functions for importing, processing and plotting data.

## Experiments

### SR104 stability

Quick-and-dirty test that of an SR104 against a HP 3458A (aka testing the stability of the 3458A 😂).

Scripts:
* `ks3458a-sr104-log.py`: Log SR104 resistance on 3458A
* `ks3458a-k2000-sr104-log.py`: Log SR104 resistance on 3458A and built-in thermistor on Keithley 2000
* `plot-sr104.py`: Plot results.

## Datron 4910 stability

Quick-and-dirty test (spotting a pattern yet) of Datron 4910 against Fluke 732A and EDC MV106. Various DMMs are used as nullmeters to compare the 10V output of the several references. It measures the four individual 10V reference outputs of the 4910 against the average output, and the Fluke 732A and EDC MV106 against the 4910 average output.

Scripts:
* `k199-x2-3458A-x2-k2000-x2-D4910-F732A-MV106-log.py`: Log difference between 10V references
* `plot-F732A-mv106-d4910.py`: Plot the results
