import pytest
from ldfparser.lin import LIN_VERSION_1_3, LIN_VERSION_2_0, LIN_VERSION_2_1, LIN_VERSION_2_2

@pytest.mark.unit()
def test_linversion_str():
    assert str(LIN_VERSION_2_0) == "2.0"

@pytest.mark.unit()
def test_linversion_equal_version():
    assert LIN_VERSION_2_0 == LIN_VERSION_2_0

@pytest.mark.unit()
def test_linversion_not_equal_version():
    assert LIN_VERSION_1_3 != LIN_VERSION_2_1
    assert LIN_VERSION_2_0 != LIN_VERSION_2_1
    assert LIN_VERSION_2_1 != LIN_VERSION_2_2

@pytest.mark.unit()
def test_linversion_less_than_version():
    assert LIN_VERSION_1_3 < LIN_VERSION_2_1
    assert LIN_VERSION_2_0 < LIN_VERSION_2_1
    assert LIN_VERSION_2_1 < LIN_VERSION_2_2

@pytest.mark.unit()
def test_linversion_greater_than_version():
    assert not LIN_VERSION_1_3 > LIN_VERSION_2_0
    assert LIN_VERSION_2_0 > LIN_VERSION_1_3
    assert LIN_VERSION_2_1 > LIN_VERSION_2_0
    assert LIN_VERSION_2_2 > LIN_VERSION_2_1

@pytest.mark.unit()
def test_linversion_less_than_equal_version():
    assert LIN_VERSION_2_0 <= LIN_VERSION_2_1
    assert LIN_VERSION_2_1 <= LIN_VERSION_2_1

@pytest.mark.unit()
def test_linversion_greater_than_equal_version():
    assert LIN_VERSION_2_1 >= LIN_VERSION_2_1
    assert LIN_VERSION_2_1 >= LIN_VERSION_2_0

@pytest.mark.unit()
def test_linversion_float():
    assert float(LIN_VERSION_2_2) == 2.2
