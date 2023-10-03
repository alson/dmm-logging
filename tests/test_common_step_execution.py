from pprint import pprint
from common_step_execution import (FourWireResistanceCommand, Instrument, InstrumentSettingCommand, Dut, Res4WDutSettings, TransferDirection, decade_transfer_range, decade_transfer_unidirectional, generate_resistance_transfer_steps, get_value_decade_for_instrument, generate_resistance_steps, Step3)

class TestGenerateResistanceTransferSteps:
    def test_forward_transfer_direction_from_large_to_small(self):
        instrument = Instrument('ag3458a_1', InstrumentSettingCommand())
        reference = Dut('DUT1', 'setting1', Res4WDutSettings(range=10e3, value=10e3))
        transfer = Dut('DUT2', 'setting2', Res4WDutSettings())
        target_value = 1e3
        direction = TransferDirection.FORWARD

        result = generate_resistance_transfer_steps(instrument, reference, transfer, target_value, direction)
        pprint(result)
        assert len(result) == 4

        assert result[0].dut.name == reference.name
        assert result[0].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[0].instruments[0].setting.range == reference.dut_setting_cmd.range
        assert result[0].instruments[0].name == instrument.name

        assert result[1].dut.name == transfer.name
        assert result[1].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[1].instruments[0].setting.range == reference.dut_setting_cmd.range
        assert result[1].instruments[0].name == instrument.name

        assert result[2].dut.name == transfer.name
        assert result[2].dut.dut_setting_cmd.value == target_value
        assert result[2].instruments[0].setting.range == reference.dut_setting_cmd.range
        assert result[2].instruments[0].name == instrument.name

        assert result[3].dut.name == transfer.name
        assert result[3].dut.dut_setting_cmd.value == target_value
        assert result[3].instruments[0].setting.range == target_value
        assert result[3].instruments[0].name == instrument.name

    # Generates resistance transfer steps for reverse transfer direction
    def test_reverse_transfer_direction_from_large_to_small(self):
        instrument = Instrument('ag3458a_1', InstrumentSettingCommand())
        reference = Dut('DUT1', 'setting1', Res4WDutSettings(range=10e3, value=10e3))
        transfer = Dut('DUT2', 'setting2', Res4WDutSettings())
        target_value = 1e3
        direction = TransferDirection.REVERSE

        result = generate_resistance_transfer_steps(instrument, reference, transfer, target_value, direction)
        pprint(result)
        assert len(result) == 4

        assert result[0].dut.name == transfer.name
        assert result[0].dut.dut_setting_cmd.value == target_value
        assert result[0].instruments[0].setting.range == target_value
        assert result[0].instruments[0].name == instrument.name

        assert result[1].dut.name == transfer.name
        assert result[1].dut.dut_setting_cmd.value == target_value
        assert result[1].instruments[0].setting.range == reference.dut_setting_cmd.range
        assert result[1].instruments[0].name == instrument.name

        assert result[2].dut.name == transfer.name
        assert result[2].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[2].instruments[0].setting.range == reference.dut_setting_cmd.value
        assert result[2].instruments[0].name == instrument.name

        assert result[3].dut.name == reference.name
        assert result[3].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[3].instruments[0].setting.range == reference.dut_setting_cmd.value
        assert result[3].instruments[0].name == instrument.name

    def test_forward_transfer_direction_from_small_to_large(self):
        instrument = Instrument('ag3458a_1', InstrumentSettingCommand())
        reference = Dut('DUT1', 'setting1', Res4WDutSettings(range=10e3, value=10e3))
        transfer = Dut('DUT2', 'setting2', Res4WDutSettings())
        target_value = 100e3
        direction = TransferDirection.FORWARD

        result = generate_resistance_transfer_steps(instrument, reference, transfer, target_value, direction)
        pprint(result)
        assert len(result) == 4

        assert result[0].dut.name == reference.name
        assert result[0].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[0].instruments[0].setting.range == reference.dut_setting_cmd.range
        assert result[0].instruments[0].name == instrument.name

        assert result[1].dut.name == transfer.name
        assert result[1].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[1].instruments[0].setting.range == reference.dut_setting_cmd.range
        assert result[1].instruments[0].name == instrument.name

        assert result[2].dut.name == transfer.name
        assert result[2].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[2].instruments[0].setting.range == target_value
        assert result[2].instruments[0].name == instrument.name

        assert result[3].dut.name == transfer.name
        assert result[3].dut.dut_setting_cmd.value == target_value
        assert result[3].instruments[0].setting.range == target_value
        assert result[3].instruments[0].name == instrument.name

    # Generates resistance transfer steps for reverse transfer direction
    def test_reverse_transfer_direction_from_small_to_large(self):
        instrument = Instrument('ag3458a_1', InstrumentSettingCommand())
        reference = Dut('DUT1', 'setting1', Res4WDutSettings(range=10e3, value=10e3))
        transfer = Dut('DUT2', 'setting2', Res4WDutSettings())
        target_value = 100e3
        direction = TransferDirection.REVERSE

        result = generate_resistance_transfer_steps(instrument, reference, transfer, target_value, direction)
        pprint(result)
        assert len(result) == 4

        assert result[0].dut.name == transfer.name
        assert result[0].dut.dut_setting_cmd.value == target_value
        assert result[0].instruments[0].setting.range == target_value
        assert result[0].instruments[0].name == instrument.name

        assert result[1].dut.name == transfer.name
        assert result[1].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[1].instruments[0].setting.range == target_value
        assert result[1].instruments[0].name == instrument.name

        assert result[2].dut.name == transfer.name
        assert result[2].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[2].instruments[0].setting.range == reference.dut_setting_cmd.value
        assert result[2].instruments[0].name == instrument.name

        assert result[3].dut.name == reference.name
        assert result[3].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[3].instruments[0].setting.range == reference.dut_setting_cmd.value
        assert result[3].instruments[0].name == instrument.name

    def test_transfer_same_value(self):
        instrument = Instrument('ag3458a_1', InstrumentSettingCommand())
        reference = Dut('DUT1', 'setting1', Res4WDutSettings(range=10e3, value=10e3))
        transfer = Dut('DUT2', 'setting2', Res4WDutSettings())
        target_value = 10e3
        direction = TransferDirection.FORWARD

        result = generate_resistance_transfer_steps(instrument, reference, transfer, target_value, direction)
        pprint(result)
        assert len(result) == 1

        assert result[0].dut.name == reference.name
        assert result[0].dut.dut_setting_cmd.value == reference.dut_setting_cmd.value
        assert result[0].instruments[0].setting.range == reference.dut_setting_cmd.range
        assert result[0].instruments[0].name == instrument.name

 
class TestGetValueDecadeForInstrument:
    # Returns the correct decade for a value within the instrument range.
    def test_correct_decade_within_range(self):
        instrument = Instrument(name="ag3458a_1", setting="test")
        value = 50.0
        expected_decade = 2
        assert get_value_decade_for_instrument(instrument, value) == expected_decade

    # Returns the correct decade for a value at the lower edge of the instrument range.
    def test_correct_decade_at_lower_edge(self):
        instrument = Instrument(name="ag3458a_1", setting="test")
        value = 0.1
        expected_decade = -1
        result = get_value_decade_for_instrument(instrument, value)
        assert result == expected_decade, f'Expected {expected_decade} but got {result}'

    # Returns the correct decade for a value at the upper edge of the instrument range.
    def test_correct_decade_at_upper_edge(self):
        instrument = Instrument(name="ag3458a_1", setting="test")
        value = 1000.0
        expected_decade = 3
        assert get_value_decade_for_instrument(instrument, value) == expected_decade

    # Returns the correct decade for a value just outside the instrument range.
    def test_correct_decade_just_outside_range(self):
        instrument = Instrument(name="ag3458a_1", setting="test")
        value = 1201.0
        expected_decade = 4
        assert get_value_decade_for_instrument(instrument, value) == expected_decade


class TestGenerateResistanceSteps:

    # Returns a list of Step3 objects with correct transfer and instrument values when given a list of Dut objects
    def test_correct_transfer_and_instrument_values_with_list_of_Dut_objects(self):
        instrument = Instrument(name='ag3458a_1', setting=FourWireResistanceCommand(range=10e3))
        dut1 = Dut("DUT1", "setting1", Res4WDutSettings(value=10))
        dut2 = Dut("DUT2", "setting2", Res4WDutSettings(value=100))
        dut3 = Dut("DUT3", "setting3", Res4WDutSettings(value=1000))
        transfers = [dut1, dut2, dut3]
        expected_result = [
            Step3(dut1, [instrument.with_range(dut1.dut_setting_cmd.value)]),
            Step3(dut1, [instrument.with_range(dut2.dut_setting_cmd.value)]),
            Step3(dut2, [instrument.with_range(dut2.dut_setting_cmd.value)]),
            Step3(dut2, [instrument.with_range(dut3.dut_setting_cmd.value)]),
            Step3(dut3, [instrument.with_range(dut3.dut_setting_cmd.value)])
        ]
        assert list(generate_resistance_steps(instrument, transfers)) == expected_result

    # Returns an empty list when given an empty list of Dut objects
    def test_empty_list_of_Dut_objects(self):
        instrument = Instrument(name='ag3458a_1', setting=FourWireResistanceCommand(range=10e3))
        transfers = []
        expected_result = []
        assert list(generate_resistance_steps(instrument, transfers)) == expected_result

    # Returns a list of Step3 objects with correct transfer and instrument values when given a list with a single Dut object
    def test_correct_transfer_and_instrument_values_with_single_Dut_object(self):
        instrument = Instrument(name='ag3458a_1', setting=FourWireResistanceCommand(range=10e3))
        dut = Dut("DUT", "setting", Res4WDutSettings(value=1))
        transfers = [dut]
        expected_result = [
            Step3(dut, [instrument.with_range(dut.dut_setting_cmd.value)])
        ]
        assert list(generate_resistance_steps(instrument, transfers)) == expected_result


class TestDecadeTransferUnidirectional:

    # Returns a list of integers for a valid start and end decade
    def test_valid_start_end_decade(self):
        result = decade_transfer_unidirectional(1, 3)
        assert len(result) == 3
        assert result == [10, 100, 1000]

    # Returns a list of floats for the same start and end decade
    def test_same_start_end_decade(self):
        start_decade = end_decade = 1
        result = decade_transfer_unidirectional(start_decade, end_decade)
        assert len(result) == 1, 'Result list length is not 1'
        assert result == [10], 'Result does not match expected output'

    # Returns an empty list for a start decade greater than end decade
    def test_start_decade_greater_than_end_decade(self):
        result = decade_transfer_unidirectional(3, 1)
        assert isinstance(result, list)
        assert len(result) == 0


class TestDecadeTransferRange:
    # Test with start_decade = 1 and end_decade = 3
    def test_start_decade_1_end_decade_3(self):
        result = decade_transfer_range(1, 3)
        assert result == [10.0, 100.0, 1000.0]

    # Test with start_decade = 0 and end_decade = 2
    def test_start_decade_0_end_decade_2(self):
        result = decade_transfer_range(0, 2)
        assert result == [1.0, 10.0, 100.0]

    # Test with start_decade = -1 and end_decade = 1
    def test_start_decade_minus_1_end_decade_1(self):
        result = decade_transfer_range(-1, 1)
        assert result == [0.1, 1.0, 10.0]

    # Test with start_decade = 0 and end_decade = 0
    def test_start_decade_0_end_decade_0(self):
        result = decade_transfer_range(0, 0)
        assert result == [1.0]

    # Test with start_decade = -1 and end_decade = -3
    def test_start_decade_minus_1_end_decade_minus_3(self):
        result = decade_transfer_range(-1, -3)
        assert result == [0.1, 0.01, 0.001]

    # Test with start_decade = 1 and end_decade = -1
    def test_start_decade_1_end_decade_minus_1(self):
        result = decade_transfer_range(1, -1)
        assert result == [10, 1, 0.1]

    # start decade 3, end decade 1
    def test_start_decade_3_end_decade_1(self):
        result = decade_transfer_range(3, 1)
        assert result == [1000.0, 100.0, 10.0]
