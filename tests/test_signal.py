import pytest
from ldfparser import LinSignal

@pytest.mark.unit
def test_signal_create_scalar_valid():
    signal = LinSignal.create('LSM', 8, 0)
    assert signal.is_array() is False

@pytest.mark.unit
def test_signal_create_scalar_invalid_size():
    with pytest.raises(ValueError):
        LinSignal.create('LSM', 20, 0)

@pytest.mark.unit
def test_signal_create_array_valid():
    signal = LinSignal.create('LSM', 24, [1, 2, 3])
    assert signal.is_array() is True

@pytest.mark.unit
def test_signal_create_array_invalid_length():
    with pytest.raises(ValueError):
        LinSignal.create('LSM', 13, [0, 1, 2, 3])

@pytest.mark.unit
def test_signal_create_array_invalid_width():
    with pytest.raises(ValueError):
        LinSignal.create('LSM', 0, [0, 1])

@pytest.mark.unit
def test_signal_create_array_invalid_initvalue():
    with pytest.raises(ValueError):
        LinSignal.create('LSM', 24, [1, 2, 3, 4, 5])
