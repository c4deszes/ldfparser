import sys
from unittest.mock import patch
import pytest

from ldfparser.cli import main

@pytest.mark.unit
@pytest.mark.parametrize('command', [
    ['ldfparser', '-h'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'info'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'info', '--details'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'export'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'export', '--output', './tests/tmp/test_cli_lin22.json'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'node', '--list'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'node', '--master'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'node', '--slave', 'LSM'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'frame', '--list'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'frame', '--id', '1'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'frame', '--id', '0x01'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'frame', '--name', 'LSM_Frm1'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'signal', '--list'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'signal', '--name', 'InternalLightsRequest']
])
def test_valid_commands(command):
    with pytest.raises(SystemExit) as exit_ex, patch.object(sys, 'argv', command):
        main()
    assert exit_ex.value.code == 0

@pytest.mark.unit
@pytest.mark.parametrize('command', [
    ['ldfparser', '--ldf'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'node', '--slave', 'ABC'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'frame', '--name', 'ABC'],
    ['ldfparser', '--ldf', './tests/ldf/lin22.ldf', 'signal', '--name', 'ABC']
])
def test_invalid_commands(command):
    with pytest.raises(SystemExit) as exit_ex, patch.object(sys, 'argv', command):
        main()
    assert exit_ex.value.code != 0
