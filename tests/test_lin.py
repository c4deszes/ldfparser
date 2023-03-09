# pylint: disable=invalid-name
import pytest
from ldfparser.lin import LIN_VERSION_1_3, LIN_VERSION_2_0, LIN_VERSION_2_1, LIN_VERSION_2_2, Iso17987Version

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('version', 'expected'),
    [
        (LIN_VERSION_1_3, "1.3"),
        (LIN_VERSION_2_0, "2.0"),
        (LIN_VERSION_2_1, "2.1"),
        (LIN_VERSION_2_2, "2.2")
    ]
)
def test_linversion_str(version, expected):
    assert str(version) == expected

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('a', 'b'),
    [
        (LIN_VERSION_1_3, LIN_VERSION_1_3),
        (LIN_VERSION_2_0, LIN_VERSION_2_0),
        (LIN_VERSION_2_1, LIN_VERSION_2_1)
    ]
)
def test_linversion_equal_version(a, b):
    assert a == b

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('a', 'b'),
    [
        (LIN_VERSION_1_3, LIN_VERSION_2_1),
        (LIN_VERSION_2_0, LIN_VERSION_2_1),
        (LIN_VERSION_2_2, LIN_VERSION_2_1),
        (LIN_VERSION_2_2, "2.2")
    ]
)
def test_linversion_not_equal_version(a, b):
    assert a != b

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('a', 'b'),
    [
        (LIN_VERSION_1_3, LIN_VERSION_2_1),
        (LIN_VERSION_2_0, LIN_VERSION_2_1),
        (LIN_VERSION_2_1, LIN_VERSION_2_2)
    ]
)
def test_linversion_less_than_version(a, b):
    assert a < b

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('a', 'b'),
    [
        (LIN_VERSION_2_0, LIN_VERSION_1_3),
        (LIN_VERSION_2_1, LIN_VERSION_2_0),
        (LIN_VERSION_2_2, LIN_VERSION_2_1)
    ]
)
def test_linversion_greater_than_version(a, b):
    assert a > b

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('a', 'b'),
    [
        (LIN_VERSION_1_3, LIN_VERSION_1_3),
        (LIN_VERSION_1_3, LIN_VERSION_2_0),
        (LIN_VERSION_1_3, LIN_VERSION_2_1)
    ]
)
def test_linversion_less_than_equal_version(a, b):
    assert a <= b

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('a', 'b'),
    [
        (LIN_VERSION_2_0, LIN_VERSION_1_3),
        (LIN_VERSION_2_0, LIN_VERSION_2_0),
        (LIN_VERSION_2_1, LIN_VERSION_2_0)
    ]
)
def test_linversion_greater_than_equal_version(a, b):
    assert a >= b

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('version', 'expected'),
    [
        (LIN_VERSION_1_3, 1.3),
        (LIN_VERSION_2_0, 2.0),
        (LIN_VERSION_2_1, 2.1),
        (LIN_VERSION_2_2, 2.2)
    ]
)
def test_linversion_float(version, expected):
    assert float(version) == expected

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('func', 'arg'),
    [
        (LIN_VERSION_1_3.__gt__, "2.0"),
        (LIN_VERSION_1_3.__lt__, "2.0"),
        (LIN_VERSION_1_3.__ge__, "2.0"),
        (LIN_VERSION_1_3.__le__, "2.0")
    ]
)
def test_linversion_typerror(func, arg):
    with pytest.raises(TypeError):
        func(arg)

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('a', 'b', 'op', 'result'),
    [
        (Iso17987Version(2015), Iso17987Version(2015), Iso17987Version.__eq__, True),
        (Iso17987Version(2015), Iso17987Version(2016), Iso17987Version.__eq__, False),
        (Iso17987Version(2015), Iso17987Version(2015), Iso17987Version.__ne__, False),
        (Iso17987Version(2015), Iso17987Version(2016), Iso17987Version.__ne__, True),
        (Iso17987Version(2015), Iso17987Version(2016), Iso17987Version.__gt__, False),
        (Iso17987Version(2015), LIN_VERSION_2_0, Iso17987Version.__gt__, True),
        (Iso17987Version(2015), Iso17987Version(2015), Iso17987Version.__ge__, True),
        (Iso17987Version(2015), Iso17987Version(2016), Iso17987Version.__lt__, True),
        (Iso17987Version(2015), LIN_VERSION_2_0, Iso17987Version.__lt__, False),
        (Iso17987Version(2015), Iso17987Version(2015), Iso17987Version.__le__, True)
    ]
)
def test_linversion_iso_compare(a, b, op, result):
    assert op(a, b) == result
