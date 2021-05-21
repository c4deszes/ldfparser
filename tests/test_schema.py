import ldfparser
import os
import glob
import json
import pytest

from jsonschema import validate


ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
ldf_files = glob.glob(ldf_directory + '/*.ldf')

json_schema = json.load(open('schemas/ldf.json',))


@pytest.mark.unit
@pytest.mark.parametrize(
	('ldf_path'),
	ldf_files
)
def test_json_schema(ldf_path):
	data = ldfparser.parseLDFtoDict(ldf_path)
	validate(data, schema=json_schema)
