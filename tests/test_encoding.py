from ldfparser.lin import LinSignal
import pytest
from ldfparser.encoding import ASCIIValue, BCDValue, LinSignalType, PhysicalValue, LogicalValue


@pytest.mark.unit
def test_encode_physical_unitless_numeric():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
	assert physicalValue.encode(0, motorSignal) == 0
	assert physicalValue.encode(100, motorSignal) == 254

	with pytest.raises(ValueError):
		physicalValue.encode(-1, motorSignal)

	with pytest.raises(ValueError):
		physicalValue.encode(101, motorSignal)


@pytest.mark.unit
def test_encode_physical_unitless_string():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
	assert physicalValue.encode('0', motorSignal) == 0
	assert physicalValue.encode('100', motorSignal) == 254

	with pytest.raises(ValueError):
		physicalValue.encode('-1', motorSignal)

	with pytest.raises(ValueError):
		physicalValue.encode('101', motorSignal)


@pytest.mark.unit
def test_encode_physical_string_with_unit():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
	assert physicalValue.encode('0rpm', motorSignal) == 0
	assert physicalValue.encode('100rpm', motorSignal) == 254

	with pytest.raises(ValueError):
		physicalValue.encode('-1rpm', motorSignal)

	with pytest.raises(ValueError):
		physicalValue.encode('101rpm', motorSignal)


@pytest.mark.unit
def test_encode_physical_string_with_wrong_unit():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
	with pytest.raises(ValueError):
		physicalValue.encode('50deg', motorSignal)

	with pytest.raises(ValueError):
		physicalValue.encode('101deg', motorSignal)


@pytest.mark.unit
def test_encode_physical_scale_zero():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	value = PhysicalValue(100, 255, 0, 100, 'rpm')
	assert value.encode(100, motorSignal) == 100
	assert value.encode(120, motorSignal) == 100


@pytest.mark.unit
def test_decode_physical_valid():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
	assert physicalValue.decode(0, motorSignal) == 0
	assert abs(physicalValue.decode(254, motorSignal) - 100.0) < 0.01


@pytest.mark.unit
def test_decode_physical_invalid():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
	with pytest.raises(ValueError):
		physicalValue.decode(-1, motorSignal)


@pytest.mark.unit
def test_encode_logical():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	logicalValue = LogicalValue(1, "on")
	assert logicalValue.encode("on", motorSignal) == 1

	with pytest.raises(ValueError):
		logicalValue.encode('off', motorSignal)


@pytest.mark.unit
def test_decode_logical():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	logicalValue = LogicalValue(1, "on")
	assert logicalValue.decode(1, motorSignal) == "on"

	with pytest.raises(ValueError):
		logicalValue.decode(0, motorSignal)


@pytest.mark.unit
def test_encode_logical_no_signal_info():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	logicalValue = LogicalValue(1)

	assert logicalValue.encode(1, motorSignal) == 1

	with pytest.raises(ValueError):
		logicalValue.encode(0, motorSignal)


@pytest.mark.unit
def test_decode_logical_no_signal_info():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	logicalValue = LogicalValue(1)

	assert logicalValue.decode(1, motorSignal) == 1

	with pytest.raises(ValueError):
		logicalValue.decode(0, motorSignal)


@pytest.mark.unit
def test_encode_bcd():
	bcdValue = BCDValue()

	assert bcdValue.encode(1, LinSignal('Counter', 8, [0])) == [1]
	assert bcdValue.encode(12, LinSignal('Counter', 16, [0, 0])) == [1, 2]
	assert bcdValue.encode(123, LinSignal('Counter', 24, [0, 0, 0])) == [1, 2, 3]
	assert bcdValue.encode(1234, LinSignal('Counter', 32, [0, 0, 0, 0])) == [1, 2, 3, 4]
	assert bcdValue.encode(12345, LinSignal('Counter', 40, [0, 0, 0, 0, 0])) == [1, 2, 3, 4, 5]
	assert bcdValue.encode(123456, LinSignal('Counter', 48, [0, 0, 0, 0, 0, 0])) == [1, 2, 3, 4, 5, 6]


@pytest.mark.unit
def test_encode_bcd_out_of_bounds():
	bcdValue = BCDValue()

	with pytest.raises(ValueError):
		bcdValue.encode(123, LinSignal('Counter', 16, [0, 0]))


@pytest.mark.unit
def test_decode_bcd():
	bcdValue = BCDValue()

	assert bcdValue.decode([1], LinSignal('Counter', 8, [0])) == 1
	assert bcdValue.decode([1, 2], LinSignal('Counter', 16, [0, 0])) == 12
	assert bcdValue.decode([1, 2, 3], LinSignal('Counter', 24, [0, 0, 0])) == 123
	assert bcdValue.decode([1, 2, 3, 4], LinSignal('Counter', 32, [0, 0, 0, 0])) == 1234
	assert bcdValue.decode([1, 2, 3, 4, 5], LinSignal('Counter', 40, [0, 0, 0, 0, 0])) == 12345
	assert bcdValue.decode([1, 2, 3, 4, 5, 6], LinSignal('Counter', 48, [0, 0, 0, 0, 0, 0])) == 123456


@pytest.mark.unit
def test_encode_ascii():
	idSignal = LinSignal('Id', 48, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
	asciiValue = ASCIIValue()

	assert asciiValue.encode('ABC123', idSignal) == [65, 66, 67, 49, 50, 51]


@pytest.mark.unit
def test_decode_ascii():
	idSignal = LinSignal('Id', 48, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
	asciiValue = ASCIIValue()

	assert asciiValue.decode([65, 66, 67, 49, 50, 51], idSignal) == 'ABC123'


@pytest.mark.integration
def test_encode_signal_scalar():
	motorSignal = LinSignal('MotorRPM', 8, 0)
	offValue = LogicalValue(0, 'off')
	motorSpeed = PhysicalValue(1, 99, 1, 0, 'rpm')
	overdrive = PhysicalValue(100, 255, 0, 100)

	signalType = LinSignalType('MotorType', [motorSpeed, overdrive, offValue])
	assert signalType.encode('off', motorSignal) == 0
	assert signalType.encode(99, motorSignal) == 99
	assert signalType.encode(101, motorSignal) == 100
	assert signalType.encode(120, motorSignal) == 100


@pytest.mark.integration
def test_encode_signal_bcd():
	counterSignal = LinSignal('Counter', 24, [0, 1, 2])
	counterValue = BCDValue()

	signalType = LinSignalType('CounterType', [counterValue])
	assert signalType.encode(1, counterSignal) == [0, 0, 1]
	assert signalType.encode(12, counterSignal) == [0, 1, 2]
	assert signalType.encode(123, counterSignal) == [1, 2, 3]


@pytest.mark.integration
def test_encode_signal_ascii():
	textSignal = LinSignal('Text', 24, list("ABC"))
	textValue = ASCIIValue()

	signalType = LinSignalType('TextType', [textValue])
	assert signalType.encode("ABC", textSignal) == [65, 66, 67]
