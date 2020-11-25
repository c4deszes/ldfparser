from ldfparser.encoding import LogicalValue
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

	assert ldf.signal('InternalLightsRequest') is not None
	assert ldf.frame('LSM_Frm2') is not None
	assert ldf.slave('LSM') is not None


@pytest.mark.unit
def test_load_valid_lin22():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin22.ldf")
	ldf = ldfparser.parseLDF(path)

	assert ldf.protocol_version == 2.2
	assert ldf.language_version == 2.2
	assert ldf.baudrate == 19200
	assert ldf.channel == 'DB'

	assert ldf.signal('InternalLightsRequest') is not None
	assert ldf.frame('LSM_Frm2') is not None

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
