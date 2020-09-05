import pytest
import binascii

from ldfparser import LinFrame, LinSignal
from ldfparser.encoding import LinSignalType, LogicalValue, PhysicalValue

@pytest.mark.unit
def test_frame_raw_encoding():
	signal1 = LinSignal('Signal_1', 8, 0)
	signal2 = LinSignal('Signal_2', 4, 0)
	signal3 = LinSignal('Signal_3', 1, 0)

	frame = LinFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
	content = frame.raw({
		'Signal_1': 100,
		'Signal_2': 10,
		'Signal_3': 1
	})
	
	assert binascii.hexlify(content) == binascii.hexlify(bytearray([100, (10 << 4) | 1]))

@pytest.mark.unit
def test_frame_raw_encoding_out_of_range():
	signal1 = LinSignal('Signal_1', 8, 0)
	signal2 = LinSignal('Signal_2', 4, 0)
	signal3 = LinSignal('Signal_3', 1, 0)

	frame = LinFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
	with pytest.raises(Exception) as e:
		content = frame.raw({
			'Signal_1': 100,
			'Signal_2': 30,
			'Signal_3': 1
		})

@pytest.mark.unit
def test_frame_signals_overlapping():
	signal1 = LinSignal('Signal_1', 8, 0)
	signal2 = LinSignal('Signal_2', 4, 0)
	signal3 = LinSignal('Signal_3', 1, 0)

	with pytest.raises(Exception) as e:
		frame = LinFrame(1, 'Frame_1', 2, {0: signal1, 7: signal2, 15: signal3})

@pytest.mark.unit
def test_frame_signal_out_of_frame():
	signal1 = LinSignal('Signal_1', 8, 0)
	signal2 = LinSignal('Signal_2', 4, 0)

	with pytest.raises(Exception) as e:
		frame = LinFrame(1, 'Frame_1', 2, {0: signal1, 14: signal2})

@pytest.mark.integration
def test_frame_encode_data():
	motorSpeed = LinSignal('MotorSpeed', 7, [0])
	motorValues = [LogicalValue(0, 'off'), PhysicalValue(1, 99, 1, 0, 'rpm'), PhysicalValue(100, 128, 0, 100)]

	temperature = LinSignal('Temperature', 8, [255])
	temperatureValues = [LogicalValue(0, 'MEASUREMENT_ERROR'), PhysicalValue(1, 255, 1, -50, 'C')]

	errorState = LinSignal('Error', 1, [0])
	errorValues = [LogicalValue(0, 'NO_ERROR'), LogicalValue(1, 'ERROR')]

	converters = {
		'MotorSpeed': LinSignalType('MotorSpeedType', motorValues),
		'Temperature': LinSignalType('TemperatureType', temperatureValues),
		'Error': LinSignalType('ErrorType', errorValues)
	}

	frame = LinFrame(1, 'Status', 2, {0: motorSpeed, 7: errorState, 8: temperature})
	content = frame.data(
		{
			'Temperature': -30,
			'MotorSpeed': '50rpm',
			'Error': 'NO_ERROR'
		}, 
		converters
	)
	assert binascii.hexlify(content) == binascii.hexlify(bytearray([50 << 1 | 0, ((-30) - (-50))]))