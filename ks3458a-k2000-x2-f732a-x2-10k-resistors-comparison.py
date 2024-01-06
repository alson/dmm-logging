#!/usr/bin/python3

from typing import Dict, List
import ivi
from ivi import dmm
import datetime
import csv
import os

from common_step_execution import (Res4WDutSettings, DcVoltageDutSettings, FourWireResistanceCommand, DcVoltageCommand, run_procedure, Step4, Instrument, Dut)

OUTPUT_FILE = 'ks3458a-k2000-x2-f732a-x2-10k-resistors-comparison.csv'
FIELDNAMES = ('datetime', 'dut', 'dut_setting', 'ag3458a_2_ohm_or_dcv', 'temp_2', 'last_acal_2',
              'last_acal_2_cal72', '3458a_2_function', 'ag3458a_2_range', 'ag3458a_2_delay',
              'k2000_ohm', 'k2000_20_ohm')
WRITE_INTERVAL_SECONDS = 3600
SAMPLES_PER_STEP = 16
STEP_SOAK_TIME = 60
DEBUG = False


if DEBUG:
    WRITE_INTERVAL_SECONDS = 0
    STEP_SOAK_TIME = 6
    SAMPLES_PER_STEP = 4


procedure = [
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3, allow_acal=True))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('Measurements International 9331', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),

    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10, allow_acal=True))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3, allow_acal=True))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('RTU-11k-02', '11 kOhm', Res4WDutSettings(range=11e3, value=11e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),

    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10, allow_acal=True))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3, allow_acal=True))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('UPW50-104b', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    # Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(13e3)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),

    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10, allow_acal=True))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3, allow_acal=True))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('Guildline 9330 s/n 45809', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),

    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10, allow_acal=True))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '+20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=-20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3)), Dut('F732a3+F732a2', '-20 V', DcVoltageDutSettings(value=20, range=20))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', DcVoltageCommand(10))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3, allow_acal=True))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('Guildline 9330 s/n 42709', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
    Step4([Dut('SR104', '10 kOhm', Res4WDutSettings(range=10e3, value=10e3))], [Instrument('k2000', FourWireResistanceCommand(10e3)), Instrument('k2000_20', FourWireResistanceCommand(110)), Instrument('ag3458a_2', FourWireResistanceCommand(10e3))], True),
]


def main():
    inits = init_func()
    with open(OUTPUT_FILE, 'a', newline='') as csv_file:
        initial_size = os.fstat(csv_file.fileno()).st_size
        csvw = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        if initial_size == 0:
            csvw.writeheader()
        run_procedure(csvw, procedure, inits, read_row, SAMPLES_PER_STEP, STEP_SOAK_TIME)


def init_func():
    ag3458a_2 = ivi.agilent.agilent3458A("TCPIP::gpib1::gpib,20::INSTR",
                                         reset=True)
    ag3458a_2._interface.timeout = 120
    if not DEBUG:
        ag3458a_2.advanced.offset_compensation = 'on'
        ag3458a_2.advanced.aperture_time = 100
    ag3458a_2.measurement_function = 'four_wire_resistance'
    temp_2 = ag3458a_2.utility.temp
    ag3458a_2.last_temp = datetime.datetime.utcnow()
    if DEBUG:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_temp_value = temp_2
        ag3458a_2.last_acal_cal72 = 'test'
    else:
        ag3458a_2.last_acal = datetime.datetime.utcnow()
        ag3458a_2.last_acal_temp = temp_2
        ag3458a_2.last_temp_value = temp_2
        acal_3458a_2(ag3458a_2)
        # ag3458a_2.last_acal_cal72 = 'keep'
    k2000 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,16::INSTR",
            id_query=True)
    k2000_20 = ivi.keithley.keithley2000("TCPIP::gpib1::gpib,17::INSTR",
            id_query=True)
    k2000._interface.timeout = 120
    k2000._write(':DISPLAY:ENABLE OFF')
    k2000.measurement_function = 'four_wire_resistance'
    k2000.range = 10000
    k2000._write(':FRES:NPLC 10')
    k2000_20._interface.timeout = 120
    k2000_20._write(':DISPLAY:ENABLE OFF')
    k2000_20.measurement_function = 'four_wire_resistance'
    k2000_20.range = 110
    k2000_20._write(':FRES:NPLC 10')
    return {'ag3458a_2': ag3458a_2, 'k2000': k2000, 'k2000_20': k2000_20}

def read_row(inits: Dict[str, dmm.Base], instruments: List[Instrument], **kwargs):
    sample_no = kwargs['sample_no']
    ag3458a_2 = inits['ag3458a_2']
    k2000 = inits['k2000']
    k2000_20 = inits['k2000_20']
    row = {}
    row['datetime'] = datetime.datetime.utcnow().isoformat()
    ag3458a_2_instrument = ([instrument for instrument in instruments if instrument.name == 'ag3458a_2'] or [None])[0]

    if ((datetime.datetime.utcnow() - ag3458a_2.last_temp).total_seconds()
            > 30 * 60):
        temp_2 = ag3458a_2.utility.temp
        ag3458a_2.last_temp = datetime.datetime.utcnow()
        ag3458a_2.last_temp_value = temp_2
        row['temp_2'] = temp_2
        row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
        row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
        ag3458a_2.measurement.initiate()
        ag3458a_2.measurement.fetch(360)
        acal_if_necessary(ag3458a_2, sample_no, ag3458a_2_instrument)
    else:
        acal_if_necessary(ag3458a_2, sample_no, ag3458a_2_instrument)
        for instrument in instruments:
            if instrument.name == 'ag3458a_2':
                ag3458a_2.measurement.initiate()
        row['k2000_ohm'] = None
        row['k2000_20_ohm'] = None
        row['ag3458a_2_ohm_or_dcv'] = None
        for instrument in instruments:
            if instrument.name == 'k2000':
                row['k2000_ohm'] = k2000.measurement.fetch(1)
            elif instrument.name == 'k2000_20':
                row['k2000_20_ohm'] = k2000_20.measurement.fetch(1)
            elif instrument.name == 'ag3458a_2':
                row['ag3458a_2_ohm_or_dcv'] = ag3458a_2.measurement.fetch(360)
        row['temp_2'] = None
        row['last_acal_2'] = ag3458a_2.last_acal.isoformat()
        row['last_acal_2_cal72'] = ag3458a_2.last_acal_cal72
        row['ag3458a_2_range'] = ag3458a_2.range
        row['ag3458a_2_delay'] = ag3458a_2.trigger.delay
        print(f"ag3458a_2: {row['ag3458a_2_ohm_or_dcv']}, k2000: {row['k2000_ohm']}, k2000_20: {row['k2000_20_ohm']}")
    return row, row['temp_2'] is None

def acal_if_necessary(ag3458a_2, sample_no, ag3458a_2_instrument: Instrument):
    if sample_no != 1:
        return
    do_acal_3458a_2 = False
    print(f"ACAL if neccessary, last_acal_temp: {ag3458a_2.last_acal_temp}, last_temp_value: {ag3458a_2.last_temp_value}, ag3458a_2_instrument: {ag3458a_2_instrument}, allow_acal: {ag3458a_2_instrument.setting.allow_acal if ag3458a_2_instrument else None}")
    if ((ag3458a_2_instrument is None) or ag3458a_2_instrument.setting.allow_acal) and (((datetime.datetime.utcnow() - ag3458a_2.last_acal).total_seconds() > 24 * 3600) \
                or (abs(ag3458a_2.last_acal_temp - ag3458a_2.last_temp_value) >= 0.5)):
        print(f"Running ACAL, last_acal_temp: {ag3458a_2.last_acal_temp}, last_temp_value: {ag3458a_2.last_temp_value}, ag3458a_2_instrument: {ag3458a_2_instrument}, allow_acal: {ag3458a_2_instrument.setting.allow_acal if ag3458a_2_instrument else None}")
        do_acal_3458a_2 = True
    if do_acal_3458a_2:
        acal_3458a_2(ag3458a_2)

def acal_3458a_2(ag3458a_2):
    ag3458a_2.acal.start_dcv()
    ag3458a_2.acal.start_ohms()

if __name__ == '__main__':
    main()
