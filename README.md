# dmm-logging

This is a loose collection of scripts to collect and plot data from several DMMs for different experiments, generally related to metrology and comparing the stability and temperature/humidity/pressure coefficients of sources.

## General scripts

`thp_log.py` and `start_thp_log.sh` log the temperature, humidity and pressure from a BME280 sensor connected via I2C.

`common_step_execution.py` contains functions for executing a series of steps with different duts / measurement instruments / settings, used for example for scripted sweeps and range transfers.

`manual-log.py` is similar to other scripts that log data, except that this receives its data using manual input instead of automation. It has some smarts like history to make data entry more efficient.

## Experiments

### Measurement tests

Testing various theories, mostly relating to the HPAK 3458A

Scripts:
* `ks3458a-4w-res-delay-test.py`: Test the effect of 4W resistance measurement on the 3458A with offset compensation on.
* `ks3458a1-4w-res-nplc-aper-test.py`: Compare NPLC 100 vs APER 1 with resistance measurements on the 3458A.
* `ks3458a-dcv-guard-test.py`: Test the effect of the guard open / to lo switch on the 3458A.

#### 3458A tempco

Measure the 3458A tempco on DCV and resistance relative to other standards.

Scripts:
* `ks3458a-dcv-tc-log-w-acal.py`: Measure tempco of 3458A built-in voltage reference against external voltage reference.
* `ks3458a-k2000-x2-sr104-log.py`: Measure tempco of 3458A R207 against SR104 (corrected for its temperature using its thermistor).
* `ks3458a-wo-acal-k2000-x2-sr104-log.py`: Meaure tempco of 3458A 10 kOhm range against  SR104 (corrected for its temperature using its thermistor).

### SR104 stability

Scripts:
* `ks3458a-sr104-log.py`: Log SR104 resistance on 3458A
* `ks3458a-k2000-sr104-log.py`: Log SR104 resistance on 3458A and built-in thermistor on Keithley 2000

### Datron 4910 stability

Quick-and-dirty test (spotting a pattern yet) of Datron 4910 against Fluke 732A and EDC MV106. Various DMMs are used as nullmeters to compare the 10V output of the several references. It measures the four individual 10V reference outputs of the 4910 against the average output, and the Fluke 732A and EDC MV106 against the 4910 average output.

Scripts:
* `k199-x2-3458A-x2-k2000-x2-D4910-F732A-MV106-log.py`: Log difference between 10V references

### Voltage reference comparisons

Comparing the stability of various voltage references against each other and against a 3458A.

Scripts:
* `ks3458a-dcv-log.py`: Interactively (prompt for DUT and value anytime it detects a change in value) log DCV on 3458A (absolute value of references).
* `k182-dcv-mv-log.py`: Interactively (prompt for DUT and value anytime it detects a change in value) log DC mV on Keithley 182 (relative difference between references back to back).
* `ks3458a1-dcv-mv-log.py`: Interactively (prompt for DUT and value anytime it detects a change in value) log DC mV on 3458A (relative difference between references back to back).
* `k2000-dcv-log.py`: Interactively (prompt for DUT and value anytime it detects a change in value) log DCV on Keithley 2000 (absolute value of reference).
* `k2000-ad588-log.py`: Log values of a set of AD588 references on Keithley 2000 using its built-in scanner.
* `k2000-lm399-log.py`: Log values of a set of LM399 references on Keithley 2000 using its built-in scanner.
* `k2000-x2-6031A-ad588-log-v+-v-.py`: Log AD588 using Keithley 2000 with scanner and both voltage rails using another Keithley 2000 and Prema 6031.
* `k2000-x2-lm399-log.py`: Log values of a set of LM399 references using two Keithley 2000s connected to the same scanner.
* `k2000-x2-lm399-v+-log.py`: Log values of a set of LM399 references using Keithley 2000 with scanner and another Keithley 2000 to monitor the input voltage.

### Resistance transfers

Comparing the stability of various resistance standards and calibrators against each other and against a 3458A.

Scripts:
* `ks3458a-2w-res-log.py`: Interactively (prompt for DUT and value anytime it detects a change in value) measure 2W resistance with HPAK 3458A. Usually used for higher resistance values starting around 1 MOhm / 10 MOhm, to compare them either to the 3458A or do 1:1 or 1:10 transfers.
* `ks3458a-4w-res-log.py`: Interactively (prompt for DUT and value anytime it detects a change in value) measure 4W resistance with HPAK 3458A. Usually used for lower resistance values up to 100 kOhm / 1 MOhm, to compare them either to the 3458A or do 1:1 or 1:10 transfers.
* `ks3458a-2w-res-unattended-log.py`: Unattendedly (one fixed DUT without any prompts) measure 2W resistance with HPAK 3458A.
* `ks3458a-f5450a-best-resistors-comparison.py`: Compare Fluke 5450A to other standard resistors using 3458A for 1:1 and 1:10 transfers.
* `ks3458a-k2000-sr104-log.py`: Log SR104 resistance on 3458A and built-in thermistor on Keithley 2000
* `ks3458a-k2000-transfer-sr104-log.py`: Log SR104 resistance on 3458A and built-in thermistor on Keithley 2000 before transferring to other resistors.
* `ks3458a-k2000-x2-sr104-log.py`: Log SR104 resistance on 3458A and built-in thermistor on Keithley 2000 and PT100 on another Keithley 2000
* `ks3458a-sr104-log.py`: Log SR104 resistance on 3458A

### Resistance temperature coefficient measurements

Measure the tempco of manganin resistance standards against SR104.

Scripts:
* `ks3458a-k2000-20-res-tempco-log.py`: Transfer from SR104, then measure DUT in same range, and then back to SR104.

### ACV stability measurements

Checking stability of Fluke 510A or other sources against HPAK 3458A or Wavetek 4920.

Scripts:
* `ks3458a-acv-log.py`: Log ACV on 3458A
* `w4920-acv-log.py`: Log ACV on Wavetek 4920

### ACV transfers

Comparing 4x F510 against F7001 using ks3458a + W4950 + W4920 using round-robin measurements.

Scripts:
* `ks3458a1-f510-reading.py`: Rotate through standards on KS3458a
* `w4920-f510-reading.py`: Rotate through standards on W4920
* `w4950-f510-reading.py`: Rotate through standards on W4950 (requiring manual ACV mode switching because this feature is broken on my W4950)

### SMUs

Scripts:
* `k237-trace.py`: Trace a two terminal device like a diode with Keithley 237 SMU
* `k2400-trace.py`: Trace a two terminal device like a diode with Keithley 2400 SMU

### Meter and calibrator comparisons

Comparing the stability of various meters against each other.

Scripts:
* `ks3458a1-w4920-acv-log.py`: Interactively (prompt for DUT anytime it detects a change in value) compare HPAK 3458A vs Wavetek 4920 on ACV source (e.g. F510A)

* `ks3458a1-v2703-acv-sweep.py`: ACV sweep HPAK 3458A vs Valhalla 2703
* `ks3458a1-w4920-w4950-v2703-acv-sweep.py`: Sweep HPAK 3458A vs Wavetek 4920 vs Wavetek 4950 on Valhalla 2703 and F510A ACV source
* `ks3458a-d4700-dcv-dci-sweep.py`: DCV and DCI sweep HPAK 3458A vs Datron 4700 in one script (connect 3458A lo and hi to D4700 lo and hi, 3458A lo also to D4700 I- and 3458A amps to D4700 I+)
* `ks3458a-d4700-dci-sweep.py`: DCI sweep HPAK 3458A vs Datron 4700
* `ks3458a-d4700-dcv-sweep.py`: DCV sweep HPAK 3458A vs Datron 4700
* `ks3458a-d4700-resistance-sweep.py`: Resistance sweep HPAK 3458A vs Datron 4700
* `ks3458a-f5450a-sweep.py`: Resistance sweep HPAK 3458A vs Fluke 5450A (only decade values).
* `ks3458a-f5450a-sweep-with-1.9.py`: Resistance sweep HPAK 3458A vs Fluke 5450A (all values).
* `ks3458a-v2703-v2500-aci-sweep.py`: ACI sweep HPAK 3458A vs Valhalla 2703 with Valhalla 2500
* `ks3458a-x2-d4910-v2500-dci-sweep.py`: DCI sweep HPAK 3458A vs Valhalla 2500 using Datron 4910 as DCV input to Valhalla 2500.
* `w4920-v2703-acv-sweep.py`: ACV sweep Wavetek 4920 vs Valhalla 2703
* `w4950-d4700-dci-sweep.py`: DCI sweep Wavetek 4950 vs Datron 4700
* `w4950-d4700-dcv-sweep.py`: DCV sweep Wavetek 4950 vs Datron 4700
* `w4950-d4700-dcv-dci-r-sweep.py`: DCV, DCI and resistance sweep Wavetek 4950 vs Datron 4700 in one script (connect all banana plugs by color)
* `w4950-d4700-resistance-sweep.py`: Resistance sweep Wavetek 4950 vs Datron 4700
* `w4950-f5450a-sweep.py`: Resistance sweep Wavetek 4950 vs Fluke 5450A (only decade values).
* `w4950-ks3458a-d4910-v2500-dci-sweep.py`: DCI sweep Wavetek 4950 vs Valhalla 2500 using HPAK 3458A as DCV input to Valhalla 2500.
* `w4950-log.py`: Log data on any range and function of Wavetek 4950
* `w4950-v2703-acv-sweep.py`: ACV sweep Wavetek 4950 vs Valhalla 2703
* `w4950-v2703-v2500-aci-sweep.py`: ACI sweep Wavetek 4950 vs Valhalla 2703 with Valhalla 2500

### Environmental monitoring

Monitoring environmental conditions (temperature, humidity and/or pressure).

Scripts:
* `k2000-4w-res-log.py`: Log 4W resistance on Keithley 2000, generally used to measure PT100
* `k2000-sr104-thermistor-log.py`: Log 10k thermistor in ESI SR104 using Keithley 2000