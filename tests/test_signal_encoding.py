import pytest

from ldfparser.encoding import LinSignalType, PhysicalValue, LogicalValue

@pytest.mark.integration
def test_signal_encode():
	offValue = LogicalValue(0, 'off')
	motorSpeed = PhysicalValue(1, 99, 1, 0, 'rpm')
	overdrive = PhysicalValue(100, 255, 0, 100)

	signalType = LinSignalType('MotorType', [motorSpeed, overdrive, offValue])
	assert signalType.encode('off') == 0
	assert signalType.encode(99) == 99
	assert signalType.encode(101) == 100
	assert signalType.encode(120) == 100