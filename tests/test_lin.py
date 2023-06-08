# pylint: disable=invalid-name
import pytest
from ldfparser.lin import LIN_VERSION_1_3, LIN_VERSION_2_0, LIN_VERSION_2_1, LIN_VERSION_2_2, LinVersion, Iso17987Version, parse_lin_version, J2602Version

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

@pytest.mark.parametrize(
    ('a', 'b', 'op', 'exc'),
    [
        (Iso17987Version(2015), 2015, Iso17987Version.__gt__, TypeError),
        (Iso17987Version(2015), 2015, Iso17987Version.__lt__, TypeError)
    ]
)
def test_linversion_iso_invalid(a, b, op, exc):
    with pytest.raises(exc):
        op(a, b)

@pytest.mark.parametrize(
    ('value'),
    [
        '',
        '2.1.2',
        'ISO17987:abc',
        'J2602_1_1_1.0',
    ]
)
def test_linversion_parse_invalid(value):
    with pytest.raises(ValueError):
        parse_lin_version(value)

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('value', 'major', 'minor', 'part'),
    [
        ('J2602_1_1.0', 1, 0, 1),
        ('J2602_3_1.0', 1, 0, 3),
        ('J2602_1_1.1', 1, 1, 1),
    ]
)
def test_linversion_j2602_valid(value, major, minor, part):
    version = J2602Version.from_string(value)
    assert version.major == major
    assert version.minor == minor
    assert version.part == part
    assert str(J2602Version(major=major, minor=minor, part=part)) == value

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('value'),
    [
        '',
        '1.2',
        'ISO17987:2016',
        'J2602_1_2.0'
    ]
)
def test_linversion_unsupported_j2602(value):
    with pytest.raises(ValueError):
        J2602Version.from_string(value)

@pytest.mark.unit()
@pytest.mark.parametrize(
    ('value', 'expected'), [
        ('2.0', LIN_VERSION_2_0),
        ('ISO17987:2015', Iso17987Version(2015)),
        ('J2602_3_1.0', J2602Version(1, 0, 3))
    ]
)
def test_parse_linversion(value, expected):
    version = parse_lin_version(value)
    assert version == expected

@pytest.mark.unit()
@pytest.mark.parametrize(
    'a, b, op, result', [
        (J2602Version(1, 0, 1), LIN_VERSION_2_0, J2602Version.__eq__, True),
        (J2602Version(1, 0, 1), J2602Version(1, 1, 1), J2602Version.__eq__, False),
        (J2602Version(1, 0, 1), J2602Version(1, 0, 1), J2602Version.__eq__, True),
        (J2602Version(1, 0, 1), LIN_VERSION_2_2, J2602Version.__eq__, False),
        (J2602Version(1, 0, 1), Iso17987Version(2015), J2602Version.__eq__, False),
        (J2602Version(1, 0, 1), LIN_VERSION_2_2, J2602Version.__lt__, True),
        (J2602Version(1, 0, 1), Iso17987Version(2015), J2602Version.__lt__, True),
        (J2602Version(1, 0, 1), LIN_VERSION_1_3, J2602Version.__gt__, True),
        (J2602Version(1, 0, 1), LIN_VERSION_1_3, J2602Version.__lt__, False),
        (J2602Version(1, 0, 1), Iso17987Version(2015), J2602Version.__gt__, False),
        (J2602Version(1, 0, 1), Iso17987Version(2015), J2602Version.__ne__, True),
        (J2602Version(1, 0, 1), LIN_VERSION_2_2, J2602Version.__ne__, True),
        (LIN_VERSION_2_0, J2602Version(1, 0, 1), LinVersion.__eq__, True),
        (LIN_VERSION_2_2, J2602Version(1, 0, 1), LinVersion.__gt__, True),
        (LIN_VERSION_1_3, J2602Version(1, 0, 1), LinVersion.__lt__, True),
    ]
)
def test_linversion_j2602_compare(a, b, op, result):
    assert op(a, b) == result


