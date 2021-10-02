import glob
import json
import os

import pytest
from jsonschema import validate
import ldfparser

ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
ldf_files = glob.glob(ldf_directory + '/*.ldf')

json_schema = json.load(open('schemas/ldf.json',))

@pytest.mark.unit
@pytest.mark.parametrize(
    ('ldf_path'),
    ldf_files
)
def test_json_schema(ldf_path):
    data = ldfparser.parse_ldf_to_dict(ldf_path)
    validate(data, schema=json_schema)
