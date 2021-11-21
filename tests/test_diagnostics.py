import pytest

from ldfparser.diagnostics import (
    LIN_PCI_CONSECUTIVE_FRAME, LIN_PCI_FIRST_FRAME, LIN_PCI_SINGLE_FRAME, LIN_SID_DATA_DUMP, LIN_SID_READ_BY_ID,
    LinDiagnosticFrame, LinDiagnosticRequest, LinDiagnosticResponse, pci_byte, rsid
)
from ldfparser.signal import LinSignal

@pytest.mark.parametrize(
    ('pci_type', 'length', 'expected'),
    [
        (LIN_PCI_SINGLE_FRAME, 1, 0b00000001),
        (LIN_PCI_SINGLE_FRAME, 6, 0b00000110),
        (LIN_PCI_FIRST_FRAME, 10, 0b00011010),
        (LIN_PCI_CONSECUTIVE_FRAME, 7, 0b00100111)
    ]
)
@pytest.mark.unit
def test_pci_calculation(pci_type, length, expected):
    assert pci_byte(pci_type, length) == expected

@pytest.mark.parametrize(
    ('sid', 'expected'),
    [
        (LIN_SID_READ_BY_ID, 0xF2),
        (LIN_SID_DATA_DUMP, 0xF4)
    ]
)
@pytest.mark.unit
def test_rsid_calculation(sid, expected):
    assert rsid(sid) == expected

@pytest.fixture(scope="session")
def diagnostic_request():
    frame = LinDiagnosticFrame(0x3C, 'MasterReq', 8, {
        0: LinSignal('MasterReqB0', 8, 0),
        8: LinSignal('MasterReqB1', 8, 0),
        16: LinSignal('MasterReqB2', 8, 0),
        24: LinSignal('MasterReqB3', 8, 0),
        32: LinSignal('MasterReqB4', 8, 0),
        40: LinSignal('MasterReqB5', 8, 0),
        48: LinSignal('MasterReqB6', 8, 0),
        56: LinSignal('MasterReqB7', 8, 0),
    })
    return LinDiagnosticRequest(frame)

@pytest.mark.unit
def test_encode_assign_nad(diagnostic_request):
    data = diagnostic_request.encode_assign_nad(0x00, 0x7FFF, 0xFFFF, 0x01)
    assert data == b'\x00\x06\xB0\xFF\x7F\xFF\xFF\x01'

@pytest.mark.unit
def test_encode_conditional_change_nad(diagnostic_request):
    data = diagnostic_request.encode_conditional_change_nad(0x7F, 0x01, 0x03, 0x01, 0xFF, 0x01)
    assert data == b'\x7F\x06\xB3\x01\x03\x01\xFF\x01'

@pytest.mark.unit
def test_encode_data_dump(diagnostic_request):
    data = diagnostic_request.encode_data_dump(0x01, [0x00, 0x01, 0x02, 0x03, 0x04])
    assert data == b'\x01\x06\xB4\x00\x01\x02\x03\x04'

@pytest.mark.unit
def test_encode_save_configuration(diagnostic_request):
    data = diagnostic_request.encode_save_configuration(0x01)
    assert data == b'\x01\x01\xB6\xFF\xFF\xFF\xFF\xFF'

@pytest.mark.unit
def test_encode_assign_frame_id_range(diagnostic_request):
    data = diagnostic_request.encode_assign_frame_id_range(0x01, 0, [0x32, 0x33, 0x34, 0x35])
    assert data == b'\x01\x06\xB7\x00\x32\x33\x34\x35'

@pytest.mark.unit
def test_encode_read_by_id(diagnostic_request):
    data = diagnostic_request.encode_read_by_id(0x00, 0x05, 0x7FFF, 0xFFFF)
    assert data == b'\x00\x06\xB2\x05\xFF\x7F\xFF\xFF'

@pytest.fixture(scope="session")
def diagnostic_response():
    frame = LinDiagnosticFrame(0x3D, 'SlaveResp', 8, {
        0: LinSignal('SlaveRespB0', 8, 0),
        8: LinSignal('SlaveRespB1', 8, 0),
        16: LinSignal('SlaveRespB2', 8, 0),
        24: LinSignal('SlaveRespB3', 8, 0),
        32: LinSignal('SlaveRespB4', 8, 0),
        40: LinSignal('SlaveRespB5', 8, 0),
        48: LinSignal('SlaveRespB6', 8, 0),
        56: LinSignal('SlaveRespB7', 8, 0),
    })
    return LinDiagnosticResponse(frame)

@pytest.mark.unit
def test_decode_assign_frame_id_response(diagnostic_response):
    data = diagnostic_response.decode_response(b'\x00\x01\xF0\xFF\xFF\xFF\xFF\xFF')
    assert data == {
        'NAD': 0x00,
        'PCI': 0x01,
        'RSID': 0xF0,
        'D1': 0xFF,
        'D2': 0xFF,
        'D3': 0xFF,
        'D4': 0xFF,
        'D5': 0xFF
    }
