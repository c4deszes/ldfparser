import pytest
import glob
import os
import sys
from unittest.mock import patch

from ldfparser import parse_ldf, save_ldf
from ldfparser.save import main

ldf_directory = os.path.join(os.path.dirname(__file__), 'ldf')
snapshot_directory = os.path.join(os.path.dirname(__file__), 'snapshot')
ldf_files = glob.glob(ldf_directory + '/*.ldf')

class TestSave:

    @pytest.mark.unit
    @pytest.mark.parametrize(('ldf_path'), ldf_files)
    def test_save(self, ldf_path):
        """
        Tests whether the loaded LDFs can be saved as is, and then reloaded without any errors
        """
        ldf = parse_ldf(ldf_path)
        output_path = os.path.join(os.path.dirname(__file__),
                                   'tmp',
                                   'test_resave_' + os.path.basename(ldf_path))
        save_ldf(ldf, output_path)

        parse_ldf(output_path)

    @pytest.mark.unit
    @pytest.mark.parametrize(('ldf_path'), [ldf_files[0]])
    def test_save_cli(self, ldf_path):
        """
        Tests whether LDFs can be saved using the command line interface
        """
        output_path = os.path.join(os.path.dirname(__file__),
                                   'tmp',
                                   'test_resave_cli_' + os.path.basename(ldf_path))
        command = ['python', '-f', ldf_path, '-o', output_path]
        with patch.object(sys, 'argv', command):
            main()
