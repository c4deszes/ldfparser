import glob
import os

import ldfparser
import pytest
from ldfparser import LinSignal
from ldfparser.encoding import LogicalValue, PhysicalValue

ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
ldf_files = glob.glob(ldf_directory + '/*.ldf')

@pytest.mark.parametrize(
    ('ldf_path'),
    ldf_files
)
@pytest.mark.performance
def test_performance_load(benchmark, ldf_path):
    path = os.path.join(os.path.dirname(__file__), "ldf", ldf_path)
    benchmark(ldfparser.parseLDF, path)

@pytest.mark.performance
def test_performance_physical_encoding(benchmark):
    motorSignal = LinSignal('MotorRPM', 8, 0)
    physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    benchmark(physicalValue.encode, value=0, signal=motorSignal)

@pytest.mark.performance
def test_performance_logical_encoding(benchmark):
    motorSignal = LinSignal('MotorRPM', 8, 0)
    logicalValue = LogicalValue(1, "on")
    benchmark(logicalValue.encode, value='on', signal=motorSignal)

@pytest.mark.performance
def test_performance_physical_decoding(benchmark):
    motorSignal = LinSignal('MotorRPM', 8, 0)
    physicalValue = PhysicalValue(0, 254, 0.3937, 0, 'rpm')
    benchmark(physicalValue.decode, value=200, signal=motorSignal)

@pytest.mark.performance
def test_performance_logical_decoding(benchmark):
    motorSignal = LinSignal('MotorRPM', 8, 0)
    logicalValue = LogicalValue(1, "on")
    benchmark(logicalValue.decode, value=1, signal=motorSignal)
