import pytest

from ldfparser.frame import LinUnconditionalFrame
from ldfparser.signal import LinSignal
from ldfparser.encoding import LinSignalEncodingType, LogicalValue, PhysicalValue

@pytest.mark.unit
def test_frame_raw_encoding():
    signal1 = LinSignal('Signal_1', 8, 0)
    signal2 = LinSignal('Signal_2', 4, 0)
    signal3 = LinSignal('Signal_3', 1, 0)

    frame = LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
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

    frame = LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
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

    frame = LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
    content = frame.raw({
        'Signal_2': 10,
        'Signal_3': 1
    })

    assert list(content) == [255, 10 | 1 << 7]

@pytest.mark.unit
def test_frame_raw_encoding_array():
    signal1 = LinSignal('Signal_1', 16, [0, 0])
    frame = LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1})
    content = frame.raw({
        'Signal_1': [1, 2]
    })
    assert list(content) == [1, 2]

@pytest.mark.unit
def test_frame_raw_encoding_array2():
    signal1 = LinSignal('Signal_1', 16, [0, 0])
    signal2 = LinSignal('Signal_2', 8, 0)
    frame = LinUnconditionalFrame(1, 'Frame_1', 3, {0: signal1, 16: signal2})
    content = frame.raw({
        'Signal_1': [1, 2],
        'Signal_2': 3
    })
    assert list(content) == [1, 2, 3]

@pytest.mark.unit
def test_frame_raw_decoding_array():
    signal1 = LinSignal('Signal_1', 16, [0, 0])
    frame = LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1})
    assert frame.parse_raw(bytearray([1, 2])) == {"Signal_1": [1, 2]}

@pytest.mark.unit
def test_frame_raw_decoding_array2():
    signal1 = LinSignal('Signal_1', 16, [0, 0])
    signal2 = LinSignal('Signal_2', 8, 0)
    frame = LinUnconditionalFrame(1, 'Frame_1', 3, {0: signal1, 16: signal2})
    assert frame.parse_raw(bytearray([1, 2, 3])) == {"Signal_1": [1, 2], "Signal_2": 3}

@pytest.mark.unit
def test_frame_raw_encoding_out_of_range():
    signal1 = LinSignal('Signal_1', 8, 0)
    signal2 = LinSignal('Signal_2', 4, 0)
    signal3 = LinSignal('Signal_3', 1, 0)

    frame = LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1, 8: signal2, 15: signal3})
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
        LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1, 7: signal2, 15: signal3})

@pytest.mark.unit
def test_frame_signal_out_of_frame():
    signal1 = LinSignal('Signal_1', 8, 0)
    signal2 = LinSignal('Signal_2', 4, 0)

    with pytest.raises(ValueError):
        LinUnconditionalFrame(1, 'Frame_1', 2, {0: signal1, 14: signal2})

@pytest.mark.unit
def test_frame_encode_data():
    motor_speed = LinSignal('MotorSpeed', 7, 0)
    motor_values = [
        LogicalValue(0, 'off'),
        PhysicalValue(1, 99, 1, 0, 'rpm'),
        PhysicalValue(100, 128, 0, 100)]

    temperature = LinSignal('Temperature', 8, 255)
    temperature_values = [
        LogicalValue(0, 'MEASUREMENT_ERROR'),
        PhysicalValue(1, 255, 1, -50, 'C')]

    error_state = LinSignal('Error', 1, 0)
    error_values = [
        LogicalValue(0, 'NO_ERROR'),
        LogicalValue(1, 'ERROR')]

    converters = {
        'MotorSpeed': LinSignalEncodingType('MotorSpeedType', motor_values),
        'Temperature': LinSignalEncodingType('TemperatureType', temperature_values),
        'Error': LinSignalEncodingType('ErrorType', error_values)
    }

    frame = LinUnconditionalFrame(1, 'Status', 2, {0: motor_speed, 7: error_state, 8: temperature})
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
    motor_speed = LinSignal('MotorSpeed', 8, 0)
    motor_values = [PhysicalValue(0, 255, 0, 100)]

    converters = {
        'MotorSpeed': LinSignalEncodingType('MotorSpeedType', motor_values)
    }
    frame = LinUnconditionalFrame(1, 'Status', 1, {0: motor_speed})

    with pytest.raises(ValueError):
        frame.data({'MissingSignal': 0}, converters)

@pytest.mark.unit
def test_frame_decode_data():
    motor_speed = LinSignal('MotorSpeed', 7, 0)
    motor_values = [
        LogicalValue(0, 'off'),
        PhysicalValue(1, 99, 1, 0, 'rpm'),
        PhysicalValue(100, 128, 0, 100)]

    temperature = LinSignal('Temperature', 8, 255)
    temperature_values = [
        LogicalValue(0, 'MEASUREMENT_ERROR'),
        PhysicalValue(1, 255, 1, -50, 'C')]

    error_state = LinSignal('Error', 1, 0)
    error_values = [
        LogicalValue(0, 'NO_ERROR'),
        LogicalValue(1, 'ERROR')]

    converters = {
        'MotorSpeed': LinSignalEncodingType('MotorSpeedType', motor_values),
        'Temperature': LinSignalEncodingType('TemperatureType', temperature_values),
        'Error': LinSignalEncodingType('ErrorType', error_values)
    }

    frame = LinUnconditionalFrame(1, 'Status', 2, {0: motor_speed, 7: error_state, 8: temperature})
    frame.parse(
        [0x88, 0x88],
        converters
    )

@pytest.mark.unit
def test_frame_decode_data_missing_decoder():
    motor_speed = LinSignal('MotorSpeed', 8, 0)

    converters = {}
    frame = LinUnconditionalFrame(1, 'Status', 1, {0: motor_speed})

    with pytest.raises(ValueError):
        frame.parse([0x88], converters)

#
#
#

@pytest.fixture(scope="function")
def frame():
    motor_signal = LinSignal('MotorSpeed', 8, 0xFF)
    temp_signal = LinSignal('InternalTemperature', 6, 0x3F)
    reserved1_signal = LinSignal('Reserved1', 4, 0)
    int_error_signal = LinSignal('InternalError', 1, 0)
    comm_error_signal = LinSignal('CommError', 1, 0)
    return LinUnconditionalFrame(0x20, 'EcuStatus', 3, {
        0: motor_signal,
        8: temp_signal,
        14: reserved1_signal,
        18: int_error_signal,
        19: comm_error_signal,
    })

@pytest.fixture(scope="function")
def range_type():
    return LinSignalEncodingType('MotorSpeedType', [PhysicalValue(0, 255, 50, 0, 'rpm')])

@pytest.mark.unit
class TestLinUnconditionalFrameEncodingRaw:

    def test_encode_raw_partial(self, frame):
        data = frame.encode_raw({
            'MotorSpeed': 100,
            'CommError': 1
        })
        assert data == b'\x64\x3F\x08'

    @pytest.mark.parametrize(
        ['data', 'expected'],
        [
            ({
                'MotorSpeed': 0x64,
                'InternalTemperature': 0x32,
                'Reserved1': 0,
                'InternalError': 0,
                'CommError': 1
            }, b'\x64\x32\x08')
        ]
    )
    def test_encode_raw(self, frame, data, expected):
        assert frame.encode_raw(data) == expected

@pytest.mark.unit
class TestLinUnconditionalFrameEncoding:

    def test_encode_builtin(self, frame, range_type):
        frame._get_signal('MotorSpeed').encoding_type = range_type
        encoded = frame.encode({'MotorSpeed': '1000rpm'})
        assert encoded == b'\x14\x3F\x00'

    def test_encode_custom(self, frame, range_type):
        encoded = frame.encode({'MotorSpeed': '1000rpm'}, {'MotorSpeed': range_type})
        assert encoded == b'\x14\x3F\x00'

    def test_encode_int(self, frame):
        encoded = frame.encode({'MotorSpeed': 40})
        assert encoded == b'\x28\x3F\x00'

    @pytest.mark.parametrize(
        'value', ['1000rpm', '1000', 1000.0]
    )
    def test_encode_error_type(self, frame, value):
        with pytest.raises(ValueError):
            frame.encode({'MotorSpeed': value})

@pytest.mark.unit
@pytest.mark.parametrize("use_converter", [True, False])
def test_encode_decode_array(use_converter):
    signal = LinSignal('BattCurr', 24, [0, 0, 2])
    encoding_type = LinSignalEncodingType(
        "BattCurrCoding",
        [PhysicalValue(0, 182272, 0.00390625, -512, "A")]
    )
    converters = {}
    if use_converter:
        converters["BattCurr"] = encoding_type
    else:
        signal.encoding_type = encoding_type

    frame = LinUnconditionalFrame(0x20, "LinStatus", 3, {0: signal})
    raw = {"BattCurr": [1, 1, 1]}
    encoded_expected = bytearray([1, 1, 1])
    decoded_expected = {"BattCurr": [-511.99609375, -511.99609375, -511.99609375]}
    encoded_raw = frame.encode_raw(raw)
    assert encoded_raw == encoded_expected

    decoded = frame.decode(encoded_raw, converters)
    assert decoded == decoded_expected

    encoded = frame.encode(decoded, converters)
    decoded_raw = frame.decode_raw(encoded)
    assert decoded_raw == raw

@pytest.mark.unit
def test_encode_decode_array_no_converter():
    signal = LinSignal('BattCurr', 24, [0, 0, 2])
    frame = LinUnconditionalFrame(0x20, "LinStatus", 3, {0: signal})
    raw = {"BattCurr": [1, 1, 1]}
    encoded_expected = bytearray([1, 1, 1])

    encoded = frame.encode(raw)
    assert encoded == encoded_expected

    decoded = frame.decode(encoded)
    assert decoded == raw

@pytest.mark.unit
class TestLinUnconditionalFrameDecodingRaw:

    @pytest.mark.parametrize(
        ['data', 'expected'],
        [
            (b'\x64\x32\x08', {
                'MotorSpeed': 0x64,
                'InternalTemperature': 0x32,
                'Reserved1': 0,
                'InternalError': 0,
                'CommError': 1
            }),
            (b'\x20\x3F\x08', {
                'MotorSpeed': 0x20,
                'InternalTemperature': 0x3F,
                'Reserved1': 0,
                'InternalError': 0,
                'CommError': 1
            })
        ]
    )
    def test_decode_raw(self, frame, data, expected):
        assert frame.decode_raw(data) == expected

@pytest.mark.unit
class TestLinUnconditionalFrameDecoding:

    def test_decode_builtin(self, frame, range_type):
        frame._get_signal('MotorSpeed').encoding_type = range_type
        decoded = frame.decode(b'\x20\x3F\x08')
        assert decoded['MotorSpeed'] == 1600.0

    def test_decode_custom(self, frame, range_type):
        decoded = frame.decode(b'\x20\x3F\x08', {'MotorSpeed': range_type})
        assert decoded['MotorSpeed'] == 1600.0

    def test_decode_int(self, frame):
        decoded = frame.decode(b'\x20\x3F\x08')
        assert decoded['MotorSpeed'] == 0x20

    def test_decode_with_unit(self, frame, range_type):
        decoded = frame.decode(b'\x20\x3F\x08', {'MotorSpeed': range_type}, keep_unit=True)
        assert decoded['MotorSpeed'] == '1600.000 rpm'
