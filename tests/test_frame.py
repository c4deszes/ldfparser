import pytest

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

	assert list(content) == [100, 10 | 1 << 7]


@pytest.mark.unit
def test_frame_raw_encoding_zero():
	signal1 = LinSignal('Signal_1', 8, 255)
	signal2 = LinSignal('Signal_2', 4, 15)
	signal3 = LinSignal('Signal_3', 1, 1)

	frame = LinFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
	content = frame.raw({
		'Signal_1': 0,
		'Signal_2': 10,
		'Signal_3': 1
	})

	assert list(content) == [0, 10 | 1 << 7]


@pytest.mark.unit
def test_frame_raw_encoding_no_signal():
	signal1 = LinSignal('Signal_1', 8, 255)
	signal2 = LinSignal('Signal_2', 4, 255)
	signal3 = LinSignal('Signal_3', 1, 255)

	frame = LinFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
	content = frame.raw({
		'Signal_2': 10,
		'Signal_3': 1
	})

	assert list(content) == [255, 10 | 1 << 7]


@pytest.mark.unit
def test_frame_raw_encoding_array():
	signal1 = LinSignal('Signal_1', 16, [0, 0])
	frame = LinFrame(1, 'Frame_1', 2, {0: signal1})
	content = frame.raw({
		'Signal_1': [1, 2]
	})
	assert list(content) == [1, 2]


@pytest.mark.unit
def test_frame_raw_encoding_array2():
	signal1 = LinSignal('Signal_1', 16, [0, 0])
	signal2 = LinSignal('Signal_2', 8, 0)
	frame = LinFrame(1, 'Frame_1', 3, {0: signal1, 16: signal2})
	content = frame.raw({
		'Signal_1': [1, 2],
		'Signal_2': 3
	})
	assert list(content) == [1, 2, 3]


@pytest.mark.unit
def test_frame_raw_decoding_array():
	signal1 = LinSignal('Signal_1', 16, [0, 0])
	frame = LinFrame(1, 'Frame_1', 2, {0: signal1})
	assert frame.parse_raw(bytearray([1, 2])) == {"Signal_1": [1, 2]}


@pytest.mark.unit
def test_frame_raw_decoding_array2():
	signal1 = LinSignal('Signal_1', 16, [0, 0])
	signal2 = LinSignal('Signal_2', 8, 0)
	frame = LinFrame(1, 'Frame_1', 3, {0: signal1, 16: signal2})
	assert frame.parse_raw(bytearray([1, 2, 3])) == {"Signal_1": [1, 2], "Signal_2": 3}


@pytest.mark.unit
def test_frame_raw_encoding_out_of_range():
	signal1 = LinSignal('Signal_1', 8, 0)
	signal2 = LinSignal('Signal_2', 4, 0)
	signal3 = LinSignal('Signal_3', 1, 0)

	frame = LinFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
	with pytest.raises(Exception):
		frame.raw({
			'Signal_1': 100,
			'Signal_2': 30,
			'Signal_3': 1
		})


@pytest.mark.unit
def test_frame_signals_overlapping():
	signal1 = LinSignal('Signal_1', 8, 0)
	signal2 = LinSignal('Signal_2', 4, 0)
	signal3 = LinSignal('Signal_3', 1, 0)

	with pytest.raises(ValueError):
		LinFrame(1, 'Frame_1', 2, {0: signal1, 7: signal2, 15: signal3})


@pytest.mark.unit
def test_frame_signal_out_of_frame():
	signal1 = LinSignal('Signal_1', 8, 0)
	signal2 = LinSignal('Signal_2', 4, 0)

	with pytest.raises(ValueError):
		LinFrame(1, 'Frame_1', 2, {0: signal1, 14: signal2})


@pytest.mark.unit
def test_frame_encode_data():
	motorSpeed = LinSignal('MotorSpeed', 7, 0)
	motorValues = [
		LogicalValue(0, 'off'),
		PhysicalValue(1, 99, 1, 0, 'rpm'),
		PhysicalValue(100, 128, 0, 100)]

	temperature = LinSignal('Temperature', 8, 255)
	temperatureValues = [
		LogicalValue(0, 'MEASUREMENT_ERROR'),
		PhysicalValue(1, 255, 1, -50, 'C')]

	errorState = LinSignal('Error', 1, 0)
	errorValues = [
		LogicalValue(0, 'NO_ERROR'),
		LogicalValue(1, 'ERROR')]

	converters = {
		'MotorSpeed': LinSignalType('MotorSpeedType', motorValues),
		'Temperature': LinSignalType('TemperatureType', temperatureValues),
		'Error': LinSignalType('ErrorType', errorValues)
	}

	frame = LinFrame(1, 'Status', 2, {0: motorSpeed, 7: errorState, 8: temperature})
	frame.data(
		{
			'Temperature': -30,
			'MotorSpeed': '50rpm',
			'Error': 'NO_ERROR'
		},
		converters
	)


@pytest.mark.unit
def test_frame_encode_data_missing_encoder():
	motorSpeed = LinSignal('MotorSpeed', 8, 0)
	motorValues = [PhysicalValue(0, 255, 0, 100)]

	converters = {
		'MotorSpeed': LinSignalType('MotorSpeedType', motorValues)
	}
	frame = LinFrame(1, 'Status', 1, {0: motorSpeed})

	with pytest.raises(ValueError):
		frame.data({'MissingSignal': 0}, converters)


@pytest.mark.unit
def test_frame_decode_data():
	motorSpeed = LinSignal('MotorSpeed', 7, 0)
	motorValues = [
		LogicalValue(0, 'off'),
		PhysicalValue(1, 99, 1, 0, 'rpm'),
		PhysicalValue(100, 128, 0, 100)]

	temperature = LinSignal('Temperature', 8, 255)
	temperatureValues = [
		LogicalValue(0, 'MEASUREMENT_ERROR'),
		PhysicalValue(1, 255, 1, -50, 'C')]

	errorState = LinSignal('Error', 1, 0)
	errorValues = [
		LogicalValue(0, 'NO_ERROR'),
		LogicalValue(1, 'ERROR')]

	converters = {
		'MotorSpeed': LinSignalType('MotorSpeedType', motorValues),
		'Temperature': LinSignalType('TemperatureType', temperatureValues),
		'Error': LinSignalType('ErrorType', errorValues)
	}

	frame = LinFrame(1, 'Status', 2, {0: motorSpeed, 7: errorState, 8: temperature})
	frame.parse(
		[0x88, 0x88],
		converters
	)


@pytest.mark.unit
def test_frame_decode_data_missing_decoder():
	motorSpeed = LinSignal('MotorSpeed', 8, 0)

	converters = {}
	frame = LinFrame(1, 'Status', 1, {0: motorSpeed})

	with pytest.raises(ValueError):
		frame.parse([0x88], converters)
