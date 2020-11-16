import pytest
import os
import ldfparser

@pytest.mark.integration
def test_comment_collection_lin13():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin13.ldf")
	ldf = ldfparser.parseLDF(path, captureComments=True)
	assert len(ldf.comments) >= 0
	assert '// This is a LIN description example file' in ldf.comments


@pytest.mark.integration
def test_comment_collection_lin20():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin20.ldf")
	ldf = ldfparser.parseLDF(path, captureComments=True)
	assert len(ldf.comments) >= 0


@pytest.mark.integration
def test_comment_collection_lin21():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin21.ldf")
	ldf = ldfparser.parseLDF(path, captureComments=True)
	assert len(ldf.comments) >= 0
	assert "// Source: https://lin-cia.org/fileadmin/microsites/lin-cia.org/resources/documents/LIN-Spec_Pac2_1.pdf" in ldf.comments


@pytest.mark.integration
def test_comment_collection_lin22():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin22.ldf")
	ldf = ldfparser.parseLDF(path, captureComments=True)
	assert len(ldf.comments) >= 0
	assert "// Source: https://lin-cia.org/fileadmin/microsites/lin-cia.org/resources/documents/LIN_2.2A.pdf" in ldf.comments
