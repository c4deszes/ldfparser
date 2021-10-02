import pytest

from ldfparser.signal import LinSignal
from ldfparser.encoding import (
    ASCIIValue, BCDValue, PhysicalValue, LogicalValue, LinSignalEncodingType
)

@pytest.mark.unit
def test_encode_physical_unitless_numeric():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    assert physical_value.encode(0, motor_signal) == 0
    assert physical_value.encode(100, motor_signal) == 254

    with pytest.raises(ValueError):
        physical_value.encode(-1, motor_signal)

    with pytest.raises(ValueError):
        physical_value.encode(101, motor_signal)

@pytest.mark.unit
def test_encode_physical_unitless_string():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    assert physical_value.encode('0', motor_signal) == 0
    assert physical_value.encode('100', motor_signal) == 254

    with pytest.raises(ValueError):
        physical_value.encode('-1', motor_signal)

    with pytest.raises(ValueError):
        physical_value.encode('101', motor_signal)

@pytest.mark.unit
def test_encode_physical_string_with_unit():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    assert physical_value.encode('0rpm', motor_signal) == 0
    assert physical_value.encode('100rpm', motor_signal) == 254

    with pytest.raises(ValueError):
        physical_value.encode('-1rpm', motor_signal)

    with pytest.raises(ValueError):
        physical_value.encode('101rpm', motor_signal)

@pytest.mark.unit
def test_encode_physical_string_with_wrong_unit():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    with pytest.raises(ValueError):
        physical_value.encode('50deg', motor_signal)

    with pytest.raises(ValueError):
        physical_value.encode('101deg', motor_signal)

@pytest.mark.unit
def test_encode_physical_scale_zero():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    value = PhysicalValue(100, 255, 0, 100, 'rpm')
    assert value.encode(100, motor_signal) == 100
    assert value.encode(120, motor_signal) == 100

@pytest.mark.unit
def test_decode_physical_valid():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    assert physical_value.decode(0, motor_signal) == 0
    assert abs(physical_value.decode(254, motor_signal) - 100.0) < 0.01

@pytest.mark.unit
def test_decode_physical_invalid():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    with pytest.raises(ValueError):
        physical_value.decode(-1, motor_signal)

@pytest.mark.unit
def test_encode_logical():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    logical_value = LogicalValue(1, "on")
    assert logical_value.encode("on", motor_signal) == 1

    with pytest.raises(ValueError):
        logical_value.encode('off', motor_signal)

@pytest.mark.unit
def test_decode_logical():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    logical_value = LogicalValue(1, "on")
    assert logical_value.decode(1, motor_signal) == "on"

    with pytest.raises(ValueError):
        logical_value.decode(0, motor_signal)

@pytest.mark.unit
def test_encode_logical_no_signal_info():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    logical_value = LogicalValue(1)

    assert logical_value.encode(1, motor_signal) == 1

    with pytest.raises(ValueError):
        logical_value.encode(0, motor_signal)

@pytest.mark.unit
def test_decode_logical_no_signal_info():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    logical_value = LogicalValue(1)

    assert logical_value.decode(1, motor_signal) == 1

    with pytest.raises(ValueError):
        logical_value.decode(0, motor_signal)

@pytest.mark.unit
def test_encode_bcd():
    bcd_value = BCDValue()

    assert bcd_value.encode(1, LinSignal('Counter', 8, [0])) == [1]
    assert bcd_value.encode(12, LinSignal('Counter', 16, [0, 0])) == [1, 2]
    assert bcd_value.encode(123, LinSignal('Counter', 24, [0, 0, 0])) == [1, 2, 3]
    assert bcd_value.encode(1234, LinSignal('Counter', 32, [0, 0, 0, 0])) == [1, 2, 3, 4]
    assert bcd_value.encode(12345, LinSignal('Counter', 40, [0, 0, 0, 0, 0])) == [1, 2, 3, 4, 5]
    assert bcd_value.encode(123456, LinSignal('Counter', 48, [0, 0, 0, 0, 0, 0])) == [1, 2, 3, 4, 5, 6]

@pytest.mark.unit
def test_encode_bcd_out_of_bounds():
    bcd_value = BCDValue()

    with pytest.raises(ValueError):
        bcd_value.encode(123, LinSignal('Counter', 16, [0, 0]))

@pytest.mark.unit
def test_decode_bcd():
    bcd_value = BCDValue()

    assert bcd_value.decode([1], LinSignal('Counter', 8, [0])) == 1
    assert bcd_value.decode([1, 2], LinSignal('Counter', 16, [0, 0])) == 12
    assert bcd_value.decode([1, 2, 3], LinSignal('Counter', 24, [0, 0, 0])) == 123
    assert bcd_value.decode([1, 2, 3, 4], LinSignal('Counter', 32, [0, 0, 0, 0])) == 1234
    assert bcd_value.decode([1, 2, 3, 4, 5], LinSignal('Counter', 40, [0, 0, 0, 0, 0])) == 12345
    assert bcd_value.decode([1, 2, 3, 4, 5, 6], LinSignal('Counter', 48, [0, 0, 0, 0, 0, 0])) == 123456

@pytest.mark.unit
def test_encode_ascii():
    id_signal = LinSignal('Id', 48, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    ascii_value = ASCIIValue()

    assert ascii_value.encode('ABC123', id_signal) == [65, 66, 67, 49, 50, 51]

@pytest.mark.unit
def test_decode_ascii():
    id_signal = LinSignal('Id', 48, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    ascii_value = ASCIIValue()

    assert ascii_value.decode([65, 66, 67, 49, 50, 51], id_signal) == 'ABC123'

@pytest.mark.integration
def test_encode_signal_scalar():
    motor_signal = LinSignal('MotorRPM', 8, 0)
    off_value = LogicalValue(0, 'off')
    motor_speed = PhysicalValue(1, 99, 1, 0, 'rpm')
    overdrive = PhysicalValue(100, 255, 0, 100)

    signal_type = LinSignalEncodingType('MotorType', [motor_speed, overdrive, off_value])
    assert signal_type.encode('off', motor_signal) == 0
    assert signal_type.encode(99, motor_signal) == 99
    assert signal_type.encode(101, motor_signal) == 100
    assert signal_type.encode(120, motor_signal) == 100

@pytest.mark.integration
def test_encode_signal_bcd():
    counter_signal = LinSignal('Counter', 24, [0, 1, 2])
    counter_value = BCDValue()

    signal_type = LinSignalEncodingType('CounterType', [counter_value])
    assert signal_type.encode(1, counter_signal) == [0, 0, 1]
    assert signal_type.encode(12, counter_signal) == [0, 1, 2]
    assert signal_type.encode(123, counter_signal) == [1, 2, 3]

@pytest.mark.integration
def test_encode_signal_ascii():
    text_signal = LinSignal('Text', 24, list("ABC"))
    text_value = ASCIIValue()

    signal_type = LinSignalEncodingType('TextType', [text_value])
    assert signal_type.encode("ABC", text_signal) == [65, 66, 67]
