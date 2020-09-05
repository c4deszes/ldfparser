import pytest
from ldfparser.encoding import PhysicalValue, LogicalValue

@pytest.fixture
def physicalValue():
	# maps 0-100 rpm values to 0 - 254 values
	return PhysicalValue(0, 254, 0.3937, 0, 'rpm')

@pytest.mark.unit
def test_range_encode_unitless_numeric(physicalValue):
	assert physicalValue.encode(0) == 0
	assert physicalValue.encode(100) == 254
	
	with pytest.raises(ValueError) as e:
		physicalValue.encode(-1)

	with pytest.raises(ValueError) as e:
		physicalValue.encode(101)

@pytest.mark.unit
def test_range_encode_unitless_string(physicalValue):
	assert physicalValue.encode('0') == 0
	assert physicalValue.encode('100') == 254
	
	with pytest.raises(ValueError) as e:
		physicalValue.encode('-1')

	with pytest.raises(ValueError) as e:
		physicalValue.encode('101')

@pytest.mark.unit
def test_range_encode_string_with_unit(physicalValue):
	assert physicalValue.encode('0rpm') == 0
	assert physicalValue.encode('100rpm') == 254
	
	with pytest.raises(ValueError) as e:
		physicalValue.encode('-1rpm')

	with pytest.raises(ValueError) as e:
		physicalValue.encode('101rpm')

@pytest.mark.unit
def test_range_encode_string_with_wrong_unit(physicalValue):
	with pytest.raises(ValueError) as e:
		physicalValue.encode('50deg')

	with pytest.raises(ValueError) as e:
		physicalValue.encode('101deg')

@pytest.mark.unit
def test_range_encode_scale_zero():
	value = PhysicalValue(100, 255, 0, 100, 'rpm')
	assert value.encode(100) == 100
	assert value.encode(120) == 100

@pytest.mark.unit
def test_range_decode_valid(physicalValue):
	assert physicalValue.decode(0) == 0
	assert abs(physicalValue.decode(254) - 100.0) < 0.01

@pytest.mark.unit
def test_range_decode_invalid(physicalValue):
	with pytest.raises(ValueError) as e:
		physicalValue.decode(-1)

@pytest.fixture
def logicalValue():
	# maps the value 1 to 'on' state
	return LogicalValue(1, "on")

@pytest.mark.unit
def test_logical_encode(logicalValue):
	assert logicalValue.encode("on") == 1

	with pytest.raises(ValueError) as e:
		logicalValue.encode('off')

@pytest.mark.unit
def test_logical_decode(logicalValue):
	assert logicalValue.decode(1) == "on"

	with pytest.raises(ValueError) as e:
		logicalValue.decode(0)

@pytest.mark.unit
def test_logical_encode_no_signal_info():
	logicalValue = LogicalValue(1)

	assert logicalValue.encode(1) == 1

	with pytest.raises(ValueError) as e:
		logicalValue.encode(0)

@pytest.mark.unit
def test_logical_decode_no_signal_info():
	logicalValue = LogicalValue(1)

	assert logicalValue.decode(1) == 1

	with pytest.raises(ValueError) as e:
		logicalValue.decode(0)