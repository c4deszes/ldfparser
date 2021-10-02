import glob
import os
import pytest

from ldfparser.parser import parse_ldf
from ldfparser.signal import LinSignal
from ldfparser.encoding import PhysicalValue, LogicalValue

ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
ldf_files = glob.glob(ldf_directory + '/*.ldf')

@pytest.mark.parametrize(
    ('ldf_path'),
    ldf_files
)
@pytest.mark.performance
def test_performance_load(benchmark, ldf_path):
    path = os.path.join(os.path.dirname(__file__), "ldf", ldf_path)
    benchmark(parse_ldf, path)

@pytest.mark.performance
def test_performance_physical_encoding(benchmark):
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    benchmark(physical_value.encode, value=0, signal=motor_signal)

@pytest.mark.performance
def test_performance_logical_encoding(benchmark):
    motor_signal = LinSignal('MotorRPM', 8, 0)
    logical_value = LogicalValue(1, "on")
    benchmark(logical_value.encode, value='on', signal=motor_signal)

@pytest.mark.performance
def test_performance_physical_decoding(benchmark):
    motor_signal = LinSignal('MotorRPM', 8, 0)
    physical_value = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    benchmark(physical_value.decode, value=200, signal=motor_signal)

@pytest.mark.performance
def test_performance_logical_decoding(benchmark):
    motor_signal = LinSignal('MotorRPM', 8, 0)
    logical_value = LogicalValue(1, "on")
    benchmark(logical_value.decode, value=1, signal=motor_signal)
