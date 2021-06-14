from ldfparser.encoding import PhysicalValue, LogicalValue, BCDValue, ASCIIValue
import os
import pytest
import ldfparser


@pytest.mark.unit
def test_load_valid_lin13():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin13.ldf")
	ldf = ldfparser.parseLDF(path)

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
	ldf = ldfparser.parseLDF(path)

	assert ldf.protocol_version == 2.0
	assert ldf.language_version == 2.0
	assert ldf.baudrate == 19200

	assert ldf.signal('InternalLightsRequest') is not None
	assert ldf.frame('VL1_CEM_Frm1') is not None
	assert ldf.slave('LSM') is not None


@pytest.mark.unit
def test_load_valid_lin21():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin21.ldf")
	ldf = ldfparser.parseLDF(path)

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
	ldf = ldfparser.parseLDF(path)

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
	assert LSM.product_id.supplier_id == 0x4A4F
	assert LSM.product_id.function_id == 0x4841

	converter = ldf.converters['InternalLightsRequest']
	assert converter.name == 'Dig2Bit'
	assert isinstance(converter._converters[0], LogicalValue)


@pytest.mark.unit
def test_no_signal_subscribers():
	path = os.path.join(os.path.dirname(__file__), "ldf", "no_signal_subscribers.ldf")
	ldf = ldfparser.parseLDF(path)

	assert ldf.protocol_version == 2.2
	assert ldf.language_version == 2.2
	assert ldf.baudrate == 19200

	assert ldf.signal('DummySignal_0') is not None
	assert ldf.frame('DummyFrame') is not None


@pytest.mark.unit
def test_load_valid_lin_encoders():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin_encoders.ldf")
	ldf = ldfparser.parseLDF(path)

	assert ldf.protocol_version == 2.1
	assert ldf.language_version == 2.1
	assert ldf.baudrate == 19200

	bcd_signal = ldf.signal('bcd_signal')
	assert bcd_signal is not None
	assert bcd_signal.publisher.name == 'remote_node'
	assert len(bcd_signal.subscribers) == 1
	assert bcd_signal in ldf.slave('remote_node').publishes

	ascii_signal = ldf.signal('ascii_signal')
	assert ascii_signal is not None
	assert ascii_signal.publisher.name == 'remote_node'
	assert len(ascii_signal.subscribers) == 1
	assert ascii_signal in ldf.slave('remote_node').publishes

	byte_array_signal_0 = ldf.signal('byte_array_signal_0')
	assert byte_array_signal_0 is not None
	assert byte_array_signal_0.publisher.name == 'remote_node'
	assert len(byte_array_signal_0.subscribers) == 1
	assert byte_array_signal_0 in ldf.slave('remote_node').publishes
	assert byte_array_signal_0.is_array()
	assert byte_array_signal_0.init_value == [17, 34, 51, 68]

	byte_array_signal_1 = ldf.signal('byte_array_signal_1')
	assert byte_array_signal_1 is not None
	assert byte_array_signal_1.publisher.name == 'remote_node'
	assert len(byte_array_signal_1.subscribers) == 1
	assert byte_array_signal_1 in ldf.slave('remote_node').publishes
	assert byte_array_signal_1.is_array()
	assert byte_array_signal_1.init_value == [85, 102, 119, 136]

	assert ldf.frame('dummy_frame_0') is not None
	assert ldf.frame(0x25) is not None

	assert ldf.frame('dummy_frame_1') is not None
	assert ldf.frame(0x26) is not None

	remote_node = ldf.slave('remote_node')
	assert remote_node is not None
	assert remote_node.product_id.supplier_id == 0x5
	assert remote_node.product_id.function_id == 0xA5A5

	converter = ldf.converters['bcd_signal']
	assert converter.name == 'BCDEncoding'
	assert len(converter._converters) == 1
	assert isinstance(converter._converters[0], BCDValue)

	converter = ldf.converters['ascii_signal']
	assert converter.name == 'AsciiEncoding'
	assert len(converter._converters) == 1
	assert isinstance(converter._converters[0], ASCIIValue)

	converter = ldf.converters['byte_array_signal_0']
	assert converter.name == 'LargePhysicalEncoding'
	assert len(converter._converters) == 1
	assert isinstance(converter._converters[0], PhysicalValue)

	converter = ldf.converters['byte_array_signal_1']
	assert converter.name == 'LargeLogicalEncoding'
	assert len(converter._converters) == 5
	logical_values = [0x88776655, 0x00000000, 0xFF00FF00, 0x00FFFF00, 0xFFFFFFFF]
	for c, value in zip(converter._converters, logical_values):
		assert isinstance(c, LogicalValue)
		assert c.phy_value == value
