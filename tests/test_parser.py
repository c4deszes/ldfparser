import os
import pytest
import unittest
import ldfparser

@pytest.mark.unit
def test_load_valid():
	path = os.path.join(os.path.dirname(__file__), "ldf", "valid.ldf")
	ldf = ldfparser.LDF(path)

@pytest.mark.unit
def test_load_ldf_with_syntax_error():
	with pytest.raises(Exception) as e:
		path = os.path.join(os.path.dirname(__file__), "ldf", "syntax_error.ldf")
		ldf = ldfparser.LDF(path)

@pytest.mark.unit
def test_load_ldf_with_logical_error():
	with pytest.raises(Exception) as e:
		path = os.path.join(os.path.dirname(__file__), "ldf", "logic_error.ldf")
		ldf = ldfparser.LDF(path)

@pytest.mark.integration
def test_retrieve_signals():
	path = os.path.join(os.path.dirname(__file__), "ldf", "valid.ldf")
	ldf = ldfparser.LDF(path)

	assert len(ldf.signals) == 4

	sig = ldf.signal('backlight_level')
	assert sig is not None
	assert sig.name == 'backlight_level'
	assert sig.width == 4
	assert sig.init_value == [0]

@pytest.mark.integration
def test_retrieve_frames():
	path = os.path.join(os.path.dirname(__file__), "ldf", "valid.ldf")
	ldf = ldfparser.LDF(path)

	assert len(ldf.frames) == 2

	frame = ldf.frame('Backlight')
	assert frame.frame_id == 11
	assert frame.name == 'Backlight'
	assert frame.signals[0].name == 'backlight_level'