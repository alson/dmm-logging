#!/usr/bin/python3
import subprocess
from dataclasses import dataclass
from enum import Enum
from math import log10, ceil
from typing import Optional, List, Union

import ivi
import time
import os


@dataclass
class DutSettingCommand:
    function: Optional[str] = None
    range: Optional[float] = None
    value: Optional[float] = None

    def with_value(self, value: float) -> 'DutSettingCommand':
        return DutSettingCommand(self.function, value, value)


@dataclass
class Dut:
    name: str
    setting: str
    dut_setting_cmd: DutSettingCommand

    def with_value(self, value: float) -> 'Dut':
        return Dut(self.name, self.setting, self.dut_setting_cmd.with_value(value))


@dataclass
class Res2WDutSettings(DutSettingCommand):
    function: str = 'two_wire_resistance'


@dataclass
class Res4WDutSettings(DutSettingCommand):
    function: str = 'four_wire_resistance'


@dataclass
class DcVoltageDutSettings(DutSettingCommand):
    function: str = 'dc_volts'


@dataclass
class AcVoltageDutSettings(DutSettingCommand):
    freq: Optional[float] = None
    function: str = 'ac_volts'


@dataclass
class DcCurrentDutSettings(DutSettingCommand):
    function: str = 'dc_current'


@dataclass
class AcCurrentDutSettings(DutSettingCommand):
    freq: Optional[float] = None
    function: str = 'ac_current'


@dataclass
class InstrumentSettingCommand:
    range: Optional[float] = None
    measurement_function: Optional[str] = None

    def __str__(self):
        return f'{self.measurement_function} {self.range:e}'

    def with_range(self, range_: float) -> 'InstrumentSettingCommand':
        return InstrumentSettingCommand(range_, self.measurement_function)


@dataclass
class FourWireResistanceCommand(InstrumentSettingCommand):
    measurement_function: str = 'four_wire_resistance'


@dataclass
class DcVoltageCommand(InstrumentSettingCommand):
    measurement_function: str = 'dc_volts'


@dataclass
class DcCurrentCommand(InstrumentSettingCommand):
    measurement_function: str = 'dc_current'


@dataclass
class AcVoltageCommand(InstrumentSettingCommand):
    freq: Optional[float] = None
    measurement_function: str = 'ac_volts'


@dataclass
class AcCurrentCommand(InstrumentSettingCommand):
    freq: Optional[float] = None
    measurement_function: str = 'ac_current'


@dataclass
class Instrument:
    name: str
    setting: InstrumentSettingCommand

    def with_range(self, range: float) -> 'Instrument':
        return Instrument(self.name, self.setting.with_range(range))

    def range_max(self):
        if self.name.startswith('ag3458a_'):
            return 1.2
        elif self.name == 'w4950':
            return 1.1
        elif self.name == 'w4920':
            raise NotImplementedError


@dataclass
class Step:
    dut: str
    dut_setting: str
    dut_setting_cmd: DutSettingCommand
    instrument: str
    instrument_setting: InstrumentSettingCommand
    manual_prompt: bool = False

    def __str__(self):
        return f'{self.dut} at {self.dut_setting} measured by {self.instrument} at {self.instrument_setting}'

    def to_step3(self):
        return Step3(Dut(self.dut, self.dut_setting, self.dut_setting_cmd), [Instrument(self.instrument, self.instrument_setting)], self.manual_prompt)


@dataclass
class Step2:
    dut: str
    dut_setting: str
    dut_setting_cmd: DutSettingCommand
    instruments: List[Instrument]
    manual_prompt: bool = False

    def __str__(self):
        return f'{self.dut} at {self.dut_setting} measured by {self.instruments[0].name} at {self.instruments[0].setting}'

    def to_step3(self):
        return Step3(Dut(self.dut, self.dut_setting, self.dut_setting_cmd), self.instruments, self.manual_prompt)


@dataclass
class Step3:
    dut: Dut
    instruments: List[Instrument]
    manual_prompt: bool = False

    def __str__(self):
        return f'{self.dut.name} at {self.dut.setting} measured by {self.instruments[0].name} at {self.instruments[0].setting}'


class TransferDirection(Enum):
    FORWARD = 'forward'
    REVERSE = 'reverse'


def run_procedure(csvw, procedure: List[Step3], inits, read_row, samples_per_step, step_soak_time):
    previous_step = None
    try:
        for step_number, step in enumerate(procedure):
            print(f'Step {step_number+1}/{len(procedure)}')
            execute_step(csvw, step, previous_step, inits, read_row, samples_per_step, step_soak_time)
            previous_step = step
    finally:
        beep()


def generate_resistance_transfer_steps(instrument: Instrument, reference: Dut, transfer: Dut, target_value: float, direction: TransferDirection) -> List[Step3]:
    transfers = []
    if direction == TransferDirection.FORWARD:
        transfers = [reference] + generate_resistance_range(instrument, transfer, reference.dut_setting_cmd.value, target_value)
    elif direction == TransferDirection.REVERSE:
        transfers = generate_resistance_range(instrument, transfer, target_value, reference.dut_setting_cmd.value) + [reference]
    return list(generate_resistance_steps(instrument, transfers))


def generate_resistance_range(instrument: Instrument, transfer: Dut, start_value: float, end_value: float) -> List[Dut]:
    start_decade = get_value_decade_for_instrument(instrument, start_value)
    end_decade = get_value_decade_for_instrument(instrument, end_value)
    if start_decade == end_decade:
        return []
    return [Dut(transfer.name, transfer.setting, Res4WDutSettings(value=value, range=value)) for value in decade_transfer_range(start_decade, end_decade)]


def decade_transfer_range(start_decade: int, end_decade: int) -> List[float]:
    if start_decade < end_decade:
        return decade_transfer_unidirectional(start_decade, end_decade)
    else:
        return list(reversed(decade_transfer_unidirectional(end_decade, start_decade)))


def decade_transfer_unidirectional(start_decade: int, end_decade: int) -> List[float]:
    decade_range = list(range(start_decade, end_decade + 1))
    return [10 ** decade for decade in decade_range]


def get_value_decade_for_instrument(instrument: Instrument, value: float) -> int:
    instrument_max_in_range = instrument.range_max()
    value = value / instrument_max_in_range
    return ceil(log10(value))


def generate_resistance_steps(instrument: Instrument, transfers: List[Dut]) -> List[Step3]:
    previous_transfer = None
    previous_decade_value = None
    for transfer in transfers:
        transfer_decade_value = get_value_decade_for_instrument(instrument, transfer.dut_setting_cmd.value)
        if previous_transfer:
            if previous_decade_value < transfer_decade_value:
                yield Step3(previous_transfer, [instrument.with_range(transfer.dut_setting_cmd.value)])
                yield Step3(transfer, [instrument.with_range(transfer.dut_setting_cmd.value)], previous_transfer.name != transfer.name)
            elif previous_decade_value > transfer_decade_value:
                yield Step3(transfer, [instrument.with_range(previous_transfer.dut_setting_cmd.value)], previous_transfer.name != transfer.name)
                yield Step3(transfer, [instrument.with_range(transfer.dut_setting_cmd.value)])
            else:
                yield Step3(transfer, [instrument.with_range(transfer.dut_setting_cmd.value)], previous_transfer.name != transfer.name)
        else:
            yield Step3(transfer, [instrument.with_range(transfer.dut_setting_cmd.value)], True)
        previous_transfer = transfer
        previous_decade_value = transfer_decade_value


def execute_step(csvw, step: Union[Step, Step2, Step3], previous_step: Union[Step, Step2, Step3], inits, read_row, samples_per_step, step_soak_time):
    if not isinstance(step, Step3):
        step = step.to_step3()
    if previous_step and not isinstance(previous_step, Step3):
        previous_step = previous_step.to_step3()
    set_instrument_and_dut_safe(step, previous_step, inits)
    if step.manual_prompt:
        manual_prompt(step)
    print(f'Executing step: {step}')
    setup_dut(step, inits)
    setup_instrument(step, previous_step, inits, step_soak_time)
    wait_for_settle(step, step_soak_time, step.manual_prompt)
    sample_input(step, inits, csvw, read_row, samples_per_step)


def setup_dut(step: Step3, inits):
    dut = get_dut(step, inits)
    if isinstance(dut, ivi.fluke.fluke5450a):
        f5450a = dut
        f5450a.output_function = step.dut.dut_setting_cmd.function
        f5450a.output.value = step.dut.dut_setting_cmd.value
        f5450a.output.enabled = 'on'
    elif isinstance(dut, ivi.datron_wavetek.datron4700):
        d4700 = dut
        d4700.output_function = step.dut.dut_setting_cmd.function
        d4700.range = step.dut.dut_setting_cmd.range
        if step.dut.dut_setting_cmd.function in ('two_wire_resistance', 'four_wire_resistance'):
            if step.dut.dut_setting_cmd.value == 0:
                d4700.output.full_range_or_zero = 'zero'
            else:
                d4700.output.full_range_or_zero = '+full_range'
        else:
            d4700.output.value = step.dut.dut_setting_cmd.value
        d4700.output.enabled = 'on'


def setup_instrument(step: Step3, previous_step: Step3, inits, step_soak_time: float):
    instruments = step.instruments
    previous_instruments = previous_step.instruments if previous_step else [None] * len(step.instruments)
    for instrument, previous_instrument in zip(instruments, previous_instruments):
        if instrument.name.startswith('ag3458a_'):
            ag3458a: ivi.agilent.agilent3458A = inits[instrument.name]
            measurement_function = instrument.setting.measurement_function
            ag3458a.measurement_function = 'ac_volts_sync' if measurement_function == 'ac_volts' else measurement_function
            ag3458a.range = instrument.setting.range
        elif instrument.name == 'w4950':
            w4950: ivi.datron_wavetek.wavetek4950 = inits['w4950']
            percentage = int(abs(step.dut.dut_setting_cmd.value) / step.dut.dut_setting_cmd.range * 100)
            if instrument.setting.measurement_function in ('ac_volts', 'ac_current'):
                # ACV and ACI commands are not working on my unit, ACV does nothing and ACI gives system error
                w4950._measurement_function = instrument.setting.measurement_function
                w4950._measurement_percentage = percentage
                w4950._range = instrument.setting.range
                w4950._ac_frequency_min = instrument.setting.freq
                return
            w4950.measurement_function = instrument.setting.measurement_function
            if getattr(instrument.setting, 'freq', None):
                w4950.ac.frequency_min = instrument.setting.freq
            w4950.measurement.percentage = percentage
            w4950.range = instrument.setting.range
        elif instrument.name == 'w4920':
            w4920: ivi.datron_wavetek.wavetek4920 = inits['w4920']
            if previous_step:
                freq_ratio = (previous_step.dut.dut_setting_cmd.freq / max(1e-6, step.dut.dut_setting_cmd.freq))
            if instrument.setting.range <= 0.105 and (
                    previous_step is None
                    or previous_instrument.setting.measurement_function != instrument.setting.measurement_function
                    or previous_instrument.setting.range > 0.105
                    or freq_ratio < 0.98
                    or freq_ratio > 1.02):
                if step.dut.dut_setting_cmd.value < 0.095 or step.dut.dut_setting_cmd.value > 0.105:
                    print(f'Unable to run AC millivolt gain adjustment with input: {step.dut.dut_setting_cmd.value}')
                    raise ivi.OperationNotSupportedException
                print('Waiting to stabilize for ACMV gain measurement')
                time.sleep(step_soak_time)
                print('Measuring ACMV gain')
                w4920.measurement.measure_gain()
            measurement_function = 'ac_millivolts' if instrument.setting.measurement_function == 'ac_volts' and instrument.setting.range <= 0.105 \
                else instrument.setting.measurement_function
            w4920.measurement_function = measurement_function
            w4920.range = instrument.setting.range
            low_frequency_limit = max(1, step.dut.dut_setting_cmd.freq / 2)
            w4920.ac.frequency_min = low_frequency_limit


def set_instrument_and_dut_safe(step: Step3, previous_step: Step3, inits):
    instrument_name = step.instruments[0].name
    instrument_setting = step.instruments[0].setting
    if previous_step:
        previous_instrument_setting = previous_step.instruments[0].setting
    instrument: ivi.dmm.Base = inits[instrument_name]
    if previous_step is None:
        if instrument_name == 'w4950' and instrument_setting.measurement_function in ('ac_volts', 'ac_current'):
            return
        instrument.measurement_function = instrument_setting.measurement_function
        instrument.range = instrument_setting.range
        return
    old_function = previous_step.dut.dut_setting_cmd.function
    old_range = previous_instrument_setting.range
    old_dut = get_dut(previous_step, inits)
    old_value = previous_step.dut.dut_setting_cmd.value
    new_function = step.dut.dut_setting_cmd.function
    new_range = instrument_setting.range
    new_dut = get_dut(step, inits)
    safe_transition, transition_function, transition_range = safe_function(old_function, old_range, new_function, new_range)
    is_unsafe_manual_transition = unsafe_manual_transition(step, old_function, old_value)
    if not safe_transition or is_unsafe_manual_transition:
        for dut in {old_dut, new_dut}:
            if hasattr(dut, 'output'):
                dut.output.enabled = False
    if instrument_name == 'w4920':
        transition_function = 'ac_millivolts' if transition_function == 'ac_volts' and transition_range <= 0.105 \
            else transition_function
    if instrument_name == 'w4950' and instrument_setting.measurement_function in ('ac_volts', 'ac_current'):
        # ACV and ACI commands are not working on my 4950, ACV does nothing and ACI gives system error
        instrument._measurement_function = instrument_setting.measurement_function
        instrument._range = instrument_setting.range
    else:
        instrument.measurement_function = transition_function
        instrument.range = transition_range


def manual_prompt(step: Step3):
    instrument_names = ', '.join([i.name for i in step.instruments])
    print(f'Please connect {instrument_names} to {step.dut.name} set to {step.dut.setting} for {step.dut.dut_setting_cmd.function}')
    beep()
    input('Press enter to continue...')


def safe_function(old_function: str, old_range: float, new_function: str, new_range: float):
    simple_old_function, simple_new_function = map(simplify_function, (old_function, new_function))
    if simple_old_function == simple_new_function:
        max_range = max(old_range, new_range)
        ranges = (old_range, new_range)
        functions = (old_function, new_function)
        max_function = functions[ranges.index(max_range)]
        return True, max_function, max_range
    elif 'resistance' in {simple_old_function, simple_new_function}:
        return (True, new_function, new_range) if old_function.endswith('resistance') else (True, old_function, old_range)
    elif {simple_old_function, simple_new_function} == {'current', 'volts'}:
        return False, new_function, new_range


def unsafe_manual_transition(step: Step3, old_function: str, old_value: float):
    if not step.manual_prompt:
        return False
    simple_function = simplify_function(old_function)
    if simple_function == 'resistance':
        return False
    elif simple_function == 'volts' and old_value > 30:
        return True
    elif simple_function == 'current' and old_value > 0.01:
        return True
    else:
        return True


def simplify_function(function: str):
    if function.endswith('volts'):
        return 'volts'
    elif function.endswith('current'):
        return 'current'
    elif function.endswith('resistance'):
        return 'resistance'
    else:
        return function


def get_dut(step: Step3, inits):
    if step.dut.name == 'Fluke 5450A':
        dut: ivi.fluke.fluke5450a = inits['f5450a']
        return dut
    elif step.dut.name == 'Datron 4700':
        dut: ivi.datron_wavetek.datron4700 = inits['d4700']
        return dut


def wait_for_settle(step: Step3, step_soak_time, manual_prompt=False):
    if manual_prompt:
        time.sleep(step_soak_time * 2)
    time.sleep(step_soak_time)


def sample_input(step: Step3, inits, csvw, read_row, samples_per_step):
    for sample_no in range(1, samples_per_step+1):
        while True:
            print(f"{sample_no:2d}: ", end="")
            row, has_measurement = read_row(inits, step.instruments)
            if has_measurement:
                row['dut'] = step.dut.name
                row['dut_setting'] = step.dut.setting
            csvw.writerow(row)
            if has_measurement:
                break


def check_valid_value(instrument, value):
    if instrument.measurement.is_over_range(value) or instrument.measurement.is_under_range(value):
        # beep()
        raise IOError(f'Received under/overrange value {value} from {instrument}')

def beep():
    os.environ['PULSE_SERVER'] = 'nufan'
    subprocess.run(['paplay', 'suspend-error.oga'])


def resistance_is_4w(value) -> bool:
    return value <= 1e6
