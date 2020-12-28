import pytest
import sys
from unittest.mock import patch

from ldfparser.cli import main

@pytest.mark.parametrize('command', [
	['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'info'],
	['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'info', '--details'],
	['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'export'],
	['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'export'],	# TODO: test with --output
	['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'node', '--list'],
	['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'node', '--master'],
	['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'node', '--slave', 'LSM']
])
def test_valid_commands(command):
	with patch.object(sys, 'argv', command):
		main()