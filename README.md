# dmm-logging

This is a loose collection of scripts to collect and plot data from several DMMs for different experiments, generally related to metrology and comparing the stability and temperature/humidity/pressure coefficients of sources.

## General scripts

`thp_log.py` and `start_thp_log.sh` log the temperature, humidity and pressure from a BME280 sensor connected via I2C.

`common_plotting.py` module with commonly used functions for importing, processing and plotting data.

## Experiments

### Measurement tests

Testing various theories, mostly relating to the HPAK 3458A

Scripts:
* `ks3458a-4w-res-delay-test.py`: Test the effect of 4W resistance measurement on the 3458A with offset compensation on.
* `ks3458a1-4w-res-nplc-aper-test.py`: Compare NPLC 100 vs APER 1 with resistance measurements on the 3458A.
* `ks3458a-dcv-guard-test.py`: Test the effect of the guard open / to lo switch on the 3458A.

### SR104 stability

Scripts:
* `ks3458a-sr104-log.py`: Log SR104 resistance on 3458A
* `ks3458a-k2000-sr104-log.py`: Log SR104 resistance on 3458A and built-in thermistor on Keithley 2000

## Datron 4910 stability

Quick-and-dirty test (spotting a pattern yet) of Datron 4910 against Fluke 732A and EDC MV106. Various DMMs are used as nullmeters to compare the 10V output of the several references. It measures the four individual 10V reference outputs of the 4910 against the average output, and the Fluke 732A and EDC MV106 against the 4910 average output.

Scripts:
* `k199-x2-3458A-x2-k2000-x2-D4910-F732A-MV106-log.py`: Log difference between 10V references

## Voltage reference comparisons

Comparing the stability of various voltage references against each other and against a 3458A.

Scripts:
* `ks3458a-dcv-log.py`: Log DCV on 3458A (absolute value of references).
* `k182-dcv-mv-log.py`: Log DCV on Keithley 182 (relative difference between references back to back).

## Resistance transfers

Comparing the stability of various resistance standards and calibrators against each other and against a 3458A.

Scripts:
* `ks3458a-2w-res-log.py`
* `ks3458a-4w-res-log.py`