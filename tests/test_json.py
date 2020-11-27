import ldfparser
import os
import json
import glob
import difflib
import pytest
import warnings


ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
snapshot_directory = os.path.join(os.path.dirname(__file__), 'snapshot')
ldf_files = glob.glob(ldf_directory + '/*.ldf')


@pytest.mark.snapshot
@pytest.mark.parametrize(
	('ldf_path'),
	ldf_files
)
def test_compare_json(ldf_path):
	snapshot_file = os.path.join(snapshot_directory, os.path.basename(ldf_path)) + '.json'
	if not os.path.exists(snapshot_file):
		warnings.warn(f'Snapshot for {ldf_path} not found!')
		pytest.skip('Snapshot not found.')
	with open(snapshot_file, 'r') as snapshot:
		snapshot_content = snapshot.read()
		current = json.dumps(ldfparser.parseLDFtoDict(ldf_path))
		diff = ''.join(difflib.unified_diff(snapshot_content, current))
		assert not bool(diff), f"{ldf_path} not matching snapshot: {diff}"
