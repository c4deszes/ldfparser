import pytest

from ldfparser.diagnostics import LinDiagnosticFrame, LinDiagnosticRequest, LinDiagnosticResponse
from ldfparser.signal import LinSignal

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
