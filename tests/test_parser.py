import os
import pytest
from ldfparser.diagnostics import LIN_MASTER_REQUEST_FRAME_ID, LIN_SLAVE_RESPONSE_FRAME_ID

from ldfparser.parser import parse_ldf
from ldfparser.frame import LinFrame
from ldfparser.signal import LinSignal
from ldfparser.encoding import ASCIIValue, BCDValue, LogicalValue


@pytest.mark.unit
def test_load_valid_lin13():
    path = os.path.join(os.path.dirname(__file__), "ldf", "lin13.ldf")
    ldf = parse_ldf(path)

    assert ldf.protocol_version == 1.3
    assert ldf.language_version == 1.3
    assert ldf.baudrate == 19200

    assert ldf.master.timebase == 0.005
    assert ldf.master.jitter == 0.0001

    assert ldf.signal('StartHeater') is not None
    assert ldf.frame('VL1_CEM_Frm1') is not None
    assert ldf.slave('LSM') is not None


@pytest.mark.unit
def test_load_valid_lin20():
    path = os.path.join(os.path.dirname(__file__), "ldf", "lin20.ldf")
    ldf = parse_ldf(path)

    assert ldf.protocol_version == 2.0
    assert ldf.language_version == 2.0
    assert ldf.baudrate == 19200

    assert ldf.signal('InternalLightsRequest') is not None
    assert ldf.frame('VL1_CEM_Frm1') is not None
    assert ldf.slave('LSM') is not None

    with pytest.raises(LookupError):
        ldf.get_unconditional_frame('VL1_CEM_Frm1234')

    with pytest.raises(TypeError):
        ldf.get_unconditional_frame(['VL1_CEM_Frm1'])


@pytest.mark.unit
def test_load_valid_lin21():
    path = os.path.join(os.path.dirname(__file__), "ldf", "lin21.ldf")
    ldf = parse_ldf(path)

    assert ldf.protocol_version == 2.1
    assert ldf.language_version == 2.1
    assert ldf.baudrate == 19200
    assert ldf.channel == 'DB'

    internalLightRequest = ldf.signal('InternalLightsRequest')
    assert internalLightRequest is not None
    assert internalLightRequest.publisher.name == 'CEM'
    assert len(internalLightRequest.subscribers) == 2
    assert internalLightRequest in ldf.master.publishes

    assert ldf.frame('LSM_Frm2') is not None
    assert ldf.frame(0x03) is not None
    assert ldf.slave('LSM') is not None


@pytest.mark.unit
def test_load_valid_lin22():
    path = os.path.join(os.path.dirname(__file__), "ldf", "lin22.ldf")
    ldf = parse_ldf(path)

    assert ldf.protocol_version == 2.2
    assert ldf.language_version == 2.2
    assert ldf.baudrate == 19200
    assert ldf.channel == 'DB'

    internalLightRequest = ldf.signal('InternalLightsRequest')
    assert internalLightRequest is not None
    assert internalLightRequest.publisher.name == 'CEM'
    assert len(internalLightRequest.subscribers) == 2
    assert internalLightRequest in ldf.master.publishes

    assert ldf.frame('LSM_Frm2') is not None
    assert ldf.frame(0x03) is not None

    LSM = ldf.slave('LSM')
    assert LSM is not None
    assert isinstance(LSM.subscribes_to[0], LinSignal)
    assert isinstance(LSM.publishes[0], LinSignal)
    assert isinstance(LSM.publishes_frames[0], LinFrame)
    assert LSM.product_id.supplier_id == 0x4A4F
    assert LSM.product_id.function_id == 0x4841
    assert LSM.fault_state_signals == [ldf.signal('IntTest')]
    assert LSM.response_error == ldf.signal('LSMerror')
    assert LSM.configurable_frames[0] == ldf.get_frame('Node_Status_Event')
    assert LSM.configurable_frames[1] == ldf.get_frame('CEM_Frm1')
    assert LSM.configurable_frames[2] == ldf.get_frame('LSM_Frm1')
    assert LSM.configurable_frames[3] == ldf.get_frame('LSM_Frm2')

    RSM = ldf.slave('RSM')
    assert RSM.configurable_frames[0] == ldf.get_frame('Node_Status_Event')
    assert RSM.configurable_frames[1] == ldf.get_frame('CEM_Frm1')
    assert RSM.configurable_frames[2] == ldf.get_frame('RSM_Frm1')
    assert RSM.configurable_frames[3] == ldf.get_frame('RSM_Frm2')

    converter = ldf.converters['InternalLightsRequest']
    assert converter.name == 'Dig2Bit'
    assert isinstance(converter._converters[0], LogicalValue)


@pytest.mark.unit
def test_no_signal_subscribers():
    path = os.path.join(os.path.dirname(__file__), "ldf", "no_signal_subscribers.ldf")
    ldf = parse_ldf(path)

    assert ldf.protocol_version == 2.2
    assert ldf.language_version == 2.2
    assert ldf.baudrate == 19200

    assert ldf.signal('DummySignal_0') is not None
    assert ldf.frame('DummyFrame') is not None
    assert ldf.signal('DummySignal_0').frame.name == 'DummyFrame'


@pytest.mark.unit
def test_load_valid_lin_encoders():
    path = os.path.join(os.path.dirname(__file__), "ldf", "lin_encoders.ldf")
    ldf = parse_ldf(path)

    assert ldf.protocol_version == 2.1
    assert ldf.language_version == 2.1
    assert ldf.baudrate == 19200

    bcd_signal = ldf.signal('bcd_signal')
    assert bcd_signal is not None
    assert bcd_signal.publisher.name == 'remote_node'
    assert len(bcd_signal.subscribers) == 1
    assert bcd_signal in ldf.slave('remote_node').publishes
    assert bcd_signal.init_value == [0x32, 32]

    ascii_signal = ldf.signal('ascii_signal')
    assert ascii_signal is not None
    assert ascii_signal.publisher.name == 'remote_node'
    assert len(ascii_signal.subscribers) == 1
    assert ascii_signal in ldf.slave('remote_node').publishes
    assert ascii_signal.init_value == [16, 0x16]

    assert ldf.frame('dummy_frame') is not None
    assert ldf.frame(0x25) is not None

    remote_node = ldf.slave('remote_node')
    assert remote_node is not None
    assert remote_node.product_id.supplier_id == 0x5
    assert remote_node.product_id.function_id == 0xA5A5

    converter = ldf.converters['bcd_signal']
    assert converter.name == 'BCDEncoding'
    assert len(converter._converters) == 1
    assert isinstance(converter._converters[0], BCDValue)

    converter = ldf.get_signal_encoding_type('AsciiEncoding')
    assert converter.name == 'AsciiEncoding'
    assert len(converter._converters) == 1
    assert isinstance(converter._converters[0], ASCIIValue)

    with pytest.raises(LookupError):
        ldf.get_signal_encoding_type('abc123')

@pytest.mark.unit
def test_load_valid_diagnostics():
    path = os.path.join(os.path.dirname(__file__), "ldf", "lin_diagnostics.ldf")
    ldf = parse_ldf(path)

    assert len(ldf.get_diagnostic_frames()) >= 0
    assert ldf.get_diagnostic_frame('MasterReq').frame_id == LIN_MASTER_REQUEST_FRAME_ID
    assert ldf.get_diagnostic_frame(LIN_MASTER_REQUEST_FRAME_ID).frame_id == LIN_MASTER_REQUEST_FRAME_ID
    assert ldf.master_request_frame.frame_id == LIN_MASTER_REQUEST_FRAME_ID
    assert ldf.slave_response_frame.frame_id == LIN_SLAVE_RESPONSE_FRAME_ID

    assert len(ldf.get_diagnostic_signals()) >= 0
    assert ldf.get_diagnostic_signal('MasterReqB0').width == 8

    with pytest.raises(LookupError):
        ldf.get_diagnostic_signal('MasterReqB9')
