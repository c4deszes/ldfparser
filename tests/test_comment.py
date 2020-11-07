import pytest
import os
import ldfparser

def test_comment_collection_lin13():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin13.ldf")
	json = ldfparser.parseLDFtoDict(path, preserveComments=True)

def test_comment_collection_lin20():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin20.ldf")
	json = ldfparser.parseLDFtoDict(path, preserveComments=True)

def test_comment_collection_lin21():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin21.ldf")
	json = ldfparser.parseLDFtoDict(path, preserveComments=True)

def test_comment_collection_lin22():
	path = os.path.join(os.path.dirname(__file__), "ldf", "lin22.ldf")
	json = ldfparser.parseLDFtoDict(path, preserveComments=True)