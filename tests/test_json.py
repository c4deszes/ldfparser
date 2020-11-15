from os.path import dirname, basename, splitext, join
from pathlib import Path
import pytest
import ldfparser
import json
import glob
from difflib import unified_diff

# For development purposes only
AUTO_APPROVE = False

ldf_dir = join(dirname(__file__), 'ldf')
ldf_files = [basename(f) for f in glob.glob(ldf_dir + '/*.ldf')]

@pytest.mark.parametrize('path', ldf_files)
def test_json_valid(path):
	ldf_path = join(ldf_dir, path)
	json_path = splitext(ldf_path)[0] + '.json'

	data = ldfparser.parseLDFtoDict(ldf_path)

	received = json.dumps(data, indent='\t', sort_keys=True)
	
	if AUTO_APPROVE:
		Path(json_path).write_text(received)
	
	approved = Path(json_path).read_text()

	diff = '\n'.join(unified_diff(approved.split('\n'), received.split('\n')))
	has_diff = bool(diff)
	assert not has_diff, 'Mismatch found in ' + path + ':\n' + diff

	assert not AUTO_APPROVE, 'Disable AUTO_APPROVE'

