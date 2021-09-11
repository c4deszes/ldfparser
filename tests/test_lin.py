import pytest
from ldfparser.lin import LIN_VERSION_2_0, LIN_VERSION_2_1, LinVersion

@pytest.mark.unit()
def test_linversion_str():
    assert str(LIN_VERSION_2_0) == "2.0"

@pytest.mark.unit()
def test_linversion_equal_float():
    assert LIN_VERSION_2_0 == 2.0

@pytest.mark.unit()
def test_linversion_equal_version():
    assert LIN_VERSION_2_0 == LIN_VERSION_2_0

@pytest.mark.unit()
def test_linversion_notequal_float():
    assert LIN_VERSION_2_1 != 2.0

@pytest.mark.unit()
def test_linversion_notequal_version():
    assert LIN_VERSION_2_0 != LIN_VERSION_2_1
